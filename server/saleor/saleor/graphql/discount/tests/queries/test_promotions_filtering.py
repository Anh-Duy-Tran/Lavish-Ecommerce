from datetime import timedelta

import graphene
import pytest
from django.utils import timezone

from ....tests.utils import get_graphql_content

QUERY_PROMOTIONS = """
    query Promotions($where: PromotionWhereInput){
        promotions(first: 10, where: $where) {
            edges {
                node {
                    id
                    name
                    description
                    startDate
                    rules {
                        id
                    }
                }
            }
        }
    }
"""


def test_query_promotions_filter_by_id(
    promotion_list, staff_api_client, permission_manage_discounts
):
    # given
    ids = [
        graphene.Node.to_global_id("Promotion", promotion.pk)
        for promotion in promotion_list[:2]
    ]
    variables = {"where": {"ids": ids}}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PROMOTIONS, variables, permissions=(permission_manage_discounts,)
    )

    # then
    content = get_graphql_content(response)
    promotions = content["data"]["promotions"]["edges"]
    assert len(promotions) == 2
    names = {node["node"]["name"] for node in promotions}
    assert names == {promotion_list[0].name, promotion_list[1].name}


@pytest.mark.parametrize("value", [None, []])
def test_query_promotions_filter_by_ids_empty_values(
    value, promotion_list, staff_api_client, permission_manage_discounts
):
    # given
    variables = {"where": {"ids": value}}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PROMOTIONS, variables, permissions=(permission_manage_discounts,)
    )

    # then
    content = get_graphql_content(response)
    promotions = content["data"]["promotions"]["edges"]
    assert len(promotions) == 0


@pytest.mark.parametrize(
    "where, indexes",
    [
        ({"eq": "Promotion 2"}, [1]),
        ({"eq": "Non-existing"}, []),
        ({"eq": None}, []),
        ({"eq": ""}, []),
        ({"oneOf": ["Promotion 1", "Promotion 3"]}, [0, 2]),
        ({"oneOf": ["Promotion 3"]}, [2]),
        ({"oneOf": ["Non-existing 1", "Non-existing 2"]}, []),
        ({"oneOf": []}, []),
        (None, []),
    ],
)
def test_query_promotions_filter_by_name(
    where, indexes, promotion_list, staff_api_client, permission_manage_discounts
):
    # given
    variables = {"where": {"name": where}}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PROMOTIONS, variables, permissions=(permission_manage_discounts,)
    )

    # then
    content = get_graphql_content(response)
    promotions = content["data"]["promotions"]["edges"]
    assert len(promotions) == len(indexes)
    names = {node["node"]["name"] for node in promotions}
    assert names == {promotion_list[index].name for index in indexes}


@pytest.mark.parametrize(
    "where, indexes",
    [
        (
            {
                "range": {
                    "gte": (timezone.now() + timedelta(days=5)).isoformat(),
                    "lte": (timezone.now() + timedelta(days=25)).isoformat(),
                }
            },
            [0, 1],
        ),
        (
            {
                "range": {
                    "gte": (timezone.now() + timedelta(days=5)).isoformat(),
                }
            },
            [0, 1, 2],
        ),
        (
            {
                "range": {
                    "lte": (timezone.now() + timedelta(days=25)).isoformat(),
                }
            },
            [0, 1],
        ),
        (
            {
                "range": {
                    "lte": (timezone.now() - timedelta(days=5)).isoformat(),
                }
            },
            [],
        ),
        (None, []),
        ({"range": {"gte": None}}, []),
        ({"range": {"lte": None}}, []),
        ({"range": {"lte": None, "gte": None}}, []),
        ({"eq": None}, []),
        ({"oneOf": []}, []),
        ({}, []),
    ],
)
def test_query_promotions_filter_by_end_date(
    where, indexes, promotion_list, staff_api_client, permission_manage_discounts
):
    # given
    variables = {
        "where": {
            "endDate": where,
        },
    }

    # when
    response = staff_api_client.post_graphql(
        QUERY_PROMOTIONS, variables, permissions=(permission_manage_discounts,)
    )

    # then
    content = get_graphql_content(response)
    promotions = content["data"]["promotions"]["edges"]
    assert len(promotions) == len(indexes)
    names = {node["node"]["name"] for node in promotions}
    assert names == {promotion_list[index].name for index in indexes}


@pytest.mark.parametrize(
    "where, indexes",
    [
        (
            {
                "range": {
                    "gte": (timezone.now() + timedelta(days=3)).isoformat(),
                    "lte": (timezone.now() + timedelta(days=25)).isoformat(),
                }
            },
            [1, 2],
        ),
        (
            {
                "range": {
                    "gte": (timezone.now() + timedelta(days=3)).isoformat(),
                }
            },
            [1, 2],
        ),
        (
            {
                "range": {
                    "lte": (timezone.now() + timedelta(days=25)).isoformat(),
                }
            },
            [0, 1, 2],
        ),
        (
            {
                "range": {
                    "lte": (timezone.now() - timedelta(days=5)).isoformat(),
                }
            },
            [],
        ),
        (None, []),
        ({"range": {"gte": None}}, []),
        ({"range": {"lte": None}}, []),
        ({"range": {"lte": None, "gte": None}}, []),
        ({"eq": None}, []),
        ({"oneOf": []}, []),
        ({}, []),
    ],
)
def test_query_promotions_filter_by_start_date(
    where, indexes, promotion_list, staff_api_client, permission_manage_discounts
):
    # given
    variables = {
        "where": {"startDate": where},
    }

    # when
    response = staff_api_client.post_graphql(
        QUERY_PROMOTIONS, variables, permissions=(permission_manage_discounts,)
    )

    # then
    content = get_graphql_content(response)
    promotions = content["data"]["promotions"]["edges"]
    assert len(promotions) == len(indexes)
    names = {node["node"]["name"] for node in promotions}
    assert names == {promotion_list[index].name for index in indexes}


@pytest.mark.parametrize("value, indexes", [(True, [0]), (False, [1, 2])])
def test_query_promotions_filter_by_is_old_sale(
    value, indexes, promotion_list, staff_api_client, permission_manage_discounts
):
    # given
    promotion_list[0].old_sale_id = 1
    promotion_list[0].save(update_fields=["old_sale_id"])
    variables = {"where": {"isOldSale": value}}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PROMOTIONS, variables, permissions=(permission_manage_discounts,)
    )

    # then
    content = get_graphql_content(response)
    promotions = content["data"]["promotions"]["edges"]
    assert len(promotions) == len(indexes)
    assert {promotion_list[index].name for index in indexes} == {
        promotion["node"]["name"] for promotion in promotions
    }
