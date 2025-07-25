from testutils import assert_raises

assert len(dict()) == 0

assert len({}) == 0
assert len({"a": "b"}) == 1
assert len({"a": "b", "b": 1}) == 2
assert len({"a": "b", "b": 1, "a" + "b": 2 * 2}) == 3

d = {}
d["a"] = d
assert repr(d) == "{'a': {...}}"

assert {"a": 123}.get("a") == 123
assert {"a": 123}.get("b") == None
assert {"a": 123}.get("b", 456) == 456

d = {"a": 123, "b": 456}
assert list(reversed(d)) == ["b", "a"]
assert list(reversed(d.keys())) == ["b", "a"]
assert list(reversed(d.values())) == [456, 123]
assert list(reversed(d.items())) == [("b", 456), ("a", 123)]
with assert_raises(StopIteration):
    dict_reversed = reversed(d)
    for _ in range(len(d) + 1):
        next(dict_reversed)
assert "dict" in dict().__doc__

d = {"a": 123, "b": 456}
assert 1 not in d.items()
assert "a" not in d.items()
assert "a", 123 not in d.items()
assert () not in d.items()
assert (1) not in d.items()
assert ("a") not in d.items()
assert ("a", 123) in d.items()
assert ("b", 456) in d.items()
assert ("a", 123, 3) not in d.items()
assert ("a", 123, "b", 456) not in d.items()

d = {1: 10, "a": "ABC", (3, 4): 5}
assert 1 in d.keys()
assert (1) in d.keys()
assert "a" in d.keys()
assert (3, 4) in d.keys()
assert () not in d.keys()
assert 10 not in d.keys()
assert (1, 10) not in d.keys()
assert "abc" not in d.keys()
assert ((3, 4), 5) not in d.keys()

d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
assert d1.items().isdisjoint(d2.items())
assert d1.keys().isdisjoint(d2.keys())
d2 = {"b": 3, "d": 4}
assert d1.items().isdisjoint(d2.items())
assert not d1.keys().isdisjoint(d2.keys())
d2 = {"c": 2, "d": 4}
assert d1.items().isdisjoint(d2.items())
assert d1.keys().isdisjoint(d2.keys())
d2 = {"b": 2, "d": 4}
assert not d1.items().isdisjoint(d2.items())
assert not d1.keys().isdisjoint(d2.keys())


assert dict(a=2, b=3) == {"a": 2, "b": 3}
assert dict({"a": 2, "b": 3}, b=4) == {"a": 2, "b": 4}
assert dict([("a", 2), ("b", 3)]) == {"a": 2, "b": 3}

assert {} == {}
assert not {"a": 2} == {}
assert not {} == {"a": 2}
assert not {"b": 2} == {"a": 2}
assert not {"a": 4} == {"a": 2}
assert {"a": 2} == {"a": 2}

nan = float("nan")
assert {"a": nan} == {"a": nan}

a = {"g": 5}
b = {"a": a, "d": 9}
c = dict(b)
c["d"] = 3
c["a"]["g"] = 2
assert a == {"g": 2}
assert b == {"a": a, "d": 9}

a.clear()
assert len(a) == 0

a = {"a": 5, "b": 6}
res = set()
for value in a.values():
    res.add(value)
assert res == set([5, 6])

count = 0
for key, value in a.items():
    assert a[key] == value
    count += 1
assert count == len(a)

res = set()
for key in a.keys():
    res.add(key)
assert res == set(["a", "b"])

# Deleted values are correctly skipped over:
x = {"a": 1, "b": 2, "c": 3, "d": 3}
del x["c"]
it = iter(x.items())
assert ("a", 1) == next(it)
assert ("b", 2) == next(it)
assert ("d", 3) == next(it)
with assert_raises(StopIteration):
    next(it)

with assert_raises(KeyError) as cm:
    del x[10]
assert cm.exception.args[0] == 10

# Iterating a dictionary is just its keys:
assert ["a", "b", "d"] == list(x)

# Iterating view captures dictionary when iterated.
data = {1: 2, 3: 4}
items = data.items()
assert list(items) == [(1, 2), (3, 4)]
data[5] = 6
assert list(items) == [(1, 2), (3, 4), (5, 6)]

# Values can be changed during iteration.
data = {1: 2, 3: 4}
items = iter(data.items())
assert (1, 2) == next(items)
data[3] = "changed"
assert (3, "changed") == next(items)

# But we can't add or delete items during iteration.
d = {}
a = iter(d.items())
d["a"] = 2
b = iter(d.items())
assert ("a", 2) == next(b)
with assert_raises(RuntimeError):
    next(a)
del d["a"]
with assert_raises(RuntimeError):
    next(b)

# View isn't itself an iterator.
with assert_raises(TypeError):
    next(data.keys())

assert len(data.keys()) == 2

x = {}
x[1] = 1
assert x[1] == 1

x[7] = 7
x[2] = 2
x[(5, 6)] = 5

with assert_raises(TypeError):
    x[[]]  # Unhashable type.

x["here"] = "here"
assert x.get("not here", "default") == "default"
assert x.get("here", "default") == "here"
assert x.get("not here") == None


class LengthDict(dict):
    def __getitem__(self, k):
        return len(k)


x = LengthDict()
assert type(x) == LengthDict
assert x["word"] == 4
assert x.get("word") is None

assert 5 == eval("a + word", LengthDict())


class Squares(dict):
    def __missing__(self, k):
        v = k * k
        self[k] = v
        return v


x = Squares()
assert x[-5] == 25


# An object that hashes to the same value always, and compares equal if any its values match.
class Hashable(object):
    def __init__(self, *args):
        self.values = args

    def __hash__(self):
        return 1

    def __eq__(self, other):
        for x in self.values:
            for y in other.values:
                if x == y:
                    return True
        return False


x = {}
x[Hashable(1, 2)] = 8

assert x[Hashable(1, 2)] == 8
assert x[Hashable(3, 1)] == 8

x[Hashable(8)] = 19
x[Hashable(19, 8)] = 1
assert x[Hashable(8)] == 1
assert len(x) == 2

assert list({"a": 2, "b": 10}) == ["a", "b"]
x = {}
x["a"] = 2
x["b"] = 10
assert list(x) == ["a", "b"]

y = x.copy()
x["c"] = 12
assert y == {"a": 2, "b": 10}

y.update({"c": 19, "d": -1, "b": 12})
assert y == {"a": 2, "b": 12, "c": 19, "d": -1}

y.update(y)
assert y == {"a": 2, "b": 12, "c": 19, "d": -1}  # hasn't changed

# KeyError has object that used as key as an .args[0]
with assert_raises(KeyError) as cm:
    x["not here"]
assert cm.exception.args[0] == "not here"
with assert_raises(KeyError) as cm:
    x.pop("not here")
assert cm.exception.args[0] == "not here"

with assert_raises(KeyError) as cm:
    x[10]
assert cm.exception.args[0] == 10
with assert_raises(KeyError) as cm:
    x.pop(10)
assert cm.exception.args[0] == 10


class MyClass:
    pass


obj = MyClass()

with assert_raises(KeyError) as cm:
    x[obj]
assert cm.exception.args[0] == obj
with assert_raises(KeyError) as cm:
    x.pop(obj)
assert cm.exception.args[0] == obj

x = {1: "a", "1": None}
assert x.pop(1) == "a"
assert x.pop("1") is None
assert x == {}

x = {1: "a"}
assert (1, "a") == x.popitem()
assert x == {}
with assert_raises(KeyError) as cm:
    x.popitem()
assert cm.exception.args == ("popitem(): dictionary is empty",)

x = {"a": 4}
assert 4 == x.setdefault("a", 0)
assert x["a"] == 4
assert 0 == x.setdefault("b", 0)
assert x["b"] == 0
assert None == x.setdefault("c")
assert x["c"] is None

assert {1: None, "b": None} == dict.fromkeys([1, "b"])
assert {1: 0, "b": 0} == dict.fromkeys([1, "b"], 0)

x = {"a": 1, "b": 1, "c": 1}
y = {"b": 2, "c": 2, "d": 2}
z = {"c": 3, "d": 3, "e": 3}

w = {1: 1, **x, 2: 2, **y, 3: 3, **z, 4: 4}
assert w == {
    1: 1,
    "a": 1,
    "b": 2,
    "c": 3,
    2: 2,
    "d": 3,
    3: 3,
    "e": 3,
    4: 4,
}  # not in cpython test suite

assert str({True: True, 1.0: 1.0}) == str({True: 1.0})


class A:
    def __hash__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, A)


class B:
    def __hash__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, B)


s = {1: 0, A(): 1, B(): 2}
assert len(s) == 3
assert s[1] == 0
assert s[A()] == 1
assert s[B()] == 2

# Test dict usage in set with star expressions!
a = {"bla": 2}
b = {"c": 44, "bla": 332, "d": 6}
x = ["bla", "c", "d", "f"]
c = {*a, *b, *x}
# print(c, type(c))
assert isinstance(c, set)
assert c == {"bla", "c", "d", "f"}

assert not {}.__ne__({})
assert {}.__ne__({"a": "b"})
assert {}.__ne__(1) == NotImplemented

it = iter({0: 1, 2: 3, 4: 5, 6: 7})
assert it.__length_hint__() == 4
next(it)
assert it.__length_hint__() == 3
next(it)
assert it.__length_hint__() == 2
next(it)
assert it.__length_hint__() == 1
next(it)
assert it.__length_hint__() == 0
assert_raises(StopIteration, next, it)
assert it.__length_hint__() == 0

# Test dictionary unpacking with non-mapping objects
# This should raise TypeError for non-mapping objects
with assert_raises(TypeError) as cm:
    {**[1, 2]}
assert "'list' object is not a mapping" in str(cm.exception)

with assert_raises(TypeError) as cm:
    {**[[1, 2], [3, 4]]}
assert "'list' object is not a mapping" in str(cm.exception)

with assert_raises(TypeError) as cm:
    {**"string"}
assert "'str' object is not a mapping" in str(cm.exception)

with assert_raises(TypeError) as cm:
    {**(1, 2, 3)}
assert "'tuple' object is not a mapping" in str(cm.exception)

# Test that valid mappings still work
assert {**{"a": 1}, **{"b": 2}} == {"a": 1, "b": 2}

# Test OrderedDict unpacking preserves order
import collections

od = collections.OrderedDict([("a", 1), ("b", 2)])
od.move_to_end("a")  # Move 'a' to end: ['b', 'a']
expected_order = list(od.items())  # [('b', 2), ('a', 1)]


def test_func(**kwargs):
    return kwargs


result = test_func(**od)
assert list(result.items()) == expected_order, (
    f"Expected {expected_order}, got {list(result.items())}"
)

# Test multiple OrderedDict unpacking
od1 = collections.OrderedDict([("x", 10), ("y", 20)])
od2 = collections.OrderedDict([("z", 30), ("w", 40)])
od2.move_to_end("z")  # Move 'z' to end: ['w', 'z']

result = test_func(**od1, **od2)
# Should preserve order: x, y, w, z
expected_keys = ["x", "y", "w", "z"]
assert list(result.keys()) == expected_keys, (
    f"Expected {expected_keys}, got {list(result.keys())}"
)
