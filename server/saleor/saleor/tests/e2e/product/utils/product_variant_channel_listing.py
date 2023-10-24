from ...utils import get_graphql_content

PRODUCT_CHANNEL_LISTING_UPDATE_MUTATION = """
mutation UpdateProductVariantChannelListing(
    $productVariantId: ID!, $input: [ProductVariantChannelListingAddInput!]!
) {
  productVariantChannelListingUpdate(id: $productVariantId, input: $input) {
    errors {
      field
      message
      code
    }
    variant {
      id
      channelListings {
        id
        price {
          amount
        }
        channel {
          id
        }
      }
    }
  }
}
"""


def raw_create_product_variant_channel_listing(
    staff_api_client,
    product_variant_id,
    channel_id,
    price,
):
    variables = {
        "productVariantId": product_variant_id,
        "input": [
            {
                "channelId": channel_id,
                "price": price,
            },
        ],
    }

    response = staff_api_client.post_graphql(
        PRODUCT_CHANNEL_LISTING_UPDATE_MUTATION,
        variables,
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    data = content["data"]["productVariantChannelListingUpdate"]
    assert data["errors"] == []

    return data


def create_product_variant_channel_listing(
    staff_api_client,
    product_variant_id,
    channel_id,
    price,
):
    response = raw_create_product_variant_channel_listing(
        staff_api_client,
        product_variant_id,
        channel_id,
        price,
    )

    data = response["variant"]
    assert data["id"] == product_variant_id
    channel_listing_data = data["channelListings"][0]
    assert channel_listing_data["channel"]["id"] == channel_id
    assert channel_listing_data["price"]["amount"] == float(price)

    return data
