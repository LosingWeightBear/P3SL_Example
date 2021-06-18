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