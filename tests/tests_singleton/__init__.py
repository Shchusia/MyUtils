# mypy: ignore-errors

from my_utilities.singleton import SingletonMeta, SingletonABC, SingletonABCMeta


class ExampleSingleton(metaclass=SingletonMeta):
    def __init__(self, value) -> None:
        self.value = value


class ExampleSingleton2(metaclass=SingletonMeta):
    def __init__(self, value) -> None:
        self.value = value


def test_singleton_creates_only_one_instance() -> None:
    a = ExampleSingleton(1)
    b = ExampleSingleton(2)

    assert a is b, "Singleton must return same instance"
    assert a.value == 1, "Second init should not change state of existing instance"


def test_reset_instance_force_allows_recreation() -> None:
    a = ExampleSingleton(1)
    ExampleSingleton.reset_instance_force()

    b = ExampleSingleton(2)

    assert a is not b, "After reset, new instance should be created"
    assert b.value == 2


def test_is_initialized_reflects_state() -> None:
    ExampleSingleton.reset_instance_force()
    assert not ExampleSingleton.is_initialized()

    _ = ExampleSingleton(1)
    assert ExampleSingleton.is_initialized()

    ExampleSingleton.reset_instance_force()
    assert not ExampleSingleton.is_initialized()


def test_multiple_singletons_are_independent() -> None:
    class A(metaclass=SingletonMeta):
        pass

    class B(metaclass=SingletonMeta):
        pass

    a1 = A()
    a2 = A()
    b1 = B()
    b2 = B()

    assert a1 is a2
    assert b1 is b2
    assert a1 is not b1


def test_singletonabc_works_as_singleton() -> None:
    class MySingleton(SingletonABC):
        def __init__(self):
            self.data = 123

    x1 = MySingleton()
    x2 = MySingleton()
    assert x1 is x2
    assert isinstance(MySingleton, SingletonABCMeta)


def test_reset_and_recreate_with_abc_singleton() -> None:
    class MySingleton(SingletonABC):
        def __init__(self):
            self.counter = getattr(self, "counter", 0) + 1

    MySingleton.reset_instance_force()
    a = MySingleton()
    MySingleton.reset_instance_force()
    b = MySingleton()

    assert a is not b
    assert b.counter == 1


def test_singleton_first_call_creates_instance(monkeypatch) -> None:
    ExampleSingleton.reset_instance_force()

    created = []
    original_call = SingletonMeta.__call__

    def wrapped_call(cls, *args, **kwargs):
        created.append(True)
        return original_call(cls, *args, **kwargs)

    monkeypatch.setattr(SingletonMeta, "__call__", wrapped_call)
    instance = ExampleSingleton(1)
    assert created, "Должен быть вызов создания нового объекта"
    ExampleSingleton.reset_instance_force()
    monkeypatch.setattr(SingletonMeta, "__call__", original_call)


def test_reset_instance_force_does_nothing_if_not_initialized() -> None:
    v1 = ExampleSingleton(5)
    v2 = ExampleSingleton(6)
    v3 = ExampleSingleton2(3)
    v4 = ExampleSingleton2(6)
    assert id(v1) == id(v2)
    assert id(v3) == id(v4)
    SingletonMeta.reset_instance_force(ExampleSingleton)
    assert not SingletonMeta.is_initialized(ExampleSingleton)

    _ = SingletonMeta.__call__(ExampleSingleton, 1)
    assert SingletonMeta.is_initialized(ExampleSingleton)
    ExampleSingleton.reset_instance_force()
    ExampleSingleton.reset_instance_force()
    assert not ExampleSingleton.is_initialized()
    SingletonMeta.reset_instance_force(ExampleSingleton)
    assert not SingletonMeta.is_initialized(ExampleSingleton)

    instance = SingletonMeta.__call__(ExampleSingleton, 42)
    assert isinstance(instance, ExampleSingleton)
    assert SingletonMeta.is_initialized(ExampleSingleton)


def test_is_initialized_true_and_false() -> None:
    ExampleSingleton.reset_instance_force()
    assert not ExampleSingleton.is_initialized()
    _ = ExampleSingleton(123)
    assert ExampleSingleton.is_initialized()
    ExampleSingleton.reset_instance_force()
    assert not ExampleSingleton.is_initialized()


def test_abc_singleton_meta_behavior() -> None:
    class MySingleton(SingletonABC):
        def __init__(self) -> None:
            self.val = 42

    MySingleton.reset_instance_force()
    a = MySingleton()
    b = MySingleton()
    assert a is b
    assert isinstance(MySingleton, SingletonABCMeta)
    assert MySingleton.is_initialized()
    MySingleton.reset_instance_force()
    assert not MySingleton.is_initialized()
