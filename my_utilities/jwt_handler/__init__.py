# from my_utilities.cache import CacheEngine
#
#
# class JWTCacheHandler:
#     key_template_access = "user_{id}_access_tokens"
#     key_template_refresh = "user_{id}_refresh_tokens"
#     _cache: CacheEngine = None
#
#     def __init__(self,
#                  cache: CacheEngine=None,
#                  ) -> None:
#         if cache:
#             if not isinstance(cache, CacheEngine):
#                 raise TypeError(
#                     f"Variable cache should be instance of Cache and not {type(cache)}"
#                 )
#             self._cache = cache
#
#
#
