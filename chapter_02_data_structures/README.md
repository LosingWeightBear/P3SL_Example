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