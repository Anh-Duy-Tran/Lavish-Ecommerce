import jwt
import pytest
from freezegun import freeze_time
from jwt import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError

from ...permission.enums import get_permissions_from_names
from ...permission.models import Permission
from ..auth_backend import JSONWebTokenBackend
from ..jwt import (
    JWT_ACCESS_TYPE,
    create_access_token,
    create_access_token_for_app,
    create_refresh_token,
    jwt_encode,
    jwt_user_payload,
)


@pytest.mark.parametrize("token_type", ["Basic", "Bearer"])
def test_use_authorization_bearer_header_when_authorization_is_provided(
    token_type, rf, staff_user, customer_user
):
    staff_access_token = create_access_token(staff_user)
    request = rf.request(
        HTTP_AUTHORIZATION_BEARER=f"{staff_access_token}",
        HTTP_AUTHORIZATION=f"{token_type} ABC1234",
    )
    backend = JSONWebTokenBackend()
    user = backend.authenticate(request)
    assert user == staff_user


def test_use_saleor_header_as_a_first_try(rf, staff_user, customer_user):
    staff_access_token = create_access_token(staff_user)
    customer_access_token = create_access_token(customer_user)

    request = rf.request(
        HTTP_AUTHORIZATION_BEARER=f"{staff_access_token}",
        HTTP_AUTHORIZATION=f"JWT {customer_access_token}",
    )
    backend = JSONWebTokenBackend()
    user = backend.authenticate(request)
    assert user == staff_user


def test_user_authenticated(rf, staff_user):
    access_token = create_access_token(staff_user)
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{access_token}")
    backend = JSONWebTokenBackend()
    user = backend.authenticate(request)
    assert user == staff_user


def test_user_deactivated(rf, staff_user):
    staff_user.is_active = False
    staff_user.save()
    access_token = create_access_token(staff_user)
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{access_token}")
    backend = JSONWebTokenBackend()
    with pytest.raises(InvalidTokenError):
        backend.authenticate(request)


def test_incorect_type_of_token(rf, staff_user):
    token = create_refresh_token(staff_user)
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{token}")
    backend = JSONWebTokenBackend()
    with pytest.raises(InvalidTokenError):
        backend.authenticate(request)


def test_saleor_is_not_owner_of_token(rf, staff_user, settings):
    payload = jwt_user_payload(
        staff_user,
        JWT_ACCESS_TYPE,
        settings.JWT_TTL_ACCESS,
        token_owner="mirumee.custom.auth.plugin",
    )
    token = jwt_encode(payload)
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{token}")
    backend = JSONWebTokenBackend()

    assert backend.authenticate(request) is None


def test_incorrect_token(rf, staff_user, settings):
    payload = jwt_user_payload(
        staff_user,
        JWT_ACCESS_TYPE,
        settings.JWT_TTL_ACCESS,
    )
    token = jwt.encode(
        payload,
        "Wrong secret",
        "HS256",
    )
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{token}")
    backend = JSONWebTokenBackend()
    with pytest.raises(InvalidSignatureError):
        backend.authenticate(request)


def test_missing_token(rf, staff_user):
    request = rf.request(HTTP_AUTHORIZATION_BEARER="")
    backend = JSONWebTokenBackend()
    assert backend.authenticate(request) is None


def test_missing_header(rf, staff_user):
    request = rf.request()
    backend = JSONWebTokenBackend()
    assert backend.authenticate(request) is None


def test_token_expired(rf, staff_user):
    with freeze_time("2019-03-18 12:00:00"):
        access_token = create_access_token(staff_user)
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{access_token}")
    backend = JSONWebTokenBackend()
    with pytest.raises(ExpiredSignatureError):
        backend.authenticate(request)


def test_user_doesnt_exist(rf, staff_user):
    access_token = create_access_token(staff_user)
    staff_user.delete()
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{access_token}")
    backend = JSONWebTokenBackend()
    with pytest.raises(InvalidTokenError):
        backend.authenticate(request)


def test_user_deactivated_token(rf, staff_user):
    access_token = create_access_token(staff_user)
    staff_user.jwt_token_key = "New key"
    staff_user.save()
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{access_token}")
    backend = JSONWebTokenBackend()
    with pytest.raises(InvalidTokenError):
        backend.authenticate(request)


def test_user_doesnt_have_permissions_from_token(staff_user, app, rf):
    staff_user.user_permissions.set(
        Permission.objects.filter(codename__in=["manage_checkouts", "manage_orders"])
    )
    app.permissions.set(
        Permission.objects.filter(codename__in=["manage_apps", "manage_checkouts"])
    )
    access_token_for_app = create_access_token_for_app(app, staff_user)

    expected_permissions = Permission.objects.filter(codename__in=["manage_checkouts"])

    # user doesn't have the same permissions as in the token
    staff_user.user_permissions.set(expected_permissions)

    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{access_token_for_app}")
    backend = JSONWebTokenBackend()
    user = backend.authenticate(request)
    assert user == staff_user
    assert set(user.effective_permissions) == set(expected_permissions)


@pytest.mark.parametrize(
    "user_permissions, app_permissions, expected_limited_permissions",
    [
        (
            ["manage_apps", "manage_checkouts"],
            ["manage_checkouts"],
            ["MANAGE_CHECKOUTS"],
        ),
        ([], ["manage_checkouts"], []),
        ([], [], []),
        (["manage_apps"], ["manage_checkouts"], []),
        (["manage_checkouts"], [], []),
        (
            ["manage_orders", "manage_checkouts", "manage_apps"],
            ["manage_checkouts", "manage_apps"],
            ["MANAGE_CHECKOUTS", "MANAGE_APPS"],
        ),
    ],
)
def test_user_with_limited_permissions(
    user_permissions, app_permissions, expected_limited_permissions, rf, staff_user, app
):
    staff_user.user_permissions.set(
        Permission.objects.filter(codename__in=user_permissions)
    )
    app.permissions.set(Permission.objects.filter(codename__in=app_permissions))
    access_token_for_app = create_access_token_for_app(app, staff_user)
    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{access_token_for_app}")
    backend = JSONWebTokenBackend()
    user = backend.authenticate(request)
    assert user == staff_user
    user_permissions = user.effective_permissions
    limited_permissions = get_permissions_from_names(expected_limited_permissions)
    assert set(user_permissions) == set(limited_permissions)


def test_user_payload_doesnt_have_user_token(rf, staff_user, settings):
    access_payload = jwt_user_payload(
        staff_user, JWT_ACCESS_TYPE, settings.JWT_TTL_ACCESS
    )
    del access_payload["token"]
    access_token = jwt_encode(access_payload)

    request = rf.request(HTTP_AUTHORIZATION_BEARER=f"{access_token}")
    backend = JSONWebTokenBackend()
    with pytest.raises(InvalidTokenError):
        backend.authenticate(request)
