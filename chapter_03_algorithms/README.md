# Chapter 3 -- Algorithms

[toc]

> Python includes several modules for implementing algorithms elegantly and concisely using
whatever style is most appropriate for the task. It supports purely procedural, objectoriented,
and functional styles, and all three styles are frequently mixed within different
parts of the same program.

Python 包括几个模块，用于使用最适合任务的任何样式优雅而简洁地实现算法。
它支持纯过程式、面向对象式和函数式风格，并且这三种风格经常在同一程序的不同部分中混合使用。

> `functools` (page 143) includes functions for creating function decorators, enabling
aspect-oriented programming and code reuse beyond what a traditional object-oriented
approach supports. It also provides a class decorator for implementing all of the rich comparison
APIs using a shortcut, and `partial` objects for creating references to functions with
their arguments included.

`functools`（第 143 页）包括用于创建函数装饰器的函数，支持面向方面编程和代码重用，超出了传统面向对象方法的支持范围。
它还提供了一个类装饰器，用于使用快捷方式实现所有丰富的比较 API，以及用于创建对包含其参数的函数的引用的“部分”对象。

> The `itertools` (page 163) module includes functions for creating and working with
iterators and generators used in functional programming. The `operator` (page 183) module
eliminates the need for many trivial lambda functions when using a functional programming
style by providing function-based interfaces to built-in operations such as arithmetic or item
lookup.

`itertools`（第 163 页）模块包括用于创建和使用函数式编程中使用的迭代器和生成器的函数。
`operator`（第 183 页）模块通过为内置运算（如算术或项目查找）提供基于函数的接口，消除了在使用函数式编程风格时对许多普通 lambda 函数的需求。


> No matter which style is used in a program, `contextlib` (page 191) makes resource
management easier, more reliable, and more concise. Combining context managers and the
`with` statement reduces the number of `try:finally` blocks and indentation levels needed,
while ensuring that files, sockets, database transactions, and other resources are closed and
released at the right time.

无论程序中使用哪种风格，`contextlib`（第 191 页）都使资源管理更容易、更可靠、更简洁。
结合上下文管理器和 `with` 语句减少了 `try:finally` 块的数量和所需的缩进级别，同时确保文件、套接字、数据库事务和其他资源在正确的时间关闭和释放。

## 3.1 functools: Tools for Manipulating Functions

> The `functools` module provides tools for adapting or extending functions and other callable
objects, without completely rewriting them.

`functools` 模块提供了用于调整或扩展函数和其他可调用对象的工具，而无需完全重写它们。


### 3.1.1 Decorators

装饰器

> The primary tool supplied by the `functools` module is the class partial, which can be used
to “wrap” a callable object with default arguments. The resulting object is itself callable
and can be treated as though it is the original function. It takes all of the same arguments
as the original, and can be invoked with extra positional or named arguments as well. A
`partial` can be used instead of a `lambda` to provide default arguments to a function, while
leaving some arguments unspecified.

`functools` 模块提供的主要工具是部分类，它可用于“包装”具有默认参数的可调用对象。
结果对象本身是可调用的，可以将其视为原始函数。
它采用与原始参数相同的所有参数，也可以使用额外的位置或命名参数进行调用。
可以使用 `partial` 代替 `lambda` 来为函数提供默认参数，同时保留一些未指定的参数。

#### 3.1.1.1 Partial Objects

> The first example shows two simple `partial` objects for the function `myfunc()`. The output
of `show_details()` includes the `func`, `args`, and `keywords` attributes of the partial object.

第一个示例显示了函数`myfunc()`的两个简单的`partial`对象。
`show_details()` 的输出包括部分对象的`func`、`args`和`keywords`属性。

> At the end of the example, the first `partial` created is invoked without passing a value
for a, causing an exception.

在示例的最后，创建的第一个 `partial` 被调用而没有为 `a` 传递值，从而导致异常。

```python
import functools


def myfunc(a, b=2):
    """Docstring for myfunc()."""
    print(' called myfunc with:', (a, b))


def show_details(name, f, is_partial=False):
    """Show details of a callable object."""
    print('{}:'.format(name))
    print(' object:', f)
    if not is_partial:
        print(' __name__:', f.__name__)
    if is_partial:
        print(' func:', f.func)
        print(' args:', f.args)
        print(' keywords:', f.keywords)
    return


show_details('myfunc', myfunc)
myfunc('a', 3)
print()

# Set a different default value for 'b', but require
# the caller to provide 'a'.
p1 = functools.partial(myfunc, b=4)
show_details('partial with named default', p1, True)
p1('passing a')
p1('override b', b=5)
print()

# Set default values for both 'a' and 'b'.
p2 = functools.partial(myfunc, 'default a', b=99)
show_details('partial with defaults', p2, True)
p2()
p2(b='override b')
print()

print('Insufficient arguments:')
p1()

```

```text
myfunc:
 object: <function myfunc at 0x0000019D8CFB4AF0>
 __name__: myfunc
 called myfunc with: ('a', 3)

partial with named default:
 object: functools.partial(<function myfunc at 0x0000019D8CFB4AF0>, b=4)
 func: <function myfunc at 0x0000019D8CFB4AF0>
 args: ()
 keywords: {'b': 4}
 called myfunc with: ('passing a', 4)
 called myfunc with: ('override b', 5)

partial with defaults:
 object: functools.partial(<function myfunc at 0x0000019D8CFB4AF0>, 'default a', b=99)
 func: <function myfunc at 0x0000019D8CFB4AF0>
 args: ('default a',)
 keywords: {'b': 99}
 called myfunc with: ('default a', 99)
 called myfunc with: ('default a', 'override b')

Insufficient arguments:
Insufficient arguments:
Traceback (most recent call last):
  File "C:/Users/ABCX1C/MyProjects/P3SL_Example/chapter_03_algorithms/2_84_functools_partial.py", line 41, in <module>
    p1()
TypeError: myfunc() missing 1 required positional argument: 'a'
python-BaseException
```


#### 3.1.1.2 Acquiring Function Properties

> The `partial` object does not have `__name__` or `__doc__` attributes by default, and without
those attributes, decorated functions are more difficult to debug. `update_wrapper()` can be
used to copy or add attributes from the original function to the `partial` object.

`partial` 对象默认没有 `__name__` 或 `__doc__` 属性，如果没有这些属性，修饰函数更难调试。 
`update_wrapper()` 可用于将原始函数的属性复制或添加到 `partial` 对象。

> The attributes added to the wrapper are defined in `WRAPPER_ASSIGNMENTS`, while
`WRAPPER_UPDATES` lists values to be modified.

添加到包装器的属性在`WRAPPER_ASSIGNMENTS` 中定义，而`WRAPPER_UPDATES` 列出要修改的值。


```python
import functools


def myfunc(a, b=2):
    """Docstring for myfunc()."""
    print(' called myfunc with:', (a, b))


def show_details(name, f):
    """Show details of a callable object."""
    print('{}:'.format(name))
    print(' object:', f)
    print(' __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
    print(' __doc__', repr(f.__doc__))
    print()


show_details('myfunc', myfunc)

p1 = functools.partial(myfunc, b=4)
show_details('raw wrapper', p1)

print('Updating wrapper:')
print(' assign:', functools.WRAPPER_ASSIGNMENTS)
print(' update:', functools.WRAPPER_UPDATES)
print()

functools.update_wrapper(p1, myfunc)
show_details('updated wrapper', p1)
```

```text
myfunc:
 object: <function myfunc at 0x0000019166E3E0D0>
 __name__: myfunc
 __doc__ 'Docstring for myfunc().'

raw wrapper:
 object: functools.partial(<function myfunc at 0x0000019166E3E0D0>, b=4)
 __name__: (no __name__)
 __doc__ 'partial(func, *args, **keywords) - new function with partial application\n    of the given arguments and keywords.\n'

Updating wrapper:
 assign: ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')
 update: ('__dict__',)

updated wrapper:
 object: functools.partial(<function myfunc at 0x0000019166E3E0D0>, b=4)
 __name__: myfunc
 __doc__ 'Docstring for myfunc().'
```


#### 3.1.1.3 Other Callables

> Partials work with any callable object, not just with stand-alone functions.

Partials 适用于任何可调用的对象，而不仅仅是独立的函数。

> This example creates partials from an instance of a class with a `__call__()` method.

此示例使用 `__call__()` 方法从类的实例创建partials。


```python
# 3_3_functools_callable.py
import functools


class MyClass:
    """Demonstration class for functools"""

    def __call__(self, e, f=6):
        """Docstring for MyClass.__call__"""
        print(' called object with:', (self, e, f))


def show_details(name, f):
    """Show details of a callable object."""
    print('{}:'.format(name))
    print(' object:', f)
    print(' __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
        print(' __doc__', repr(f.__doc__))
    return


o = MyClass()

show_details('instance', o)
o('e goes here')
print()

p = functools.partial(o, e='default for e', f=8)
functools.update_wrapper(p, o)
show_details('instance wrapper', p)
p()

```

```text
instance:
 object: <__main__.MyClass object at 0x000001E3FB269FA0>
 __name__: (no __name__)
 __doc__ 'Demonstration class for functools'
 called object with: (<__main__.MyClass object at 0x000001E3FB269FA0>, 'e goes here', 6)

instance wrapper:
 object: functools.partial(<__main__.MyClass object at 0x000001E3FB269FA0>, e='default for e', f=8)
 __name__: (no __name__)
 __doc__ 'Demonstration class for functools'
 called object with: (<__main__.MyClass object at 0x000001E3FB269FA0>, 'default for e', 8)

Process finished with exit code 0

```

#### 3.1.1.4 Methods and Functions

> While `partial()` returns a callable ready to be used directly, `partialmethod()` returns a
callable ready to be used as an unbound method of an object. In the following example,
the same stand-alone function is added as an attribute of `MyClass` twice, once using
`partialmethod()` as `method1()` and again using `partial()` as `method2()`.

`partial()`返回一个可直接使用的可调用对象，而`partialmethod()`返回一个可调用对象，可用作对象的未绑定方法。
在下面的示例中，相同的独立函数被添加为`MyClass`的属性两次，一次使用`partialmethod()`作为`method1()`，再次使用`partial()`作为`method2()`

> `method1()` can be called from an instance of `MyClass`, and the instance is passed as the
first argument, just as with methods that are defined in the usual way. `method2()` is not set
up as a bound method, so the `self` argument must be passed explicitly; otherwise, the call
will result in a `TypeError`.

`method1()` 可以从 `MyClass` 的实例中调用，并且该实例作为第一个参数传递，就像以通常方式定义的方法一样。 
`method2()` 未设置为绑定方法，因此必须显式传递 `self` 参数；否则，调用将导致 `TypeError`。


```python
# 3_4_functools_partialmethod.py
import functools


def standalone(self, a=1, b=2):
    """Standalone function"""
    print(' called standalone with:', (self, a, b))
    if self is not None:
        print(' self.attr =', self.attr)


class MyClass:
    """Demonstration class for functools"""

    def __init__(self):
        self.attr = 'instance attribute'

    method1 = functools.partialmethod(standalone)
    method2 = functools.partial(standalone)


o = MyClass()
print('standalone')
standalone(None)
print()

print('method1 as partialmethod')
o.method1()
print()

print('method2 as partial')
try:
    o.method2()
except TypeError as err:
    print('ERROR: {}'.format(err))
```

```text
standalone
 called standalone with: (None, 1, 2)

method1 as partialmethod
 called standalone with: (<__main__.MyClass object at 0x000002A360369F10>, 1, 2)
 self.attr = instance attribute

method2 as partial
ERROR: standalone() missing 1 required positional argument: 'self'

```


#### 3.1.1.5 Acquiring Function Properties for Decorators

> Updating the properties of a wrapped callable is especially useful for decorators, because
the transformed function ends up with properties of the original “bare” function.

更新包装的可调用对象的属性对于装饰器特别有用，因为转换后的函数最终具有原始“裸”函数的属性。

> `functools` provides a decorator, `wraps()`, that applies `update_wrapper()` to the decorated
function.


`functools` provides a decorator, `wraps()`, that applies `update_wrapper()` to the decorated
function.


```python
# 3_5_functools_wraps.py
import functools


def show_details(name, f):
    """Show details of a callable object."""
    print('{}:'.format(name))
    print(' object:', f)
    print(' __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
        print(' __doc__', repr(f.__doc__))
        print()


def simple_decorator(f):
    @functools.wraps(f)
    def decorated(a='decorated defaults', b=1):
        print(' decorated:', (a, b))
        print(' ', end=' ')
        return f(a, b=b)
    return decorated


def myfunc(a, b=2):
    """myfunc() is not complicated"""
    print(' myfunc:', (a, b))
    return


# The raw function
show_details('myfunc', myfunc)
myfunc('unwrapped, default b')
myfunc('unwrapped, passing b', 3)
print()


# Wrap explicitly.
wrapped_myfunc = simple_decorator(myfunc)
show_details('wrapped_myfunc', wrapped_myfunc)
wrapped_myfunc()
wrapped_myfunc('args to wrapped', 4)
print()


# Wrap with decorator syntax.
@simple_decorator
def decorated_myfunc(a, b):
    myfunc(a, b)
    return


show_details('decorated_myfunc', decorated_myfunc)
decorated_myfunc()
decorated_myfunc('args to decorated', 4)

```

```text
myfunc:
 object: <function myfunc at 0x0000024C777CE8B0>
 __name__: myfunc
 myfunc: ('unwrapped, default b', 2)
 myfunc: ('unwrapped, passing b', 3)

wrapped_myfunc:
 object: <function myfunc at 0x0000024C77A051F0>
 __name__: myfunc
 decorated: ('decorated defaults', 1)
   myfunc: ('decorated defaults', 1)
 decorated: ('args to wrapped', 4)
   myfunc: ('args to wrapped', 4)

decorated_myfunc:
 object: <function decorated_myfunc at 0x0000024C77A053A0>
 __name__: decorated_myfunc
 decorated: ('decorated defaults', 1)
   myfunc: ('decorated defaults', 1)
 decorated: ('args to decorated', 4)
   myfunc: ('args to decorated', 4)

```

### 3.1.2 Comparison

> Under Python 2, classes could define a `__cmp__()` method that returns -1, 0, or 1 based
on whether the object is less than, equal to, or greater than, respectively, the item being
compared. Python 2.1 introduced the rich comparison methods API (`__lt__()`, `__le__()`,
`__eq__()`, `__ne__()`, `__gt__()`, and `__ge__()`), which perform a single comparison operation
and return a boolean value. Python 3 deprecated `__cmp__()` in favor of these new methods,
and functools provides tools to make it easier to write classes that comply with the new
comparison requirements in Python 3.

在 Python 2 下，类可以定义一个 `__cmp__()` 方法，该方法根据对象是小于、等于还是大于被比较的项目分别返回 -1、0 或 1。
Python 2.1 引入了丰富的比较方法 API（`__lt__()`、`__le__()`、`__eq__()`、`__ne__()`、`__gt__()` 和 `__ge__()`），它们执行单个比较操作并返回一个布尔值。
Python 3 弃用了 `__cmp__()` 以支持这些新方法，并且 functools 提供的工具可以更轻松地编写符合 Python 3 中新比较要求的类。


#### 3.1.2.1 Rich Comparison

> The rich comparison API is designed to allow classes with complex comparisons to implement
each test in the most efficient way possible. However, for classes where comparison is
relatively simple, there is no point in manually creating each of the rich comparison methods.
The `total_ordering()` class decorator takes a class that provides some of the methods,
and adds the rest of them.

丰富的比较 API 旨在允许具有复杂比较的类以最有效的方式实现每个测试。 但是，对于比较相对简单的类，手动创建每个丰富的比较方法是没有意义的。 
`total_ordering()` 类装饰器接受一个提供一些方法的类，并添加其余的方法。

> The class must provide implementation of `__eq__()` and one other rich comparison
method. The decorator adds implementations of the rest of the methods that work by using
the comparisons provided. If a comparison cannot be made, the method should return
`NotImplemented` so the comparison can be tried using the reverse comparison operators on
the other object, before failing entirely.

该类必须提供`__eq__()` 和另一种丰富的比较方法的实现。装饰器通过使用提供的比较来添加其余方法的实现。
如果无法进行比较，则该方法应返回`NotImplemented`，以便在完全失败之前可以在另一个对象上使用反向比较运算符尝试进行比较。

```python
# 3_6_functools_total_ordering.py

import functools
import inspect
from pprint import pprint


@functools.total_ordering
class MyObject:

    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        print(' testing __eq__({}, {})'.format(self.val, other.val))
        return self.val == other.val

    def __gt__(self, other):
        print(' testing __gt__({}, {})'.format(self.val, other.val))
        return self.val > other.val


print('Methods:\n')
pprint(inspect.getmembers(MyObject, inspect.isfunction))

a = MyObject(1)
b = MyObject(2)

print('\nComparisons:')
for expr in ['a < b', 'a <= b', 'a == b', 'a >= b', 'a > b']:
    print('\n{:<6}:'.format(expr))
    result = eval(expr)
    print(' result of {}: {}'.format(expr, result))
```

```text
[('__eq__', <function MyObject.__eq__ at 0x000002985BA60550>),
 ('__ge__', <function _ge_from_gt at 0x000002985B96B160>),
 ('__gt__', <function MyObject.__gt__ at 0x000002985BA605E0>),
 ('__init__', <function MyObject.__init__ at 0x000002985BA55E50>),
 ('__le__', <function _le_from_gt at 0x000002985B96B1F0>),
 ('__lt__', <function _lt_from_gt at 0x000002985B96B0D0>)]

Comparisons:

a < b :
 testing __gt__(1, 2)
 testing __eq__(1, 2)
 result of a < b: True

a <= b:
 testing __gt__(1, 2)
 result of a <= b: True

a == b:
 testing __eq__(1, 2)
 result of a == b: False

a >= b:
 testing __gt__(1, 2)
 testing __eq__(1, 2)
 result of a >= b: False

a > b :
 testing __gt__(1, 2)
 result of a > b: False
```


#### 3.1.2.2 Collation Order

> Since old-style comparison functions are deprecated in Python 3, the `cmp` argument to
functions like `sort()` is also no longer supported. Older programs that use comparison
functions can use `cmp_to_key()` to convert them to a function that returns a `collation key`,
which is used to determine the position in the final sequence.

由于旧式比较函数在 Python 3 中已弃用，因此也不再支持像 `sort()` 这样的函数的 `cmp` 参数。
使用比较函数的旧程序可以使用 `cmp_to_key()` 将它们转换为返回 `collat​​ion key` 的函数，用于确定最终序列中的位置


> Normally `cmp_to_key()` would be used directly, but in this example an extra wrapper
function is introduced to print out more information as the key function is being called.
 
通常会直接使用 `cmp_to_key()`，但在这个例子中，引入了一个额外的包装函数来在调用 key 函数时打印出更多信息。

> The output shows that `sorted()` starts by calling `get_key_wrapper()` for each item
in the sequence to produce a key. The keys returned by `cmp_to_key()` are instances of a
class defined in `functools` that implements the rich comparison API using the old-style
comparison function passed in. After all of the keys are created, the sequence is sorted by
comparing the keys.

输出显示`sorted()`首先为序列中的每个项目调用`get_key_wrapper()`以生成一个键。 
`cmp_to_key()` 返回的键是 `functools` 中定义的类的实例，该类使用传入的旧式比较函数实现了丰富的比较 API。
创建所有键后，通过比较键对序列进行排序。

```python
# 3_6_functools_cmp_to_key.py
import functools


class MyObject:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return 'MyObject({})'.format(self.val)


def compare_obj(a, b):
    """Old-style comparison function."""
    print('comparing {} and {}'.format(a, b))
    if a.val < b.val:
        return -1
    elif a.val > b.val:
        return 1
    return 0


# Make a key function using cmp_to_key().
get_key = functools.cmp_to_key(compare_obj)


def get_key_wrapper(o):
    """Wrapper function for get_key to allow for print statements."""
    new_key = get_key(o)
    print('key_wrapper({}) -> {!r}'.format(o, new_key))
    return new_key


objs = [MyObject(x) for x in range(5, 0, -1)]

for o in sorted(objs, key=get_key_wrapper):
    print(o)

```

```text
key_wrapper(MyObject(5)) -> <functools.KeyWrapper object at 0x000001A1DBF9CE90>
key_wrapper(MyObject(4)) -> <functools.KeyWrapper object at 0x000001A1DBF9CE70>
key_wrapper(MyObject(3)) -> <functools.KeyWrapper object at 0x000001A1DBF9CCB0>
key_wrapper(MyObject(2)) -> <functools.KeyWrapper object at 0x000001A1DBF9CC90>
key_wrapper(MyObject(1)) -> <functools.KeyWrapper object at 0x000001A1DBF9CE50>
comparing MyObject(4) and MyObject(5)
comparing MyObject(3) and MyObject(4)
comparing MyObject(2) and MyObject(3)
comparing MyObject(1) and MyObject(2)
MyObject(1)
MyObject(2)
MyObject(3)
MyObject(4)
MyObject(5)
```



### 3.1.3 Caching

> The `lru_cache()` decorator wraps a function in a “least recently used” cache. Arguments to
the function are used to build a hash key, which is then mapped to the result. Subsequent
calls with the same arguments will fetch the value from the cache instead of calling the
function. The decorator also adds methods to the function to examine the state of the
cache (`cache_info()`) and empty the cache (`cache_clear()`).
 
`lru_cache()` 装饰器将函数包装在“最近最少使用”缓存中。 该函数的参数用于构建哈希键，然后将其映射到结果。
具有相同参数的后续调用将从缓存中获取值，而不是调用该函数。 装饰器还向函数添加了检查缓存状态（`cache_info()`）和清空缓存（`cache_clear()`）的方法。

> This example makes several calls to `expensive()` in a set of nested loops. The second
time those calls are made with the same values, the results appear in the cache. When the
cache is cleared and the loops are run again, the values must be recomputed.
 
此示例在一组嵌套循环中多次调用 `expensive()`。 第二次使用相同的值进行这些调用时，结果出现在缓存中。
当缓存被清除并再次运行循环时，必须重新计算这些值。

```python
# 3_7_functools_lru_cache.py
import functools


@functools.lru_cache()
def expensive(a, b):
    print('expensive({}, {})'.format(a, b))
    return a * b

MAX = 2

print('First set of calls:')
for i in range(MAX):
    for j in range(MAX):
        expensive(i, j)
print(expensive.cache_info())

print('\nSecond set of calls:')
for i in range(MAX + 1):
    for j in range(MAX + 1):
        expensive(i, j)
print(expensive.cache_info())

print('\nClearing cache:')
expensive.cache_clear()
print(expensive.cache_info())

print('\nThird set of calls:')
for i in range(MAX):
    for j in range(MAX):
        expensive(i, j)
print(expensive.cache_info())
```


```text
First set of calls:
expensive(0, 0)
expensive(0, 1)
expensive(1, 0)
expensive(1, 1)
CacheInfo(hits=0, misses=4, maxsize=128, currsize=4)

Second set of calls:
expensive(0, 2)
expensive(1, 2)
expensive(2, 0)
expensive(2, 1)
expensive(2, 2)
CacheInfo(hits=4, misses=9, maxsize=128, currsize=9)

Clearing cache:
CacheInfo(hits=0, misses=0, maxsize=128, currsize=0)

Third set of calls:
expensive(0, 0)
expensive(0, 1)
expensive(1, 0)
expensive(1, 1)
CacheInfo(hits=0, misses=4, maxsize=128, currsize=4)

Process finished with exit code 0

```

> To prevent the cache from growing without bounds in a long-running process, it is given
a maximum size. The default is 128 entries, but that size can be changed for each cache
using the `maxsize` argument.

为了防止缓存在长时间运行的进程中无限增长，它被赋予了最大大小。 默认值为 128 个条目，但可以使用 `maxsize` 参数为每个缓存更改该大小。