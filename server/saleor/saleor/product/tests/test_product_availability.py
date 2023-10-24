import datetime
from decimal import Decimal

from django.utils import timezone
from freezegun import freeze_time
from prices import Money, TaxedMoney, TaxedMoneyRange

from ...tax import TaxCalculationStrategy
from .. import models
from ..utils.availability import get_product_availability


def test_availability(stock, monkeypatch, settings, channel_USD):
    product = stock.product_variant.product
    tax_class = product.tax_class or product.product_type.tax_class

    tc = channel_USD.tax_configuration
    tc.tax_calculation_strategy = TaxCalculationStrategy.FLAT_RATES
    tc.charge_taxes = True
    tc.prices_entered_with_tax = False
    tc.save()

    tax_rate = Decimal(23)
    country = "PL"
    tax_class.country_rates.update_or_create(rate=tax_rate, country=country)

    product_channel_listing = product.channel_listings.first()
    variants = product.variants.all()
    variants_channel_listing = models.ProductVariantChannelListing.objects.filter(
        variant__in=variants
    )
    taxed_price = TaxedMoney(Money("10.0", "USD"), Money("12.30", "USD"))
    availability = get_product_availability(
        product_channel_listing=product_channel_listing,
        variants_channel_listing=variants_channel_listing,
        tax_rate=tax_rate,
        tax_calculation_strategy=tc.tax_calculation_strategy,
        prices_entered_with_tax=tc.prices_entered_with_tax,
    )
    taxed_price_range = TaxedMoneyRange(start=taxed_price, stop=taxed_price)
    assert availability.price_range == taxed_price_range

    availability = get_product_availability(
        product_channel_listing=product_channel_listing,
        variants_channel_listing=variants_channel_listing,
        tax_rate=tax_rate,
        tax_calculation_strategy=tc.tax_calculation_strategy,
        prices_entered_with_tax=tc.prices_entered_with_tax,
    )
    assert availability.price_range.start.tax.amount
    assert availability.price_range.stop.tax.amount
    assert availability.price_range_undiscounted.start.tax.amount
    assert availability.price_range_undiscounted.stop.tax.amount


def test_availability_with_all_variant_channel_listings(stock, channel_USD):
    # given
    tax_config = channel_USD.tax_configuration

    product = stock.product_variant.product
    product_channel_listing = product.channel_listings.first()
    variants = product.variants.all()
    variants_channel_listing = models.ProductVariantChannelListing.objects.filter(
        variant__in=variants, channel=channel_USD
    )
    [variant1_channel_listing, variant2_channel_listing] = variants_channel_listing
    variant2_channel_listing.price_amount = Decimal(15)
    variant2_channel_listing.discounted_price_amount = Decimal(15)
    variant2_channel_listing.save()

    # when
    availability = get_product_availability(
        product_channel_listing=product_channel_listing,
        variants_channel_listing=variants_channel_listing,
        prices_entered_with_tax=tax_config.prices_entered_with_tax,
        tax_calculation_strategy=tax_config.tax_calculation_strategy,
        tax_rate=Decimal(0),
    )

    # then
    price_range = availability.price_range
    assert price_range.start.gross.amount == variant1_channel_listing.price_amount
    assert price_range.stop.gross.amount == variant2_channel_listing.price_amount


def test_availability_no_prices(stock, channel_USD):
    # given
    product = stock.product_variant.product
    tax_class = product.tax_class or product.product_type.tax_class

    tc = channel_USD.tax_configuration
    tc.tax_calculation_strategy = TaxCalculationStrategy.FLAT_RATES
    tc.charge_taxes = True
    tc.prices_entered_with_tax = False
    tc.save()

    tax_rate = Decimal(23)
    country = "PL"
    tax_class.country_rates.update_or_create(rate=tax_rate, country=country)

    product_channel_listing = product.channel_listings.first()
    variants = product.variants.all()
    variants_channel_listing = models.ProductVariantChannelListing.objects.filter(
        variant__in=variants
    )
    variants_channel_listing.update(price_amount=None)

    # when
    availability = get_product_availability(
        product_channel_listing=product_channel_listing,
        variants_channel_listing=variants_channel_listing,
        tax_rate=tax_rate,
        tax_calculation_strategy=tc.tax_calculation_strategy,
        prices_entered_with_tax=tc.prices_entered_with_tax,
    )

    # then
    assert availability.price_range is None
    assert availability.price_range_undiscounted is None


def test_availability_with_missing_variant_channel_listings(stock, channel_USD):
    # given
    product = stock.product_variant.product

    product_channel_listing = product.channel_listings.first()
    variants = product.variants.all()
    variants_channel_listing = models.ProductVariantChannelListing.objects.filter(
        variant__in=variants, channel=channel_USD
    )
    [variant1_channel_listing, variant2_channel_listing] = variants_channel_listing
    variant2_channel_listing.delete()

    # when
    availability = get_product_availability(
        product_channel_listing=product_channel_listing,
        variants_channel_listing=variants_channel_listing,
        prices_entered_with_tax=channel_USD.tax_configuration.prices_entered_with_tax,
        tax_calculation_strategy="TAX_APP",
        tax_rate=Decimal(0),
    )

    # then
    price_range = availability.price_range
    assert price_range.start.gross.amount == variant1_channel_listing.price_amount
    assert price_range.stop.gross.amount == variant1_channel_listing.price_amount


def test_availability_without_variant_channel_listings(stock, channel_USD):
    # given
    product = stock.product_variant.product
    product_channel_listing = product.channel_listings.first()
    variants = product.variants.all()
    models.ProductVariantChannelListing.objects.filter(
        variant__in=variants, channel=channel_USD
    ).delete()

    # when
    availability = get_product_availability(
        product_channel_listing=product_channel_listing,
        variants_channel_listing=[],
        tax_rate=Decimal(0),
        tax_calculation_strategy="TAX_APP",
        prices_entered_with_tax=True,
    )

    # then
    price_range = availability.price_range
    assert price_range is None


def test_available_products_only_published(product_list, channel_USD):
    channel_listing = product_list[0].channel_listings.get()
    channel_listing.is_published = False
    channel_listing.save(update_fields=["is_published"])

    available_products = models.Product.objects.published(channel_USD.slug)
    assert available_products.count() == 2
    assert all(
        [
            product.channel_listings.get(channel__slug=channel_USD.slug).is_published
            for product in available_products
        ]
    )


def test_available_products_only_available(product_list, channel_USD):
    channel_listing = product_list[0].channel_listings.get()
    date_tomorrow = timezone.now() + datetime.timedelta(days=1)
    channel_listing.published_at = date_tomorrow
    channel_listing.save(update_fields=["published_at"])

    available_products = models.Product.objects.published(channel_USD.slug)
    assert available_products.count() == 2
    assert all(
        [
            product.channel_listings.get(channel__slug=channel_USD.slug).is_published
            for product in available_products
        ]
    )


def test_available_products_available_from_yesterday(product_list, channel_USD):
    channel_listing = product_list[0].channel_listings.get()
    date_tomorrow = timezone.now() - datetime.timedelta(days=1)
    channel_listing.published_at = date_tomorrow
    channel_listing.save(update_fields=["published_at"])

    available_products = models.Product.objects.published(channel_USD.slug)
    assert available_products.count() == 3
    assert all(
        [
            product.channel_listings.get(channel__slug=channel_USD.slug).is_published
            for product in available_products
        ]
    )


def test_available_products_available_without_channel_listings(
    product_list, channel_PLN
):
    available_products = models.Product.objects.published(channel_PLN.slug)
    assert available_products.count() == 0


def test_available_products_available_with_many_channels(
    product_list_with_many_channels, channel_USD, channel_PLN
):
    models.ProductChannelListing.objects.filter(
        product__in=product_list_with_many_channels, channel=channel_PLN
    ).update(is_published=False)

    available_products = models.Product.objects.published(channel_PLN.slug)
    assert available_products.count() == 0
    available_products = models.Product.objects.published(channel_USD.slug)
    assert available_products.count() == 3


@freeze_time("2020-03-18 12:00:00")
def test_product_is_visible_from_today(product):
    product_channel_listing = product.channel_listings.get()
    product_channel_listing.published_at = timezone.now()
    product_channel_listing.save()
    assert product_channel_listing.is_visible


def test_available_products_with_variants(product_list, channel_USD):
    product = product_list[0]
    product.variants.all().delete()

    available_products = models.Product.objects.published_with_variants(
        channel_USD.slug
    )
    assert available_products.count() == 2


def test_available_products_with_variants_in_many_channels_usd(
    product_list_with_variants_many_channel, channel_USD
):
    available_products = models.Product.objects.published_with_variants(
        channel_USD.slug
    )
    assert available_products.count() == 1


def test_available_products_with_variants_in_many_channels_pln(
    product_list_with_variants_many_channel, channel_PLN
):
    available_products = models.Product.objects.published_with_variants(
        channel_PLN.slug
    )
    assert available_products.count() == 2


def test_visible_to_customer_user(customer_user, product_list, channel_USD):
    product = product_list[0]
    product.variants.all().delete()

    available_products = models.Product.objects.visible_to_user(
        customer_user, channel_USD.slug
    )
    assert available_products.count() == 2


def test_visible_to_staff_user(
    staff_user, product_list, channel_USD, permission_manage_products
):
    product = product_list[0]
    product.variants.all().delete()

    staff_user.user_permissions.add(permission_manage_products)

    available_products = models.Product.objects.visible_to_user(
        staff_user,
        channel_USD.slug,
    )
    assert available_products.count() == 3


def test_filter_not_published_product_is_unpublished(product, channel_USD):
    channel_listing = product.channel_listings.get()
    channel_listing.is_published = False
    channel_listing.save(update_fields=["is_published"])

    available_products = models.Product.objects.not_published(channel_USD.slug)
    assert available_products.count() == 1


def test_filter_not_published_product_published_tomorrow(product, channel_USD):
    date_tomorrow = timezone.now() + datetime.timedelta(days=1)
    channel_listing = product.channel_listings.get()
    channel_listing.is_published = True
    channel_listing.published_at = date_tomorrow
    channel_listing.save(update_fields=["is_published", "published_at"])

    available_products = models.Product.objects.not_published(channel_USD.slug)
    assert available_products.count() == 1


def test_filter_not_published_product_not_published_tomorrow(product, channel_USD):
    date_tomorrow = timezone.now() + datetime.timedelta(days=1)
    channel_listing = product.channel_listings.get()
    channel_listing.is_published = False
    channel_listing.published_at = date_tomorrow
    channel_listing.save(update_fields=["is_published", "published_at"])

    available_products = models.Product.objects.not_published(channel_USD.slug)
    assert available_products.count() == 1


def test_filter_not_published_product_is_published(product, channel_USD):
    available_products = models.Product.objects.not_published(channel_USD.slug)
    assert available_products.count() == 0


def test_filter_not_published_product_is_unpublished_other_channel(
    product, channel_USD, channel_PLN
):
    models.ProductChannelListing.objects.create(
        product=product, channel=channel_PLN, is_published=False
    )

    available_products_usd = models.Product.objects.not_published(channel_USD.slug)
    assert available_products_usd.count() == 0

    available_products_pln = models.Product.objects.not_published(channel_PLN.slug)
    assert available_products_pln.count() == 1


def test_filter_not_published_product_without_assigned_channel(
    product, channel_USD, channel_PLN
):
    not_available_products_usd = models.Product.objects.not_published(channel_USD.slug)
    assert not_available_products_usd.count() == 0

    not_available_products_pln = models.Product.objects.not_published(channel_PLN.slug)
    assert not_available_products_pln.count() == 1
