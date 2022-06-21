# Module `converter_size_to_pretty_view.py`
```text
Module with function for convert bytes size to correct size in kb/mb/gb
```

> Path: `my_utils\view\converter_size_to_pretty_view.py`
## Class `SystemTypes`
```text
Enum of available conversion systems
```

### Basses(s)
+ Enum
### SubElement(s)
 > `SI`: str = "si_name"
 > `IEC`: str = "iec_name"
 > `VERBOSE`: str = "verbose_name"
 > `ALTERNATIVE`: str = "alternative_name"
 > `TRADITIONAL`: str = "traditional_name"
## Class `SystemValue`
```text
Class for storing information about different weights
```

### Basses(s)
+ BaseModel
### SubElement(s)
 > `pow`: int = Field(..., description='the power to which you need to raise the bytes for the correct calculation')
 > `traditional_name`: str = Field(..., description='Traditional name for this type')
 > `alternative_name`: Union[str, Tuple[str, str]] = Field(..., description='Alternative name for this type')
 > `verbose_name`: Tuple[str, str] = Field(..., description='Full name without abbreviations')
 > `iec_name`: str = Field(..., description='IEC system name')
 > `si_name`: str = Field(None, description='Si system name')
 > `value_base`: int = Field(None, description='The number of bytes in one unit of this type')
 > `value_si`: int = Field(None, description='The number of bytes in one unit of this type in system si')
 > ## Function  `__init__`
 > ### Argument(s)
 > + **`data` - empty doc string
 > ## Function  `get_size_suffix`
 > ```text
 > method return str title for chose type
 > ```
 > 
 > ### Argument(s)
 > + `system`: Optional[str] - title system for view
 > allowed: [si, iec, verbose, alternative, traditional]
 > ### Return
 > ```text
 > names for chose system
 > ```
 > 
 > #### Declared returns: `Optional[Union[str, Tuple[str, str]]]`
 > ## Function  `get_amount`
 > ```text
 > Method get size of bytes value in system
 > ```
 > 
 > ### Argument(s)
 > + `bytes_value`: int - bytes to convert
 > + `round_to`: Optional[int] - decimal point rounding precision
 > + `is_si`: Optional[bool] - is to 'si' system convert
 > #### Declared returns: `float`
 > ## Function  `get_normalized_size`
 > ```text
 > Method convert bytes value in chose system
 > ```
 > 
 > ### Argument(s)
 > + `bytes_value`: int - bytes value to convert
 > + `system`: Optional[str] - system to which to convert
 > + `round_to`: Optional[int] - empty doc string
 > ### Return
 > ```text
 > converted value
 > ```
 > 
 > #### Declared returns: `str`
 > ## Function  `__lt__`
 > ### Argument(s)
 > + `other` - empty doc string
 > ## Function  `__le__`
 > ### Argument(s)
 > + `other`: Union[Number, SystemValue] - empty doc string
 > ## Function  `__gt__`
 > ### Argument(s)
 > + `other`: Union[Number, SystemValue] - empty doc string
 > ## Function  `__eq__`
 > ### Argument(s)
 > + `other`: Union[Number, SystemValue] - empty doc string
 > ## Function  `__ge__`
 > ### Argument(s)
 > + `other`: Union[Number, SystemValue] - empty doc string
`LIST_SYSTEMS` = [SystemValue(pow=5, traditional_name='P', alternative_name='PB', verbose_name=(' petabyte', ' petabytes'), iec_name='Pi'), SystemValue(pow=4, traditional_name='T', alternative_name='TB', verbose_name=(' terabyte', ' terabytes'), iec_name='Ti'), SystemValue(pow=3, traditional_name='G', alternative_name='GB', verbose_name=(' gigabyte', ' gigabytes'), iec_name='Gi'), SystemValue(pow=2, traditional_name='M', alternative_name='MB', verbose_name=(' megabyte', ' megabytes'), iec_name='Mi'), SystemValue(pow=1, traditional_name='K', alternative_name='KB', verbose_name=(' kilobyte', ' kilobytes'), iec_name='Ki'), SystemValue(pow=0, traditional_name='B', alternative_name=(' byte', ' bytes'), verbose_name=(' byte', ' bytes'), iec_name='')]
## Function  `size`
```text
Method for print size of file from bytes to pretty print
```
        
### Argument(s)
+ `bytes_value`: int - bytes to convert
+ `system`: Optional[str] - empty doc string
+ `round_to`: int - decimal point rounding precision
### Return
```text
converted bytes_value to pretty string
```
                    
#### Declared returns: `str`
### Example 
```python
Using the traditional system, where a factor of 1024 is used::
>>> size(10)
'10B'
>>> size(2000)
'1.95K'
>>> size(20000)
'19.53K'
>>> size(200000)
'0.19M'
>>> size(1000000)
'0.95M'
>>> size(2000000)
'1.91M'
# use si
>>> size(10, system="si")
'10B'
>>> size(2000, system="si")
'2K'
>>> size(20000, system="si")
'20K'
>>> size(200000, system="si")
'0.2M'
>>> size(1000000, system="si")
'1M'
>>> size(2000000, system="si")
'2M'
```
