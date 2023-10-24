import pytest
from django.utils import timezone

from .....discount import RewardValueType
from .....discount.models import Promotion, PromotionRule
from ....tests.utils import assert_graphql_error_with_message, get_graphql_content


@pytest.fixture
def sales_for_sorting_with_channels(db, channel_USD, channel_PLN):
    promotions = Promotion.objects.bulk_create(
        [
            Promotion(name="Sale1"),
            Promotion(name="Sale2"),
            Promotion(name="Sale3"),
            Promotion(name="Sale4"),
            Promotion(name="Sale15"),
        ]
    )

    for promotion in promotions:
        promotion.assign_old_sale_id()

    rules = PromotionRule.objects.bulk_create(
        [
            PromotionRule(
                promotion=promotions[0],
                reward_value=1,
                reward_value_type=RewardValueType.PERCENTAGE,
            ),
            PromotionRule(
                promotion=promotions[0],
                reward_value=7,
                reward_value_type=RewardValueType.PERCENTAGE,
            ),
            PromotionRule(
                promotion=promotions[1],
                reward_value=7,
                reward_value_type=RewardValueType.FIXED,
            ),
            PromotionRule(
                promotion=promotions[1],
                reward_value=1,
                reward_value_type=RewardValueType.FIXED,
            ),
            PromotionRule(
                promotion=promotions[2],
                reward_value=5,
                reward_value_type=RewardValueType.PERCENTAGE,
            ),
            PromotionRule(
                promotion=promotions[3],
                reward_value=2,
                reward_value_type=RewardValueType.FIXED,
            ),
            PromotionRule(
                promotion=promotions[4],
                reward_value=2,
                reward_value_type=RewardValueType.FIXED,
            ),
            PromotionRule(
                promotion=promotions[4],
                reward_value=5,
                reward_value_type=RewardValueType.FIXED,
            ),
        ]
    )
    channel_USD.promotionrule_set.add(rules[0], rules[2], rules[4], rules[6])
    channel_PLN.promotionrule_set.add(rules[1], rules[3], rules[5], rules[7])

    promotions[4].save()
    promotions[2].save()
    promotions[0].save()
    promotions[1].save()
    promotions[3].save()

    return promotions


QUERY_SALES_WITH_SORTING_AND_FILTERING = """
    query (
        $sortBy: SaleSortingInput, $filter: SaleFilterInput, $channel: String
    ){
        sales (
            first: 10, sortBy: $sortBy, filter: $filter, channel: $channel
        ) {
            edges {
                node {
                    name
                }
            }
        }
    }
"""


def test_sales_with_sorting_and_without_channel(
    staff_api_client,
    permission_manage_discounts,
):
    # given
    variables = {"sortBy": {"field": "VALUE", "direction": "ASC"}}

    # when
    response = staff_api_client.post_graphql(
        QUERY_SALES_WITH_SORTING_AND_FILTERING,
        variables,
        permissions=[permission_manage_discounts],
        check_no_permissions=False,
    )

    # then
    assert_graphql_error_with_message(response, "A default channel does not exist.")


@pytest.mark.parametrize(
    "sort_by, sales_order",
    [
        (
            {"field": "VALUE", "direction": "ASC"},
            ["Sale1", "Sale15", "Sale3", "Sale2"],
        ),
        (
            {"field": "VALUE", "direction": "DESC"},
            ["Sale2", "Sale3", "Sale15", "Sale1"],
        ),
        (
            {"field": "CREATED_AT", "direction": "ASC"},
            ["Sale1", "Sale2", "Sale3", "Sale15"],
        ),
        (
            {"field": "CREATED_AT", "direction": "DESC"},
            ["Sale15", "Sale3", "Sale2", "Sale1"],
        ),
        (
            {"field": "LAST_MODIFIED_AT", "direction": "ASC"},
            ["Sale15", "Sale3", "Sale1", "Sale2"],
        ),
        (
            {"field": "LAST_MODIFIED_AT", "direction": "DESC"},
            ["Sale2", "Sale1", "Sale3", "Sale15"],
        ),
    ],
)
def test_sales_with_sorting_and_channel_USD(
    sort_by,
    sales_order,
    staff_api_client,
    permission_manage_discounts,
    sales_for_sorting_with_channels,
    channel_USD,
):
    # given
    variables = {"sortBy": sort_by, "channel": channel_USD.slug}

    # when
    response = staff_api_client.post_graphql(
        QUERY_SALES_WITH_SORTING_AND_FILTERING,
        variables,
        permissions=[permission_manage_discounts],
        check_no_permissions=False,
    )

    # then
    content = get_graphql_content(response)
    sales_nodes = content["data"]["sales"]["edges"]
    for index, sale_name in enumerate(sales_order):
        assert sale_name == sales_nodes[index]["node"]["name"]


@pytest.mark.parametrize(
    "sort_by, sales_order",
    [
        (
            {"field": "VALUE", "direction": "ASC"},
            ["Sale2", "Sale4", "Sale15", "Sale1"],
        ),
        (
            {"field": "VALUE", "direction": "DESC"},
            ["Sale1", "Sale15", "Sale4", "Sale2"],
        ),
        (
            {"field": "CREATED_AT", "direction": "ASC"},
            ["Sale1", "Sale2", "Sale4", "Sale15"],
        ),
        (
            {"field": "CREATED_AT", "direction": "DESC"},
            ["Sale15", "Sale4", "Sale2", "Sale1"],
        ),
        (
            {"field": "LAST_MODIFIED_AT", "direction": "ASC"},
            ["Sale15", "Sale1", "Sale2", "Sale4"],
        ),
        (
            {"field": "LAST_MODIFIED_AT", "direction": "DESC"},
            ["Sale4", "Sale2", "Sale1", "Sale15"],
        ),
    ],
)
def test_sales_with_sorting_and_channel_PLN(
    sort_by,
    sales_order,
    staff_api_client,
    permission_manage_discounts,
    sales_for_sorting_with_channels,
    channel_PLN,
):
    # given
    variables = {"sortBy": sort_by, "channel": channel_PLN.slug}

    # when
    response = staff_api_client.post_graphql(
        QUERY_SALES_WITH_SORTING_AND_FILTERING,
        variables,
        permissions=[permission_manage_discounts],
        check_no_permissions=False,
    )

    # then
    content = get_graphql_content(response)
    sales_nodes = content["data"]["sales"]["edges"]
    for index, sale_name in enumerate(sales_order):
        assert sale_name == sales_nodes[index]["node"]["name"]


def test_vouchers_with_sorting_and_not_existing_channel_asc(
    staff_api_client,
    permission_manage_discounts,
    sales_for_sorting_with_channels,
    channel_USD,
):
    # given
    variables = {
        "sortBy": {"field": "VALUE", "direction": "ASC"},
        "channel": "Not-existing",
    }

    # when
    response = staff_api_client.post_graphql(
        QUERY_SALES_WITH_SORTING_AND_FILTERING,
        variables,
        permissions=[permission_manage_discounts],
        check_no_permissions=False,
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["sales"]["edges"]


QUERY_SALE_WITH_SORT = """
    query ($sort_by: SaleSortingInput!) {
        sales(first:5, sortBy: $sort_by) {
            edges{
                node{
                    name
                }
            }
        }
    }
"""


@pytest.mark.parametrize(
    "sale_sort, result_order",
    [
        ({"field": "NAME", "direction": "ASC"}, ["BigSale", "Sale2", "Sale3"]),
        ({"field": "NAME", "direction": "DESC"}, ["Sale3", "Sale2", "BigSale"]),
        ({"field": "TYPE", "direction": "ASC"}, ["Sale2", "Sale3", "BigSale"]),
        ({"field": "TYPE", "direction": "DESC"}, ["BigSale", "Sale3", "Sale2"]),
        ({"field": "START_DATE", "direction": "ASC"}, ["Sale3", "Sale2", "BigSale"]),
        ({"field": "START_DATE", "direction": "DESC"}, ["BigSale", "Sale2", "Sale3"]),
        ({"field": "END_DATE", "direction": "ASC"}, ["Sale2", "Sale3", "BigSale"]),
        ({"field": "END_DATE", "direction": "DESC"}, ["BigSale", "Sale3", "Sale2"]),
    ],
)
def test_query_sales_with_sort(
    sale_sort, result_order, staff_api_client, permission_manage_discounts, channel_USD
):
    # given
    promotions = Promotion.objects.bulk_create(
        [
            Promotion(name="BigSale"),
            Promotion(
                name="Sale2",
                start_date=timezone.now().replace(year=2012, month=1, day=5),
                end_date=timezone.now().replace(year=2013, month=1, day=5),
            ),
            Promotion(
                name="Sale3",
                start_date=timezone.now().replace(year=2011, month=1, day=5),
                end_date=timezone.now().replace(year=2015, month=12, day=31),
            ),
        ]
    )
    for promotion in promotions:
        promotion.assign_old_sale_id()

    rules = PromotionRule.objects.bulk_create(
        [
            PromotionRule(
                promotion=promotion,
                reward_value=5,
                reward_value_type=RewardValueType.FIXED,
            )
            for promotion in promotions
        ]
    )
    rules[0].reward_value_type = RewardValueType.PERCENTAGE
    rules[0].save(update_fields=["reward_value_type"])

    variables = {"sort_by": sale_sort}
    staff_api_client.user.user_permissions.add(permission_manage_discounts)

    # when
    response = staff_api_client.post_graphql(QUERY_SALE_WITH_SORT, variables)

    # then
    content = get_graphql_content(response)
    sales = content["data"]["sales"]["edges"]

    for order, sale_name in enumerate(result_order):
        assert sales[order]["node"]["name"] == sale_name
