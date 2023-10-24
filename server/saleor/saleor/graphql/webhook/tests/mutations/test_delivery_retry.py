from unittest.mock import patch

import graphene

from .....graphql.tests.utils import assert_no_permission, get_graphql_content

WEBHOOK_DELIVERY_RETRY_MUTATION = """
    mutation eventDeliveryRetry($id: ID!){
      eventDeliveryRetry(id: $id){
        errors{
          field
          message
        }
        delivery{
          id
        }
      }
    }
"""


@patch("saleor.plugins.manager.PluginsManager.event_delivery_retry")
def test_delivery_retry_mutation(
    mocked_send_request_async,
    app_api_client,
    permission_manage_apps,
    event_delivery,
    settings,
):
    # given
    query = WEBHOOK_DELIVERY_RETRY_MUTATION
    delivery_id = graphene.Node.to_global_id("EventDelivery", event_delivery.pk)
    variables = {"id": delivery_id}

    # when
    response = app_api_client.post_graphql(
        query,
        variables=variables,
        permissions=[permission_manage_apps],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    mocked_send_request_async.assert_called_once_with(event_delivery)
    errors = content["data"]["eventDeliveryRetry"]["errors"]
    assert len(errors) == 0


def test_webhook_delivery_retry_without_permission(
    staff_api_client, app, event_delivery
):
    query = WEBHOOK_DELIVERY_RETRY_MUTATION
    delivery_id = graphene.Node.to_global_id("EventDelivery", event_delivery.pk)
    variables = {"id": delivery_id}
    response = staff_api_client.post_graphql(query, variables=variables)
    assert_no_permission(response)


def test_webhook_delivery_retry_wrong_type(
    staff_api_client, app, event_attempt, permission_manage_apps
):
    query = WEBHOOK_DELIVERY_RETRY_MUTATION
    delivery_wrong_id = graphene.Node.to_global_id(
        "EventDeliveryAttempt", event_attempt.id
    )
    variables = {"id": delivery_wrong_id}
    expected_message = "Must receive a EventDelivery id."
    response = staff_api_client.post_graphql(
        query,
        variables=variables,
        permissions=[permission_manage_apps],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    errors = content["data"]["eventDeliveryRetry"]["errors"]
    assert len(errors) == 1
    assert errors[0]["field"] == "id"
    assert errors[0]["message"] == expected_message


def test_delivery_retry_mutation_wrong_id(
    app_api_client, permission_manage_apps, event_delivery
):
    # given
    query = WEBHOOK_DELIVERY_RETRY_MUTATION
    variables = {"id": "/w"}
    expected_message = "Couldn't resolve id: /w."
    # when
    response = app_api_client.post_graphql(
        query,
        variables=variables,
        permissions=[permission_manage_apps],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    # then
    errors = content["data"]["eventDeliveryRetry"]["errors"]
    assert len(errors) == 1
    assert errors[0]["field"] == "id"
    assert errors[0]["message"] == expected_message
