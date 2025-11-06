# mypy: ignore-errors

from collections import OrderedDict

import pytest

from my_utilities.types.ttl_dict import TTLDict


def test_init():
    t = TTLDict(default_ttl=5)
    assert isinstance(t, TTLDict)
    assert isinstance(t._dict, OrderedDict)
    assert isinstance(t._timers, dict)


@pytest.mark.parametrize("key, value", [("test_key", "test_value")])
def test_setitem(key, value):
    t = TTLDict(default_ttl=5)
    t[key] = value
    assert value == t._dict[key]


@pytest.mark.parametrize(
    "key, value, new_value", [("test_key", "test_value", "new_test_value")]
)
def test_setitem_update(key, value, new_value):
    t = TTLDict(default_ttl=5)
    t[key] = value
    t[key] = new_value
    assert new_value == t._dict[key]


def test_getitem():
    key, value = "test_key", "test_value"
    t = TTLDict(default_ttl=5)
    t[key] = value
    assert value == t[key]


def test_delitem():
    key, value = "test_key", "test_value"
    t = TTLDict(default_ttl=5)
    t[key] = value
    assert value == t[key]
    del t[key]
    assert key not in t._dict


def test_contains():
    key, value = "test_key", "test_value"
    t = TTLDict(default_ttl=5)
    assert key not in t
    t[key] = value
    assert key in t


def test_items():
    key, value = "test_key", "test_value"
    t = TTLDict(default_ttl=5)
    assert list(t.items()) == []
    t[key] = value
    assert list(t.items()) == [(key, value)]


def test_values():
    key, value = "test_key", "test_value"
    t = TTLDict(default_ttl=5)
    assert list(t.values()) == []
    t[key] = value
    assert list(t.values()) == [value]


def test_keys():
    key, value = "test_key", "test_value"
    t = TTLDict(default_ttl=5)
    assert list(t.keys()) == []
    t[key] = value
    assert list(t.keys()) == [key]


def test_extend_ttl_key_exists():
    key, value = "test_key", "test_value"
    t = TTLDict(default_ttl=5)

    t[key] = value
    t.extend_ttl(key)

    assert key in t._dict


def test_extend_ttl_key_not_exists():
    key = "test_key"
    t = TTLDict(default_ttl=5)
    with pytest.raises(KeyError):
        t.extend_ttl(key)
