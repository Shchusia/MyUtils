# Module `chunk.py`
```text
Module with functions for generate chunks
```

> Path: `my_utils\iterables\chunk.py`
## Function  `chunks`
```text
Method for splitting into many parts with len size_chunk generator
```
        
### Argument(s)
+ `iterable`: Union[List[Any], Tuple[Any, ...]] - object to split
+ `size_chunk`: int - size_chunk
+ `is_yield`: bool - use yield or not for build generator
### Raise(s)
+ `TypeError` - if incorrect type of `iterable` variable
### Return
```text
generator of split iterable object len generator equal cnt variable
```
                    
#### Declared returns: `Generator`