# mypy: ignore-errors
import time
from collections import OrderedDict

import pytest

from my_utilities.types.ttl_dict import TTLDict

TEST_DICT = dict()


def cleanup_function(item):
    global TEST_DICT
    TEST_DICT[item] = item


def test_init():
    t = TTLDict(default_ttl=5)
    assert isinstance(t, TTLDict)
    assert isinstance(t._dict, OrderedDict)
    assert isinstance(t._timers, dict)


@pytest.mark.parametrize("key, value", [("test_key", "test_value")])
def test_setitem(key, value):
    t = TTLDict(default_ttl=1)
    t[key] = value
    assert value == t._dict[key]
    time.sleep(1.1)
    assert t.get(key, None) is None


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


@pytest.mark.parametrize("key, value", [("test_key", "test_value")])
def test_cleanup_function(key, value):
    global TEST_DICT
    TEST_DICT.clear()

    t = TTLDict(default_ttl=1, function_on_expired=cleanup_function)
    t[key] = value
    assert len(TEST_DICT.keys()) == 0
    assert t.get(key, None) == value
    time.sleep(1.1)
    assert len(TEST_DICT.keys()) == 1
    assert t.get(key, None) is None


@pytest.mark.parametrize("key, value", [("test_key", "test_value")])
def test_other_functions(key, value):
    t = TTLDict(default_ttl=1, function_on_expired=cleanup_function)
    t[key] = value
    for item in t:
        assert item == key
    assert f"{{'{key}': '{value}'}}" == str(t)

    assert len(t) == 1
    t.clear()
    assert len(t) == 0

    t[key] = 1
    t.setdefault(key, 2)
    t.setdefault("key2", 3)
    assert t[key] == 1
    assert t["key2"] == 3
    t.clear()
    t2 = TTLDict()

    t[key] = value
    t2[key] = value
    tmp_dict = {key: value}
    assert t == t2
    assert t == tmp_dict
    with pytest.raises(TypeError):
        _ = t == [1]

    t2["new_key"] = 5
    tmp_dict["new_key1"] = 6
    t.update(t2)
    t.update(tmp_dict)
    with pytest.raises(TypeError):
        t.update([1])
    assert len(t) == 3

    t.clear()
    t2.clear()


@pytest.mark.parametrize("key, value", [("test_key", "test_value")])
def test_pop_function(key, value):
    global TEST_DICT
    TEST_DICT.clear()

    t = TTLDict(default_ttl=1, function_on_expired=cleanup_function)
    t[key] = value
    assert len(TEST_DICT.keys()) == 0
    assert t.get(key, None) == value
    # with pytest.raises(KeyError):
    assert t.pop("key2") is None
    assert t.pop(key) == value
    # time.sleep(1.1)
    assert len(TEST_DICT.keys()) == 0
    # assert t.get(key, None) is None
