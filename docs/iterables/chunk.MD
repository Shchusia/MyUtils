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
### Raise(s)
+ `TypeError` - if incorrect type of `iterable` or `size_chunk` variables
+ `ValueError` - if `size_chunk` variable is not in a valid value
### Return
```text
generator of split iterable object len generator equal cnt variable
```
                    
#### Declared returns: `Generator`