from collections import OrderedDict
from collections.abc import Callable
from threading import Timer
from typing import Any


class TTLDict:
    """
    TTLDict(default_ttl=300)

    A dictionary-like container with time-to-live (TTL)
     functionality for its keys. The keys in this
     dictionary automatically expire and get removed after
     a specified duration.

    Attributes:
        default_ttl (int): The default time-to-live for keys in seconds.
        _dict (OrderedDict): The main dictionary to store key-value pairs.
        _timers (dict): A dictionary to store Timer objects for each key.
    """

    def __init__(
        self,
        default_ttl: int = 300,
        name: str = None,
        function_on_expired: Callable[[Any], None] | None = None,
    ):
        self._default_ttl = default_ttl
        self._dict = OrderedDict()  # type: ignore
        self._timers = {}  # type: ignore
        self._name = name
        self._on_expired = function_on_expired

    def __setitem__(
        self,
        key: Any,
        value: Any,
    ) -> None:
        # if self._dict.get(key) is None:
        #     DEFAULT_LOGGER.debug("add key %s", key)
        self._dict[key] = value
        self._set_ttl(key, self._default_ttl)

    def _set_ttl(self, key: Any, ttl: int) -> None:
        """
        Args:
            key: The key for which the TTL (Time To Live) is being set.
            ttl: The time in seconds after which the key should expire.

        """
        if key in self._timers:
            self._timers[key].cancel()
        self._timers[key] = Timer(ttl, self._expire, args=[key])
        self._timers[key].start()

    def extend_ttl(self, key: Any) -> None:
        """
        Attempts to extend the time-to-live (TTL) value for the specified key.

        If the key exists in the internal dictionary, it resets its TTL to the default
         TTL value. If the key does not exist, a KeyError is raised.

        Args:
            key: The key for which the TTL is to be extended.

        Raises:
            KeyError: If the key is not found in the internal dictionary.
        """
        if key not in self._dict:
            raise KeyError(f"Key {key} not found")
        self._set_ttl(key, self._default_ttl)

    def __getitem__(self, key: Any) -> Any:
        return self._dict[key]

    def __delitem__(self, key: Any) -> None:
        self._cleanup(key, is_expire_cleanup=False)
        del self._dict[key]
        self._timers[key].cancel()
        del self._timers[key]

    def __contains__(self, key: Any) -> bool:
        return key in self._dict

    def _expire(self, key: Any) -> None:
        """
        Args:
            key: The key of the item to expire from the dictionary.
        """
        self._cleanup(key, is_expire_cleanup=True)
        del self._dict[key]
        del self._timers[key]

    def _cleanup(self, key: Any, is_expire_cleanup: bool = False) -> None:
        """
        Args:
            key: The key used to identify the item to be cleaned up.
        """
        if is_expire_cleanup and self._on_expired is not None:
            self._on_expired(key)

    def items(self) -> Any:
        """
        Returns all items in the dictionary.

        Returns:
            dict_items: A view object that displays a list of a dictionary's
             key-value tuple pairs.
        """
        return self._dict.items()

    def values(self) -> Any:
        """
        Gets the values from the internal dictionary.

        Returns:
            dict_values: An object containing all the values in the dictionary.
        """
        return self._dict.values()

    def keys(self) -> Any:
        """
        Returns the keys of the internal dictionary.

        Returns:
            dict_keys: A view object that displays a list of all the keys.
        """
        return self._dict.keys()

    def __iter__(self) -> Any:
        return self._dict.items()

    def __str__(self) -> str:
        return str(self._dict)

    def get(self, key: Any, default: Any = None) -> Any:
        return self._dict.get(key, default)
