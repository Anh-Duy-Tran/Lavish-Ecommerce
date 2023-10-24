import uuid
from decimal import Decimal

import graphene
import pytest

from ....attribute.utils import associate_attribute_values_to_instance
from ....product import ProductTypeKind
from ....product.models import (
    Category,
    Collection,
    CollectionChannelListing,
    Product,
    ProductChannelListing,
    ProductType,
    ProductVariant,
    ProductVariantChannelListing,
)
from ....tests.utils import dummy_editorjs
from ....warehouse.models import Stock
from ...tests.utils import get_graphql_content


@pytest.fixture
def categories_for_pagination(product_type):
    categories = Category.tree.build_tree_nodes(
        {
            "id": 1,
            "name": "Category2",
            "slug": "cat1",
            "children": [
                {"parent_id": 1, "name": "CategoryCategory1", "slug": "cat_cat1"},
                {"parent_id": 1, "name": "CategoryCategory2", "slug": "cat_cat2"},
                {"parent_id": 1, "name": "Category1", "slug": "cat2"},
                {"parent_id": 1, "name": "Category3", "slug": "cat3"},
            ],
        }
    )
    categories = Category.objects.bulk_create(categories)
    Product.objects.bulk_create(
        [
            Product(
                name="Prod1",
                slug="prod1",
                product_type=product_type,
                category=categories[4],
            ),
            Product(
                name="Prod2",
                slug="prod2",
                product_type=product_type,
                category=categories[4],
            ),
            Product(
                name="Prod3",
                slug="prod3",
                product_type=product_type,
                category=categories[2],
            ),
        ]
    )
    return categories


QUERY_CATEGORIES_PAGINATION = """
    query (
        $first: Int, $last: Int, $after: String, $before: String,
        $sortBy: CategorySortingInput, $filter: CategoryFilterInput
    ){
        categories(
            first: $first, last: $last, after: $after, before: $before,
            sortBy: $sortBy, filter: $filter
        ) {
            edges {
                node {
                    name


                }
            }
            pageInfo{
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
        }
    }
"""


@pytest.mark.parametrize(
    "sort_by, categories_order",
    [
        (
            {"field": "NAME", "direction": "ASC"},
            ["Category1", "Category2", "Category3"],
        ),
        (
            {"field": "NAME", "direction": "DESC"},
            ["CategoryCategory2", "CategoryCategory1", "Category3"],
        ),
        (
            {"field": "SUBCATEGORY_COUNT", "direction": "ASC"},
            ["Category1", "Category3", "CategoryCategory1"],
        ),
        (
            {"field": "PRODUCT_COUNT", "direction": "ASC"},
            ["Category1", "CategoryCategory1", "CategoryCategory2"],
        ),
    ],
)
def test_categories_pagination_with_sorting(
    sort_by,
    categories_order,
    staff_api_client,
    categories_for_pagination,
):
    page_size = 3

    variables = {"first": page_size, "after": None, "sortBy": sort_by}
    response = staff_api_client.post_graphql(
        QUERY_CATEGORIES_PAGINATION,
        variables,
    )
    content = get_graphql_content(response)
    categories_nodes = content["data"]["categories"]["edges"]
    assert categories_order[0] == categories_nodes[0]["node"]["name"]
    assert categories_order[1] == categories_nodes[1]["node"]["name"]
    assert categories_order[2] == categories_nodes[2]["node"]["name"]
    assert len(categories_nodes) == page_size


@pytest.mark.parametrize(
    "filter_by, categories_order",
    [
        ({"search": "CategoryCategory"}, ["CategoryCategory1", "CategoryCategory2"]),
        ({"search": "cat_cat"}, ["CategoryCategory1", "CategoryCategory2"]),
        ({"search": "Category1"}, ["CategoryCategory1", "Category1"]),
    ],
)
def test_categories_pagination_with_filtering(
    filter_by,
    categories_order,
    staff_api_client,
    categories_for_pagination,
):
    page_size = 2

    variables = {"first": page_size, "after": None, "filter": filter_by}
    response = staff_api_client.post_graphql(
        QUERY_CATEGORIES_PAGINATION,
        variables,
    )
    content = get_graphql_content(response)
    categories_nodes = content["data"]["categories"]["edges"]
    assert categories_order[0] == categories_nodes[0]["node"]["name"]
    assert categories_order[1] == categories_nodes[1]["node"]["name"]
    assert len(categories_nodes) == page_size


@pytest.fixture
def collections_for_pagination(product, product_with_single_variant, channel_USD):
    collections = Collection.objects.bulk_create(
        [
            Collection(name="Collection1", slug="col1"),
            Collection(name="CollectionCollection1", slug="col_col1"),
            Collection(name="CollectionCollection2", slug="col_col2"),
            Collection(name="Collection2", slug="col2"),
            Collection(name="Collection3", slug="col3"),
        ]
    )
    collections[2].products.add(product)
    collections[4].products.add(product_with_single_variant)
    published = (True, True, False, False, True)
    CollectionChannelListing.objects.bulk_create(
        [
            CollectionChannelListing(
                channel=channel_USD, is_published=published[num], collection=collection
            )
            for num, collection in enumerate(collections)
        ]
    )
    return collections


QUERY_COLLECTIONS_PAGINATION = """
    query (
        $first: Int, $last: Int, $after: String, $before: String, $channel: String,
        $sortBy: CollectionSortingInput, $filter: CollectionFilterInput
    ){
        collections (
            first: $first, last: $last, after: $after, before: $before,
            sortBy: $sortBy, filter: $filter, channel: $channel
        ) {
            edges {
                node {
                    name
                    products{
                        totalCount
                    }
                }
            }
            pageInfo{
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
        }
    }
"""


@pytest.mark.parametrize(
    "sort_by, collections_order",
    [
        (
            {"field": "NAME", "direction": "ASC"},
            ["Collection1", "Collection2", "Collection3"],
        ),
        (
            {"field": "NAME", "direction": "DESC"},
            ["CollectionCollection2", "CollectionCollection1", "Collection3"],
        ),
        (
            {"field": "AVAILABILITY", "direction": "ASC"},
            ["Collection2", "CollectionCollection2", "Collection1"],
        ),
        (
            {"field": "PRODUCT_COUNT", "direction": "DESC"},
            ["CollectionCollection2", "Collection3", "CollectionCollection1"],
        ),
    ],
)
def test_collections_pagination_with_sorting(
    sort_by,
    collections_order,
    staff_api_client,
    permission_manage_products,
    collections_for_pagination,
    channel_USD,
):
    page_size = 3
    variables = {
        "first": page_size,
        "after": None,
        "sortBy": sort_by,
        "channel": channel_USD.slug,
    }
    response = staff_api_client.post_graphql(
        QUERY_COLLECTIONS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    collections_nodes = content["data"]["collections"]["edges"]
    assert collections_order[0] == collections_nodes[0]["node"]["name"]
    assert collections_order[1] == collections_nodes[1]["node"]["name"]
    assert collections_order[2] == collections_nodes[2]["node"]["name"]
    assert len(collections_nodes) == page_size


@pytest.mark.parametrize(
    "filter_by, collections_order",
    [
        (
            {"search": "CollectionCollection"},
            ["CollectionCollection1", "CollectionCollection2"],
        ),
        ({"search": "col_col"}, ["CollectionCollection1", "CollectionCollection2"]),
        ({"search": "Collection1"}, ["Collection1", "CollectionCollection1"]),
        ({"published": "HIDDEN"}, ["Collection2", "CollectionCollection2"]),
    ],
)
def test_collections_pagination_with_filtering(
    filter_by,
    collections_order,
    staff_api_client,
    permission_manage_products,
    collections_for_pagination,
    channel_USD,
):
    page_size = 2
    variables = {
        "first": page_size,
        "after": None,
        "filter": filter_by,
        "channel": channel_USD.slug,
    }
    response = staff_api_client.post_graphql(
        QUERY_COLLECTIONS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    collections_nodes = content["data"]["collections"]["edges"]
    assert collections_order[0] == collections_nodes[0]["node"]["name"]
    assert collections_order[1] == collections_nodes[1]["node"]["name"]
    assert len(collections_nodes) == page_size


@pytest.fixture
def products_for_pagination(
    product_type, color_attribute, category, warehouse, channel_USD
):
    product_type2 = ProductType.objects.create(
        name="Apple", kind=ProductTypeKind.NORMAL
    )
    products = Product.objects.bulk_create(
        [
            Product(
                name="Product1",
                slug="prod1",
                category=category,
                product_type=product_type2,
                description=dummy_editorjs("Test description 1."),
            ),
            Product(
                name="ProductProduct1",
                slug="prod_prod1",
                category=category,
                product_type=product_type,
            ),
            Product(
                name="ProductProduct2",
                slug="prod_prod2",
                category=category,
                product_type=product_type2,
            ),
            Product(
                name="Product2",
                slug="prod2",
                category=category,
                product_type=product_type,
                description=dummy_editorjs("Test description 2."),
            ),
            Product(
                name="Product3",
                slug="prod3",
                category=category,
                product_type=product_type2,
                description=dummy_editorjs("Test description 3."),
            ),
        ]
    )
    ProductChannelListing.objects.bulk_create(
        [
            ProductChannelListing(
                product=products[0],
                channel=channel_USD,
                is_published=True,
                discounted_price_amount=Decimal(5),
            ),
            ProductChannelListing(
                product=products[1],
                channel=channel_USD,
                is_published=True,
                discounted_price_amount=Decimal(15),
            ),
            ProductChannelListing(
                product=products[2],
                channel=channel_USD,
                is_published=False,
                discounted_price_amount=Decimal(4),
            ),
            ProductChannelListing(
                product=products[3],
                channel=channel_USD,
                is_published=True,
                discounted_price_amount=Decimal(7),
            ),
        ]
    )

    product_attrib_values = color_attribute.values.all()
    associate_attribute_values_to_instance(
        products[1], color_attribute, product_attrib_values[0]
    )
    associate_attribute_values_to_instance(
        products[3], color_attribute, product_attrib_values[1]
    )

    variants = ProductVariant.objects.bulk_create(
        [
            ProductVariant(
                product=products[0],
                sku=str(uuid.uuid4()).replace("-", ""),
                track_inventory=True,
            ),
            ProductVariant(
                product=products[1],
                sku=str(uuid.uuid4()).replace("-", ""),
                track_inventory=True,
            ),
            ProductVariant(
                product=products[2],
                sku=str(uuid.uuid4()).replace("-", ""),
                track_inventory=True,
            ),
            ProductVariant(
                product=products[3],
                sku=str(uuid.uuid4()).replace("-", ""),
                track_inventory=True,
            ),
            ProductVariant(
                product=products[4],
                sku=str(uuid.uuid4()).replace("-", ""),
                track_inventory=True,
            ),
        ]
    )
    ProductVariantChannelListing.objects.bulk_create(
        [
            ProductVariantChannelListing(
                variant=variants[0],
                channel=channel_USD,
                price_amount=Decimal(10),
                currency=channel_USD.currency_code,
            ),
            ProductVariantChannelListing(
                variant=variants[1],
                channel=channel_USD,
                price_amount=Decimal(15),
                currency=channel_USD.currency_code,
            ),
            ProductVariantChannelListing(
                variant=variants[2],
                channel=channel_USD,
                price_amount=Decimal(8),
                currency=channel_USD.currency_code,
            ),
            ProductVariantChannelListing(
                variant=variants[3],
                channel=channel_USD,
                price_amount=Decimal(7),
                currency=channel_USD.currency_code,
            ),
        ]
    )
    Stock.objects.bulk_create(
        [
            Stock(warehouse=warehouse, product_variant=variants[0], quantity=100),
            Stock(warehouse=warehouse, product_variant=variants[1], quantity=0),
            Stock(warehouse=warehouse, product_variant=variants[2], quantity=0),
        ]
    )

    return products


QUERY_PRODUCTS_PAGINATION = """
    query (
        $first: Int, $last: Int, $after: String, $before: String, $channel: String,
        $sortBy: ProductOrder, $filter: ProductFilterInput
    ){
        products (
            first: $first, last: $last, after: $after, before: $before,
            sortBy: $sortBy, filter: $filter, channel: $channel
        ) {
            edges {
                node {
                    name
                    slug
                }
            }
            pageInfo{
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
        }
    }
"""


@pytest.mark.parametrize(
    "sort_by, products_order",
    [
        ({"field": "NAME", "direction": "ASC"}, ["Product1", "Product2", "Product3"]),
        (
            {"field": "NAME", "direction": "DESC"},
            ["ProductProduct2", "ProductProduct1", "Product3"],
        ),
        (
            {"field": "TYPE", "direction": "ASC"},
            ["Product1", "Product3", "ProductProduct2"],
        ),
    ],
)
def test_products_pagination_with_sorting(
    sort_by,
    products_order,
    staff_api_client,
    permission_manage_products,
    products_for_pagination,
):
    page_size = 3

    variables = {"first": page_size, "after": None, "sortBy": sort_by}
    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    assert products_order[0] == products_nodes[0]["node"]["name"]
    assert products_order[1] == products_nodes[1]["node"]["name"]
    assert products_order[2] == products_nodes[2]["node"]["name"]
    assert len(products_nodes) == page_size


@pytest.mark.parametrize(
    "sort_by, products_order",
    [
        (
            {"field": "PUBLISHED", "direction": "ASC"},
            ["ProductProduct2", "Product1", "Product2"],
        ),
        (
            {"field": "PRICE", "direction": "ASC"},
            ["Product2", "ProductProduct2", "Product1"],
        ),
        (
            {"field": "MINIMAL_PRICE", "direction": "ASC"},
            ["ProductProduct2", "Product1", "Product2"],
        ),
    ],
)
def test_products_pagination_with_sorting_and_channel(
    sort_by,
    products_order,
    staff_api_client,
    permission_manage_products,
    products_for_pagination,
    channel_USD,
):
    page_size = 3

    variables = {
        "first": page_size,
        "after": None,
        "sortBy": sort_by,
        "channel": channel_USD.slug,
    }
    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    assert products_order[0] == products_nodes[0]["node"]["name"]
    assert products_order[1] == products_nodes[1]["node"]["name"]
    assert products_order[2] == products_nodes[2]["node"]["name"]
    assert len(products_nodes) == page_size


def test_products_pagination_with_sorting_by_attribute(
    staff_api_client,
    permission_manage_products,
    products_for_pagination,
    color_attribute,
    channel_USD,
):
    page_size = 3
    products_order = ["Product2", "ProductProduct1", "Product1"]
    attribute_id = graphene.Node.to_global_id("Attribute", color_attribute.id)

    sort_by = {"attributeId": attribute_id, "direction": "ASC"}
    variables = {"first": page_size, "after": None, "sortBy": sort_by}
    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    assert products_order[0] == products_nodes[0]["node"]["name"]
    assert products_order[1] == products_nodes[1]["node"]["name"]
    assert products_order[2] == products_nodes[2]["node"]["name"]
    assert len(products_nodes) == page_size


def test_products_pagination_for_products_with_the_same_names_two_pages(
    staff_api_client, permission_manage_products, category, product_type, channel_USD
):
    products = Product.objects.bulk_create(
        [
            Product(
                name="Product",
                slug="prod-1",
                category=category,
                product_type=product_type,
            ),
            Product(
                name="Product",
                slug="prod-2",
                category=category,
                product_type=product_type,
            ),
            Product(
                name="Product",
                slug="prod-3",
                category=category,
                product_type=product_type,
            ),
        ]
    )
    page_size = 2
    variables = {"first": page_size, "after": None}

    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )

    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    page_info = content["data"]["products"]["pageInfo"]

    assert len(products_nodes) == 2
    assert products_nodes[0]["node"]["slug"] == products[0].slug
    assert products_nodes[1]["node"]["slug"] == products[1].slug
    assert page_info["hasNextPage"] is True

    end_cursor = page_info["endCursor"]
    variables["after"] = end_cursor

    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )

    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    page_info = content["data"]["products"]["pageInfo"]
    assert len(products_nodes) == 1
    assert products_nodes[0]["node"]["slug"] == products[2].slug
    assert page_info["hasNextPage"] is False


def test_products_pagination_for_products_with_the_same_names_one_page(
    staff_api_client, permission_manage_products, category, product_type, channel_USD
):
    products = Product.objects.bulk_create(
        [
            Product(
                name="Product",
                slug="prod-1",
                category=category,
                product_type=product_type,
            ),
            Product(
                name="Product",
                slug="prod-2",
                category=category,
                product_type=product_type,
            ),
            Product(
                name="Product",
                slug="prod-3",
                category=category,
                product_type=product_type,
            ),
        ]
    )
    page_size = 3
    variables = {"first": page_size, "after": None}

    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )

    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    page_info = content["data"]["products"]["pageInfo"]

    assert len(products_nodes) == 3
    assert products_nodes[0]["node"]["slug"] == products[0].slug
    assert products_nodes[1]["node"]["slug"] == products[1].slug
    assert products_nodes[2]["node"]["slug"] == products[2].slug
    assert page_info["hasNextPage"] is False


@pytest.mark.parametrize(
    "filter_by, products_order",
    [
        ({"hasCategory": True}, ["Product1", "Product2"]),
        (
            {"stockAvailability": "OUT_OF_STOCK"},
            ["Product2", "ProductProduct1"],
        ),
    ],
)
def test_products_pagination_with_filtering(
    filter_by,
    products_order,
    staff_api_client,
    permission_manage_products,
    products_for_pagination,
    channel_USD,
):
    page_size = 2

    variables = {
        "first": page_size,
        "after": None,
        "filter": filter_by,
        "channel": channel_USD.slug,
    }
    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    assert len(products_nodes) == page_size
    assert products_order[0] == products_nodes[0]["node"]["name"]
    assert products_order[1] == products_nodes[1]["node"]["name"]


@pytest.mark.parametrize(
    "filter_by, products_order",
    [
        ({"isPublished": True}, ["Product1", "Product2"]),
        ({"price": {"gte": 8, "lte": 12}}, ["Product1", "ProductProduct2"]),
    ],
)
def test_products_pagination_with_filtering_and_channel(
    filter_by,
    products_order,
    staff_api_client,
    permission_manage_products,
    products_for_pagination,
    channel_USD,
):
    page_size = 2

    variables = {
        "first": page_size,
        "after": None,
        "filter": filter_by,
        "channel": channel_USD.slug,
    }
    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    assert products_order[0] == products_nodes[0]["node"]["name"]
    assert products_order[1] == products_nodes[1]["node"]["name"]
    assert len(products_nodes) == page_size


def test_products_pagination_with_filtering_by_attribute(
    staff_api_client, permission_manage_products, products_for_pagination, channel_USD
):
    page_size = 2
    products_order = ["Product2", "ProductProduct1"]
    filter_by = {
        "attributes": [{"slug": "color", "values": ["red", "blue"]}],
    }

    variables = {
        "first": page_size,
        "after": None,
        "filter": filter_by,
        "channel": channel_USD.slug,
    }
    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    assert products_order[0] == products_nodes[0]["node"]["name"]
    assert products_order[1] == products_nodes[1]["node"]["name"]
    assert len(products_nodes) == page_size


def test_products_pagination_with_filtering_by_product_types(
    staff_api_client,
    permission_manage_products,
    products_for_pagination,
    product_type,
    channel_USD,
):
    page_size = 2
    products_order = ["Product2", "ProductProduct1"]
    product_type_id = graphene.Node.to_global_id("ProductType", product_type.id)
    filter_by = {"productTypes": [product_type_id]}

    variables = {"first": page_size, "after": None, "filter": filter_by}
    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    assert products_order[0] == products_nodes[0]["node"]["name"]
    assert products_order[1] == products_nodes[1]["node"]["name"]
    assert len(products_nodes) == page_size


def test_products_pagination_with_filtering_by_stocks(
    staff_api_client,
    permission_manage_products,
    products_for_pagination,
    warehouse,
    channel_USD,
):
    page_size = 2
    products_order = ["ProductProduct1", "ProductProduct2"]
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.id)
    filter_by = {"stocks": {"warehouseIds": [warehouse_id], "quantity": {"lte": 10}}}

    variables = {"first": page_size, "after": None, "filter": filter_by}
    response = staff_api_client.post_graphql(
        QUERY_PRODUCTS_PAGINATION,
        variables,
        permissions=[permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)
    products_nodes = content["data"]["products"]["edges"]
    assert products_order[0] == products_nodes[0]["node"]["name"]
    assert products_order[1] == products_nodes[1]["node"]["name"]
    assert len(products_nodes) == page_size


@pytest.fixture
def product_types_for_pagination(db):
    return ProductType.objects.bulk_create(
        [
            ProductType(
                name="ProductType1",
                slug="pt1",
                is_digital=True,
                is_shipping_required=False,
            ),
            ProductType(
                name="ProductTypeProductType1",
                slug="pt_pt1",
                is_digital=False,
                is_shipping_required=False,
            ),
            ProductType(
                name="ProductTypeProductType2",
                slug="pt_pt2",
                is_digital=False,
                is_shipping_required=True,
            ),
            ProductType(
                name="ProductType2",
                slug="pt2",
                is_digital=False,
                is_shipping_required=True,
                has_variants=False,
            ),
            ProductType(
                name="ProductType3",
                slug="pt3",
                is_digital=True,
                is_shipping_required=False,
                has_variants=False,
            ),
        ]
    )


QUERY_PRODUCT_TYPES_PAGINATION = """
    query (
        $first: Int, $last: Int, $after: String, $before: String,
        $sortBy: ProductTypeSortingInput, $filter: ProductTypeFilterInput
    ){
        productTypes (
            first: $first, last: $last, after: $after, before: $before,
            sortBy: $sortBy, filter: $filter
        ) {
            edges {
                node {
                    name
                }
            }
            pageInfo{
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
        }
    }
"""


@pytest.mark.parametrize(
    "sort_by, product_types_order",
    [
        (
            {"field": "NAME", "direction": "ASC"},
            ["ProductType1", "ProductType2", "ProductType3"],
        ),
        (
            {"field": "NAME", "direction": "DESC"},
            ["ProductTypeProductType2", "ProductTypeProductType1", "ProductType3"],
        ),
        (
            {"field": "DIGITAL", "direction": "ASC"},
            ["ProductType2", "ProductTypeProductType1", "ProductTypeProductType2"],
        ),
        (
            {"field": "SHIPPING_REQUIRED", "direction": "ASC"},
            ["ProductType1", "ProductType3", "ProductTypeProductType1"],
        ),
    ],
)
def test_product_types_pagination_with_sorting(
    sort_by,
    product_types_order,
    staff_api_client,
    product_types_for_pagination,
):
    page_size = 3

    variables = {"first": page_size, "after": None, "sortBy": sort_by}
    response = staff_api_client.post_graphql(QUERY_PRODUCT_TYPES_PAGINATION, variables)
    content = get_graphql_content(response)
    product_types_nodes = content["data"]["productTypes"]["edges"]
    assert product_types_order[0] == product_types_nodes[0]["node"]["name"]
    assert product_types_order[1] == product_types_nodes[1]["node"]["name"]
    assert product_types_order[2] == product_types_nodes[2]["node"]["name"]
    assert len(product_types_nodes) == page_size


@pytest.mark.parametrize(
    "filter_by, product_types_order",
    [
        (
            {"search": "ProductTypeProductType"},
            ["ProductTypeProductType1", "ProductTypeProductType2"],
        ),
        ({"search": "ProductType1"}, ["ProductType1", "ProductTypeProductType1"]),
        ({"search": "pt_pt"}, ["ProductTypeProductType1", "ProductTypeProductType2"]),
        (
            {"productType": "DIGITAL"},
            ["ProductType1", "ProductType3"],
        ),
        ({"productType": "SHIPPABLE"}, ["ProductType2", "ProductTypeProductType2"]),
        ({"configurable": "CONFIGURABLE"}, ["ProductType1", "ProductTypeProductType1"]),
        ({"configurable": "SIMPLE"}, ["ProductType2", "ProductType3"]),
    ],
)
def test_product_types_pagination_with_filtering(
    filter_by,
    product_types_order,
    staff_api_client,
    product_types_for_pagination,
):
    page_size = 2

    variables = {"first": page_size, "after": None, "filter": filter_by}
    response = staff_api_client.post_graphql(
        QUERY_PRODUCT_TYPES_PAGINATION,
        variables,
    )
    content = get_graphql_content(response)
    product_types_nodes = content["data"]["productTypes"]["edges"]
    assert product_types_order[0] == product_types_nodes[0]["node"]["name"]
    assert product_types_order[1] == product_types_nodes[1]["node"]["name"]
    assert len(product_types_nodes) == page_size
