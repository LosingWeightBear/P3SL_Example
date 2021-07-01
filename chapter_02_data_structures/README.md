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

在基于程序控制之外的值创建`namedtuple` 的情况下（例如表示数据库查询返回的行，其中模式事先未知），`rename` 选项应设置为`True`,所以无效的字段被重命名。

> The new names for renamed fields depend on their index in the tuple, so the field with name `class` becomes `_1` and the duplicate `age` field is changed to `_2`.

重命名字段的新名称取决于它们在元组中的索引，因此名称为 `class` 的字段变为 `_1`，重复的 `age` 字段更改为 `_2`。


```python
import collections

with_class = collections.namedtuple('Person', 'name class age', rename=True)
print(with_class._fields)

two_ages = collections.namedtuple('Person', 'name age age', rename=True)
print(two_ages._fields)
```

```text
('name', '_1', 'age')
('name', 'age', '_2')
```


#### 2.2.5.3 Special Attributes

> `namedtuple` provides several useful attributes and methods for working with subclasses and instances. All of these built-in properties have names prefixed with an underscore (`_`), which by convention in most Python programs indicates a private attribute. For `namedtuple`, however, the prefix is intended to protect the name from collision with user-provided attribute names.

> The names of the fields passed to `namedtuple` to define the new class are saved in the `_fields` attribute.

`namedtuple` 提供了几个有用的属性和方法来处理子类和实例。所有这些内置属性的名称都以下划线 (`_`) 为前缀，按照惯例，在大多数 Python 程序中，下划线表示私有属性。然而，对于`namedtuple`，前缀旨在保护名称免于与用户提供的属性名称冲突。

传递给`namedtuple` 以定义新类的字段名称保存在`_fields` 属性中。

> Although the argument is a single space-separated string, the stored value is the sequence of individual names.

尽管参数是单个空格分隔的字符串，但存储的值是单个名称的序列。

```python
# 2_35_collections_namedtuple_fields.py
import collections

Person = collections.namedtuple('Person', 'name age')
bob = Person(name='Bob', age=30)
print('Representation:', bob)
print('Fields:', bob._fields)
```

```text
Representation: Person(name='Bob', age=30)
Fields: ('name', 'age')
```

> `namedtuple` instances can be converted to `OrderedDict` instances using `_asdict()`.

`namedtuple` 实例可以使用 `_asdict()` 转换为 `OrderedDict` 实例。

> The keys of the `OrderedDict` are in the same order as the fields for the `namedtuple`.

`OrderedDict` 的键与 `namedtuple` 的字段顺序相同。


```python
# 2_36_collections_namedtuple_asdict.py
import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('Representation:', bob)
print('As Dictionary:', bob._asdict())
```

```text
Representation: Person(name='Bob', age=30)
As Dictionary: {'name': 'Bob', 'age': 30}
```


> The `_replace()` method builds a new instance, replacing the values of some fields in the process.

`_replace()` 方法构建一个新实例，替换进程中某些字段的值。

> Although the name implies it is modifying the existing object, because `namedtuple` instances are immutable the method actually returns a new object.

尽管名称暗示它正在修改现有对象，但因为`namedtuple` 实例是不可变的，该方法实际上返回一个新对象。

```python
# 2_37_collections_namedtuple_replace.py
import collections

Person = collections.namedtuple('Person', 'name age')
bob = Person(name='Bob', age=30)
print('\nBefore:', bob)
bob2 = bob._replace(name='Robert')
print('After:', bob2)
print('Same?:', bob is bob2)
```

```text

Before: Person(name='Bob', age=30)
After: Person(name='Robert', age=30)
Same?: False
```

### 2.2.6 OrderedDict: Remember the Order Keys Are Added to a Dictionary

> An `OrderedDict` is a dictionary subclass that remembers the order in which its contents are added.

`OrderedDict` 是一个字典子类，它记住其内容添加的顺序。

> A regular `dict` does not track the insertion order, and iterating over it produces the values in order based on how the keys are stored in the hash table, which is in turn influenced by a random value to reduce collisions. In an `OrderedDict`, by contrast, the order in which the items are inserted is remembered and used when creating an iterator.

常规的`dict`不跟踪插入顺序，并且根据键在哈希表中的存储方式对其进行迭代，从而按顺序生成值，而哈希表又受随机值的影响以减少冲突。相比之下，在`OrderedDict`中，插入项的顺序会在创建迭代器时被记住和使用。


```python
# 2_38_collections_ordereddict_iter.py
import collections

print('Regular dictionary:')
d = {}
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)

print('\nOrderedDict:')
d = collections.OrderedDict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)
```

[^_^]: 这个案例并没有看出区别啊！！！

```text
Regular dictionary:
a A
b B
c C

OrderedDict:
a A
b B
c C
```


#### 2.2.6.1 Equality

> A regular `dict` looks at its contents when testing for equality. An `OrderedDict` also considers the order in which the items were added.

常规的“dict”在测试相等性时会查看其内容。 `OrderedDict` 还考虑了添加项目的顺序。

> In this case, since the two ordered dictionaries are created from values in a different order, they are considered to be different.

这个案例显示，由于两个有序字典是根据不同顺序的值创建的，因此它们被认为是不同的。

```python
# 2_39_collections_ordereddict_equality.py
import collections

print('dict       :', end=' ')
d1 = {}
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = {}
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'

print(d1 == d2)

print('OrderedDict:', end=' ')

d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = collections.OrderedDict()
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'

print(d1 == d2)
```

```text
dict       : True
OrderedDict: False
```

#### 2.2.6.2 Reordering

> It is possible to change the order of the keys in an `OrderedDict` by moving them to either the beginning or the end of the sequence using `move_to_end()`.

可以通过使用 `move_to_end()` 将它们移动到序列的开头或结尾来更改 `OrderedDict` 中键的顺序。

> The last argument tells `move_to_end()` whether to move the item to be the last item in the key sequence (when `True`) or the first (when `False`).

后一个参数告诉 `move_to_end()` 是将项移动到键序列中的最后一项（当 `True` 时）还是第一个（当 `False` 时）。

```python
# 2_40_collections_ordereddict_move_to_end.py
import collections

d = collections.OrderedDict(
    [('a', 'A'), ('b', 'B'), ('c', 'C')]
)

print('Before:')
for k, v in d.items():
    print(k, v)

d.move_to_end('b')

print('\nmove_to_end():')
for k, v in d.items():
    print(k, v)

d.move_to_end('b', last=False)

print('\nmove_to_end(last=False):')
for k, v in d.items():
    print(k, v)
```

```text
Before:
a A
b B
c C

move_to_end():
a A
c C
b B

move_to_end(last=False):
b B
a A
c C
```


### 2.2.7 collections.abc: Abstract Base Classes for Containers

> The `collections.abc` module contains abstract base classes that define the APIs for container data structures built into Python and provided by the `collections` module. Refer to Table 2.1 for a list of the classes and their purposes.

`collections.abc` 模块包含抽象基类，这些类定义了 Python 内置并由 `collections` 模块提供的容器数据结构的 API。有关类别及其用途的列表，请参阅表 2.1。


> In addition to clearly defining the APIs for containers with different semantics, these abstract base classes can be used to test whether an object supports an API before invoking it using `isinstance()`. Some of the classes also provide implementations of methods, and they can be used as mix-ins to build up custom container types without implementing every method from scratch.

除了为不同语义的容器明确定义 API 外，这些抽象基类还可用于在使用 isinstance() 调用对象之前测试对象是否支持 API。一些类还提供方法的实现，它们可以用作混合来构建自定义容器类型，而无需从头开始实现每个方法。


||||
|--|--|--|
||||

## 2.3 array: Sequence of Fixed-Type Data

> The `array` module defines a sequence data structure that looks very much like a `list`, except that all of the members have to be of the same primitive type. The types supported are all numeric or other fixed-size primitive types such as bytes.

`array` 模块定义了一个看起来非常像 `list` 的序列数据结构，除了所有成员必须是相同的原始类型。支持的类型都是数字或其他固定大小的原始类型，例如字节。

> Refer to Table 2.2 for some of the supported types. The standard library documentation for `array` includes a complete list of type codes.

有关一些支持的类型，请参阅表 2.2。 `array` 的标准库文档包括完整的类型代码列表。


### 2.3.1 Initialization

> An `array` is instantiated with an argument describing the type of data to be allowed, and possibly an initial sequence of data to store in the array.

`array` 使用描述允许的数据类型的参数进行实例化，并且可能是要存储在数组中的初始数据序列。

> In this example, the array is configured to hold a sequence of bytes and is initialized with a simple byte string.

在这个例子中，数组被配置为保存一个字节序列并用一个简单的字节字符串初始化。

```python
# 2_41_array_string.pys
import array
import binascii

s = b'This is the array.'
a = array.array('b', s)

print('As byte string:', s)
print('As array      :', a)
print('As hex        :', binascii.hexlify(a))
```

```text
As byte string: b'This is the array.'
As array      : array('b', [84, 104, 105, 115, 32, 105, 115, 32, 116, 104, 101, 32, 97, 114, 114, 97, 121, 46])
As hex        : b'54686973206973207468652061727261792e'
```


### 2.3.2 Manipulating Arrays

> An `array` can be extended and otherwise manipulated in the same ways as other Python sequences.

`array` 可以以与其他 Python 序列相同的方式进行扩展和操作。

> The supported operations include slicing, iterating, and adding elements to the end.

支持的操作包括切片、迭代和添加元素到最后。

```python
# 2_42_array_sequence.py
import array
import pprint

a = array.array('i', range(3))
print('Initial :', a)

a.extend(range(3))
print('Extended:', a)

print('Slice :', a[2:5])

print('Iterator:')
print(list(enumerate(a)))
```

```text
Initial : array('i', [0, 1, 2])
Extended: array('i', [0, 1, 2, 0, 1, 2])
Slice   : array('i', [2, 0, 1])
Iterator:
[(0, 0), (1, 1), (2, 2), (3, 0), (4, 1), (5, 2)]
```

### 2.3.3 Arrays and Files

> The contents of an array can be written to and read from files using built-in methods coded efficiently for that purpose.

可以使用内置方法将数组的内容写入文件和从文件中读取，为此提高编码效率。

> This example illustrates reading the data “raw,” meaning directly from the binary file, versus reading it into a new array and converting the bytes to the appropriate types.

此示例说明了读取“原始”数据，即直接从二进制文件中读取数据，而不是将其读取到新数组中并将字节转换为适当的类型。

[^_^]: 这里要注意，原书中的示例代码在Win10下，会报`PermissionError: [Errno 13] Permission denied`,用这种方式创建的临时文件，在linux系统里不关闭文件即可再次打开读取内容，但是在windows系统，不关闭就没有权限再次打开。另外，文件默认的是，一旦关闭，就会被自动清除。所以这里就有了一个矛盾：不关闭文件就没有打开的权限；关闭之后文件就删除了，更无法打开。要解决这个问题，我们需要三个关键步骤：（1）修改NamedTemporaryFile的delete参数，让文件关闭后不会自动清理。（2）读取之前，先关闭。（3）最后“手动”清理这个临时文件。

```python
# 2_43_array_file.py
import array
import binascii
import tempfile
import os

a = array.array('i', range(5))
print('A1:', a)

# Write the array of numbers to a temporary file.
# for Windows close the tmp file before open it again
output = tempfile.NamedTemporaryFile(delete=False) # for windows set delelte as False
a.tofile(output.file) # Must pass an *actual* file
output.flush()
output.close() # close the tmp file

# Read the raw data.
with open(output.name, 'rb') as input:
    raw_data = input.read()
    print('Raw Contents:', binascii.hexlify(raw_data))

    # Read the data into an array.
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print('A2:', a2)


os.remove(output.name) # delete the tmp file
```

```text
A1: array('i', [0, 1, 2, 3, 4])
Raw Contents: b'0000000001000000020000000300000004000000'
A2: array('i', [0, 1, 2, 3, 4])
```


> `tofile()` uses `tobytes()` to format the data, and `fromfile()` uses `frombytes()` to convert it back to an array instance.

`tofile()` 使用 `tobytes()` 来格式化数据，`fromfile()` 使用 `frombytes()` 将其转换回数组实例。

> Both `tobytes()` and `frombytes()` work on byte strings, not Unicode strings.

tobytes()` 和 `frombytes()` 都适用于字节字符串，而不是 Unicode 字符串。


```python
# 2_44_array_tobytes.py
import array
import binascii

a = array.array('i', range(5))
print('A1:', a)

as_bytes = a.tobytes()
print('Bytes:', binascii.hexlify(as_bytes))

a2 = array.array('i')
a2.frombytes(as_bytes)
print('A2:', a2)
```

```text
A1: array('i', [0, 1, 2, 3, 4])
Bytes: b'0000000001000000020000000300000004000000'
A2: array('i', [0, 1, 2, 3, 4])
```


### 2.3.4 Alternative Byte Ordering

> If the data in the array is not in the native byte order, or if the data needs to be swapped before being sent to a system with a different byte order (or over the network), it is possible to convert the entire array without iterating over the elements from Python.

如果数组中的数据不是本机字节顺序，或者如果数据在发送到具有不同字节顺序的系统（或通过网络）之前需要交换，则可以在不迭代的情况下转换整个数组在 Python 中的元素。

> The `byteswap()` method switches the byte order of the items in the array from within C, so it is much more efficient than looping over the data in Python.

`byteswap()` 方法从 C 中切换数组中项目的字节顺序，因此它比在 Python 中循环数据要高效得多。


```python
# 2_45_array_byteswap.py
import array
import binascii


def to_hex(a):
    chars_per_item = a.itemsize * 2 # 2 hex digits
    hex_version = binascii.hexlify(a)
    num_chunks = len(hex_version) // chars_per_item
    for i in range(num_chunks):
        start = i * chars_per_item
        end = start + chars_per_item
        yield hex_version[start:end]

    
start = int('0x12345678', 16)
end = start + 5
a1 = array.array('i', range(start, end))
a2 = array.array('i', range(start, end))
a2.byteswap()

fmt = '{:>12} {:>12} {:>12} {:>12}'
print(fmt.format('A1 hex', 'A1', 'A2 hex', 'A2'))
print(fmt.format('-' * 12, '-' * 12, '-' * 12, '-' * 12))
fmt = '{!r:>12} {:12} {!r:>12} {:12}'
for values in zip(to_hex(a1), a1, to_hex(a2), a2):
    print(fmt.format(*values))
```

```text
      A1 hex           A1       A2 hex           A2
------------ ------------ ------------ ------------
 b'78563412'    305419896  b'12345678'   2018915346
 b'79563412'    305419897  b'12345679'   2035692562
 b'7a563412'    305419898  b'1234567a'   2052469778
 b'7b563412'    305419899  b'1234567b'   2069246994
 b'7c563412'    305419900  b'1234567c'   2086024210
```


## 2.4 heapq: Heap Sort Algorithm

> A heap is a tree-like data structure in which the child nodes have a sort-order relationship with the parents. Binary heaps can be represented using a list or array organized so that the children of element N are at positions 2*N+1 and 2*N+2 (for zero-based indexes). This layout makes it possible to rearrange heaps in place, so it is not necessary to reallocate as much memory when adding or removing items. 

堆是一种树状数据结构，其中子节点与父节点具有排序关系。二元堆可以使用一个列表或数组来表示，这样组织起来，元素 N 的子元素位于 2*N+1 和 2*N+2 位置（对于从零开始的索引）。这种布局可以就地重新排列堆，因此在添加或删除项目时不需要重新分配尽可能多的内存。

> A max-heap ensures that the parent is larger than or equal to both of its children. A min-heap requires that the parent be less than or equal to its children. Python’s `heapq` module implements a min-heap.

最大堆确保父级大于或等于其两个子级。最小堆要求父级小于或等于其子级。Python 的 `heapq` 模块实现了一个最小堆。


### 2.4.1 Example Data

> The examples in this section use the data in `heapq_heapdata.py`.

本节中的示例使用了 `heapq_heapdata.py` 中的数据。



```python
# This data was generated with the random module.
data = [19, 9, 4, 10, 11]
```


> The heap output is printed using `heapq_showtree.py`.

堆输出使用 `heapq_showtree.py` 打印。

```python
import math
from io import StringIO


def show_tree(tree, total_width=36, fill=' '):
    """Pretty-print a tree."""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2 ** row
        col_width = int(math.floor(total_width / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print('-' * total_width)
    print()
```


### 2.4.2 Creating a Heap

> There are two basic ways to create a heap: `heappush()` and `heapify()`.

有两种基本的方法来创建堆：`heappush()` 和 `heapify()`。


> When `heappush()` is used, the heap sort order of the elements is maintained as new items are added from a data source.

当使用 `heappush()` 时，元素的堆排序顺序会在从数据源添加新项目时保持不变。

```python
# 2_48_heapq_heappush.py
import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

heap = []
print('random :', data)
print()

for n in data:
    print('add {:>3}:'.format(n))
    heapq.heappush(heap, n)
    show_tree(heap)
```

```text
random : [19, 9, 4, 10, 11]

add  19:

                 19
------------------------------------

add   9:

                 9
        19
------------------------------------

add   4:

                 4
        19                9
------------------------------------

add  10:

                 4
        10                9
    19
------------------------------------

add  11:

                 4
        10                9
    19       11
------------------------------------
```


> If the data is already in memory, it is more efficient to use `heapify()` to rearrange the items of the list in place.

如果数据已经在内存中，使用 `heapify()` 来重新安排列表的项目会更有效。

> The result of building a list in heap order one item at a time is the same as building an unordered list and then calling `heapify()`.

以堆顺序构建一个列表一次一个项目的结果与构建一个无序列表然后调用`heapify()`的结果相同。

```python
# 2_49_heapq_heapify.py
import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

print('random :', data)
heapq.heapify(data)
print('heapified :')
show_tree(data)
```


```text
random : [19, 9, 4, 10, 11]
heapified :

                 4
        9                 19
    10       11
------------------------------------
```


### 2.4.3 Accessing the Contents of a Heap

> Once the heap is organized correctly, use `heappop()` to remove the element with the lowest value.

一旦堆被正确组织，使用`heappop()`删除具有最低值的元素。


> In this example, adapted from the standard library documentation, `heapify()` and `heappop()` are used to sort a list of numbers.

在这个例子中，改编自标准库文档，`heapify()` 和 `heappop()` 用于对数字列表进行排序。


```python
# 2_50_heapq_heappop.py
import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

print('random :', data)
heapq.heapify(data)

print('heapified :')
show_tree(data)
print

for i in range(2):
    smallest = heapq.heappop(data)
    print('pop {:>3}:'.format(smallest))
    show_tree(data)
```

```text
random : [19, 9, 4, 10, 11]
heapified :

                 4
        9                 19
    10       11
------------------------------------

pop   4:

                 9
        10                19
    11
------------------------------------

pop   9:

                 10
        11                19
------------------------------------
```


> To remove existing elements and replace them with new values in a single operation, use `heapreplace()`.

要在单个操作中删除现有元素并用新值替换它们，请使用 `heapreplace()`。

> Replacing elements in place makes it possible to maintain a fixed-size heap, such as a queue of jobs ordered by priority.

就地替换元素可以维护固定大小的堆，例如按优先级排序的作业队列。

```python
# 2_51_heapq_heapreplace.py
import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

heapq.heapify(data)
print('start:')
show_tree(data)

for n in [0, 13]:
    smallest = heapq.heapreplace(data, n)
    print('replace {:>2} with {:>2}:'.format(smallest, n))
    show_tree(data)
```


```text
start:

                 4
        9                 19
    10       11
------------------------------------

replace  4 with  0:

                 0
        9                 19
    10       11
------------------------------------

replace  0 with 13:

                 9
        10                19
    13       11
------------------------------------
```


### 2.4.4 Data Extremes from a Heap


> `heapq` also includes two functions to examine an iterable and find a range of the largest or smallest values it contains.

`heapq` 还包括两个函数来检查迭代并找到它包含的最大值或最小值的范围。

> Using `nlargest()` and `nsmallest()` is efficient only for relatively small values of `n > 1`, but can still come in handy in a few cases.

使用 `nlargest()` 和 `nsmallest()` 仅对相对较小的 `n > 1` 值有效，但在少数情况下仍然可以派上用场。

```python
# 2_52_heapq_extremes.py
import heapq
from heapq_heapdata import data

print('all :', data)
print('3 largest :', heapq.nlargest(3, data))
print('from sort :', list(reversed(sorted(data)[-3:])))
print('3 smallest:', heapq.nsmallest(3, data))
print('from sort :', sorted(data)[:3])
```

```text
all : [19, 9, 4, 10, 11]
3 largest : [19, 11, 10]
from sort : [19, 11, 10]
3 smallest: [4, 9, 10]
from sort : [4, 9, 10]
```


### 2.4.5 Efficiently Merging Sorted Sequences

> Combining several sorted sequences into one new sequence is easy for small data sets.

对于小数据集，将几个排序的序列组合成一个新序列很容易。

> `list(sorted(itertools.chain(*data)))`

> For larger data sets, this technique can use a considerable amount of memory. Instead of sorting the entire combined sequence, `merge()` uses a heap to generate a new sequence one item at a time, determining the next item using a fixed amount of memory.

对于较大的数据集，此技术可能会使用大量内存。`merge()` 不是对整个组合序列进行排序，而是使用堆来一次生成一个新序列,使用固定数量的内存来确定下一个项目。

> Because the implementation of `merge()` uses a heap, it consumes memory based on the number of sequences being merged, rather than the number of items in those sequences.

因为 `merge()` 的实现使用堆，它根据被合并的序列数量消耗内存，而不是这些序列中的项目数量。

```python
# 2_53_heapq_merge.py
import heapq
import random

random.seed(2016)

data = []
for i in range(4):
    new_data = list(random.sample(range(1, 101), 5))
    new_data.sort()
    data.append(new_data)

for i, d in enumerate(data):
    print('{}: {}'.format(i, d))

print('\nMerged:')
for i in heapq.merge(*data):
    print(i, end=' ')
print()
```

```text
0: [33, 58, 71, 88, 95]
1: [10, 11, 17, 38, 91]
2: [13, 18, 39, 61, 63]
3: [20, 27, 31, 42, 45]

Merged:
10 11 13 17 18 20 27 31 33 38 39 42 45 58 61 63 71 88 91 95
```


## 2.5 bisect: Maintain Lists in Sorted Order

> The `bisect` module implements an algorithm for inserting elements into a list while maintaining the list in sorted order.

`bisect` 模块实现了一种算法，用于将元素插入到列表中，同时保持列表的排序顺序。

### 2.5.1 Inserting in Sorted Order

> Here is a simple example in which `insort()` is used to insert items into a list in sorted order.

这是一个简单的示例，其中使用 `insort()` 将项目按排序顺序插入到列表中。

> The first column of the output shows the new random number. The second column shows the position where the number will be inserted into the list. The remainder of each line is the current sorted list.

输出的第一列显示新的随机数。第二列显示将数字插入列表的位置。每行的其余部分是当前的排序列表。

```python
# 2_54_bisect_example.py
import bisect

# A series of random numbers
values = [14, 85, 77, 26, 50, 45, 66, 79, 10, 3, 84, 77, 1]

print('New Pos Contents')
print('--- --- --------')

l = []
for i in values:
    position = bisect.bisect(l, i)
    bisect.insort(l, i)
    print('{:3} {:3}'.format(i, position), l)
```


```text
New Pos Contents
--- --- --------
 14   0 [14]
 85   1 [14, 85]
 77   1 [14, 77, 85]
 26   1 [14, 26, 77, 85]
 50   2 [14, 26, 50, 77, 85]
 45   2 [14, 26, 45, 50, 77, 85]
 66   4 [14, 26, 45, 50, 66, 77, 85]
 79   6 [14, 26, 45, 50, 66, 77, 79, 85]
 10   0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
  3   0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
 84   9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
 77   8 [3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
  1   0 [1, 3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
```


> This is a simple example. In fact, given the amount of data being manipulated, it might be faster to simply build the list and then sort it once. By contrast, for long lists, significant time and memory savings can be achieved using an insertion sort algorithm such as this, especially when the operation to compare two members of the list requires expensive computation.

这是一个简单的例子。事实上，考虑到要处理的数据量，简单地构建列表然后对它进行一次排序可能会更快。相比之下，对于长列表，使用诸如此类的插入排序算法可以实现显着的时间和内存节省，特别是当比较列表的两个成员的操作需要昂贵的计算时。


### 2.5.2 Handling Duplicates

> The result set shown previously includes a repeated value, `77`. The `bisect` module provides two ways to handle repeats: New values can be inserted either to the left of existing values, or to the right. The `insort()` function is actually an alias for `insort_right()`, which inserts an item after the existing value. The corresponding function `insort_left()` inserts an item before the existing value.

前面显示的结果集包含一个重复值`77`。`bisect` 模块提供了两种处理重复的方法：新值可以插入到现有值的左侧，也可以插入到右侧。`insort()` 函数实际上是 `insort_right()` 的别名，它在现有值之后插入一个项目。相应的函数 `insort_left()` 在现有值之前插入一个项目。


```python
# 2_55_bisect_example2.py
import bisect

# A series of random numbers
values = [14, 85, 77, 26, 50, 45, 66, 79, 10, 3, 84, 77, 1]

print('New Pos Contents')
print('--- --- --------')
# Use bisect_left and insort_left.

l = []
for i in values:
    position = bisect.bisect_left(l, i)
    bisect.insort_left(l, i)
    print('{:3} {:3}'.format(i, position), l)
```

```text
New Pos Contents
--- --- --------
 14   0 [14]
 85   1 [14, 85]
 77   1 [14, 77, 85]
 26   1 [14, 26, 77, 85]
 50   2 [14, 26, 50, 77, 85]
 45   2 [14, 26, 45, 50, 77, 85]
 66   4 [14, 26, 45, 50, 66, 77, 85]
 79   6 [14, 26, 45, 50, 66, 77, 79, 85]
 10   0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
  3   0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
 84   9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
 77   7 [3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
  1   0 [1, 3, 10, 14, 26, 45, 50, 66, 77, 77, 79, 84, 85]
```


> When the same data is manipulated using `bisect_left()` and `insort_left()`, the results are the same sorted list but the insert positions are different for the duplicate values.

当使用 `bisect_left()` 和 `insort_left()` 处理相同的数据时，结果是相同的排序列表，但重复值的插入位置不同。


## 2.6 queue: Thread-Safe FIFO Implementation

> The `queue` module provides a first-in, first-out (FIFO) data structure suitable for multithreaded programming. It can be used to pass messages or other data between producer and consumer threads safely. Locking is handled for the caller, so many threads can work with the same `Queue` instance safely and easily. The size of a `Queue` (the number of elements it contains) may be restricted to throttle memory usage or processing.

`queue` 模块提供了适合多线程编程的先进先出 (FIFO) 数据结构。它可用于在生产者和消费者线程之间安全地传递消息或其他数据。锁定是为调用者处理的，因此许多线程可以安全轻松地使用同一个 `Queue` 实例。`Queue` 的大小（它包含的元素数量）可能会受到限制内存使用或处理的限制。


### 2.6.1 Basic FIFO Queue

> The `Queue` class implements a basic first-in, first-out container. Elements are added to one “end” of the sequence using `put()`, and removed from the other end using `get()`.

`Queue` 类实现了一个基本的先进先出容器。使用`put()`将元素添加到序列的一端，并使用`get()`从另一端删除元素。

> This example uses a single thread to illustrate that elements are removed from the queue in the same order in which they are inserted.

此示例使用单个线程来说明元素从队列中删除的顺序与它们插入的顺序相同。

```python
# 2_56_queue_fifo.py
import queue

q = queue.Queue()

for i in range(5):
    q.put(i)

while not q.empty():
    print(q.get(), end=' ')
print()
```

```text
0 1 2 3 4
```


### 2.6.2 LIFO Queue

> In contrast to the standard FIFO implementation of Queue, the `LifoQueue` uses last-in, first-out ordering (normally associated with a stack data structure).

与 Queue 的标准 FIFO 实现相反，“LifoQueue”使用后进先出排序（通常与堆栈数据结构相关联）。

> The item most recently `put` into the queue is removed by `get`.

最近被“放入”队列的项目被“获取”删除。

```python
# 2_57_queue_lifo.py
import queue

q = queue.Queue()

for i in range(5):
    q.put(i)

while not q.empty():
    print(q.get(), end=' ')
print()
```

```text
4 3 2 1 0 
```


### 2.6.3 Priority Queue

> Sometimes the processing order of the items in a queue needs to be based on characteristics of those items, rather than just the order they are created or added to the queue. For example, print jobs from the payroll department may take precedence over a code listing that a developer wants to print. `PriorityQueue` uses the sort order of the contents of the queue to decide which item to retrieve.

有时，队列中项目的处理顺序需要基于这些项目的特征，而不仅仅是它们被创建或添加到队列中的顺序。例如，来自工资部门的打印作业可能优先于开发人员想要打印的代码列表。 `PriorityQueue` 使用队列内容的排序顺序来决定要检索的项目。

> This example has multiple threads consuming the jobs, which are processed based on the priority of items in the queue at the time `get()` was called. The order of processing for items added to the queue while the consumer threads are running depends on thread context switching.

此示例有多个线程使用作业，这些作业根据调用`get()`时队列中项目的优先级进行处理。消费者线程运行时添加到队列的项目的处理顺序取决于线程上下文切换。

```python
# 2_58_queeu_priority.py
import functools
import queue
import threading


@functools.total_ordering
class Job:

    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('New job:', description)
        return

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented


q = queue.PriorityQueue()

q.put(Job(3, 'Mid-level job'))
q.put(Job(10, 'Low-level job'))
q.put(Job(1, 'Important job'))


def process_job(q):
    while True:
        next_job = q.get()
        print('Processing job:', next_job.description)
        q.task_done()


workers = [
    threading.Thread(target=process_job, args=(q,)),
    threading.Thread(target=process_job, args=(q,)),
]
for w in workers:
    w.setDaemon(True)
    w.start()

q.join()
```

```text
New job: Mid-level job
New job: Low-level job
New job: Important job
Processing job: Important job
Processing job: Mid-level job
Processing job: Low-level job
```


### 2.6.4 Building a Threaded Podcast Client

> The source code for the podcasting client in this section demonstrates how to use the `Queue` class with multiple threads. The program reads one or more `RSS` feeds, queues up the enclosures for the five most recent episodes from each feed to be downloaded, and processes several downloads in parallel using threads. It does not have enough error handling for production use, but the skeleton implementation illustrates the use of the `queue` module.

本节中播客客户端的源代码演示了如何在多线程中使用 `Queue` 类。该程序读取一个或多个“RSS”提要，将要下载的每个提要中最近五集的附件排队，并使用线程并行处理多个下载。它没有足够的错误处理以供生产使用，但框架实现说明了 `queue` 模块的使用。

> First, some operating parameters are established. Usually, these would come from user inputs (e.g., preferences or a database). The example uses hard-coded values for the number of threads and list of URLs to fetch.

首先，建立一些操作参数。通常，这些将来自用户输入（例如，偏好或数据库）。该示例使用硬编码值作为要获取的线程数和 URL 列表。

> The function `download_enclosures()` runs in the worker thread and processes the downloads using `urllib`.

函数`download_enclosures()`在工作线程中运行并使用`urllib`处理下载。


> Once the target function for the threads is defined, the worker threads can be started. When `download_enclosures()` processes the statement `url = q.get()`, it blocks and waits until the queue has something to return. That means it is safe to start the threads before there is anything in the queue.

一旦定义了线程的目标函数，就可以启动工作线程。当`download_enclosures()` 处理语句`url = q.get()` 时，它会阻塞并等待队列有东西要返回。这意味着在队列中有任何东西之前启动线程是安全的。


> The next step is to retrieve the feed contents using the `feedparser` module and enqueue the URLs of the enclosures. As soon as the first URL is added to the queue, one of the worker threads picks it up and starts downloading it. The loop continues to add items until the feed is exhausted, and the worker threads take turns dequeuing URLs to download them.

下一步是使用 `feedparser` 模块检索提要内容并将附件的 URL 加入队列。一旦第一个 URL 被添加到队列中，一个工作线程就会选择它并开始下载它。循环继续添加项目，直到提要耗尽，工作线程轮流将 URL 出列以下载它们。


> The only thing left to do is wait for the queue to empty out again, using `join()`.

唯一剩下要做的就是等待队列再次清空，使用`join()`。

```python
# 2_59_fetch_podcasts.py
from queue import Queue
import threading
import time
import urllib
from urllib.parse import urlparse

import feedparser

# Set up some global variables.
num_fetch_threads = 2
enclosure_queue = Queue()

# A real app wouldn't use hard-coded data.
feed_urls = [
    'http://talkpython.fm/episodes/rss',
]

def message(s):
    print('{}: {}'.format(threading.current_thread().name, s))



def download_enclosures(q):
    """This is the worker thread function.
    It processes items in the queue one after
    another. These daemon threads go into an
    infinite loop, and exit only when
    the main thread ends.
    """
    while True:
        message('looking for the next enclosure')
        url = q.get()
        filename = url.rpartition('/')[-1]
        message('downloading {}'.format(filename))
        response = urllib.request.urlopen(url)
        data = response.read()
        # Save the downloaded file to the current directory.
        message('writing to {}'.format(filename))
        with open(filename, 'wb') as outfile:
            outfile.write(data)
        q.task_done()


# Set up some threads to fetch the enclosures.
for i in range(num_fetch_threads):
    worker = threading.Thread(
        target=download_enclosures,
        args=(enclosure_queue,),
        name='worker-{}'.format(i),
    )
    worker.setDaemon(True)
    worker.start()



# Download the feed(s) and put the enclosure URLs into
# the queue.
for url in feed_urls:
    response = feedparser.parse(url, agent='fetch_podcasts.py')
    for entry in response['entries'][:5]:
        for enclosure in entry.get('enclosures', []):
            parsed_url = urlparse(enclosure['url'])
            message('queuing {}'.format(
                parsed_url.path.rpartition('/')[-1]))
            enclosure_queue.put(enclosure['url'])


# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
message('*** main thread waiting')
enclosure_queue.join()
message('*** done')
```


```text
worker-0: looking for the next enclosure
worker-1: looking for the next enclosure
MainThread: queuing a-path-into-data-science.mp3
MainThread: queuing htmx-clean-dynamic-html-pages.mp3
worker-0: downloading a-path-into-data-science.mp3
worker-1: downloading htmx-clean-dynamic-html-pages.mp3
MainThread: queuing python-in-the-electrical-energy-sector.mp3
MainThread: queuing typosquatting-and-supply-chains-vulnerabilities.mp3
MainThread: queuing measuring-your-ml-impact-with-codecarbon.mp3
MainThread: *** main thread waiting
worker-0: writing to a-path-into-data-science.mp3
worker-0: looking for the next enclosure
worker-0: downloading python-in-the-electrical-energy-sector.mp3
worker-0: writing to python-in-the-electrical-energy-sector.mp3
worker-0: looking for the next enclosure
worker-0: downloading typosquatting-and-supply-chains-vulnerabilities.mp3
worker-0: writing to typosquatting-and-supply-chains-vulnerabilities.mp3
worker-0: looking for the next enclosure
worker-0: downloading measuring-your-ml-impact-with-codecarbon.mp3
worker-1: writing to htmx-clean-dynamic-html-pages.mp3
worker-1: looking for the next enclosure
worker-0: writing to measuring-your-ml-impact-with-codecarbon.mp3
worker-0: looking for the next enclosure
MainThread: *** done
```

## 2.7 struct: Binary Data Structures

> The `struct` module includes functions for converting between strings of bytes and native Python data types such as numbers and strings.

`struct` 模块包括用于在字节字符串和本机 Python 数据类型（如数字和字符串）之间进行转换的函数。

### 2.7.1 Functions Versus Struct Class

> A set of module-level functions is available for working with structured values, as well as the `Struct` class. Format specifiers are converted from their string format to a compiled representation, similar to the way regular expressions are handled. The conversion takes some resources, so it is typically more efficient to do it once when creating a `Struct` instance and call methods on the instance instead of using the module-level functions. All of the following examples use the `Struct` class.


一组模块级函数可用于处理结构化值以及 `Struct` 类。格式说明符从其字符串格式转换为已编译的表示形式，类似于处理正则表达式的方式。转换需要一些资源，因此在创建 `Struct` 实例并在实例上调用方法而不是使用模块级函数时，执行一次通常更有效。以下所有示例都使用 Struct 类。


### 2.7.2 Packing and Unpacking

> Structs support packing data into strings, and unpacking data from strings using format specifiers made up of characters representing the type of the data and optional count and endianness indicators. Refer to the standard library documentation for a complete list of the supported format specifiers.

结构支持将数据打包成字符串，并使用格式说明符从字符串中解压缩数据，格式说明符由表示数据类型的字符和可选的计数和字节序指示符组成。有关支持的格式说明符的完整列表，请参阅标准库文档。

> In this example, the specifier calls for an integer or long integer value, a two-byte string, and a floating-point number. The spaces in the format specifier are included to separate the type indicators, and are ignored when the format is compiled.

在此示例中，说明符调用整数或长整数值、两字节字符串和浮点数。格式说明符中的空格用于分隔类型指示符，并在编译格式时被忽略。

> The example converts the packed value to a sequence of hex bytes for printing with `binascii.hexlify()`, since some of the characters are nulls.

该示例将打包值转换为十六进制字节序列，以便使用 `binascii.hexlify()` 进行打印，因为某些字符是空值。

```python
# 2_60_struct_pack.py
import struct
import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
s = struct.Struct('I 2s f')
packed_data = s.pack(*values)

print('Original values:', values)
print('Format string  :', s.format)
print('Uses           :', s.size, 'bytes')
print('Packed Value   :', binascii.hexlify(packed_data))
```

```text
Original values: (1, b'ab', 2.7)
Format string  : I 2s f
Uses           : 12 bytes
Packed Value   : b'0100000061620000cdcc2c40'
```

> Use `unpack()` to extract data from its packed representation.

使用 `unpack()` 从其打包表示中提取数据。

> Passing the packed value to `unpack()`, gives basically the same values back (note the discrepancy in the floating point value).


将打包值传递给 `unpack()`，返回基本相同的值（注意浮点值的差异）。

```python
# 2_61_struct_unpack.py
import struct
import binascii

packed_data = binascii.unhexlify(b'0100000061620000cdcc2c40')

s = struct.Struct('I 2s f')
unpacked_data = s.unpack(packed_data)
print('Unpacked Values:', unpacked_data)
```

```text
Unpacked Values: (1, b'ab', 2.700000047683716)
```


### 2.7.3 Endianness

字节序

> By default, values are encoded using the native C library notion of endianness. It is easy to override that choice by providing an explicit endianness directive in the format string.

默认情况下，值使用本机 C 库的字节序概念进行编码。通过在格式字符串中提供显式字节序指令，很容易覆盖该选择。

```python
# 2_62_struct_endianness.py
import struct
import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
print('Original values:', values)

endianness = [
    ('@', 'native, native'),
    ('=', 'native, standard'),
    ('<', 'little-endian'),
    ('>', 'big-endian'),
    ('!', 'network'),
]

for code, name in endianness:
    s = struct.Struct(code + ' I 2s f')
    packed_data = s.pack(*values)
    print()
    print('Format string :', s.format, 'for', name)
    print('Uses :', s.size, 'bytes')
    print('Packed Value :', binascii.hexlify(packed_data))
    print('Unpacked Value :', s.unpack(packed_data))
```

```text
Original values: (1, b'ab', 2.7)

Format string : @ I 2s f for native, native
Uses : 12 bytes
Packed Value : b'0100000061620000cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string : = I 2s f for native, standard
Uses : 10 bytes
Packed Value : b'010000006162cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string : < I 2s f for little-endian
Uses : 10 bytes
Packed Value : b'010000006162cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string : > I 2s f for big-endian
Uses : 10 bytes
Packed Value : b'000000016162402ccccd'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string : ! I 2s f for network
Uses : 10 bytes
Packed Value : b'000000016162402ccccd'
Unpacked Value : (1, b'ab', 2.700000047683716)
```


> Table 2.3 lists the byte order specifiers used by `Struct`.

|Code|Meaning|
| :----: |----|
|`@`|Native order|
|`=`|Native standard|
|`<`|Little-endian|
|`>`|Big-endian|
|`!`|Network order|


### 2.7.4 Buffers

> Working with binary packed data is typically reserved for performance-sensitive situations or passing data into and out of extension modules. These cases can be optimized by avoiding the overhead of allocating a new buffer for each packed structure. The `pack_into()` and `unpack_from()` methods support writing to pre-allocated buffers directly.

使用二进制打包数据通常保留用于性能敏感的情况或将数据传入和传出扩展模块。可以通过避免为每个打包结构分配新缓冲区的开销来优化这些情况。`pack_into()` 和 `unpack_from()` 方法支持直接写入预先分配的缓冲区。

> The `size` attribute of the `Struct` tells us how big the buffer needs to be.

`Struct` 的 `size` 属性告诉我们缓冲区需要多大。

```python
# 2_63_struct_buffers.py
import array
import binascii
import ctypes
import struct

s = struct.Struct('I 2s f')
values = (1, 'ab'.encode('utf-8'), 2.7)
print('Original:', values)

print()
print('ctypes string buffer')

b = ctypes.create_string_buffer(s.size)
print('Before :', binascii.hexlify(b.raw))
s.pack_into(b, 0, *values)
print('After :', binascii.hexlify(b.raw))
print('Unpacked:', s.unpack_from(b, 0))

print()
print('array')

a = array.array('b', b'\0' * s.size)
print('Before :', binascii.hexlify(a))
s.pack_into(a, 0, *values)
print('After :', binascii.hexlify(a))
print('Unpacked:', s.unpack_from(a, 0))
```


```text
Original: (1, b'ab', 2.7)

ctypes string buffer
Before : b'000000000000000000000000'
After : b'0100000061620000cdcc2c40'
Unpacked: (1, b'ab', 2.700000047683716)

array
Before : b'000000000000000000000000'
After : b'0100000061620000cdcc2c40'
Unpacked: (1, b'ab', 2.700000047683716)
```


## 2.8 weakref: Impermanent References to Objects

> The `weakref` module supports weak references to objects. A normal reference increments the reference count on the object and prevents it from being garbage collected. This outcome is not always desirable, especially when a circular reference might be present or when a cache of objects should be deleted when memory is needed. A weak reference is a handle to an object that does not keep it from being cleaned up automatically.

`weakref` 模块支持对对象的弱引用。普通引用会增加对象的引用计数并防止它被垃圾收集。这种结果并不总是可取的，尤其是当可能存在循环引用或需要内存时应删除对象缓存时。弱引用是一个对象的句柄，它不会阻止它被自动清理。


### 2.8.1 References

> Weak references to objects are managed through the `ref` class. To retrieve the original object, call the reference object.

对对象的弱引用通过 `ref` 类进行管理。要检索原始对象，请调用引用对象

> In this case, since `obj` is deleted before the second call to the reference, the `ref` returns `None`.

在这种情况下，由于在第二次调用引用之前删除了 `obj`，所以 `ref` 返回 `None`。

```python
# 2_64_weakref_ref.py
import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting {})'.format(self))


obj = ExpensiveObject()
r = weakref.ref(obj)

print('obj:', obj)
print('ref:', r)
print('r():', r())

print('deleting obj')
del obj
print('r():', r())
```

```text
obj: <__main__.ExpensiveObject object at 0x000001C334A82FD0>
ref: <weakref at 0x000001C334A7E900; to 'ExpensiveObject' at 0x000001C334A82FD0>
r(): <__main__.ExpensiveObject object at 0x000001C334A82FD0>
deleting obj
(Deleting <__main__.ExpensiveObject object at 0x000001C334A82FD0>)
r(): None
```