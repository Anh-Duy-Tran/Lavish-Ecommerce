from typing import TYPE_CHECKING, Optional, Union, cast

import graphene
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from .....app.models import App
from .....channel import TransactionFlowStrategy
from .....channel.models import Channel
from .....checkout import models as checkout_models
from .....order import models as order_models
from .....payment import TransactionEventType
from .....payment import models as payment_models
from .....payment.error_codes import TransactionProcessErrorCode
from .....payment.interface import PaymentGatewayData
from .....payment.utils import (
    get_final_session_statuses,
    handle_transaction_process_session,
)
from ....core.descriptions import ADDED_IN_313, ADDED_IN_316, PREVIEW_FEATURE
from ....core.doc_category import DOC_CATEGORY_PAYMENTS
from ....core.mutations import BaseMutation
from ....core.scalars import JSON
from ....core.types import common as common_types
from ....plugins.dataloaders import get_plugin_manager_promise
from ...types import TransactionEvent, TransactionItem
from .utils import clean_customer_ip_address

if TYPE_CHECKING:
    pass


class TransactionProcess(BaseMutation):
    transaction = graphene.Field(
        TransactionItem, description="The processed transaction."
    )
    transaction_event = graphene.Field(
        TransactionEvent,
        description="The event created for the processed transaction.",
    )
    data = graphene.Field(
        JSON, description="The json data required to finalize the payment."
    )

    class Arguments:
        id = graphene.ID(
            description="The ID of the transaction to process.",
            required=True,
        )
        data = graphene.Argument(
            JSON, description="The data that will be passed to the payment gateway."
        )
        customer_ip_address = graphene.String(
            description=(
                "The customer's IP address. If not provided Saleor will try to "
                "determine the customer's IP address on its own. "
                "The customer's IP address will be passed to the payment app. "
                "The IP should be in ipv4 or ipv6 format. "
                "The field can be used only by an app that has `HANDLE_PAYMENTS` "
                "permission." + ADDED_IN_316
            )
        )

    class Meta:
        doc_category = DOC_CATEGORY_PAYMENTS
        description = (
            "Processes a transaction session. It triggers the webhook "
            "`TRANSACTION_PROCESS_SESSION`, to the assigned `paymentGateways`. "
            + ADDED_IN_313
            + PREVIEW_FEATURE
        )
        error_type_class = common_types.TransactionProcessError

    @classmethod
    def get_action(cls, event: payment_models.TransactionEvent, channel: "Channel"):
        if event.type == TransactionEventType.AUTHORIZATION_REQUEST:
            return TransactionFlowStrategy.AUTHORIZATION
        elif event.type == TransactionEventType.CHARGE_REQUEST:
            return TransactionFlowStrategy.CHARGE

        return channel.default_transaction_flow_strategy

    @classmethod
    def get_source_object(
        cls, transaction_item: payment_models.TransactionItem
    ) -> Union[checkout_models.Checkout, order_models.Order]:
        if transaction_item.checkout_id:
            checkout = cast(checkout_models.Checkout, transaction_item.checkout)
            return checkout
        if transaction_item.order_id:
            order = cast(order_models.Order, transaction_item.order)
            return order
        raise ValidationError(
            {
                "id": ValidationError(
                    "Transaction doesn't have attached order or checkout.",
                    code=TransactionProcessErrorCode.INVALID.value,
                )
            }
        )

    @classmethod
    def get_request_event(cls, events: QuerySet) -> payment_models.TransactionEvent:
        """Get event with details of requested action.

        This searches for a request event with the appropriate type and
        include_in_calculations set to false. Request events created from
        transactionInitialize have their include_in_calculation set to false by default.
        """
        for event in events:
            if (
                event.type
                in [
                    TransactionEventType.AUTHORIZATION_REQUEST,
                    TransactionEventType.CHARGE_REQUEST,
                ]
                and not event.include_in_calculations
            ):
                return event
        raise ValidationError(
            {
                "id": ValidationError(
                    "Missing call of `transactionInitialize` mutation.",
                    code=TransactionProcessErrorCode.INVALID.value,
                )
            }
        )

    @classmethod
    def get_already_processed_event(cls, events) -> Optional[TransactionEvent]:
        for event in events:
            if (
                event.type in get_final_session_statuses()
                and event.include_in_calculations
            ):
                return event
        return None

    @classmethod
    def clean_payment_app(cls, transaction_item: payment_models.TransactionItem) -> App:
        if not transaction_item.app_identifier:
            raise ValidationError(
                {
                    "id": ValidationError(
                        "Transaction doesn't have attached app that could process the "
                        "request.",
                        code=TransactionProcessErrorCode.MISSING_PAYMENT_APP_RELATION.value,
                    )
                }
            )
        app = App.objects.filter(identifier=transaction_item.app_identifier).first()
        if not app:
            raise ValidationError(
                {
                    "id": ValidationError(
                        "Payment app attached to the transaction, doesn't exist.",
                        code=TransactionProcessErrorCode.MISSING_PAYMENT_APP.value,
                    )
                }
            )
        return app

    @classmethod
    def perform_mutation(cls, root, info, *, id, data=None, customer_ip_address=None):
        transaction_item = cls.get_node_or_error(
            info, id, only_type="TransactionItem", field="token"
        )
        transaction_item = cast(payment_models.TransactionItem, transaction_item)
        events = transaction_item.events.all()
        if processed_event := cls.get_already_processed_event(events):
            return cls(
                transaction=transaction_item,
                transaction_event=processed_event,
                data=None,
            )
        request_event = cls.get_request_event(events)
        source_object = cls.get_source_object(transaction_item)
        app = cls.clean_payment_app(transaction_item)
        app_identifier = app.identifier
        app_identifier = cast(str, app_identifier)
        action = cls.get_action(request_event, source_object.channel)
        customer_ip_address = clean_customer_ip_address(
            info,
            customer_ip_address,
            error_code=TransactionProcessErrorCode.INVALID.value,
        )

        manager = get_plugin_manager_promise(info.context).get()
        event, data = handle_transaction_process_session(
            transaction_item=transaction_item,
            source_object=source_object,
            payment_gateway_data=PaymentGatewayData(
                app_identifier=app_identifier, data=data
            ),
            app=app,
            action=action,
            customer_ip_address=customer_ip_address,
            manager=manager,
            request_event=request_event,
        )

        transaction_item.refresh_from_db()
        return cls(transaction=transaction_item, transaction_event=event, data=data)
