import datetime
import json
import os
from unittest.mock import patch
from uuid import uuid4

import graphene
import pytest
import pytz

from .....product.error_codes import ProductBulkCreateErrorCode
from .....product.models import Product
from .....product.tests.utils import create_image
from ....tests.utils import (
    get_graphql_content,
    get_multipart_request_body_with_multiple_files,
)

PRODUCT_BULK_CREATE_MUTATION = """
    mutation ProductBulkCreate(
        $products: [ProductBulkCreateInput!]!
    ) {
        productBulkCreate(products: $products) {
            results {
                errors {
                    path
                    code
                    message
                    warehouses
                    channels
                }
                product{
                    id
                    name
                    slug
                    media{
                        url
                        alt
                        type
                        oembedData
                    }
                    category{
                        name
                    }
                    description
                    attributes{
                        attribute{
                          slug
                        }
                        values{
                           value
                        }
                    }
                    channelListings{
                        id
                        channel{
                            name
                        }
                    }
                    variants{
                        name
                        stocks{
                            warehouse{
                                slug
                            }
                            quantity
                        }
                    }
                }
            }
            count
        }
    }
"""


@patch(
    "saleor.product.tasks.update_products_discounted_prices_for_promotion_task.delay"
)
def test_product_bulk_create_with_base_data(
    update_products_discounted_price_task_mock,
    staff_api_client,
    product_type,
    category,
    description_json,
    permission_manage_products,
):
    # given
    description_json_string = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION,
        {"products": products},
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    products = Product.objects.all()
    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert data["results"][0]["product"]["name"] == product_name_1
    assert data["results"][0]["product"]["slug"] == "test-name-1"
    assert data["results"][0]["product"]["description"] == description_json_string
    assert data["results"][0]["product"]["category"]["name"] == category.name
    assert data["results"][1]["product"]["name"] == product_name_2
    assert data["results"][1]["product"]["description"] == description_json_string
    assert data["results"][1]["product"]["category"]["name"] == category.name
    assert len(products) == 2

    for product in products:
        assert product.description == description_json
        assert product.category == category
        assert product.product_type == product_type

    update_products_discounted_price_task_mock.assert_called_once()
    args = set(update_products_discounted_price_task_mock.call_args.args[0])
    assert args == {product.id for product in products}


@patch("saleor.plugins.manager.PluginsManager.product_created")
def test_product_bulk_create_send_product_created_webhook(
    created_webhook_mock,
    staff_api_client,
    product_type,
    category,
    description_json,
    permission_manage_products,
):
    # given
    description_json_string = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION,
        {"products": products},
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert created_webhook_mock.call_count == 2
    for call in created_webhook_mock.call_args_list:
        assert isinstance(call.args[0], Product)


def test_product_bulk_create_with_same_name_and_no_slug(
    staff_api_client,
    product_type,
    category,
    description_json,
    permission_manage_products,
):
    # given
    description_json_string = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name = "test name"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name,
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name,
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION,
        {"products": products},
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert data["results"][0]["product"]["name"] == product_name
    assert data["results"][0]["product"]["slug"] == "test-name"
    assert data["results"][1]["product"]["name"] == product_name
    assert data["results"][1]["product"]["slug"] == "test-name-2"


def test_product_bulk_create_with_invalid_attributes(
    staff_api_client,
    product_type,
    category,
    description_json,
    permission_manage_products,
):
    # given
    description_json_string = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "attributes": [
                {"id": "invalidID", "values": ["invalidValue"]},
            ],
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION,
        {"products": products},
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    assert data["count"] == 0
    assert data["results"][0]["errors"]
    error = data["results"][0]["errors"][0]
    assert error["path"] == "attributes"
    assert error["message"] == "Couldn't resolve id: invalidID."


def test_product_bulk_create_with_media(
    staff_api_client,
    product_type,
    category,
    description_json,
    permission_manage_products,
    media_root,
):
    # given
    description_json_string = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    image_file_1, image_name_1 = create_image(image_name="prod1")
    image_file_2, image_name_2 = create_image(image_name="prod2")
    image_file_3, image_name_3 = create_image(image_name="prod3")

    media_1 = {
        "alt": "",
        "image": image_name_1,
    }

    media_2 = {
        "alt": "",
        "image": image_name_2,
    }

    media_3 = {
        "alt": "",
        "image": image_name_3,
    }

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "media": [media_1, media_2],
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "media": [media_3],
        },
    ]

    files = [image_file_1, image_file_2, image_file_3]

    map_dict = {
        0: ["variables.products.0.media.0.image"],
        1: ["variables.products.0.media.1.image"],
        2: ["variables.products.1.media.0.image"],
    }

    # when
    body = get_multipart_request_body_with_multiple_files(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}, files, map_dict
    )

    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_multipart(body)

    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]
    products = Product.objects.all()

    product_1_media = products[0].media.all()
    product_2_media = products[1].media.all()

    # then
    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert len(product_1_media) == 2
    assert len(product_2_media) == 1

    assert data["results"][0]["product"]["media"][0]["type"] == "IMAGE"
    assert data["results"][0]["product"]["media"][1]["type"] == "IMAGE"
    assert data["results"][1]["product"]["media"][0]["type"] == "IMAGE"

    assert product_1_media[0].image.file
    img_1_name, format = os.path.splitext(image_file_1._name)
    file_1_name = product_1_media[0].image.name
    assert file_1_name != image_file_1._name
    assert file_1_name.startswith(f"products/{img_1_name}")
    assert file_1_name.endswith(format)

    assert product_2_media[0].image.file
    img_3_name, format = os.path.splitext(image_file_3._name)
    file_3_name = product_2_media[0].image.name
    assert file_3_name != image_file_3._name
    assert file_3_name.startswith(f"products/{img_3_name}")
    assert file_3_name.endswith(format)


@pytest.mark.vcr
def test_product_bulk_create_with_media_with_media_url(
    staff_api_client,
    product_type,
    category,
    description_json,
    permission_manage_products,
    media_root,
):
    # given
    description_json_string = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    alt = "Rick Astley - Never Gonna Give You Up (Official Music Video)"
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    media_1 = {
        "alt": "",
        "mediaUrl": url,
    }

    media_2 = {
        "alt": "",
        "mediaUrl": url,
    }

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "media": [media_1],
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json_string,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "media": [media_2],
        },
    ]

    # when
    body = get_multipart_request_body_with_multiple_files(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}, [], {}
    )

    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_multipart(body)

    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]
    products = Product.objects.all()

    product_1_media = products[0].media.all()
    product_2_media = products[1].media.all()

    # then
    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert len(product_1_media) == 1
    assert len(product_2_media) == 1
    assert data["results"][0]["product"]["media"][0]["type"] == "VIDEO"
    assert data["results"][0]["product"]["media"][0]["alt"] == alt
    assert data["results"][0]["product"]["media"][0]["url"] == url
    assert data["results"][1]["product"]["media"][0]["type"] == "VIDEO"
    assert data["results"][1]["product"]["media"][0]["alt"] == alt
    assert data["results"][1]["product"]["media"][0]["url"] == url

    oembed_data = json.loads(data["results"][0]["product"]["media"][0]["oembedData"])
    assert oembed_data["url"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert oembed_data["type"] == "video"
    assert oembed_data["html"] is not None
    assert oembed_data["thumbnail_url"] == (
        "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    )


def test_product_bulk_create_with_attributes(
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
    media_root,
    channel_USD,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    # Default attribute defined in product_type fixture
    color_attr = product_type.product_attributes.get(name="Color")
    color_value_name = color_attr.values.first().name
    color_attr_id = graphene.Node.to_global_id("Attribute", color_attr.id)

    # Add second attribute
    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "attributes": [
                {
                    "externalReference": color_attr.external_reference,
                    "values": [color_value_name],
                },
                {"id": size_attr_id, "values": [non_existent_attr_value]},
            ],
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "attributes": [
                {"id": color_attr_id, "values": [color_value_name]},
                {"id": size_attr_id, "values": [non_existent_attr_value]},
            ],
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    products = Product.objects.all()

    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert (
        data["results"][0]["product"]["attributes"][0]["attribute"]["slug"]
        == color_attr.slug
    )
    assert (
        data["results"][1]["product"]["attributes"][0]["attribute"]["slug"]
        == color_attr.slug
    )

    for product in products:
        first_attribute_assignment = product.attributes.first()
        assert product.attributes.count() == 2
        assert first_attribute_assignment.attribute == color_attr
        assert first_attribute_assignment.values.count() == 1


def test_product_bulk_create_with_attributes_using_external_refs(
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
    media_root,
    channel_USD,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    # Default attribute defined in product_type fixture
    color_attr = product_type.product_attributes.get(name="Color")
    color_value_external_reference = color_attr.values.first().external_reference

    # Add second attribute
    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "attributes": [
                {
                    "externalReference": color_attr.external_reference,
                    "dropdown": {"externalReference": color_value_external_reference},
                },
                {"id": size_attr_id, "values": [non_existent_attr_value]},
            ],
        }
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    products = Product.objects.all()

    assert not data["results"][0]["errors"]
    assert data["count"] == 1
    assert (
        data["results"][0]["product"]["attributes"][0]["attribute"]["slug"]
        == color_attr.slug
    )

    for product in products:
        first_attribute_assignment = product.attributes.first()
        assert product.attributes.count() == 2
        assert first_attribute_assignment.attribute == color_attr
        assert first_attribute_assignment.values.count() == 1


def test_product_bulk_create_with_attributes_and_create_new_value_with_external_ref(
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
    media_root,
    channel_USD,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    # Default attribute defined in product_type fixture
    color_attr = product_type.product_attributes.get(name="Color")
    color_attr_values_count = color_attr.values.count()
    color_value_external_reference = color_attr.values.first().external_reference

    new_value = "NewTestValue"
    new_external_ref = color_value_external_reference + "New"
    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "attributes": [
                {
                    "externalReference": color_attr.external_reference,
                    "dropdown": {
                        "externalReference": new_external_ref,
                        "value": new_value,
                    },
                },
            ],
        }
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    product = Product.objects.last()

    assert not data["results"][0]["errors"]
    assert data["count"] == 1
    assert (
        data["results"][0]["product"]["attributes"][0]["attribute"]["slug"]
        == color_attr.slug
    )
    assert color_attr.values.count() == color_attr_values_count + 1
    first_attribute_assignment = product.attributes.first()
    assert product.attributes.count() == 1
    assert first_attribute_assignment.attribute == color_attr
    assert first_attribute_assignment.values.count() == 1


def test_product_bulk_create_return_error_when_attribute_id_and_external_ref_provided(
    staff_api_client,
    product_type,
    category,
    description_json,
    permission_manage_products,
    media_root,
    channel_USD,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    # Default attribute defined in product_type fixture
    color_attr = product_type.product_attributes.get(name="Color")
    color_value_external_reference = color_attr.values.first().external_reference
    color_attr_id = graphene.Node.to_global_id("Attribute", color_attr.id)

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "attributes": [
                {
                    "id": color_attr_id,
                    "externalReference": color_attr.external_reference,
                    "dropdown": {"externalReference": color_value_external_reference},
                }
            ],
        }
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    assert data["results"][0]["errors"]
    error = data["results"][0]["errors"][0]
    assert error["path"] == "attributes"
    assert error["message"] == (
        "Argument 'id' cannot be combined with 'externalReference'"
    )


def test_product_bulk_create_with_meta_data(
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
):
    # given

    description_json = json.dumps(description_json)
    metadata_key = "md key"
    metadata_value = "md value"
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "metadata": [{"key": metadata_key, "value": metadata_value}],
            "privateMetadata": [{"key": metadata_key, "value": metadata_value}],
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "metadata": [{"key": metadata_key, "value": metadata_value}],
            "privateMetadata": [{"key": metadata_key, "value": metadata_value}],
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    products = Product.objects.all()

    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert len(products) == 2

    for product in products:
        assert product.metadata == {metadata_key: metadata_value}
        assert product.private_metadata == {metadata_key: metadata_value}


def test_product_bulk_create_with_channel_listings(
    staff_api_client,
    product_type,
    category,
    description_json,
    permission_manage_products,
    channel_USD,
):
    # given

    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    channel_id = graphene.Node.to_global_id("Channel", channel_USD.id)
    publication_at = datetime.datetime.now(pytz.utc)

    channel_listings = [
        {
            "channelId": channel_id,
            "isPublished": True,
            "visibleInListings": True,
            "isAvailableForPurchase": True,
            "publishedAt": publication_at,
        }
    ]

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "channelListings": channel_listings,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "channelListings": channel_listings,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert (
        data["results"][0]["product"]["channelListings"][0]["channel"]["name"]
        == channel_USD.name
    )
    assert (
        data["results"][1]["product"]["channelListings"][0]["channel"]["name"]
        == channel_USD.name
    )
    assert Product.objects.count() == 2
    assert channel_USD.product_listings.count() == 2


def test_product_bulk_create_with_variants(
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    sku_1 = str(uuid4())[:12]
    variant_1_name = "new-variant-1-name"

    sku_2 = str(uuid4())[:12]
    variant_2_name = "new-variant-2-name"

    sku_3 = str(uuid4())[:12]
    variant_3_name = "new-variant-3-name"

    variants_prod_1 = [
        {
            "sku": sku_1,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_1_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        },
        {
            "sku": sku_2,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_2_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        },
    ]

    variants_prod_2 = [
        {
            "sku": sku_3,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_3_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        }
    ]

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "variants": variants_prod_1,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "variants": variants_prod_2,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    products = Product.objects.all()
    product_1_variants = products[0].variants.all()
    product_2_variants = products[1].variants.all()

    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert data["results"][0]["product"]["variants"]
    assert data["results"][1]["product"]["variants"]
    assert len(products) == 2
    assert len(product_1_variants) == 2
    assert len(product_2_variants) == 1

    for variant in product_1_variants:
        assert variant.name in [variant_1_name, variant_2_name]
        assert variant.sku in [sku_1, sku_2]
        attribute_assignment = variant.attributes.first()
        assert variant.attributes.count() == 1
        assert attribute_assignment.attribute == size_attribute
        assert attribute_assignment.values.count() == 1

    for variant in product_2_variants:
        assert variant.name == variant_3_name
        assert variant.sku == sku_3
        attribute_assignment = variant.attributes.first()
        assert variant.attributes.count() == 1
        assert attribute_assignment.attribute == size_attribute
        assert attribute_assignment.values.count() == 1


def test_product_bulk_create_with_variants_with_duplicated_sku(
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    sku = str(uuid4())[:12]
    variant_1_name = "new-variant-1-name"
    variant_2_name = "new-variant-2-name"

    variants_prod_1 = [
        {
            "sku": sku,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_1_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        }
    ]
    variants_prod_2 = [
        {
            "sku": sku,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_2_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        }
    ]

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "variants": variants_prod_1,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "variants": variants_prod_2,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    prod_1_errors = data["results"][0]["errors"]
    prod_2_errors = data["results"][1]["errors"]
    assert prod_1_errors
    assert prod_2_errors
    assert data["count"] == 0
    assert prod_1_errors[0]["path"] == "variants.0.sku"
    assert prod_2_errors[0]["path"] == "variants.0.sku"
    assert prod_1_errors[0]["code"] == ProductBulkCreateErrorCode.UNIQUE.name
    assert prod_2_errors[0]["code"] == ProductBulkCreateErrorCode.UNIQUE.name


@patch(
    "saleor.graphql.product.bulk_mutations."
    "product_bulk_create.get_webhooks_for_event"
)
@patch("saleor.plugins.manager.PluginsManager.product_variant_created")
@patch("saleor.plugins.manager.PluginsManager.product_created")
def test_product_bulk_create_with_variants_send_product_variant_created_event(
    product_created_webhook_mock,
    variant_created_webhook_mock,
    mocked_get_webhooks_for_event,
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
    gift_card_expiry_date,
    any_webhook,
    settings,
):
    # given
    mocked_get_webhooks_for_event.return_value = [any_webhook]
    settings.PLUGINS = ["saleor.plugins.webhook.plugin.WebhookPlugin"]

    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    sku_1 = str(uuid4())[:12]
    variant_1_name = "new-variant-1-name"

    sku_2 = str(uuid4())[:12]
    variant_2_name = "new-variant-2-name"

    sku_3 = str(uuid4())[:12]
    variant_3_name = "new-variant-3-name"

    variants_prod_1 = [
        {
            "sku": sku_1,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_1_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        },
        {
            "sku": sku_2,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_2_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        },
    ]

    variants_prod_2 = [
        {
            "sku": sku_3,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_3_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        }
    ]

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "variants": variants_prod_1,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "variants": variants_prod_2,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert product_created_webhook_mock.call_count == 2
    assert variant_created_webhook_mock.call_count == 3


def test_product_bulk_create_with_variants_and_stocks(
    staff_api_client,
    product_type,
    size_attribute,
    category,
    description_json,
    permission_manage_products,
    warehouse,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    sku_1 = str(uuid4())[:12]
    variant_1_name = "new-variant-1-name"

    sku_2 = str(uuid4())[:12]
    variant_2_name = "new-variant-2-name"

    quantity = 20
    stocks = [
        {
            "warehouse": graphene.Node.to_global_id("Warehouse", warehouse.pk),
            "quantity": quantity,
        }
    ]

    variants_prod_1 = [
        {
            "sku": sku_1,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_1_name,
            "stocks": stocks,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        }
    ]

    variants_prod_2 = [
        {
            "sku": sku_2,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_2_name,
            "stocks": stocks,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        }
    ]

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "variants": variants_prod_1,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "variants": variants_prod_2,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    products = Product.objects.all()
    product_1_variant = products[0].variants.last()
    product_2_variant = products[1].variants.last()

    variant_1_data = data["results"][0]["product"]["variants"][0]
    variant_2_data = data["results"][1]["product"]["variants"][0]

    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert variant_1_data["stocks"][0]["quantity"] == quantity
    assert variant_1_data["stocks"][0]["warehouse"]["slug"] == warehouse.slug
    assert variant_2_data["stocks"][0]["quantity"] == quantity
    assert variant_2_data["stocks"][0]["warehouse"]["slug"] == warehouse.slug
    assert len(products) == 2
    assert product_1_variant.stocks.count() == 1
    assert product_2_variant.stocks.count() == 1


def test_product_bulk_create_with_variants_and_invalid_stock(
    staff_api_client,
    product_type,
    size_attribute,
    category,
    description_json,
    permission_manage_products,
    warehouse,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name = "test name 1"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    sku_1 = str(uuid4())[:12]
    variant_1_name = "new-variant-1-name"

    sku_2 = str(uuid4())[:12]
    variant_2_name = "new-variant-2-name"

    quantity = 20
    stocks = [
        {
            "warehouse": graphene.Node.to_global_id("Warehouse", warehouse.pk),
            "quantity": quantity,
        }
    ]

    variants_prod_1 = [
        {
            "sku": sku_1,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_1_name,
            "stocks": stocks,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        },
        {
            "sku": sku_2,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_2_name,
            "stocks": [
                {
                    "warehouse": "invalidId",
                    "quantity": quantity,
                }
            ],
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
        },
    ]

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "variants": variants_prod_1,
        }
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    assert not data["results"][0]["product"]
    errors = data["results"][0]["errors"]
    assert errors
    assert errors[0]["path"] == "variants.1.stocks.0.warehouse"
    assert errors[0]["code"] == ProductBulkCreateErrorCode.NOT_FOUND.name
    assert data["count"] == 0


@patch(
    (
        "saleor.graphql.product.bulk_mutations."
        "product_bulk_create.get_webhooks_for_event"
    )
)
@patch("saleor.plugins.manager.PluginsManager.channel_updated")
def test_product_bulk_create_with_variants_and_channel_listings(
    channel_updated_webhook_mock,
    mocked_get_webhooks_for_event,
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
    channel_USD,
    any_webhook,
    settings,
):
    # given
    mocked_get_webhooks_for_event.return_value = [any_webhook]
    settings.PLUGINS = ["saleor.plugins.webhook.plugin.WebhookPlugin"]
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    product_name_2 = "test name 2"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    sku_1 = str(uuid4())[:12]
    variant_1_name = "new-variant-1-name"

    sku_2 = str(uuid4())[:12]
    variant_2_name = "new-variant-2-name"

    channel_id = graphene.Node.to_global_id("Channel", channel_USD.id)
    publication_at = datetime.datetime.now(pytz.utc)

    product_channel_listings = [
        {
            "channelId": channel_id,
            "isPublished": True,
            "visibleInListings": True,
            "isAvailableForPurchase": True,
            "publishedAt": publication_at,
        }
    ]

    price = 10.0
    cost_price = 11.0
    variant_channel_listings = [
        {
            "price": price,
            "costPrice": cost_price,
            "channelId": channel_id,
        }
    ]

    variants_prod_1 = [
        {
            "sku": sku_1,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_1_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
            "channelListings": variant_channel_listings,
        },
    ]

    variants_prod_2 = [
        {
            "sku": sku_2,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_2_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
            "channelListings": variant_channel_listings,
        }
    ]

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "channelListings": product_channel_listings,
            "variants": variants_prod_1,
        },
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_2,
            "slug": f"{base_product_slug}-2",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "channelListings": product_channel_listings,
            "variants": variants_prod_2,
        },
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    products = Product.objects.all()
    product_1_variant = products[0].variants.last()
    product_2_variant = products[1].variants.last()

    assert not data["results"][0]["errors"]
    assert not data["results"][1]["errors"]
    assert data["count"] == 2
    assert data["results"][0]["product"]["variants"]
    assert data["results"][1]["product"]["variants"]
    assert len(products) == 2

    assert product_1_variant.channel_listings.last().channel_id == channel_USD.id
    assert product_2_variant.channel_listings.last().channel_id == channel_USD.id

    # 2 product channel listing and 2 variant channel listing were created but
    # all are using same channel so only one event should be sent
    channel_updated_webhook_mock.assert_called_once_with(
        channel_USD, webhooks=[any_webhook]
    )


def test_product_bulk_create_with_variants_and_channel_listings_with_wrong_price(
    staff_api_client,
    product_type,
    category,
    size_attribute,
    description_json,
    permission_manage_products,
    channel_USD,
):
    # given
    description_json = json.dumps(description_json)
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.pk)
    category_id = graphene.Node.to_global_id("Category", category.pk)

    product_name_1 = "test name 1"
    base_product_slug = "product-test-slug"
    product_charge_taxes = True
    product_tax_rate = "STANDARD"

    product_type.product_attributes.add(size_attribute)
    size_attr_id = graphene.Node.to_global_id("Attribute", size_attribute.id)
    non_existent_attr_value = "The cake is a lie"

    sku_1 = str(uuid4())[:12]
    variant_1_name = "new-variant-1-name"

    channel_id = graphene.Node.to_global_id("Channel", channel_USD.id)
    publication_at = datetime.datetime.now(pytz.utc)

    product_channel_listings = [
        {
            "channelId": channel_id,
            "isPublished": True,
            "visibleInListings": True,
            "isAvailableForPurchase": True,
            "publishedAt": publication_at,
        }
    ]

    price = 10.000001
    cost_price = 11.0000001

    variant_channel_listings = [
        {
            "price": price,
            "costPrice": cost_price,
            "channelId": channel_id,
        }
    ]

    variants_prod_1 = [
        {
            "sku": sku_1,
            "weight": 2.5,
            "trackInventory": True,
            "name": variant_1_name,
            "attributes": [{"id": size_attr_id, "values": [non_existent_attr_value]}],
            "channelListings": variant_channel_listings,
        },
    ]

    products = [
        {
            "productType": product_type_id,
            "category": category_id,
            "name": product_name_1,
            "slug": f"{base_product_slug}-1",
            "description": description_json,
            "chargeTaxes": product_charge_taxes,
            "taxCode": product_tax_rate,
            "weight": 2,
            "channelListings": product_channel_listings,
            "variants": variants_prod_1,
        }
    ]

    # when
    staff_api_client.user.user_permissions.add(permission_manage_products)
    response = staff_api_client.post_graphql(
        PRODUCT_BULK_CREATE_MUTATION, {"products": products}
    )
    content = get_graphql_content(response)
    data = content["data"]["productBulkCreate"]

    # then
    assert data["count"] == 0
    assert not data["results"][0]["product"]
    errors = data["results"][0]["errors"]
    assert len(errors) == 2
    assert errors[0]["path"] == "variants.0.channelListings.0.price"
    assert errors[0]["code"] == ProductBulkCreateErrorCode.INVALID_PRICE.name
    assert errors[0]["channels"] == [channel_id]
    assert errors[1]["path"] == "variants.0.channelListings.0.costPrice"
    assert errors[1]["code"] == ProductBulkCreateErrorCode.INVALID_PRICE.name
    assert errors[1]["channels"] == [channel_id]
