from datetime import timedelta
from unittest.mock import patch

import graphene
from django.utils import timezone
from freezegun import freeze_time

from .....discount import RewardValueType
from .....discount.error_codes import DiscountErrorCode
from ....tests.utils import get_graphql_content
from ...enums import DiscountValueTypeEnum
from ...utils import convert_migrated_sale_predicate_to_catalogue_info

SALE_UPDATE_MUTATION = """
    mutation  saleUpdate($id: ID!, $input: SaleInput!) {
        saleUpdate(id: $id, input: $input) {
            errors {
                field
                code
                message
            }
            sale {
                name
                type
                startDate
                endDate
            }
        }
    }
"""


@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale(
    updated_webhook_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
    product_list,
):
    # given
    query = SALE_UPDATE_MUTATION

    # Set discount value type to 'fixed' and change it in mutation
    promotion = promotion_converted_from_sale
    rule = promotion.rules.first()
    assert rule.reward_value_type == RewardValueType.FIXED

    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    new_product_pks = [product.id for product in product_list]
    new_product_ids = [
        graphene.Node.to_global_id("Product", product_id)
        for product_id in new_product_pks
    ]

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {
            "type": DiscountValueTypeEnum.PERCENTAGE.name,
            "products": new_product_ids,
        },
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]
    assert data["type"] == RewardValueType.PERCENTAGE.upper()
    promotion.refresh_from_db()
    rule = promotion.rules.first()
    assert rule.reward_value_type == RewardValueType.PERCENTAGE

    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        rule.catalogue_predicate
    )
    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_name(
    updated_webhook_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
    product_list,
):
    # given
    query = SALE_UPDATE_MUTATION
    promotion = promotion_converted_from_sale
    new_name = "New name"
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {
            "name": new_name,
        },
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]
    assert data["name"] == new_name
    promotion.refresh_from_db()
    assert promotion.name == new_name

    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        promotion.rules.first().catalogue_predicate
    )
    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    update_products_discounted_prices_for_promotion_task_mock.assert_not_called()


@freeze_time("2020-03-18 12:00:00")
@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_toggle")
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_start_date_after_current_date_notification_not_sent(
    updated_webhook_mock,
    sale_toggle_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
):
    """Ensure the notification is not sent when the start date is set after the current
    date.
    """
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    promotion.last_notification_scheduled_at = None
    promotion.save(update_fields=["last_notification_scheduled_at"])
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    start_date = timezone.now() + timedelta(days=1)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {"startDate": start_date},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]
    assert data["startDate"] == start_date.isoformat()
    promotion.refresh_from_db()
    assert promotion.start_date.isoformat() == start_date.isoformat()
    assert promotion.last_notification_scheduled_at is None

    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        promotion.rules.first().catalogue_predicate
    )
    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    sale_toggle_mock.assert_not_called()
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@freeze_time("2020-03-18 12:00:00")
@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_toggle")
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_start_date_before_current_date_notification_already_sent(
    updated_webhook_mock,
    sale_toggle_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
):
    """Ensure the notification is not sent when the start date is set before
    current date and notification was already sent.
    """
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    last_notification_scheduled_at = timezone.now() - timedelta(minutes=5)
    promotion.last_notification_scheduled_at = last_notification_scheduled_at
    promotion.save(update_fields=["last_notification_scheduled_at"])
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    start_date = timezone.now() - timedelta(days=1)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {"startDate": start_date},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]
    assert data["startDate"] == start_date.isoformat()
    promotion.refresh_from_db()
    assert promotion.start_date.isoformat() == start_date.isoformat()
    assert (
        promotion.last_notification_scheduled_at.isoformat()
        == last_notification_scheduled_at.isoformat()
    )

    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        promotion.rules.first().catalogue_predicate
    )
    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    sale_toggle_mock.assert_not_called()
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@freeze_time("2020-03-18 12:00:00")
@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_toggle")
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_start_date_before_current_date_notification_sent(
    updated_webhook_mock,
    sale_toggle_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
):
    """Ensure the sale_toggle notification is sent and the notification date is set
    when the start date is set before current date and the notification hasn't been sent
    before.
    """
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    promotion.last_notification_scheduled_at = None
    promotion.save(update_fields=["last_notification_scheduled_at"])
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    start_date = timezone.now() - timedelta(days=1)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {"startDate": start_date},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]
    assert data["startDate"] == start_date.isoformat()
    promotion.refresh_from_db()
    assert promotion.start_date.isoformat() == start_date.isoformat()
    assert promotion.last_notification_scheduled_at == timezone.now()

    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        promotion.rules.first().catalogue_predicate
    )
    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )

    sale_toggle_mock.assert_called_once_with(promotion, current_catalogue)
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@freeze_time("2020-03-18 12:00:00")
@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_toggle")
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_end_date_after_current_date_notification_not_sent(
    updated_webhook_mock,
    sale_toggle_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
):
    """Ensure the notification is not sent when the end date is set after
    the current date.
    """
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    promotion.start_date = timezone.now() - timedelta(days=1)
    promotion.save(update_fields=["start_date"])
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    end_date = timezone.now() + timedelta(days=1)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {"endDate": end_date},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]

    assert data["endDate"] == end_date.isoformat()
    promotion.refresh_from_db()
    assert promotion.end_date.isoformat() == end_date.isoformat()
    assert promotion.last_notification_scheduled_at is None

    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        promotion.rules.first().catalogue_predicate
    )
    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    sale_toggle_mock.assert_not_called()
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@freeze_time("2020-03-18 12:00:00")
@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_toggle")
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_end_date_before_current_date_notification_already_sent(
    updated_webhook_mock,
    sale_toggle_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
):
    """Ensure the notification is sent when the end date is set before
    current date, the notification was already sent but the end date was not set before.
    It means we need to notify about ending the sale.
    """
    # given
    query = SALE_UPDATE_MUTATION
    now = timezone.now()

    promotion = promotion_converted_from_sale
    last_notification_scheduled_at = now - timedelta(minutes=5)
    promotion.last_notification_scheduled_at = last_notification_scheduled_at
    promotion.start_date = now - timedelta(days=2)
    promotion.save(update_fields=["last_notification_scheduled_at", "start_date"])
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    end_date = now - timedelta(days=1)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {"endDate": end_date},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]
    assert data["endDate"] == end_date.isoformat()
    promotion.refresh_from_db()
    assert promotion.end_date.isoformat() == end_date.isoformat()
    assert promotion.last_notification_scheduled_at == now

    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        promotion.rules.first().catalogue_predicate
    )
    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    sale_toggle_mock.assert_called_once_with(promotion, current_catalogue)
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@freeze_time("2020-03-18 12:00:00")
@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_toggle")
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_end_date_before_current_date_notification_sent(
    updated_webhook_mock,
    sale_toggle_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
):
    """Ensure the sale_toggle notification is sent and the notification date is set
    when the end date is set before current date and the notification hasn't been sent
    before.
    """
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    promotion.last_notification_scheduled_at = None
    promotion.start_date = timezone.now() - timedelta(days=2)
    promotion.save(update_fields=["last_notification_scheduled_at", "start_date"])
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    end_date = timezone.now() - timedelta(days=1)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {"endDate": end_date},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]
    assert data["endDate"] == end_date.isoformat()
    promotion.refresh_from_db()
    assert promotion.end_date.isoformat() == end_date.isoformat()
    assert promotion.last_notification_scheduled_at == timezone.now()

    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        promotion.rules.first().catalogue_predicate
    )
    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    sale_toggle_mock.assert_called_once_with(promotion, current_catalogue)
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_categories(
    updated_webhook_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
    product_list,
    non_default_category,
):
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    new_category_id = graphene.Node.to_global_id("Category", non_default_category.id)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {
            "categories": [new_category_id],
        },
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    promotion.refresh_from_db()
    predicate = promotion.rules.first().catalogue_predicate
    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(predicate)
    assert current_catalogue["categories"] == {new_category_id}

    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_collections(
    updated_webhook_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
    product_list,
    published_collection,
):
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    new_collection_id = graphene.Node.to_global_id(
        "Collection", published_collection.id
    )

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {
            "collections": [new_collection_id],
        },
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    promotion.refresh_from_db()
    predicate = promotion.rules.first().catalogue_predicate
    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(predicate)
    assert current_catalogue["collections"] == {new_collection_id}

    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_variants(
    updated_webhook_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
    product_list,
    preorder_variant_global_threshold,
):
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    new_variant_id = graphene.Node.to_global_id(
        "ProductVariant", preorder_variant_global_threshold.id
    )

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {
            "variants": [new_variant_id],
        },
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    promotion.refresh_from_db()
    predicate = promotion.rules.first().catalogue_predicate
    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(predicate)
    assert current_catalogue["variants"] == {new_variant_id}

    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_products(
    updated_webhook_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    catalogue_predicate,
    permission_manage_discounts,
    product_list,
    published_collection,
):
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    previous_catalogue = convert_migrated_sale_predicate_to_catalogue_info(
        catalogue_predicate
    )
    new_product_id = graphene.Node.to_global_id("Product", product_list[-1].id)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {
            "products": [new_product_id],
        },
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    promotion.refresh_from_db()
    predicate = promotion.rules.first().catalogue_predicate
    current_catalogue = convert_migrated_sale_predicate_to_catalogue_info(predicate)
    assert current_catalogue["products"] == {new_product_id}

    updated_webhook_mock.assert_called_once_with(
        promotion, previous_catalogue, current_catalogue
    )
    update_products_discounted_prices_for_promotion_task_mock.assert_called_once()


@freeze_time("2020-03-18 12:00:00")
@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_toggle")
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_end_date_before_start_date(
    updated_webhook_mock,
    sale_toggle_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    permission_manage_discounts,
):
    # given
    query = SALE_UPDATE_MUTATION

    promotion = promotion_converted_from_sale
    promotion.start_date = timezone.now() + timedelta(days=1)
    promotion.save(update_fields=["start_date"])
    end_date = timezone.now() - timedelta(days=1)

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {"endDate": end_date},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["sale"]
    errors = content["data"]["saleUpdate"]["errors"]
    assert len(errors) == 1
    assert errors[0]["field"] == "endDate"
    assert errors[0]["code"] == DiscountErrorCode.INVALID.name
    updated_webhook_mock.assert_not_called()
    sale_toggle_mock.assert_not_called()
    update_products_discounted_prices_for_promotion_task_mock.assert_not_called()


@freeze_time("2020-03-18 12:00:00")
def test_update_sale_with_none_values(
    staff_api_client,
    promotion_converted_from_sale,
    permission_manage_discounts,
):
    """Ensure that non-required fields can be nullified."""

    # given
    query = SALE_UPDATE_MUTATION
    promotion = promotion_converted_from_sale

    promotion.name = "Sale name"
    start_date = timezone.now() + timedelta(days=1)
    promotion.start_date = start_date
    promotion.end_date = timezone.now() + timedelta(days=5)
    promotion.save(update_fields=["name", "start_date", "end_date"])

    variables = {
        "id": graphene.Node.to_global_id("Sale", promotion.old_sale_id),
        "input": {
            "name": None,
            "startDate": None,
            "endDate": None,
            "type": None,
            "collections": [],
            "categories": [],
            "products": [],
            "variants": [],
        },
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["errors"]
    data = content["data"]["saleUpdate"]["sale"]
    assert data["type"] == RewardValueType.FIXED.upper()
    assert data["name"] == "Sale name"
    assert data["startDate"] == start_date.isoformat()
    assert not data["endDate"]

    promotion.refresh_from_db()
    assert promotion.start_date.isoformat() == start_date.isoformat()
    assert promotion.start_date == start_date
    assert not promotion.end_date

    rule = promotion.rules.first()
    assert rule.reward_value_type == RewardValueType.FIXED
    assert not rule.catalogue_predicate


@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
@patch("saleor.plugins.manager.PluginsManager.sale_toggle")
@patch("saleor.plugins.manager.PluginsManager.sale_updated")
def test_update_sale_with_promotion_id(
    updated_webhook_mock,
    sale_toggle_mock,
    update_products_discounted_prices_for_promotion_task_mock,
    staff_api_client,
    promotion_converted_from_sale,
    permission_manage_discounts,
):
    # given
    query = SALE_UPDATE_MUTATION
    promotion = promotion_converted_from_sale
    end_date = timezone.now() - timedelta(days=1)

    variables = {
        "id": graphene.Node.to_global_id("Promotion", promotion.id),
        "input": {"endDate": end_date},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["sale"]
    errors = content["data"]["saleUpdate"]["errors"]
    assert len(errors) == 1
    assert errors[0]["field"] == "id"
    assert errors[0]["code"] == DiscountErrorCode.INVALID.name
    assert errors[0]["message"] == (
        "Provided ID refers to Promotion model. "
        "Please use 'promotionUpdate' mutation instead."
    )
    updated_webhook_mock.assert_not_called()
    sale_toggle_mock.assert_not_called()
    update_products_discounted_prices_for_promotion_task_mock.assert_not_called()


def test_update_sale_not_found_error(staff_api_client, permission_manage_discounts):
    # given
    query = SALE_UPDATE_MUTATION
    variables = {
        "id": graphene.Node.to_global_id("Sale", "0"),
        "input": {"name": "updated name"},
    }

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_discounts]
    )

    # then
    content = get_graphql_content(response)
    assert not content["data"]["saleUpdate"]["sale"]
    errors = content["data"]["saleUpdate"]["errors"]
    assert len(errors) == 1
    assert errors[0]["field"] == "id"
    assert errors[0]["code"] == DiscountErrorCode.NOT_FOUND.name
