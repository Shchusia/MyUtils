# Module `split.py`
```text
Module with functions for split iterable objects
```

> Path: `my_utils\iterables\split.py`
## Function  `_validate_type`
```text
Validate the type of variable iterable
```
        
### Argument(s)
+ `iterable`: Union[List[Any], Tuple[Any, ...]] - Iterable type to variable
### Return
```text
if correct type variable `iterable` than return type
```
                    
#### Declared returns: `Optional[Type]`
## Function  `split`
```text
Method for splitting into equal cnt parts generator
```
        
### Argument(s)
+ `iterable`: Union[List[Any], Tuple[Any, ...]] - object to split
+ `cnt`: int - cnt partitions
+ `is_yield`: bool - use yield or not for build generator
### Raise(s)
+ `TypeError` - if incorrect type of `iterable` variable
### Return
```text
generator of split iterable object len generator equal cnt variable
```
                    
#### Declared returns: `Generator`
## Function  `split_as_iterable`
```text
Method for splitting into equal parts
```
        
### Argument(s)
+ `iterable`: Union[List[Any], Tuple[Any, ...]] - object to split
+ `cnt`: int - cnt partitions
+ `is_yield`: bool - use yield or not for build generator
### Raise(s)
+ `TypeError` - if incorrect type of `iterable` variable
### Return
```text
iterable object with partitions
```
                    
#### Declared returns: `Union[List[List[Any]], Tuple[Tuple[Any]]]`