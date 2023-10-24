from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0111_auto_20210518_1357"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderevent",
            name="type",
            field=models.CharField(
                choices=[
                    ("DRAFT_CREATED", "draft_created"),
                    ("DRAFT_CREATED_FROM_REPLACE", "draft_created_from_replace"),
                    ("ADDED_PRODUCTS", "added_products"),
                    ("REMOVED_PRODUCTS", "removed_products"),
                    ("PLACED", "placed"),
                    ("PLACED_FROM_DRAFT", "placed_from_draft"),
                    ("OVERSOLD_ITEMS", "oversold_items"),
                    ("CANCELED", "canceled"),
                    ("ORDER_MARKED_AS_PAID", "order_marked_as_paid"),
                    ("ORDER_FULLY_PAID", "order_fully_paid"),
                    ("ORDER_REPLACEMENT_CREATED", "order_replacement_created"),
                    ("ORDER_DISCOUNT_ADDED", "order_discount_added"),
                    (
                        "ORDER_DISCOUNT_AUTOMATICALLY_UPDATED",
                        "order_discount_automatically_updated",
                    ),
                    ("ORDER_DISCOUNT_UPDATED", "order_discount_updated"),
                    ("ORDER_DISCOUNT_DELETED", "order_discount_deleted"),
                    ("ORDER_LINE_DISCOUNT_UPDATED", "order_line_discount_updated"),
                    ("ORDER_LINE_DISCOUNT_REMOVED", "order_line_discount_removed"),
                    ("ORDER_LINE_PRODUCT_DELETED", "order_line_product_deleted"),
                    ("ORDER_LINE_VARIANT_DELETED", "order_line_variant_deleted"),
                    ("UPDATED_ADDRESS", "updated_address"),
                    ("EMAIL_SENT", "email_sent"),
                    ("CONFIRMED", "confirmed"),
                    ("PAYMENT_AUTHORIZED", "payment_authorized"),
                    ("PAYMENT_CAPTURED", "payment_captured"),
                    ("EXTERNAL_SERVICE_NOTIFICATION", "external_service_notification"),
                    ("PAYMENT_REFUNDED", "payment_refunded"),
                    ("PAYMENT_VOIDED", "payment_voided"),
                    ("PAYMENT_FAILED", "payment_failed"),
                    ("INVOICE_REQUESTED", "invoice_requested"),
                    ("INVOICE_GENERATED", "invoice_generated"),
                    ("INVOICE_UPDATED", "invoice_updated"),
                    ("INVOICE_SENT", "invoice_sent"),
                    ("FULFILLMENT_CANCELED", "fulfillment_canceled"),
                    ("FULFILLMENT_RESTOCKED_ITEMS", "fulfillment_restocked_items"),
                    ("FULFILLMENT_FULFILLED_ITEMS", "fulfillment_fulfilled_items"),
                    ("FULFILLMENT_REFUNDED", "fulfillment_refunded"),
                    ("FULFILLMENT_RETURNED", "fulfillment_returned"),
                    ("FULFILLMENT_REPLACED", "fulfillment_replaced"),
                    ("TRACKING_UPDATED", "tracking_updated"),
                    ("NOTE_ADDED", "note_added"),
                    ("OTHER", "other"),
                ],
                max_length=255,
            ),
        ),
    ]
