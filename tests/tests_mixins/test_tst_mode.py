from re import match

import pytest

from my_utilities.mixins.tst_mode import TestModeMixin
import os

prod_value = 1
test_value = 5
not_overwrite_method_value = 9


class A(TestModeMixin):
    dict_tst_mode = {
        "base_method": "tst_base_method",
        'second_base_method': 'test',
        "async_third_method": "tst_async_third_method",
        "fourth_method": 'tst_fourth_method'
    }

    def base_method(self):
        return prod_value

    def tst_base_method(self):
        return test_value

    def second_base_method(self):
        return not_overwrite_method_value





class B(TestModeMixin):
    dict_tst_mode = {
        'test': 'test',
    }

class C(TestModeMixin):
    dict_tst_mode = {
        'fourth_method': 'tst_fourth_method',
    }

    async def tst_fourth_method(self):
        return test_value

    def fourth_method(self):
        return prod_value




def test_tst_mode():
    a = A()
    assert a.base_method() == prod_value
    assert a.second_base_method() == not_overwrite_method_value

    c = C()
    assert c.fourth_method() == prod_value
    os.environ['IS_TEST_MODE'] = '1'
    a = A()
    assert a.base_method() == test_value
    assert a.second_base_method() == not_overwrite_method_value
    c = C()
    assert c.fourth_method() == prod_value
    os.environ['IS_RAISE_TEST_MODE'] = '1'

    with pytest.raises(KeyError,  match='not found base method') :
        B()

    with pytest.raises(KeyError,  match='not found test method'):
        a = A()
        a.second_base_method()

    with pytest.raises(ValueError,  match='Not matched sync / async'):
        C()
