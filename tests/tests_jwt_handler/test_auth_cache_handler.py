# mypy: ignore-errors
import time
from enum import verify
from pprint import pprint
from typing import Any, List, Optional
from uuid import uuid4

import pytest

from my_utilities.cache import CacheEngine
from my_utilities.jwt_handler.auth_cache_handler import AuthCacheHandler
from my_utilities.jwt_handler.exc import (
    WrongTypeToken,
    TTLTokenExpiredError,
    NotValidSession,
)
from my_utilities.jwt_handler.jwt_handler import JWTHandlerConfig, JWTAuthHandler


class DictCache(CacheEngine):
    _memory: dict[str, Any]
    _memory_ttl: dict[str, float]

    def __init__(self):
        self._memory: dict[str, Any] = {}
        self._memory_ttl: dict[str, float] = {}

    def _is_expired(self, key: str) -> bool:
        exp_time = self._memory_ttl.get(key, 0)
        return exp_time != 0 and exp_time < time.time()

    def _cleanup_expired(self):
        expired = [k for k in self._memory_ttl if self._is_expired(k)]
        for k in expired:
            self.delete(k)

    def set(self, key: Any, value: Any, ttl: Optional[int] = None, **kwargs) -> bool:
        self._memory[key] = value
        if ttl is not None:
            self._memory_ttl[key] = time.time() + ttl
        else:
            self._memory_ttl[key] = 0
        return True

    def get(self, key: Any, **kwargs) -> Optional[Any]:
        if key not in self._memory:
            return None
        if self._is_expired(key):
            print("expixred")
            self.delete(key)
            return None
        return self._memory[key]

    def delete(self, key: Any, **kwargs) -> bool:
        existed = key in self._memory
        self._memory.pop(key, None)
        self._memory_ttl.pop(key, None)
        return existed

    def reset_cache(self, **kwargs) -> bool:
        self._memory.clear()
        self._memory_ttl.clear()
        return True

    def _connect(self):
        pass

    def _disconnect(self):
        pass

    def update_ttl(self, key: Any, ttl: int, **kwargs):
        if key not in self._memory:
            return False
        self._memory_ttl[key] = time.time() + ttl
        return True

    def keys(self) -> List[str]:
        self._cleanup_expired()
        return list(self._memory.keys())

    def lpush(self, key: str, value: Any) -> int:
        data = self._memory.get(key)
        if data is None:
            self._memory[key] = [value]
        elif isinstance(data, list):
            self._memory[key].insert(0, value)
        else:
            raise ValueError(f"Key '{key}' is not a list")
        return len(self._memory[key])

    def lpos(self, key: str, value: Any) -> int:
        data = self._memory.get(key)
        if isinstance(data, list):
            try:
                return data.index(value)
            except ValueError:
                return -1
        elif data is None:
            return -1
        else:
            raise ValueError(f"Key '{key}' is not a list")

    def lrange(self, key: str, start: int = 0, end: int = -1) -> List[Any]:
        data = self._memory.get(key)
        if not isinstance(data, list):
            if data is None:
                return []
            raise ValueError(f"Key '{key}' is not a list")

        if end == -1:
            end = len(data)
        return data[start:end]

    def lrem(self, key: str, val: Any, count: int = 0) -> int:
        data = self._memory.get(key)
        if not isinstance(data, list):
            if data is None:
                return 0
            raise ValueError(f"Key '{key}' is not a list")

        original_len = len(data)
        if count == 0:
            data = [x for x in data if x != val]
        elif count > 0:
            removed = 0
            new_data = []
            for x in data:
                if x == val and removed < count:
                    removed += 1
                    continue
                new_data.append(x)
            data = new_data
        else:  # count < 0
            removed = 0
            new_data = []
            for x in reversed(data):
                if x == val and removed < abs(count):
                    removed += 1
                    continue
                new_data.append(x)
            data = list(reversed(new_data))
        if data:
            self._memory[key] = data
        else:
            del self._memory[key]
        return original_len - len(data)

    def print(self):
        pprint(self._memory)
        print("ttl")
        pprint(self._memory_ttl)


USER_ID = "1"
PAYLOAD = {"data": "user", "some_payload_data": "data"}
HEADER = {"some_header_data": "data"}


def test_dict_cache():
    cache = DictCache()

    assert cache.set("a", 123)
    assert cache.get("a") == 123
    cache.delete("a")
    assert cache.get("a") is None

    assert cache.set("a", 123, ttl=1)
    assert cache.get("a") == 123
    time.sleep(1.1)
    assert cache.get("a") is None

    cache.set("x", 42)
    assert cache.delete("x") is True
    assert cache.delete("x") is False

    cache.set("a", 1)
    cache.set("b", 2)
    cache.reset_cache()
    assert cache.keys() == []

    cache.set("foo", "bar")
    assert cache.update_ttl("foo", 1)
    assert not cache.update_ttl("nope", 1)
    time.sleep(1.1)
    assert cache.get("foo") is None

    cache.set("a", 1, ttl=1)
    cache.set("b", 2)
    time.sleep(1.1)
    keys = cache.keys()
    assert "b" in keys
    assert "a" not in keys

    cache.lpush("list", 1)
    cache.lpush("list", 2)
    assert cache.get("list") == [2, 1]
    assert cache.lpush("list", 3) == 3

    cache.set("notlist", 123)
    with pytest.raises(ValueError):
        cache.lpush("notlist", 1)

    cache.set("lst", [1, 2, 3])
    assert cache.lpos("lst", 2) == 1
    assert cache.lpos("lst", 99) == -1
    assert cache.lpos("missing", 1) == -1
    cache.set("wrong", "str")
    with pytest.raises(ValueError):
        cache.lpos("wrong", 1)

    cache.set("nums", [1, 2, 3, 4])
    assert cache.lrange("nums", 1, 3) == [2, 3]
    assert cache.lrange("nums", 0, -1) == [1, 2, 3, 4]
    assert cache.lrange("missing") == []
    cache.set("wrong", "string")
    with pytest.raises(ValueError):
        cache.lrange("wrong")

    cache.reset_cache()

    cache.set("nums", [1, 2, 3, 4])
    assert cache.lrange("nums", 1, 3) == [2, 3]
    assert cache.lrange("nums", 0, -1) == [1, 2, 3, 4]
    assert cache.lrange("missing") == []
    cache.set("wrong", "string")
    with pytest.raises(ValueError):
        cache.lrange("wrong")
    cache.reset_cache()

    cache.set("wrong", "text")
    with pytest.raises(ValueError):
        cache.lrem("wrong", "text")
    assert cache.lrem("missing", "x") == 0

    cache.set("x", "y", ttl=1)
    assert not cache._is_expired("x")
    time.sleep(1.1)
    assert cache._is_expired("x")
    cache._cleanup_expired()
    assert "x" not in cache.keys()


def test_auth_cache_handler_multy_session() -> None:
    JWTAuthHandler.reset_instance_force()

    secret = str(uuid4())
    config = JWTHandlerConfig(
        ttl_access_token=1, ttl_refresh_token=5, secret=secret, leeway=0
    )
    cache = DictCache()
    ach = AuthCacheHandler(config=config, cache=cache, is_multy_session=True)
    at, rt = ach.get_pair_tokens(
        user_id=USER_ID, payload=PAYLOAD, headers=HEADER, is_add_expired=True
    )
    _, _ = ach.get_pair_tokens(
        user_id=USER_ID, payload=PAYLOAD, headers=HEADER, is_add_expired=True
    )
    # cache.print()
    sub_at, head_at, pl_at = ach.verify_token(at, is_access_token=True)
    sub_rt, head_rt, pl_rt = ach.verify_token(rt, is_access_token=False)
    assert sub_at == USER_ID == sub_rt
    assert pl_at == PAYLOAD == pl_rt
    assert head_at == HEADER == head_rt

    with pytest.raises(WrongTypeToken):
        ach.verify_token(rt, is_access_token=True)

    time.sleep(2)
    with pytest.raises(TTLTokenExpiredError):
        ach.verify_token(at, is_access_token=True)

    new_at, new_rt = ach.refresh_pair_tokens(rt)
    ach.verify_token(new_at)
    with pytest.raises(NotValidSession):
        ach.verify_token(rt, is_access_token=False)
    with pytest.raises(NotValidSession):
        ach.clear_other_sessions(rt, is_access_token=False)

    ach.clear_other_sessions(new_at)

    ach.delete_pair_tokens(new_at)
    with pytest.raises(NotValidSession):
        ach.clear_other_sessions(new_at, is_access_token=True)


def test_auth_cache_handler_without_multy_session() -> None:
    JWTAuthHandler.reset_instance_force()

    secret = str(uuid4())
    config = JWTHandlerConfig(
        ttl_access_token=1, ttl_refresh_token=5, secret=secret, leeway=0
    )
    cache = DictCache()

    ach = AuthCacheHandler(config=config, cache=cache, is_multy_session=False)
    at, rt = ach.get_pair_tokens(
        user_id=USER_ID, payload=PAYLOAD, headers=HEADER, is_add_expired=True
    )
    at2, rt2 = ach.get_pair_tokens(
        user_id=USER_ID, payload=PAYLOAD, headers=HEADER, is_add_expired=True
    )
    with pytest.raises(NotValidSession):
        ach.verify_token(rt, is_access_token=False)
    ach.verify_token(rt2, is_access_token=False)
    with pytest.raises(NotValidSession):
        ach.refresh_pair_tokens(rt)

    new_at, new_rt = ach.refresh_pair_tokens(rt2)
    with pytest.raises(NotValidSession):
        ach.verify_token(rt2, is_access_token=False)
    ach.verify_token(new_at, is_access_token=True)
    ach.verify_token(new_rt, is_access_token=False)

    time.sleep(2)
    with pytest.raises(TTLTokenExpiredError):
        ach.verify_token(new_at)


def test_auth_cache_without_cache() -> None:
    JWTAuthHandler.reset_instance_force()
    secret = str(uuid4())

    config = JWTHandlerConfig(
        ttl_access_token=1, ttl_refresh_token=5, secret=secret, leeway=0
    )
    ach = AuthCacheHandler(config=config, is_multy_session=False)
    at, rt = ach.get_pair_tokens(
        user_id=USER_ID, payload=PAYLOAD, headers=HEADER, is_add_expired=True
    )

    ach.verify_token(rt, is_access_token=False)
    new_at, new_rt = ach.refresh_pair_tokens(rt)
    ach.verify_token(rt, is_access_token=False)
    ach.verify_token(new_rt, is_access_token=False)
    new_payload = dict()  # type: dict[Any,Any]
    new_header = dict()  # type: dict[Any,Any]
    new_at2, new_rt2 = ach.update_user_data(
        new_at, is_access_token=True, new_payload=new_payload, new_header=new_header
    )
    _, rec_header1, rec_payload1 = ach.verify_token(new_at2, is_access_token=True)
    _, rec_header2, rec_payload2 = ach.verify_token(new_rt2, is_access_token=False)
    assert (rec_header1 == rec_header2) != HEADER
    assert (rec_payload1 == rec_payload2) != PAYLOAD

    time.sleep(2)
    with pytest.raises(TTLTokenExpiredError):
        ach.verify_token(at, is_access_token=True)
    with pytest.raises(TTLTokenExpiredError):
        ach.verify_token(new_at, is_access_token=True)
    new_payload = dict()  # type: dict[Any,Any]
    new_header = dict()  # type: dict[Any,Any]
    new_at2, new_rt2 = ach.update_user_data(
        new_rt, is_access_token=False, new_payload=new_payload, new_header=new_header
    )
    _, rec_header1, rec_payload1 = ach.verify_token(new_at2, is_access_token=True)
    _, rec_header2, rec_payload2 = ach.verify_token(new_rt2, is_access_token=False)
    assert (rec_header1 == rec_header2) != HEADER
    assert (rec_payload1 == rec_payload2) != PAYLOAD

    ach.delete_pair_tokens(new_rt2, is_access_token=False)
    ach.delete_pair_tokens(new_at2, is_access_token=True)
    ach.clear_other_sessions(new_rt2, is_access_token=False)
    ach.clear_other_sessions(new_at2, is_access_token=True)
