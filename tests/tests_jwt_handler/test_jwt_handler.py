# mypy: ignore-errors
import time
from uuid import uuid4

import pytest

from my_utilities.jwt_handler.exc import (
    IncorrectTokenError,
    TTLTokenExpiredError,
    WrongTypeToken,
    UnknownError,
)
from my_utilities.jwt_handler.jwt_handler import JWTAuthHandler, JWTHandlerConfig

USER_ID = "1"
PAYLOAD = {"data": "user", "some_payload_data": "data"}
HEADER = {"some_header_data": "data"}


def test_jwt_handler_correct():
    handler = JWTAuthHandler()
    aat, rrt = handler.get_tokens(
        USER_ID,
    )
    subject_at, header_at, payload_at = handler.verify_token(aat)
    subject_rt, header_rt, payload_rt = handler.verify_token(rrt, is_access_token=False)
    assert handler.get_subject(aat) == USER_ID
    assert header_at is header_rt is None
    assert payload_at is payload_rt is None

    aat, rrt = handler.get_tokens(USER_ID, payload=PAYLOAD, header=HEADER)
    subject_at, header_at, payload_at = handler.verify_token(aat)
    subject_rt, header_rt, payload_rt = handler.verify_token(rrt, is_access_token=False)

    assert handler.get_subject(aat) == USER_ID
    assert header_at == header_rt == HEADER
    assert payload_at == payload_rt == PAYLOAD

    token = handler._encode(
        subject=USER_ID,
        token_type="access_token",
        payload=PAYLOAD,
        header=HEADER,
        expires_in=3600,
    )
    assert token is not None

    access_token, refresh_token = handler.get_tokens(
        user_id=USER_ID, is_add_expired=False
    )
    assert access_token is not None
    assert refresh_token is not None

    with pytest.raises(WrongTypeToken):
        handler.verify_token(refresh_token, is_access_token=True)

    data = {f"keep": "value", "remove1": "v1", "remove2": "v2"}
    result = handler._remove_keys(data, ["keep"], reverse=True)
    assert result == {"keep": "value"}

    result = handler._remove_keys({}, ["key"])
    assert result is None
    JWTAuthHandler.reset_instance_force()


def test_jwt_handler_incorrect(monkeypatch):
    secret = str(uuid4())
    config = JWTHandlerConfig(
        ttl_access_token=1, ttl_refresh_token=5, secret=secret, leeway=1
    )
    JWTAuthHandler.reset_instance_force()
    handler = JWTAuthHandler(config=config)
    aat, rrt = handler.get_tokens(
        USER_ID,
    )
    subject_at, header_at, payload_at = handler.verify_token(aat)
    with pytest.raises(IncorrectTokenError):
        _, _, _ = handler.verify_token(aat + "1")

    time.sleep(3.5)
    assert handler.get_subject(aat) == USER_ID

    with pytest.raises(TTLTokenExpiredError):
        _, _, _ = handler.verify_token(aat)

    subject = handler.get_subject("invalid.token.here")
    assert subject == None

    config2 = JWTHandlerConfig(
        ttl_access_token=1, ttl_refresh_token=5, secret=secret + "1", leeway=1
    )
    JWTAuthHandler.reset_instance_force()
    wrong_handler = JWTAuthHandler(config=config2)
    with pytest.raises(IncorrectTokenError):
        wrong_handler.verify_token(aat)

    def mock_decode(*args, **kwargs):
        raise Exception("Some unexpected error")

    monkeypatch.setattr(handler, "_decode", mock_decode)

    with pytest.raises(UnknownError):
        handler.verify_token("any.token")

    JWTAuthHandler.reset_instance_force()
