import graphene

from .mutations import (
    InvoiceCreate,
    InvoiceDelete,
    InvoiceRequest,
    InvoiceRequestDelete,
    InvoiceSendNotification,
    InvoiceUpdate,
)


class InvoiceMutations(graphene.ObjectType):
    invoice_request = InvoiceRequest.Field()
    invoice_request_delete = InvoiceRequestDelete.Field()
    invoice_create = InvoiceCreate.Field()
    invoice_delete = InvoiceDelete.Field()
    invoice_update = InvoiceUpdate.Field()
    invoice_send_notification = InvoiceSendNotification.Field()
