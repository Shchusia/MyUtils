# Mixins

> The module contains mixins for add new logic to your classed

+  [TstModeMixin](./tst_mode.py) - Mixin for switching between production and test implementations of methods
    depending on the `IS_TEST_MODE` environment variable.
> envs: <br> 
> `IS_TEST_MODE` - enable test mode to overwrite methods <br>
> `IS_RAISE_TEST_MODE` - raise exceptions in tst_mode if found any problem