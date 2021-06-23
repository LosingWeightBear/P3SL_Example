# Chapter 2 -- Data Structures

[toc]


> Python includes several standard programming data structures, such as list, tuple, dict, and set, as part of its built-in types. Many applications do not require other structures, but when they do, the standard library provides powerful and well-tested versions that are ready to be used.

Python 包括几种标准的编程数据结构，例如列表、元组、字典和集合，作为其内置类型的一部分。许多应用程序不需要其他结构，但是当它们需要时，标准库会提供功能强大且经过充分测试的版本，可以随时使用。


> The `enum` (page 66) module provides an implementation of an enumeration type, with
iteration and comparison capabilities. It can be used to create well-defined symbols for
values, instead of using literal strings or integers.






## 2.1 enum: Enumeration Type

> The `enum` module defines an enumeration type with iteration and comparison capabilities. It can be used to create well-defined symbols for values, instead of using literal integers or strings.

`enum` 模块定义了具有迭代和比较功能的枚举类型。它可用于为值创建定义良好的符号，而不是使用文字整数或字符串。


### 2.1.1 Creating Enumerations

> A new enumeration is defined using the `class` syntax by subclassing `Enum` and adding class attributes describing the values.

使用 `class` 语法通过子类化 `Enum` 并添加描述值的类属性来定义一个新的枚举类。


> The members of the `Enum` are converted to instances as the class is parsed. Each instance has a `name` property corresponding to the member name and a `value` property corresponding to the value assigned to the name in the class definition.

在解析类时，`Enum` 的成员被转换为实例。每个实例都有一个与成员名称相对应的`name` 属性和一个与分配给类定义中名称的值相对应的`value` 属性。

```python
# 2_1_enum_create.py
import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

print('\nMember name: {}'.format(BugStatus.wont_fix.name))
print('Member value: {}'.format(BugStatus.wont_fix.value))
```

```text

Member name: wont_fix
Member value: 4
```

### 2.1.2 Iteration

> Iterating over the enum *class* produces the individual members of the enumeration.

迭代枚举类会产生枚举的各个成员。

> The members are produced in the order they are declared in the class definition. The names and values are not used to sort them in any way.

成员按照它们在类定义中声明的顺序生成。名称和值不以任何方式进行排序。

```python
# 2_2_enum_iterate.py
import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))
```

```text
new             = 7
incomplete      = 6
invalid         = 5
wont_fix        = 4
in_progress     = 3
fix_committed   = 2
fix_released    = 1
```


### 2.1.3 Comparing Enums

> Because enumeration members are not ordered, they support only comparison by identity
and equality.

因为枚举成员是无序的，所以它们只支持通过同一性和相等性进行比较。

> The greater-than and less-than comparison operators raise `TypeError` exceptions.

大于和小于比较运算符会引发 `TypeError` 异常。

```python
# 2_3_enum_comparison.py
import enum


class BugStatus(enum.Enum):
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


actual_state = BugStatus.wont_fix
desired_state = BugStatus.fix_released

print('Equality:',
actual_state == desired_state,
actual_state == BugStatus.wont_fix)
print('Identity:',
actual_state is desired_state,
actual_state is BugStatus.wont_fix)
print('Ordered by value:')
try:
    print('\n'.join(' ' + s.name for s in sorted(BugStatus)))
except TypeError as err:
    print(' Cannot sort: {}'.format(err))
```


```text
Equality: False True
Identity: False True
Ordered by value:
 Cannot sort: '<' not supported between instances of 'BugStatus' and 'BugStatus'
```


> Use the `IntEnum` *class* for enumerations where the members need to behave more like numbers—for example, to support comparisons.

将`IntEnum` 类用于成员需要表现得更像数字的枚举——例如，支持比较。


```python
# 2_4_enum_intenum.py
import enum


class BugStatus(enum.IntEnum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


print('Ordered by value:')
print('\n'.join(' ' + s.name for s in sorted(BugStatus)))
```

```text
Ordered by value:
 fix_released
 fix_committed
 in_progress
 wont_fix
 invalid
 incomplete
 new
```


### 2.1.4 Unique Enumeration Values

> Enum members with the same value are tracked as alias references to the same member object. Aliases do not cause repeated values to be present in the iterator for the `Enum`.

具有相同值的枚举成员作为对同一成员对象的别名引用进行跟踪。别名不会导致`Enum`的迭代器中出现重复值。

> Because `by_design` and `closed` are aliases for other members, they do not appear separately in the output when iterating over the `Enum`. The canonical name for a member is the first name attached to the value.

因为`by_design` 和`closed` 是其他成员的别名，所以在迭代`Enum` 时它们不会单独出现在输出中。成员的规范名称是附加到值的第一个名称。


```python
# 2_5_enum_aliases.py
import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

    by_design = 4
    closed = 1


for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))

print('\nSame: by_design is wont_fix: ', BugStatus.by_design is BugStatus.wont_fix)
print('Same: closed is fix_released: ', BugStatus.closed is BugStatus.fix_released)
```


```text
new             = 7
incomplete      = 6
invalid         = 5
wont_fix        = 4
in_progress     = 3
fix_committed   = 2
fix_released    = 1

Same: by_design is wont_fix:  True 
Same: closed is fix_released:  True
```


> To require all members to have unique values, add the `@unique` decorator to the `Enum`.

将 `@unique` 装饰器添加到 `Enum`，要求所有成员具有唯一值。

> Members with repeated values trigger a `ValueError` exception when the `Enum` class is being interpreted.

在解释 `Enum` 类时，具有重复值的成员会触发 `ValueError` 异常。

```python
# 2_6_enum_unique_enforce.py
import enum


@enum.unique
class BugStatus(enum.Enum):
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1
    # This will trigger an error with unique applied.
    by_design = 4
    closed = 1
```

```text
Traceback (most recent call last):
  File "c:\Users\ABCX1C\MyProjects\P3SL_Example\chapter_02_data_structures\2_6_enum_unique_enforce.py", line 5, in <module>
    class BugStatus(enum.Enum):
  File "C:\Users\ABCX1C\AppData\Local\Programs\Python\Python39\lib\enum.py", line 984, in unique
    raise ValueError('duplicate values found in %r: %s' %
ValueError: duplicate values found in <enum 'BugStatus'>: by_design -> wont_fix, closed -> fix_released
```

### 2.1.5 Creating Enumerations Programmatically

> In some cases, it is more convenient to create enumerations programmatically, rather than hard-coding them in a class definition. For those situations, `Enum` also supports passing the member names and values to the class constructor.

在某些情况下，以编程方式创建枚举比在类定义中对其进行硬编码更方便。对于这些情况，`Enum` 还支持将成员名称和值传递给类构造函数。

> The `value` argument is the name of the enumeration, which is used to build the representation of members. The `names` argument lists the members of the enumeration. When a single string is passed, it is split on whitespace and commas, and the resulting tokens are used as names for the members, which are automatically assigned values starting with 1.

`value` 参数是枚举的名称，用于构建成员的表示。`names` 参数列出了枚举的成员。当传递单个字符串时，它会在空格和逗号上拆分，生成的标记用作成员的名称，这些标记会自动分配从 1 开始的值。


```python
# 2_7_enum_programmatic_create.py
import enum


BugStatus = enum.Enum(
value='BugStatus',
names=('fix_released fix_committed in_progress '
'wont_fix invalid incomplete new'),
)

print('Member: {}'.format(BugStatus.new))

print('\nAll members:')
for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))
```

```text
Member: BugStatus.new

All members:
fix_released    = 1
fix_committed   = 2
in_progress     = 3
wont_fix        = 4
invalid         = 5
incomplete      = 6
new             = 7
```


> For more control over the values associated with members, the `names` string can be replaced
with a sequence of two-part tuples or a dictionary mapping names to values.

为了更好地控制与成员关联的值，可以将 `names` 字符串替换为由两部分组成的元组序列或将名称映射到值的字典。


> In this example, a list of two-part tuples is given instead of a single string containing only the member names. This makes it possible to reconstruct the `BugStatus` enumeration with the members in the same order as the version defined in `enum_create.py`.

在此示例中，给出了一个由两部分组成的元组列表，而不是仅包含成员名称的单个字符串。这使得可以按照与 `enum_create.py` 中定义的版本相同的顺序使用成员重构 `BugStatus` 枚举。

```python
# 2_8_enum_programmatic_mapping.py

import enum


BugStatus = enum.Enum(
    value='BugStatus',
    names=[
        ('new', 7),
        ('incomplete', 6),
        ('invalid', 5),
        ('wont_fix', 4),
        ('in_progress', 3),
        ('fix_committed', 2),
        ('fix_released', 1),
    ],
)

print('All members:')
for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))
```

```text
All members:
new             = 7
incomplete      = 6
invalid         = 5
wont_fix        = 4
in_progress     = 3
fix_committed   = 2
fix_released    = 1
```


### 2.1.6 Non-integer Member Values

> Enum member values are not restricted to integers. In fact, any type of object can be associated with a member. If the value is a tuple, the members are passed as individual arguments to `__init__()`.

枚举成员值不限于整数。事实上，任何类型的对象都可以与一个成员相关联。如果值是元组，则成员将作为单独的参数传递给`__init__()`。


> In this example, each member value is a tuple containing the numerical ID (such as might be stored in a database) and a list of valid transitions away from the current state.

在此示例中，每个成员值都是一个包含数字 ID（例如可能存储在数据库中）和远离当前状态的有效转换列表的元组。

```python
# 2_9_enum_tuple_values.py
import enum


class BugStatus(enum.Enum):

    new = (7, ['incomplete',
                'invalid',
                'wont_fix',
                'in_progress'])
    incomplete = (6, ['new', 'wont_fix'])
    invalid = (5, ['new'])
    wont_fix = (4, ['new'])
    in_progress = (3, ['new', 'fix_committed'])
    fix_committed = (2, ['in_progress', 'fix_released'])
    fix_released = (1, ['new'])

    def __init__(self, num, transitions):
        self.num = num
        self.transitions = transitions
    
    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:', BugStatus.in_progress.can_transition(BugStatus.new))
```


```text
Name: BugStatus.in_progress
Value: (3, ['new', 'fix_committed'])
Custom attribute: ['new', 'fix_committed']
Using attribute: True
```


> For more complex cases, tuples might become unwieldy. Since member values can be any type of object, dictionaries can be used for cases where there are a lot of separate attributes to track for each enum value. Complex values are passed directly to `__init__()` as the only argument other than `self`.

对于更复杂的情况，元组可能变得笨拙。由于成员值可以是任何类型的对象，因此字典可用于每个枚举值需要跟踪大量单独属性的情况。复数值直接传递给 `__init__()` 作为除 `self` 之外的唯一参数。

> This example expresses the same data as the previous example, using dictionaries rather than tuples.

此示例使用字典而不是元组来表达与前一个示例相同的数据。


```python
import enum


class BugStatus(enum.Enum):

    new = {
        'num': 7,
        'transitions': [
            'incomplete',
            'invalid',
            'wont_fix',
            'in_progress',
        ],
    }
    incomplete = {
        'num': 6,
        'transitions': ['new', 'wont_fix'],
    }
    invalid = {
        'num': 5,
        'transitions': ['new'],
    }
    wont_fix = {
        'num': 4,
        'transitions': ['new'],
    }
    in_progress = {
        'num': 3,
        'transitions': ['new', 'fix_committed'],
    }
    fix_committed = {
        'num': 2,
        'transitions': ['in_progress', 'fix_released'],
    }
    fix_released = {
        'num': 1,
        'transitions': ['new'],
    }

    def __init__(self, vals):
        self.num = vals['num']
        self.transitions = vals['transitions']
    
    def can_transition(self, new_state):
        return new_state.name in self.transitions

print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:', BugStatus.in_progress.can_transition(BugStatus.new))
```

```text
Name: BugStatus.in_progress
Value: {'num': 3, 'transitions': ['new', 'fix_committed']}
Custom attribute: ['new', 'fix_committed']
Using attribute: True
```


## 2.2 collections: Container Data Types

> The `collections` module includes container data types beyond the built-in types `list`, `dict`, and `tuple`.

`collections` 模块包括除内置类型 `list`、`dict` 和 `tuple` 之外的容器数据类型。

### 2.2.1 ChainMap: Search Multiple Dictionaries

> The `ChainMap` class manages a sequence of dictionaries, and searches through them in the order they appear to find values associated with keys. A `ChainMap` makes a good “context” container, since it can be treated as a stack for which changes happen as the stack grows, with these changes being discarded again as the stack shrinks.


`ChainMap`类管理一系列字典，并按照它们出现的顺序搜索它们以找到与键关联的值。`ChainMap` 是一个很好的“上下文”容器，因为它可以被视为一个堆栈，随着堆栈的增长而发生变化，随着堆栈的缩小，这些变化再次被丢弃。

#### 2.2.1.1 Accessing Values

> The `ChainMap` supports the same API as a regular dictionary for accessing existing values.

`ChainMap` 支持与常规字典相同的 API，用于访问现有值。

> The child mappings are searched in the order they are passed to the constructor, so the value reported for the key `'c'` comes from the `a` dictionary.

子映射按照它们传递给构造函数的顺序进行搜索，因此键`'c'`的值来自“a”字典。

```python
# 2_11_collections_chainmap_read.py
import collections

a = {'a': 'A', 'c': 'C'}

b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)

print('Individual Values')
print('a = {}'.format(m['a']))
print('b = {}'.format(m['b']))
print('c = {}'.format(m['c']))
print()

print('Keys = {}'.format(list(m.keys())))
print('Values = {}'.format(list(m.values())))
print()

print('Items:')
for k, v in m.items():
    print('{} = {}'.format(k, v))
print()

print('"d" in m: {}'.format(('d' in m)))
```

```text
Individual Values
a = A
b = B
c = C

Keys = ['b', 'c', 'a']  
Values = ['B', 'C', 'A']

Items:
b = B
c = C
a = A

"d" in m: False
```

#### 2.2.1.2 Reordering

> The `ChainMap` stores the list of mappings over which it searches in a list in its `maps` attribute. This list is mutable, so it is possible to add new mappings directly or to change the order of the elements to control lookup and update behavior.

`ChainMap` 存储它在其 `maps` 属性中的列表中搜索的映射列表。此列表是可变的，因此可以直接添加新映射或更改元素的顺序以控制查找和更新行为。

> When the list of mappings is reversed, the value associated with `'c'` changes.

当映射列表反转时，与“c”关联的值发生变化

```python
# 2_12_collections_chainmap_reorder.py
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)

print(m.maps)
print('c = {}\n'.format(m['c']))

# Reverse the list.
m.maps = list(reversed(m.maps))

print(m.maps)
print('c = {}'.format(m['c']))
```

```text
[{'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'}]
c = C

[{'b': 'B', 'c': 'D'}, {'a': 'A', 'c': 'C'}]
c = D
```

#### 2.2.1.3 Updating Values

> A `ChainMap` does not cache the values in the child mappings. Thus, if their contents are modified, the results are reflected when the `ChainMap` is accessed.

`ChainMap` 不会缓存子映射中的值。因此，如果它们的内容被修改，则在访问 `ChainMap` 时会反映结果。

> Changing the values associated with existing keys and adding new elements works the same
way.

更改与现有键关联的值和添加新元素的工作方式相同。

```python
# 2_13_collections_chainmap_update_behind.py
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)
print('Before: {}'.format(m['c']))
a['c'] = 'E'
print('After : {}'.format(m['c']))
```

```text
Before: C
After : E
```


> It is also possible to set values through the `ChainMap` directly, although only the first mapping in the chain is actually modified.

也可以直接通过 `ChainMap` 设置值，尽管实际上只修改了链中的第一个映射。

> When the new value is stored using m, the a mapping is updated.

当使用`m`存储新值时，将更新`a`映射。

```python
# 2_14_collections_chainmap_update_directly.py
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)
print('Before:', m)
m['c'] = 'E'
print('After :', m)
print('a:', a)
```

```text
Before: ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
After : ChainMap({'a': 'A', 'c': 'E'}, {'b': 'B', 'c': 'D'})
a: {'a': 'A', 'c': 'E'}
```


> `ChainMap` provides a convenience method for creating a new instance with one extra mapping at the front of the `maps` list to make it easy to avoid modifying the existing underlying data structures.

`ChainMap` 提供了一种方便的方法来创建一个新实例，在 `maps` 列表的前面有一个额外的映射，从而可以轻松避免修改现有的底层数据结构。


> This stacking behavior is what makes it convenient to use `ChainMap` instances as template or application contexts. Specifically, it is easy to add or update values in one iteration, then discard the changes for the next iteration.

这种堆叠行为使得将 `ChainMap` 实例用作模板或应用程序上下文变得很方便。具体来说，很容易在一次迭代中添加或更新值，然后在下一次迭代中丢弃更改。

```python
# 2_15_collections_chainmap_new_child.py
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m1 = collections.ChainMap(a, b)
m2 = m1.new_child()

print('m1 before:', m1)
print('m2 before:', m2)

m2['c'] = 'E'

print('m1 after:', m1)
print('m2 after:', m2)
```

```text
m1 before: ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m2 before: ChainMap({}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m1 after: ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m2 after: ChainMap({'c': 'E'}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
```

> For situations where the new context is known or built in advance, it is also possible to pass a mapping to `new_child()`.

对于新上下文已知或预先构建的情况，也可以将映射传递给`new_child()`。


```python
# 2_16_collections_chainmap_new_child_explicit.py
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}
c = {'c': 'E'}

m1 = collections.ChainMap(a, b)
# m2 = m1.new_child(c)
m2 = collections.ChainMap(c, *m1.maps)

print('m1["c"] = {}'.format(m1['c']))
print('m2["c"] = {}'.format(m2['c']))
```

```text
m1["c"] = C
m2["c"] = E
```


### 2.2.2 Counter: Count Hashable Objects

> A `Counter` is a container that keeps track of how many times equivalent values are added. It can be used to implement the same algorithms for which other languages commonly use bag or multiset data structures.

`Counter` 是一个容器，用于跟踪添加了多少次等效值。它可用于实现其他语言通常使用包或多集数据结构的相同算法。

#### 2.2.2.1 Initializing

> `Counter` supports three forms of initialization. Its constructor can be called with a sequence of items, a dictionary containing keys and counts, or using keyword arguments that map string names to counts.

`Counter` 支持三种初始化形式。可以使用一系列项目、包含键和计数的字典或使用将字符串名称映射到计数的关键字参数来调用它的构造函数。


> The results of all three forms of initialization are the same.

所有三种形式的初始化结果都是一样的。


```python
# 2_17_collections_counter_init.py
import collections

print(collections.Counter(['a', 'b', 'c', 'a', 'b', 'b']))
print(collections.Counter({'a': 2, 'b': 3, 'c': 1}))
print(collections.Counter(a=2, b=3, c=1))
```

```text
Counter({'b': 3, 'a': 2, 'c': 1})
Counter({'b': 3, 'a': 2, 'c': 1})
Counter({'b': 3, 'a': 2, 'c': 1})
```


> An empty `Counter` can be constructed with no arguments and populated via the `update()` method.

> The count values are increased based on the new data, rather than replaced. In the preceding example, the count for `a` goes from `3` to `4`.

计数值根据新数据增加，而不是被替换。在前面的示例中，`a` 的计数从`3`变为`4`。

```python
# 2_18_collections_counter_update.py
import collections

c = collections.Counter()
print('Initial :', c)

c.update('abcdaab')
print('Sequence:', c)

c.update({'a': 1, 'd': 5})
print('Dict :', c)
```

```text
Initial : Counter()
Sequence: Counter({'a': 3, 'b': 2, 'c': 1, 'd': 1})
Dict : Counter({'d': 6, 'a': 4, 'b': 2, 'c': 1})
```

#### 2.2.2.2 Accessing Counts

> Once a `Counter` is populated, its values can be retrieved using the dictionary API.

填充`Counter`后，可以使用字典 API 检索其值。

> `Counter` does not raise `KeyError` for unknown items. If a value has not been seen in the input (as with `e` in this example), its count is `0`.

`Counter` 不会为未知项目引发 `KeyError`。如果在输入中没有看到某个值（如本例中的 `e`），则其计数为0。

```python
# 2_19_collections_counter_get_values.py
import collections

c = collections.Counter('abcdaab')

for letter in 'abcde':
    print('{} : {}'.format(letter, c[letter]))

```

```text
a : 3
b : 2
c : 1
d : 1
e : 0
```

> The `elements()` method returns an iterator that produces all of the items known to the `Counter`.

elements()` 方法返回一个迭代器，该迭代器生成 `Counter` 已知的所有项目。

> The order of elements is not guaranteed, and items with counts less than or equal to zero are not included.

不保证元素的顺序，并且不包括计数小于或等于零的项目。

```python
# 2_20_collection_counter_elements.py
import collections

c = collections.Counter('extremely')
c['z'] = 0
print(c)
print(list(c.elements()))
```

```text
Counter({'e': 3, 'x': 1, 't': 1, 'r': 1, 'm': 1, 'l': 1, 'y': 1, 'z': 0})
['e', 'e', 'e', 'x', 't', 'r', 'm', 'l', 'y']
```


> Use `most_common()` to produce a sequence of the `n` most frequently encountered input values and their respective counts.

使用 `most_common()` 来生成一个由 `n` 个最常遇到的输入值及其各自的计数组成的序列。

> This example counts the letters appearing in all of the words in the system dictionary to produce a frequency distribution, then prints the three most common letters. Leaving out the argument to `most_common()` produces a list of all the items, in order of frequency.

本示例统计系统词典中所有单词中出现的字母以生成频率分布, 然后打印三个最常见的字母。省略`most_common()`的参数会按频率顺序生成所有项目的列表。

这个例子中的文件路径是linux系统。

```python
# 2_21_collections_counter_most_common.py
import collections

c = collections.Counter()
with open('/usr/share/dict/words', 'rt') as f:
    for line in f:
        c.update(line.rstrip().lower())

print('Most common:')
for letter, count in c.most_common(3):
    print('{}: {:>7}'.format(letter, count))
```

```text
Most common:
e: 235331
i: 201032
a: 199554
```


#### 2.2.2.3 Arithmetic

> `Counter` instances support arithmetic and set operations for aggregating results. This example shows the standard operators for creating new `Counter` instances, but the in-place operators `+=`, `-=`, `&=`, and `|=` are also supported.

`Counter` 实例支持用于聚合结果的算术和集合操作。此示例显示了用于创建新 `Counter` 实例的标准运算符，但也支持就地运算符 `+=`、`-=`、`&=` 和 `|=`。


> Each time a new `Counter` is produced through an operation, any items with zero or negative counts are discarded. The count for `a` is the same in `c1` and `c2`, so subtraction leaves it at zero.

每次通过操作产生一个新的“Counter”时，任何具有零或负计数的项目都将被丢弃。 `a` 的计数在 `c1` 和 `c2` 中相同，因此减法将其保留为零。

```python
# 2_22_collections_counter_arithmetic.py
import collections

c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = collections.Counter('alphabet')

print('C1:', c1)
print('C2:', c2)

print('\nCombined counts:')
print(c1 + c2)

print('\nSubtraction:')
print(c1 - c2)

print('\nIntersection (taking positive minimums):')
print(c1 & c2)

print('\nUnion (taking maximums):')
print(c1 | c2)
```


```text
C1: Counter({'b': 3, 'a': 2, 'c': 1})
C2: Counter({'a': 2, 'l': 1, 'p': 1, 'h': 1, 'b': 1, 'e': 1, 't': 1})    

Combined counts:
Counter({'a': 4, 'b': 4, 'c': 1, 'l': 1, 'p': 1, 'h': 1, 'e': 1, 't': 1})

Subtraction:
Counter({'b': 2, 'c': 1})

Intersection (taking positive minimums):
Counter({'a': 2, 'b': 1})

Union (taking maximums):
Counter({'b': 3, 'a': 2, 'c': 1, 'l': 1, 'p': 1, 'h': 1, 'e': 1, 't': 1})
```


### defaultdict: Missing Keys Return a Default Value

> The standard dictionary includes the method `setdefault()` for retrieving a value and establishing a default if the value does not exist. By contrast, `defaultdict` lets the caller specify the default up front when the container is initialized.

标准字典包含方法`setdefault()`，用于检索值并在该值不存在时建立默认值。相比之下，`defaultdict` 让调用者在容器初始化时预先指定默认值。

> This method works well as long as it is appropriate for all keys to have the same default. It can be especially useful if the default is a type used for aggregating or accumulating values, such as a `list`, `set`, or even `int`. The standard library documentation includes several examples in which `defaultdict` is used in this way.

```python
# 2_23_collections_defaultdict.py
import collections


def default_factory():
    return 'default value'

    
d = collections.defaultdict(default_factory, foo='bar')
print('d:', d)
print('foo =>', d['foo'])
print('bar =>', d['bar'])
```

```text
d: defaultdict(<function default_factory at 0x000001C86BCA0DC0>, {'foo': 'bar'})
foo => bar
bar => default value
```


### 2.2.4 deque: Double-Ended Queue

> A double-ended queue, or `deque`, supports adding and removing elements from either end of the queue. The more commonly used stacks and queues are degenerate forms of deques, where the inputs and outputs are restricted to a single end.

双端队列或`deque`，支持从队列的任一端添加和删除元素。更常用的堆栈和队列是双端队列的退化形式，其中输入和输出仅限于单端。


> Since deques are a type of sequence container, they support some of the same operations as list, such as examining the contents with `__getitem__()`, determining length, and removing elements from the middle of the queue by matching identity.

由于双端队列是一种序列容器，它们支持一些与列表相同的操作，例如使用`__getitem__()`检查内容、确定长度以及通过匹配标识从队列中间删除元素。


```python
# 2_24_collections_deque.py
import collections

d = collections.deque('abcdefg')
print('Deque:', d)
print('Length:', len(d))
print('Left end:', d[0])
print('Right end:', d[-1])

d.remove('c')
print('remove(c):', d)
```

```text
Deque: deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
Length: 7
Left end: a
Right end: g
remove(c): deque(['a', 'b', 'd', 'e', 'f', 'g'])
```


#### 2.2.4.1 Populating

> A deque can be populated from either end, termed “left” and “right” in the Python implementation.

双端队列可以从任一端填充，在 Python 实现中称为“左”和“右”。

> The `extendleft()` function iterates over its input and performs the equivalent of an `appendleft()` for each item. The end result is that the `deque` contains the input sequence in reverse order.

`extendleft()` 函数对其输入进行迭代，并为每个项目执行与 `appendleft()` 等效的操作。最终结果是 `deque` 以相反的顺序包含输入序列。


```python
# 2_25_collections_deque_populating.py
import collections

# Add to the right.
d1 = collections.deque()
d1.extend('abcdefg')
print('extend :', d1)
d1.append('h')
print('append :', d1)

# Add to the left.
d2 = collections.deque()
d2.extendleft(range(6))
print('extendleft:', d2)
d2.appendleft(6)
print('appendleft:', d2)
```


```text
extend : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
append : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
extendleft: deque([5, 4, 3, 2, 1, 0])
appendleft: deque([6, 5, 4, 3, 2, 1, 0])
```


#### 2.2.4.2 Consuming

> Similarly, the elements of the deque can be consumed from both ends or either end, depending on the algorithm being applied.

类似地，可以从两端或任一端消耗双端队列的元素，具体取决于所应用的算法。

> Use `pop()` to remove an item from the “right” end of the deque and `popleft()` to take an item from the “left” end.

使用`pop()`从双端队列的“右”端删除一个项目，使用`popleft()`从“左”端获取一个项目。

```python
# 2_26_collections_deque_consuming.py
import collections

print('From the right:')
d = collections.deque('abcdefg')
while True:
    try:
        print(d.pop(), end='')
    except IndexError:
        break
print

print('\nFrom the left:')
d = collections.deque(range(6))
while True:
    try:
        print(d.popleft(), end='')
    except IndexError:
        break
print
```

```text
From the right:
gfedcba
From the left:
012345
```

[^_^]: 这里是注释


> Since deques are thread-safe, the contents can even be consumed from both ends at the same time from separate threads.

由于双端队列是线程安全的，因此甚至可以从不同的线程同时从两端消耗内容。


> The threads in this example alternate between each end, removing items until the deque is empty.

此示例中的线程在每一端之间交替，删除项直到双端队列为空。

```python
# 2_27_collections_deque_both_ends.py
import collections
import threading
import time

candle = collections.deque(range(5))


def burn(direction, nextSource):
    while True:
        try:
            next = nextSource()
        except IndexError:
            break
        else:
            print('{:>8}: {}'.format(direction, next))
            time.sleep(0.1)
    print('{:>8} done'.format(direction))
    return

left = threading.Thread(target=burn, args=('Left', candle.popleft))
right = threading.Thread(target=burn, args=('Right', candle.pop))

left.start()
right.start()

left.join()
right.join()
```

```text
  Left: 0
   Right: 4
    Left: 1
   Right: 3
    Left: 2
   Right done
    Left done
```


#### 2.2.4.3 Rotating

> Another useful aspect of the `deque` is the ability to rotate it in either direction, so as to skip over some items.

`deque` 的另一个有用方面是能够在任一方向旋转它，以便跳过某些项。

> Rotating the `deque` to the right (using a positive rotation) takes items from the right end and moves them to the left end. Rotating to the left (with a negative value) takes items from the left end and moves them to the right end. It may help to visualize the items in the deque as being engraved along the edge of a dial.

将 `deque` 向右旋转（使用正旋转）从右端获取项目并将它们移动到左端。向左旋转（使用负值）从左端获取项目并将它们移动到右端。将`deque`中的项想象为沿表盘边缘雕刻可能会有所帮助。

```python
# 2_28_collections_deque_rotate.py
import collections

d = collections.deque(range(10))
print('Normal :', d)

d = collections.deque(range(10))
d.rotate(2)
print('Right rotation:', d)

d = collections.deque(range(10))
d.rotate(-2)
print('Left rotation :', d)
```


```text
Normal : deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Right rotation: deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])
Left rotation : deque([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])
```



#### 2.2.4.4 Constraining the Queue Size

> A `deque` instance can be configured with a maximum length so that it never grows beyond that size. When the queue reaches the specified length, existing items are discarded as new items are added. This behavior is useful for finding the last `n` items in a stream of undetermined length.

双端队列实例可以配置为最大长度，以便它永远不会超过该大小。当队列达到指定长度时，随着新项目的添加，现有项目将被丢弃。此行为对于在不确定长度的流中查找最后`n`个项很有用。

> The deque length is maintained regardless of which end the items are added to.

无论项添加到哪一端，双端队列长度都会保持不变。

```python
# 2_29_collections_deque_maxlen.py
import collections
import random

# Set the random seed so we see the same output each time
# the script is run.
random.seed(1)

d1 = collections.deque(maxlen=3)
d2 = collections.deque(maxlen=3)

for i in range(5):
    n = random.randint(0, 100)
    print('n =', n)
    d1.append(n)
    d2.appendleft(n)
    print('D1:', d1)
    print('D2:', d2)
```

```text
n = 17
D1: deque([17], maxlen=3)
D2: deque([17], maxlen=3)
n = 72
D1: deque([17, 72], maxlen=3)
D2: deque([72, 17], maxlen=3)
n = 97
D1: deque([17, 72, 97], maxlen=3)
D2: deque([97, 72, 17], maxlen=3)
n = 8
D1: deque([72, 97, 8], maxlen=3)
D2: deque([8, 97, 72], maxlen=3)
n = 32
D1: deque([97, 8, 32], maxlen=3)
D2: deque([32, 8, 97], maxlen=3)
```


### 2.2.5 namedtuple: Tuple Subclass with Named Fields

> The standard `tuple` uses numerical indexes to access its members.

标准的`tuple`使用数字索引来访问其成员。

> This makes tuples convenient containers for simple uses.

这使得元组成为简单使用的方便容器。

```python
# 2_30_collections_tuple.py
bob = ('Bob', 30, 'male')
print('Representation:', bob)

jane = ('Jane', 29, 'female')
print('\nField by index:', jane[0])

print('\nFields by index:')
for p in [bob, jane]:
    print('{} is a {} year old {}'.format(*p))
```

```text
Representation: ('Bob', 30, 'male')

Field by index: Jane

Fields by index:
Bob is a 30 year old male
Jane is a 29 year old female
```


> In contrast, remembering which index should be used for each value can lead to errors, especially if the `tuple` has a lot of fields and is constructed far from where it is used. A `namedtuple` assigns names, as well as the numerical index, to each member.

相比之下，记住每个值应该使用哪个索引可能会导致错误，特别是如果 `tuple` 有很多字段并且构造远离它的使用位置。`namedtuple` 为每个成员分配名称以及数字索引。


#### 2.2.5.1 Defining

> `namedtuple` instances are just as memory efficient as regular tuples because they do not have per-instance dictionaries. Each kind of `namedtuple` is represented by its own class, which is created by using the `namedtuple()` factory function. The arguments are the name of the new class and a string containing the names of the elements.

`namedtuple` 实例与常规元组一样具有内存效率，因为它们没有每个实例的字典。每种`namedtuple` 都由它自己的类表示，该类是使用`namedtuple()` 工厂函数创建的。参数是新类的名称和包含元素名称的字符串。


> As the example illustrates, it is possible to access the fields of the `namedtuple` by name using dotted notation (`obj.attr`) as well as by using the positional indexes of standard tuples.

如示例所示，可以使用点符号 (`obj.attr`) 以及使用标准元组的位置索引按名称访问 `namedtuple` 的字段。

```python
# 2_31_collections_namedtuple_person.py
import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('\nRepresentation:', bob)

jane = Person(name='Jane', age=29)
print('\nField by name:', jane.name)

print('\nFields by index:')
for p in [bob, jane]:
    print('{} is {} years old'.format(*p))
```

```text

Representation: Person(name='Bob', age=30)

Field by name: Jane

Fields by index:
Bob is 30 years old
Jane is 29 years old
```


> Just like a regular `tuple`, a `namedtuple` is immutable. This restriction allows `tuple` instances to have a consistent hash value, which makes it possible to use them as keys in dictionaries and to be included in sets.

就像常规的`tuple`一样，`namedtuple`是不可变的。此限制允许 `tuple` 实例具有一致的哈希值，这使得可以将它们用作字典中的键并包含在集合中。

> Trying to change a value through its named attribute results in an `AttributeError`.

尝试通过其命名属性更改值会导致 `AttributeError`

```python
# 2_32_collections_namedtuple_immutable.py
import collections

Person = collections.namedtuple('Person', 'name age')

pat = Person(name='Pat', age=12)
print('\nRepresentation:', pat)

pat.age = 21
```

```text

Representation: Person(name='Pat', age=12)
Traceback (most recent call last):
  File "c:\Users\ABCX1C\MyProjects\P3SL_Example\chapter_02_data_structures\section_22_collections\2_32_collections_namedtuple_immutable.py", line 8, in <module>
    pat.age = 21
AttributeError: can't set attribute
```

#### 2.2.5.2 Invalid Field Names

> Field names are invalid if they are repeated or conflict with Python keywords.

如果字段名称重复或与 Python 关键字冲突，则字段名称无效。

> As the field names are parsed, invalid values cause `ValueError` exceptions.

解析字段名称时，无效值会导致 `ValueError` 异常。

```python
# 2_33_collections_namedtuple_bad_fields.py
import collections

try:
    collections.namedtuple('Person', 'name class age')
except ValueError as err:
    print(err)

try:
    collections.namedtuple('Person', 'name age age')
except ValueError as err:
    print(err)
```

```text
Type names and field names cannot be a keyword: 'class'
Encountered duplicate field name: 'age'
```

> In situations where a `namedtuple` is created based on values outside the control of the program (such as to represent the rows returned by a database query, where the schema is not known in advance), the `rename` option should be set to `True` so the invalid fields are renamed.

在基于程序控制之外的值创建`namedtuple` 的情况下（例如表示数据库查询返回的行，其中模式事先未知），`rename` 选项应设置为`True` 所以无效的字段被重命名。


