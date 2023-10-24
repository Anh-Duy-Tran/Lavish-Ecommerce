import graphene
from django.db.models import F, Min, Q, QuerySet

from ..core.descriptions import CHANNEL_REQUIRED
from ..core.doc_category import DOC_CATEGORY_DISCOUNTS
from ..core.types import BaseEnum, ChannelSortInputObjectType, SortInputObjectType


class SaleSortField(BaseEnum):
    NAME = ["name", "pk"]
    START_DATE = ["start_date", "name", "pk"]
    END_DATE = ["end_date", "name", "pk"]
    VALUE = ["value", "name", "pk"]
    TYPE = ["type", "name", "pk"]
    CREATED_AT = ["created_at", "name", "pk"]
    LAST_MODIFIED_AT = ["updated_at", "name", "pk"]

    class Meta:
        doc_category = DOC_CATEGORY_DISCOUNTS

    @property
    def description(self):
        descrption_extras = {
            SaleSortField.VALUE.name: [CHANNEL_REQUIRED],  # type: ignore[attr-defined] # graphene.Enum is not typed # noqa: E501
        }
        if self.name in SaleSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            description = f"Sort sales by {sort_name}."
            if extras := descrption_extras.get(self.name):
                description += "".join(extras)
            return description
        raise ValueError(f"Unsupported enum value: {self.value}")

    @staticmethod
    def qs_with_value(queryset: QuerySet, channel_slug: str) -> QuerySet:
        return queryset.annotate(
            value=Min(
                "rules__reward_value",
                filter=Q(rules__channels__slug=str(channel_slug)),
            )
        )

    @staticmethod
    def qs_with_type(queryset: QuerySet, **kwargs) -> QuerySet:
        return queryset.annotate(type=F("rules__reward_value_type"))


class SaleSortingInput(ChannelSortInputObjectType):
    class Meta:
        doc_category = DOC_CATEGORY_DISCOUNTS
        sort_enum = SaleSortField
        type_name = "sales"


class VoucherSortField(graphene.Enum):
    CODE = ["code"]
    START_DATE = ["start_date", "name", "code"]
    END_DATE = ["end_date", "name", "code"]
    VALUE = ["discount_value", "name", "code"]
    TYPE = ["type", "name", "code"]
    USAGE_LIMIT = ["usage_limit", "name", "code"]
    MINIMUM_SPENT_AMOUNT = ["min_spent_amount", "name", "code"]

    class Meta:
        doc_category = DOC_CATEGORY_DISCOUNTS

    @property
    def description(self):
        descrption_extras = {
            VoucherSortField.VALUE.name: [CHANNEL_REQUIRED],  # type: ignore[attr-defined] # graphene.Enum is not typed # noqa: E501
            VoucherSortField.MINIMUM_SPENT_AMOUNT.name: [CHANNEL_REQUIRED],  # type: ignore[attr-defined] # graphene.Enum is not typed # noqa: E501
        }
        if self.name in VoucherSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            description = f"Sort vouchers by {sort_name}."
            if extras := descrption_extras.get(self.name):
                description += "".join(extras)
            return description
        raise ValueError(f"Unsupported enum value: {self.value}")

    @staticmethod
    def qs_with_minimum_spent_amount(queryset: QuerySet, channel_slug: str) -> QuerySet:
        return queryset.annotate(
            min_spent_amount=Min(
                "channel_listings__min_spent_amount",
                filter=Q(channel_listings__channel__slug=str(channel_slug)),
            )
        )

    @staticmethod
    def qs_with_value(queryset: QuerySet, channel_slug: str) -> QuerySet:
        return queryset.annotate(
            discount_value=Min(
                "channel_listings__discount_value",
                filter=Q(channel_listings__channel__slug=str(channel_slug)),
            )
        )


class VoucherSortingInput(ChannelSortInputObjectType):
    class Meta:
        doc_category = DOC_CATEGORY_DISCOUNTS
        sort_enum = VoucherSortField
        type_name = "vouchers"


class PromotionSortField(BaseEnum):
    NAME = ["name", "pk"]
    START_DATE = ["start_date", "name", "pk"]
    END_DATE = ["end_date", "name", "pk"]
    CREATED_AT = ["created_at", "pk"]

    class Meta:
        doc_category = DOC_CATEGORY_DISCOUNTS

    @property
    def description(self):
        if self.name in PromotionSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            description = f"Sort promotions by {sort_name}."
            return description
        raise ValueError(f"Unsupported enum value: {self.value}")


class PromotionSortingInput(SortInputObjectType):
    class Meta:
        doc_category = DOC_CATEGORY_DISCOUNTS
        sort_enum = PromotionSortField
        type_name = "promotions"
