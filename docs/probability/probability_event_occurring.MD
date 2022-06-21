# Module `probability_event_occurring.py`
```text
The module contains a function that returns whether an event has occurred
 that has a probability of occurrence
```

> Path: `my_utils\probability\probability_event_occurring.py`
## Function  `is_fate_in_awe`
```text
Method determines whether an event has occurred that
has a certain chance of falling out
```
        
### Argument(s)
+ `drop_chance`: Union[float, int, Decimal] - the probability of an event occurring
value between[0, 1]
### Raise(s)
+ `ValueError` - if the value is not in the allowed range [0, 1]
+ `TypeError` - if incorrect types
### Return
```text
is got this chance
```
                    
#### Declared returns: `bool`