import graphene
from django.core.exceptions import ValidationError

from .....core.utils.promo_code import generate_promo_code, is_available_promo_code
from .....discount import models
from .....discount.error_codes import DiscountErrorCode
from .....permission.enums import DiscountPermissions
from .....webhook.event_types import WebhookEventAsyncType
from ....channel import ChannelContext
from ....core import ResolveInfo
from ....core.descriptions import ADDED_IN_31
from ....core.doc_category import DOC_CATEGORY_DISCOUNTS
from ....core.mutations import ModelMutation
from ....core.types import BaseInputObjectType, DiscountError, NonNullList
from ....core.utils import WebhookEventInfo
from ....core.validators import validate_end_is_after_start
from ....plugins.dataloaders import get_plugin_manager_promise
from ...enums import DiscountValueTypeEnum, VoucherTypeEnum
from ...types import Voucher


class VoucherInput(BaseInputObjectType):
    type = VoucherTypeEnum(
        description="Voucher type: PRODUCT, CATEGORY SHIPPING or ENTIRE_ORDER."
    )
    name = graphene.String(description="Voucher name.")
    code = graphene.String(description="Code to use the voucher.")
    start_date = graphene.types.datetime.DateTime(
        description="Start date of the voucher in ISO 8601 format."
    )
    end_date = graphene.types.datetime.DateTime(
        description="End date of the voucher in ISO 8601 format."
    )
    discount_value_type = DiscountValueTypeEnum(
        description="Choices: fixed or percentage."
    )
    products = NonNullList(
        graphene.ID, description="Products discounted by the voucher.", name="products"
    )
    variants = NonNullList(
        graphene.ID,
        description="Variants discounted by the voucher." + ADDED_IN_31,
        name="variants",
    )
    collections = NonNullList(
        graphene.ID,
        description="Collections discounted by the voucher.",
        name="collections",
    )
    categories = NonNullList(
        graphene.ID,
        description="Categories discounted by the voucher.",
        name="categories",
    )
    min_checkout_items_quantity = graphene.Int(
        description="Minimal quantity of checkout items required to apply the voucher."
    )
    countries = NonNullList(
        graphene.String,
        description="Country codes that can be used with the shipping voucher.",
    )
    apply_once_per_order = graphene.Boolean(
        description="Voucher should be applied to the cheapest item or entire order."
    )
    apply_once_per_customer = graphene.Boolean(
        description="Voucher should be applied once per customer."
    )
    only_for_staff = graphene.Boolean(
        description="Voucher can be used only by staff user."
    )
    usage_limit = graphene.Int(
        description="Limit number of times this voucher can be used in total."
    )

    class Meta:
        doc_category = DOC_CATEGORY_DISCOUNTS


class VoucherCreate(ModelMutation):
    class Arguments:
        input = VoucherInput(
            required=True, description="Fields required to create a voucher."
        )

    class Meta:
        description = "Creates a new voucher."
        model = models.Voucher
        object_type = Voucher
        permissions = (DiscountPermissions.MANAGE_DISCOUNTS,)
        error_type_class = DiscountError
        error_type_field = "discount_errors"
        webhook_events_info = [
            WebhookEventInfo(
                type=WebhookEventAsyncType.VOUCHER_CREATED,
                description="A voucher was created.",
            )
        ]

    @classmethod
    def clean_input(cls, info: ResolveInfo, instance, data, **kwargs):
        code = data.get("code", None)
        if code == "":
            data["code"] = generate_promo_code()
        elif not is_available_promo_code(code):
            raise ValidationError(
                {
                    "code": ValidationError(
                        "Promo code already exists.",
                        code=DiscountErrorCode.ALREADY_EXISTS.value,
                    )
                }
            )
        cleaned_input = super().clean_input(info, instance, data, **kwargs)

        return cleaned_input

    @classmethod
    def success_response(cls, instance):
        instance = ChannelContext(node=instance, channel_slug=None)
        return super().success_response(instance)

    @classmethod
    def clean_instance(cls, info: ResolveInfo, instance):
        super().clean_instance(info, instance)
        start_date = instance.start_date
        end_date = instance.end_date
        try:
            validate_end_is_after_start(start_date, end_date)
        except ValidationError as error:
            error.code = DiscountErrorCode.INVALID.value
            raise ValidationError({"end_date": error})

    @classmethod
    def post_save_action(cls, info: ResolveInfo, instance, cleaned_input):
        manager = get_plugin_manager_promise(info.context).get()
        cls.call_event(manager.voucher_created, instance)
