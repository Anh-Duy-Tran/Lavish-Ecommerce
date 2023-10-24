import warnings

from .....channel.utils import DEPRECATION_WARNING_MESSAGE
from .....discount.models import Promotion, Voucher
from ....tests.utils import get_graphql_content

QUERY_SALES_WITH_SORTING_AND_FILTERING = """
    query($sortBy: SaleSortingInput){
        sales (first: 10, sortBy: $sortBy) {
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
    promotion_converted_from_sale,
    promotion_converted_from_sale_with_empty_predicate,
):
    # given
    variables = {"sortBy": {"field": "VALUE", "direction": "ASC"}}

    # when
    with warnings.catch_warnings(record=True) as warns:
        response = staff_api_client.post_graphql(
            QUERY_SALES_WITH_SORTING_AND_FILTERING,
            variables,
            permissions=[permission_manage_discounts],
            check_no_permissions=False,
        )

    # then
    content = get_graphql_content(response)
    sales_nodes = content["data"]["sales"]["edges"]
    promotion_names = [
        promotion.name
        for promotion in [
            promotion_converted_from_sale,
            promotion_converted_from_sale_with_empty_predicate,
        ]
    ]
    assert all([node["node"]["name"] in promotion_names for node in sales_nodes])

    assert any(
        [str(warning.message) == DEPRECATION_WARNING_MESSAGE for warning in warns]
    )


QUERY_VOUCHERS_WITH_SORT = """
    query ($sort_by: VoucherSortingInput!) {
        vouchers(first:5, sortBy: $sort_by) {
            edges{
                node{
                    name
                }
            }
        }
    }
"""


def test_query_vouchers_with_sort(
    staff_api_client,
    permission_manage_discounts,
    voucher_with_high_min_spent_amount,
    voucher_percentage,
):
    variables = {"sort_by": {"field": "MINIMUM_SPENT_AMOUNT", "direction": "ASC"}}
    staff_api_client.user.user_permissions.add(permission_manage_discounts)

    with warnings.catch_warnings(record=True) as warns:
        response = staff_api_client.post_graphql(QUERY_VOUCHERS_WITH_SORT, variables)

    content = get_graphql_content(response)
    vouchers = content["data"]["vouchers"]["edges"]

    assert [node["node"]["name"] for node in vouchers] == [
        voucher_percentage.name,
        voucher_with_high_min_spent_amount.name,
    ]
    assert any(
        [str(warning.message) == DEPRECATION_WARNING_MESSAGE for warning in warns]
    )


def test_filter_sales_by_query(staff_api_client, permission_manage_discounts):
    promotions = Promotion.objects.bulk_create(
        [Promotion(name="Promotion"), Promotion(name="Sale")]
    )
    for promotion in promotions:
        promotion.assign_old_sale_id()

    promotion = promotions[1]

    query = """
        query Sales($query: String) {
            sales(first:5, query: $query) {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """

    staff_api_client.user.user_permissions.add(permission_manage_discounts)

    # when
    response = staff_api_client.post_graphql(query, {"query": promotion.name})

    # then
    content = get_graphql_content(response)
    assert content["data"]["sales"]["edges"][0]["node"]["name"] == promotion.name


def test_filter_vouchers_by_query(staff_api_client, permission_manage_discounts):
    vouchers = Voucher.objects.bulk_create(
        [
            Voucher(code="code1", name="Spanish"),
            Voucher(code="code2", name="Inquisition"),
        ]
    )
    voucher = vouchers[1]

    query = """
        query Vouchers($query: String) {
            vouchers(first:5, query: $query) {
                edges {
                    node {
                        name
                        code
                    }
                }
            }
        }
    """

    staff_api_client.user.user_permissions.add(permission_manage_discounts)
    response = staff_api_client.post_graphql(query, {"query": voucher.name})
    content = get_graphql_content(response)
    assert content["data"]["vouchers"]["edges"][0]["node"]["code"] == voucher.code
