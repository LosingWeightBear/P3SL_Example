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

> Iterating over the enum `class` produces the individual members of the enumeration.


```python
```

```text
```