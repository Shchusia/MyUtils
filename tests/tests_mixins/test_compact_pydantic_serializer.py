from __future__ import annotations
from my_utilities.mixins.compact_pydantic_serializer import SerializableMixin
from typing import Any, Union, Optional, Dict, List, Tuple, Set
from enum import StrEnum


class Cities(StrEnum):
    LONDON = 'london'
    NEW_YORK = 'new york'


class Gender(StrEnum):
    MALE = 'male'
    FEMALE = 'female'


class PetsType(StrEnum):
    cat = 'cat'
    dog = 'dog'


class Status(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Address(SerializableMixin):
    city: Cities
    zip_code: int
    metadata: Dict[str, Any] = {}


class Pet(SerializableMixin):
    pet_type: PetsType
    name: str
    tags: Set[str] = set()


class V1(SerializableMixin):
    v1: int


class V2(SerializableMixin):
    v2: str


class ComplexModel(SerializableMixin):
    status: Status
    data: Dict[str, Any]


class User(SerializableMixin):
    name: str
    age: int
    address: Address
    gender: Gender
    is_married: bool = False
    child: Optional['User'] = None
    pets: List[Pet] = []
    other_data: Tuple[Pet, ...]
    other_data2: Tuple[V1, V2]
    scores: Dict[str, int] = {}
    tags: Set[str] = set()
    metadata: Dict[str, Any] = {}
    union_field: Union[int, str] = 0
    optional_field: Optional[str] = None
    nested_list: List[List[int]] = []
    mixed_data: Any = None


class ModelWithIntDict(SerializableMixin):
    int_dict: Dict[int, str] = {}
    any_dict: Dict[Any, Any] = {}


class ModelWithComplexUnion(SerializableMixin):
    complex_union: Union[List[str], Dict[str, int], None] = None
    simple_union: Union[int, str] = 0


def test_arbitrary_dict_with_non_string_keys():
    model = ModelWithIntDict(
        int_dict={1: "one", 2: "two"},
        any_dict={"key": "value", 42: "answer"}
    )

    compact = model.to_compact_dict()
    restored = ModelWithIntDict.from_compact_dict(compact)

    assert model == restored
    assert restored.int_dict == {1: "one", 2: "two"}
    assert restored.any_dict == {"key": "value", 42: "answer"}


def test_complex_tuple_with_different_types():
    user = User(
        name="TupleTest",
        age=25,
        address=Address(city=Cities.LONDON, zip_code=1000),
        gender=Gender.MALE,
        other_data=(
            Pet(pet_type=PetsType.cat, name="Cat1"),
            Pet(pet_type=PetsType.dog, name="Dog1"),
            Pet(pet_type=PetsType.cat, name="Cat2")
        ),
        other_data2=(V1(v1=1), V2(v2="test")),
        nested_list=[[1, 2], [3, 4]]
    )

    compact = user.to_compact_dict()
    restored = User.from_compact_dict(compact)

    assert user == restored
    assert len(restored.other_data) == 3
    assert restored.other_data[0].name == "Cat1"
    assert restored.other_data[1].name == "Dog1"


def test_serialize_value_with_direct_base_model():
    pet = Pet(pet_type=PetsType.cat, name="DirectTest", tags={"test"})

    serialized = Pet._serialize_value(pet, Pet)
    assert isinstance(serialized, dict)

    restored_pet = Pet.from_compact_dict(serialized)
    assert pet == restored_pet


def test_arbitrary_dict_nested_structures():
    complex_metadata = {
        "level1": {
            "level2": {
                "level3": [1, 2, 3],
                "nested_set": {1, 2, 3},
                "nested_tuple": (1, "two", 3.0)
            }
        },
        "simple": "value"
    }

    address = Address(
        city=Cities.NEW_YORK,
        zip_code=10001,
        metadata=complex_metadata
    )

    compact = address.to_compact_dict()
    restored = Address.from_compact_dict(compact)

    assert address == restored
    assert address.metadata == restored.metadata


def test_enum_deserialization_with_invalid_value():
    invalid_enum_data = {
        0: "invalid_city",
        1: 10001
    }

    try:
        restored = Address.from_compact_dict(invalid_enum_data)
        assert restored.city == "invalid_city"
    except Exception:
        pass


def test_empty_collections_and_none():
    user = User(
        name="EmptyCollections",
        age=0,
        address=Address(city=Cities.LONDON, zip_code=0, metadata={}),
        gender=Gender.MALE,
        other_data=(),
        other_data2=(V1(v1=0), V2(v2="")),
        pets=[],
        scores={},
        tags=set(),
        metadata={},
        optional_field=None,
        nested_list=[],
        mixed_data=None,
        union_field=0
    )

    compact = user.to_compact_dict()
    restored = User.from_compact_dict(compact)

    assert user == restored
    assert restored.pets == []
    assert restored.scores == {}
    assert restored.tags == set()
    assert restored.optional_field is None


def test_complex_union_types():
    model = ModelWithComplexUnion(
        complex_union=["one", "two", "three"],
        simple_union="string_value"
    )

    compact = model.to_compact_dict()
    restored = ModelWithComplexUnion.from_compact_dict(compact)

    assert model == restored
    assert restored.complex_union == ["one", "two", "three"]

    model2 = ModelWithComplexUnion(
        complex_union={"key1": 1, "key2": 2},
        simple_union=42
    )

    compact2 = model2.to_compact_dict()
    restored2 = ModelWithComplexUnion.from_compact_dict(compact2)

    assert model2 == restored2
    assert restored2.complex_union == {"key1": 1, "key2": 2}


def test_set_serialization_deserialization():
    pet = Pet(
        pet_type=PetsType.dog,
        name="SetTest",
        tags={"large", "friendly", "active"}
    )

    compact = pet.to_compact_dict()
    restored = Pet.from_compact_dict(compact)

    assert pet == restored
    assert restored.tags == {"large", "friendly", "active"}


def test_primitive_types_directly():
    result = User._deserialize_value("test_string", str)
    assert result == "test_string"

    result = User._deserialize_value(42, int)
    assert result == 42

    result = User._deserialize_value(3.14, float)
    assert result == 3.14

    result = User._deserialize_value(True, bool)
    assert result == True

    result = User._deserialize_value(None, type(None))
    assert result is None


def test_edge_case_field_types():
    class EdgeCaseModel(SerializableMixin):
        dict_with_any: Dict[Any, Any] = {}
        optional_list: Optional[List[str]] = None
        union_complex: Union[Dict[str, int], List[str], None] = None
        bare_any: Any = None

    model1 = EdgeCaseModel(
        dict_with_any={1: "one", "two": 2, 3.0: [1, 2, 3]},
        bare_any={"complex": "structure"}
    )

    compact1 = model1.to_compact_dict()
    restored1 = EdgeCaseModel.from_compact_dict(compact1)
    assert model1 == restored1

    model2 = EdgeCaseModel(
        optional_list=None,
        union_complex=["a", "b", "c"]
    )

    compact2 = model2.to_compact_dict()
    restored2 = EdgeCaseModel.from_compact_dict(compact2)
    assert model2 == restored2

    model3 = EdgeCaseModel(
        union_complex={"x": 1, "y": 2},
        bare_any=(1, 2, 3)
    )

    compact3 = model3.to_compact_dict()
    restored3 = EdgeCaseModel.from_compact_dict(compact3)
    assert model3 == restored3


def test_direct_method_calls():
    arbitrary_dict = {
        "key1": "value1",
        "key2": [1, 2, 3],
        "key3": {"nested": "value"}
    }
    result = User._serialize_arbitrary_dict(arbitrary_dict)
    assert isinstance(result, dict)

    compact_arbitrary = {
        0: "value1",
        1: [1, 2, 3],
        2: {0: "value"}
    }
    result = User._deserialize_arbitrary_dict(compact_arbitrary)
    assert isinstance(result, dict)

    assert User._serialize_value(None) is None
    assert User._serialize_value([1, 2, 3]) == [1, 2, 3]
    assert User._serialize_value((1, 2, 3)) == (1, 2, 3)
    assert User._serialize_value({1, 2, 3}) == {1, 2, 3}


def test_tuple_with_less_args_than_elements():
    class TupleTestModel(SerializableMixin):
        short_tuple: Tuple[str, int]
        values: Any

    model = TupleTestModel(
        short_tuple=("hello", 42),
        values="test"
    )

    compact = model.to_compact_dict()
    restored = TupleTestModel.from_compact_dict(compact)

    assert model == restored
    assert restored.short_tuple == ("hello", 42)
    assert restored.values == "test"


def test_deserialize_arbitrary_dict_complex():
    complex_data = {
        "nested_list": [1, 2, 3],
        "nested_dict": {"a": 1, "b": 2},
        "nested_tuple": (4, 5, 6),
        "nested_set": {7, 8, 9}
    }

    user = User(
        name="ArbitraryTest",
        age=30,
        address=Address(city=Cities.LONDON, zip_code=1000),
        gender=Gender.FEMALE,
        other_data=(Pet(pet_type=PetsType.cat, name="Test"),),
        other_data2=(V1(v1=1), V2(v2="test")),
        mixed_data=complex_data
    )

    compact = user.to_compact_dict()
    restored = User.from_compact_dict(compact)

    assert restored.mixed_data["nested_list"] == [1, 2, 3]
    assert restored.mixed_data["nested_dict"] == {"a": 1, "b": 2}
    assert restored.mixed_data["nested_tuple"] == (4, 5, 6)
    assert restored.mixed_data["nested_set"] == {7, 8, 9}


def test_mixed_data_structures():
    complex_mixed_data = {
        "string_key": "value",
        "list_data": [1, "two", 3.0, {"nested": "dict"}],
        "tuple_data": (1, 2, 3),
        "set_data": {1, 2, 3},
        "none_value": None,
        "bool_value": True
    }

    user = User(
        name="MixedTest",
        age=35,
        address=Address(city=Cities.NEW_YORK, zip_code=10001),
        gender=Gender.FEMALE,
        other_data=(Pet(pet_type=PetsType.cat, name="Mix"),),
        other_data2=(V1(v1=1), V2(v2="test")),
        mixed_data=complex_mixed_data
    )

    compact = user.to_compact_dict()
    restored = User.from_compact_dict(compact)

    assert user.name == restored.name
    assert user.age == restored.age
    assert user.address == restored.address

    assert restored.mixed_data["string_key"] == "value"
    assert restored.mixed_data["list_data"] == [1, "two", 3.0, {"nested": "dict"}]
    assert restored.mixed_data["tuple_data"] == (1, 2, 3)
    assert restored.mixed_data["set_data"] == {1, 2, 3}
    assert restored.mixed_data["none_value"] is None
    assert restored.mixed_data["bool_value"] is True


def test_deserialize_arbitrary_dict_with_numeric_keys():
    numeric_key_data = {
        0: "zero",
        1: "one",
        2: {"nested": "value"}
    }

    user = User(
        name="NumericKeys",
        age=25,
        address=Address(city=Cities.LONDON, zip_code=1000),
        gender=Gender.MALE,
        other_data=(Pet(pet_type=PetsType.dog, name="Rex"),),
        other_data2=(V1(v1=1), V2(v2="test")),
        mixed_data=numeric_key_data
    )

    compact = user.to_compact_dict()
    restored = User.from_compact_dict(compact)

    assert "0" in restored.mixed_data
    assert "1" in restored.mixed_data
    assert "2" in restored.mixed_data
    assert restored.mixed_data["0"] == "zero"
    assert restored.mixed_data["1"] == "one"
    assert restored.mixed_data["2"] == {"nested": "value"}


def test_serialize_value_with_tuple_and_no_field_type():
    test_tuple = (1, "two", 3.0, {"key": "value"})

    result = User._serialize_value(test_tuple)

    assert result == (1, "two", 3.0, {"key": "value"})
    assert isinstance(result, tuple)


def test_serialize_value_with_base_model_no_field_type():
    pet = Pet(pet_type=PetsType.cat, name="TestCat", tags={"fluffy"})

    result = User._serialize_value(pet)

    assert isinstance(result, dict)
    assert all(isinstance(k, int) for k in result.keys())


def test_serialize_arbitrary_dict_with_complex_nested():
    complex_dict = {
        "list_with_dicts": [
            {"key1": "value1"},
            {"key2": "value2", "nested": {"key3": "value3"}}
        ],
        "tuple_with_dicts": (
            {"a": 1},
            {"b": 2}
        ),
        "set_with_data": {1, 2, 3},
        "mixed": {
            "inner_list": [{"x": 1}, {"y": 2}],
            "inner_tuple": ({"z": 3},)
        }
    }

    result = User._serialize_arbitrary_dict(complex_dict)

    assert isinstance(result, dict)
    assert "list_with_dicts" in result
    assert isinstance(result["list_with_dicts"], list)
    assert len(result["list_with_dicts"]) == 2
    assert all(isinstance(item, dict) for item in result["list_with_dicts"])


def test_enum_deserialization_error_handling():
    invalid_data = "invalid_enum_value"

    result = User._deserialize_value(invalid_data, Cities)

    assert result == "invalid_enum_value"


def test_union_with_multiple_non_none_types():
    list_value = ["a", "b", "c"]
    result1 = User._deserialize_value(list_value, Union[List[str], Dict[str, int], str])
    assert result1 == ["a", "b", "c"]

    dict_value = {"key1": 1, "key2": 2}
    result2 = User._deserialize_value(dict_value, Union[List[str], Dict[str, int], str])
    assert result2 == {"key1": 1, "key2": 2}

    str_value = "test_string"
    result3 = User._deserialize_value(str_value, Union[List[str], Dict[str, int], str])
    assert result3 == "test_string"


def test_set_deserialization_with_origin_not_set():
    test_set = {1, 2, 3, 4}

    result = User._deserialize_value(test_set, Any)

    assert result == {1, 2, 3, 4}
    assert isinstance(result, set)


def test_tuple_deserialization_with_more_elements_than_args():
    test_tuple = ("element1", "element2", "element3", "element4")

    field_type = Tuple[str, int]

    result = User._deserialize_value(test_tuple, field_type)

    assert result == ("element1", "element2", "element3", "element4")
    assert len(result) == 4


def test_edge_case_union_with_only_none():
    result = User._deserialize_value("test", Union[type(None)])
    assert result == "test"


def test_serialize_value_with_set_and_no_item_type():
    test_set = {1, "two", 3.0}

    result = User._serialize_value(test_set)

    assert result == {1, "two", 3.0}
    assert isinstance(result, set)


def test_direct_enum_serialization():
    city_enum = Cities.LONDON

    result = User._serialize_value(city_enum)

    assert result == "london"


def test_complex_arbitrary_dict_with_different_value_types():
    complex_data = {
        "string": "value",
        "number": 42,
        "list": [1, 2, 3],
        "dict": {"nested": "value"},
        "none": None,
        "bool": True,
        "tuple": (1, 2),
        "set": {1, 2, 3}
    }

    result = User._serialize_arbitrary_dict(complex_data)

    assert result["string"] == "value"
    assert result["number"] == 42
    assert result["list"] == [1, 2, 3]
    assert result["dict"] == {"nested": "value"}
    assert result["none"] is None
    assert result["bool"] is True
    assert result["tuple"] == (1, 2)
    assert result["set"] == {1, 2, 3}


def test_deserialize_value_with_unknown_dict_type():
    test_dict = {0: "value1", 1: "value2"}


    result = User._deserialize_value(test_dict, str)

    assert isinstance(result, dict)
    assert "0" in result
    assert "1" in result


def test_serialize_value_tuple_no_field_type_():
    test_data = (1, "two", {"three": 3})
    result = SerializableMixin._serialize_value(test_data)

    assert result == (1, "two", {"three": 3})
    assert isinstance(result, tuple)
    pet = Pet(pet_type=PetsType.dog, name="Rex")

    result = SerializableMixin._serialize_value(pet, None)

    assert isinstance(result, dict)
    assert all(isinstance(k, int) for k in result.keys())

    complex_data = {
        "nested_dict": {
            "inner_list": [1, 2, 3],
            "inner_tuple": (4, 5, 6),
            "deep_nested": {
                "value": "test"
            }
        },
        "list_with_dicts": [
            {"a": 1},
            {"b": 2}
        ]
    }

    result = SerializableMixin._serialize_arbitrary_dict(complex_data)

    assert isinstance(result, dict)
    assert "nested_dict" in result
    assert isinstance(result["nested_dict"], dict)
    assert "inner_list" in result["nested_dict"]
    assert result["nested_dict"]["inner_list"] == [1, 2, 3]

    invalid_city_value = "invalid_city_name"

    result = SerializableMixin._deserialize_value(invalid_city_value, Cities)

    assert result == "invalid_city_name"

    optional_union = Union[List[str], None]
    result1 = SerializableMixin._deserialize_value(["a", "b"], optional_union)
    assert result1 == ["a", "b"]

    complex_union = Union[Dict[str, int], List[str], int]

    result2 = SerializableMixin._deserialize_value({"key": 1}, complex_union)
    assert result2 == {"key": 1}

    result3 = SerializableMixin._deserialize_value(["x", "y"], complex_union)
    assert result3 == ["x", "y"]

    result4 = SerializableMixin._deserialize_value(42, complex_union)
    assert result4 == 42


def test_deserialize_value_union_only_none():
    only_none_union = Union[type(None), type(None)]
    result = SerializableMixin._deserialize_value("test", only_none_union)
    assert result == "test"


def test_serialize_value_direct_base_model_call():
    address = Address(city=Cities.LONDON, zip_code=1000)

    result = SerializableMixin._serialize_value(address, None)

    assert isinstance(result, dict)
    assert all(isinstance(k, int) for k in result.keys())


def test_serialize_arbitrary_dict_with_all_collection_types():
    test_data = {
        "list": [1, 2, 3],
        "tuple": (4, 5, 6),
        "set": {7, 8, 9},
        "dict": {"nested": "value"},
        "mixed": [
            {"a": 1},
            (2, 3),
            {4, 5}
        ]
    }

    result = SerializableMixin._serialize_arbitrary_dict(test_data)

    assert result["list"] == [1, 2, 3]
    assert result["tuple"] == (4, 5, 6)
    assert result["set"] == {7, 8, 9}
    assert isinstance(result["dict"], dict)
    assert len(result["mixed"]) == 3


def test_enum_deserialization_with_valid_and_invalid():
    valid_result = SerializableMixin._deserialize_value("london", Cities)
    assert valid_result == Cities.LONDON

    invalid_result = SerializableMixin._deserialize_value("invalid", Cities)
    assert invalid_result == "invalid"


def test_union_extraction_logic():
    from typing import get_args, get_origin

    union1 = Union[str, int, None]
    origin1 = get_origin(union1)
    args1 = get_args(union1)

    assert origin1 is Union
    assert str in args1
    assert int in args1
    assert type(None) in args1

    union2 = Union[str, int]
    args2 = get_args(union2)
    non_none_types2 = [t for t in args2 if t is not type(None)]
    assert non_none_types2 == [str, int]
