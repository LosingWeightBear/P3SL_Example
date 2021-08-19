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

> In this example, the cache size is set to 2 entries. When the third set of unique arguments
(3,4) is used, the oldest item in the cache is dropped and replaced with the new
result.

在此示例中，缓存大小设置为 2 个条目。 当使用第三组唯一参数 (3,4) 时，缓存中最旧的项目将被删除并替换为新结果。

```python
import functools


@functools.lru_cache(maxsize=2)
def expensive(a, b):
    print('called expensive({}, {})'.format(a, b))
    return a * b


def make_call(a, b):
    print('({}, {})'.format(a, b), end=' ')
    pre_hits = expensive.cache_info().hits
    expensive(a, b)
    post_hits = expensive.cache_info().hits
    if post_hits > pre_hits:
        print('cache hit')


print('Establish the cache')
make_call(1, 2)
make_call(2, 3)

print('\nUse cached items')
make_call(1, 2)
make_call(2, 3)

print('\nCompute a new value, triggering cache expiration')
make_call(3, 4)

print('\nCache still contains one old item')
make_call(2, 3)

print('\nOldest item needs to be recomputed')
make_call(1, 2)

```

```text
Establish the cache
(1, 2) called expensive(1, 2)
(2, 3) called expensive(2, 3)

Use cached items
(1, 2) cache hit
(2, 3) cache hit

Compute a new value, triggering cache expiration
(3, 4) called expensive(3, 4)

Cache still contains one old item
(2, 3) cache hit

Oldest item needs to be recomputed
(1, 2) called expensive(1, 2)

```

> The keys for the cache managed by `lru_cache()` must be hashable, so all of the arguments
to the function wrapped with the cache lookup must be hashable.

`lru_cache()` 管理的缓存的键必须是可散列的，因此用缓存查找包装的函数的所有参数都必须是可散列的。

> If an object that cannot be hashed is passed in to the function, a `TypeError` is raised.

如果将无法散列的对象传递给函数，则会引发“TypeError”。

```python
# 3_10_functools_lru_cache_arguments.py
import functools


@functools.lru_cache(maxsize=2)
def expensive(a, b):
    print('called expensive({}, {})'.format(a, b))
    return a * b


def make_call(a, b):
    print('({}, {})'.format(a, b), end=' ')
    pre_hits = expensive.cache_info().hits
    expensive(a, b)
    post_hits = expensive.cache_info().hits
    if post_hits > pre_hits:
        print('cache hit')


make_call(1, 2)
try:
    make_call([1], 2)
except TypeError as err:
    print('ERROR: {}'.format(err))

try:
    make_call(1, {'2': 'two'})
except TypeError as err:
    print('ERROR: {}'.format(err))

```

```text
(1, 2) called expensive(1, 2)
([1], 2) ERROR: unhashable type: 'list'
(1, {'2': 'two'}) ERROR: unhashable type: 'dict'
```


### 3.1.4 Reducing a Data Set

> The `reduce()` function takes a callable and a sequence of data as input. It produces a
single value as output based on invoking the callable with the values from the sequence and
accumulating the resulting output.

`reduce()` 函数将一个可调用对象和一个数据序列作为输入。它基于使用序列中的值调用可调用对象并累积结果输出来生成单个值作为输出。

> This example adds up the numbers in the input sequence.

本示例将输入序列中的数字相加。

```python
# 3_11_functools_reduce.py
import functools


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


data = range(1, 5)
print(data)
result = functools.reduce(do_reduce, data)
print('result: {}'.format(result))

```


```text
range(1, 5)
do_reduce(1, 2)
do_reduce(3, 3)
do_reduce(6, 4)
result: 10
```


> The optional `initializer` argument is placed at the front of the sequence and processed
along with the other items. This can be used to update a previously computed value with
new inputs.

可选的 `initializer` 参数放置在序列的前面，并与其他项一起处理。 这可用于使用新输入更新先前计算的值。

```python
# 3_12_functools_reduce_initializer.py
import functools


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


data = range(1, 5)
print(data)
result = functools.reduce(do_reduce, data, 99)
print('result: {}'.format(result))

```

```text
range(1, 5)
do_reduce(99, 1)
do_reduce(100, 2)
do_reduce(102, 3)
do_reduce(105, 4)
result: 109
```


> Sequences with a single item automatically reduce to that value when no initializer is
present. Empty lists generate an error, unless an initializer is provided.

当没有初始值设定项时，具有单个项目的序列会自动减少到该值。除非提供初始化程序，否则空列表会产生错误。

> Because the initializer argument serves as a default, but is also combined with the new
values if the input sequence is not empty, it is important to consider carefully whether its
use is appropriate. When it does not make sense to combine the default with new values, it
is better to catch the `TypeError` rather than passing an initializer.

因为初始化参数用作默认值，但如果输入序列不为空，它也会与新值组合，所以仔细考虑它的使用是否合适是很重要的。 
当将默认值与新值结合起来没有意义时，最好捕获 `TypeError` 而不是传递初始值设定项。

```python
# 3_13_functools_reduce_short_sequences.py
import functools


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


print('Single item in sequence:', functools.reduce(do_reduce, [1]))

print('Single item in sequence with initializer:', functools.reduce(do_reduce, [1], 99))

print('Empty sequence with initializer:', functools.reduce(do_reduce, [], 99))

try:
    print('Empty sequence:', functools.reduce(do_reduce, []))
except TypeError as err:
    print('ERROR: {}'.format(err))

```

```text
Single item in sequence: 1
do_reduce(99, 1)
Single item in sequence with initializer: 100
Empty sequence with initializer: 99
ERROR: reduce() of empty sequence with no initial value
```


### 3.1.5 Generic Functions

> In a dynamically typed language like Python, there is often a need to perform slightly
different operations based on the type of an argument, especially when dealing with the
difference between a list of items and a single item. It is simple enough to check the type
of an argument directly, but in cases where the behavioral difference can be isolated into
separate functions, `functools` provides the `singledispatch()` decorator to register a set
of generic functions for automatic switching based on the type of the first argument to a
function.

在像 Python 这样的动态类型语言中，通常需要根据参数的类型执行稍微不同的操作，尤其是在处理项目列表和单个项目之间的差异时。
直接检查参数的类型很简单，但是在行为差异可以隔离到单独的函数中的情况下，
`functools` 提供了 `singledispatch()` 装饰器来注册一组通用函数，用于基于函数的第一个参数的类型。


> The `register()` attribute of the new function serves as another decorator for registering
alternative implementations. The first function wrapped with `singledispatch()` is the
default implementation if no other type-specific function is found, as with the `float` case
in this example.

新函数的 `register()` 属性用作注册替代实现的另一个装饰器。
如果没有找到其他特定于类型的函数，则用 `singledispatch()` 包装的第一个函数是默认实现，如本例中的 `float` 情况。

```python
# 3_14_functools_singledispatch.py
import functools


@functools.singledispatch
def myfunc(arg):
    print('default myfunc({!r})'.format(arg))


@myfunc.register(int)
def myfunc_int(arg):
    print('myfunc_int({})'.format(arg))


@myfunc.register(list)
def myfunc_list(arg):
    print('myfunc_list()')
    for item in arg:
        print(' {}'.format(item))


myfunc('string argument')
myfunc(1)
myfunc(2.3)
myfunc(['a', 'b', 'c'])

```

```text
default myfunc('string argument')
myfunc_int(1)
default myfunc(2.3)
myfunc_list()
 a
 b
 c
```

> When no exact match is found for the type, the inheritance order is evaluated and the
closest matching type is used.

当没有找到完全匹配的类型时，将评估继承顺序并使用最接近的匹配类型。

> In this example, classes D and E do not match exactly with any registered generic functions,
and the function selected depends on the class hierarchy.

在此示例中，类 D 和 E 与任何注册的泛型函数不完全匹配，所选函数取决于类继承结构。


## 3.2 itertools: Iterator Functions



```python
# 3_15_functools_singledispatch_mro.py
import functools


class A:
    pass


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


class E(C, D):
    pass


@functools.singledispatch
def myfunc(arg):
    print('default myfunc({})'.format(arg.__class__.__name__))


@myfunc.register(A)
def myfunc_A(arg):
    print('myfunc_A({})'.format(arg.__class__.__name__))


@myfunc.register(B)
def myfunc_B(arg):
    print('myfunc_B({})'.format(arg.__class__.__name__))


@myfunc.register(C)
def myfunc_C(arg):
    print('myfunc_C({})'.format(arg.__class__.__name__))


myfunc(A())
myfunc(B())
myfunc(C())
myfunc(D())
myfunc(E())

```

```text
myfunc_A(A)
myfunc_B(B)
myfunc_C(C)
myfunc_B(D)
myfunc_C(E)
```

## 3.2 itertools: Iterator Functions

> The `itertools` module includes a set of functions for working with sequence data sets. The
functions provided are inspired by similar features of functional programming languages
such as Clojure, Haskell, APL, and SML. They are intended to be fast and use memory efficiently. 
They can also be hooked together to express more complicated iteration-based algorithms.

`itertools` 模块包括一组用于处理序列数据集的函数。
所提供的函数的灵感来自于函数式编程语言（例如 Clojure、Haskell、APL 和 SML）的类似特性。
它们旨在快速并有效地使用内存。
它们还可以连接在一起以表达更复杂的基于迭代的算法。

> Iterator-based code offers better memory consumption characteristics than code that
uses lists. Since data is not produced from the iterator until it is needed, all of the data
does not need to be stored in memory at the same time. This “lazy” processing model can
reduce swapping and other side effects of large data sets, improving performance.

基于迭代器的代码比使用列表的代码提供更好的内存消耗特性。
由于数据在需要之前不会从迭代器中产生，因此所有数据不需要同时存储在内存中。
这种“惰性”处理模型可以减少大数据集的交换和其他副作用，从而提高性能。

> In addition to the functions defined in `itertools`, the examples in this section rely on
some of the built-in functions for iteration.

除了 `itertools` 中定义的函数，本节中的示例依赖于一些内置函数进行迭代。


### 3.2.1 Merging and Splitting Iterators

> The `chain()` function takes several iterators as arguments and returns a single iterator that
produces the contents of all of the inputs as though they came from a single iterator.

`chain()` 函数将多个迭代器作为参数并返回一个迭代器，该迭代器生成所有输入的内容，就好像它们来自单个迭代器一样。

> `chain()` makes it easy to process several sequences without constructing one large list.

`chain()` 可以很容易地处理多个序列，而无需构建一个大列表。

```python
# 3_16_itertools_chain.py
from itertools import *

for i in chain([1, 2, 3], ['a', 'b', 'c']):
    print(i, end=' ')
print()
```

```text
1 2 3 a b c
```


> If the iterables to be combined are not all known in advance, or if they need to be
evaluated lazily, `chain.from_iterable()` can be used to construct the chain instead.

如果要组合的可迭代对象不是事先知道的，或者需要懒惰地评估它们，则可以使用`chain.from_iterable()` 来构造链。


```python
# 3_17_itertools_chain_from_iterable.py
from itertools import *


def make_iterables_to_chain():
    yield [1, 2, 3]
    yield ['a', 'b', 'c']


for i in chain.from_iterable(make_iterables_to_chain()):
    print(i, end=' ')
print()
```

```text
1 2 3 a b c 

```

> The built-in function `zip()` returns an iterator that combines the elements of several
iterators into tuples.

内置函数 `zip()` 返回一个迭代器，它将多个迭代器的元素组合成元组。

> As with the other functions in this module, the return value is an iterable object that
produces values one at a time.

与此模块中的其他函数一样，返回值是一个可迭代对象，一次生成一个值。

```python
# 3_18_itertools_zip.py
for i in zip([1, 2, 3], ['a', 'b', 'c']):
    print(i)
```

```text
(1, 'a')
(2, 'b')
(3, 'c')
```

> `zip()` stops when the first input iterator is exhausted. To process all of the inputs, even if
the iterators produce different numbers of values, use `zip_longest()`.

zip()` 在第一个输入迭代器耗尽时（就短，长度最小的那个迭代器耗尽）停止。
要处理所有输入，即使迭代器产生不同数量的值，也可以使用 `zip_longest()`。

> By default, `zip_longest()` substitutes `None` for any missing values. Use the `fillvalue`
argument to use a different substitute value.

默认情况下，`zip_longest()` 将 `None` 替换为任何缺失值。
使用 `fillvalue` 参数来使用不同的替代值。

```python
# 3_19_itertools_zip_longest.py
from itertools import *

r1 = range(3)
r2 = range(2)

print('zip stops early:')
print(list(zip(r1, r2)))

r1 = range(3)
r2 = range(2)

print('\nzip_longest processes all of the values:')
print(list(zip_longest(r1, r2)))
print(list(zip_longest(r2, r1)))

```

```text
zip stops early:
[(0, 0), (1, 1)]
[(0, 0), (1, 1)]

zip_longest processes all of the values:
[(0, 0), (1, 1), (2, None)]
[(0, 0), (1, 1), (None, 2)]
```


> The `islice()` function returns an iterator that returns selected items from the input
iterator, by index.

`islice()` 函数返回一个迭代器，该迭代器通过索引从输入迭代器中返回所选项目。

> `islice()` takes the same arguments as the slice operator for lists: `start`, `stop`, and `step`.
The start and step arguments are optional.

`islice()` 与列表的切片操作符采用相同的参数：`start`、`stop` 和 `step`。 
start 和 step 参数是可选的。

```python
# 3_20_itertools_islice.py
from itertools import *

print('Stop at 5:')
for i in islice(range(100), 5):
    print(i, end=' ')
print('\n')

print('Start at 5, Stop at 10:')
for i in islice(range(100), 5, 10):
    print(i, end=' ')
print('\n')

print('By tens to 100:')
for i in islice(range(100), 0, 100, 10):
    print(i, end=' ')
print('\n')

```

```text
Stop at 5:
0 1 2 3 4 

Start at 5, Stop at 10:
5 6 7 8 9 

By tens to 100:
0 10 20 30 40 50 60 70 80 90 
```

> The `tee()` function returns several independent iterators (defaults to 2) based on a single
original input.

`tee()` 函数基于单个原始输入返回多个独立的迭代器（默认为 2）。

> `tee()` has semantics similar to the Unix `tee` utility, which repeats the values it reads from
its input and writes them to a named file and standard output. The iterators returned by
`tee()` can be used to feed the same set of data into multiple algorithms to be processed in
parallel.

`tee()` 的语义类似于 Unix 的 `tee` 实用程序，它重复从其输入读取的值并将它们写入命名文件和标准输出。 
`tee()` 返回的迭代器可用于将同一组数据提供给多个算法进行并行处理。

```python
# 3_21_itertools_tee.py
from itertools import *

r = islice(count(), 5)
i1, i2 = tee(r)
print('i1:', list(i1))
print('i2:', list(i2))
```


```text
i1: [0, 1, 2, 3, 4]
i2: [0, 1, 2, 3, 4]
```


> The new iterators created by `tee()` share their input, so the original iterator should not be
used after the new ones are created.

`tee()` 创建的新迭代器共享它们的输入，因此在创建新迭代器后不应使用原始迭代器。

> If values are consumed from the original input, the new iterators will not produce those
values.

如果从原始输入中使用值，则新迭代器将不会生成这些值。(因为新创建的迭代器共享原始迭代器，原始迭代器的使用会消耗新创建的迭代器)

```python
# 3_22_itertools_tee_error.py
from itertools import *

r = islice(count(), 5)
i1, i2 = tee(r)

print('r:', end=' ')
for i in r:
    print(i, end=' ')
    if i > 1:
        break
print()

print('i1:', list(i1))
print('i2:', list(i2))

```

```text
r: 0 1 2 
i1: [3, 4]
i2: [3, 4]
```

3.2.2 Converting Inputs
输入转换

> The built-in `map()` function returns an iterator that calls a function on the values in the
> input iterators, and returns the results. It stops when any input iterator is exhausted.

内置的 `map()` 函数返回一个迭代器，该迭代器对输入迭代器中的值调用函数，并返回结果。当任何输入迭代器用完时它就会停止。

> In the first example, the lambda function multiplies the input values by 2. In the second 
example, the lambda function multiplies two arguments, taken from separate iterators, and
returns a tuple with the original arguments and the computed value. The third example
stops after producing two tuples because the second range is exhausted.

在第一个示例中，lambda 函数将输入值乘以 2。在第二个示例中，lambda 函数将取自不同迭代器的两个参数相乘，并返回一个包含原始参数和计算值的元组。
第三个示例在生成两个元组后停止，因为第二个范围已用完


```python
# 3_23_itertools_map.py
def times_two(x):
    return 2 * x


def multiply(x, y):
    return x, y, x * y


print('Doubles:')
for i in map(times_two, range(5)):
    print(i)

print('\nMultiples:')
r1 = range(5)
r2 = range(5, 10)
for i in map(multiply, r1, r2):
    print('{:d} * {:d} = {:d}'.format(*i))

print('\nStopping:')
r1 = range(5)
r2 = range(2)
for i in map(multiply, r1, r2):
    print(i)

```


```text
Doubles:
0
2
4
6
8

Multiples:
0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36

Stopping:
(0, 0, 0)
(1, 1, 1)
```


> The `starmap()` function is similar to `map()`, but instead of constructing a tuple from
multiple iterators, it splits up the items in a single iterator as arguments to the mapping
function using the * syntax.

`starmap()` 函数类似于 `map()`，但它不是从多个迭代器构造一个元组，而是使用 * 语法将单个迭代器中的项目拆分为映射函数的参数。

> Where the mapping function to `map()` is called `f(i1,i2)`, the mapping function passed to
`starmap()` is called `f(*i)`.

其中映射到`map()`的函数称为`f(i1,i2)`，传递给`starmap()`的映射函数称为`f(*i)`。

```python
# 3_24_itertools_starmap.py
from itertools import *

values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]

for i in starmap(lambda x, y: (x, y, x * y), values):
    print('{} * {} = {}'.format(*i))

```

```text
0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36
```

### 3.2.3 Producing New Values

> The `count()` function returns an iterator that produces consecutive integers, indefinitely.
The first number can be passed as an argument (the default is zero). There is no upper
bound argument (see the built-in `range()` for more control over the result set).

`count()` 函数返回一个迭代器，它无限期地产生连续的整数。 第一个数字可以作为参数传递（默认为零）。
没有上限参数（请参阅内置 `range()` 以获取对结果集的更多控制）。

> This example stops because the list argument is consumed.

此示例停止，因为列表参数已被消耗。

```python
# 3_25_itertools_count.py
from itertools import *

for i in zip(count(1), ['a', 'b', 'c']):
    print(i)

```


```text
(1, 'a')
(2, 'b')
(3, 'c')
```


> The start and step arguments to `count()` can be any numerical values that can be added
together.

`count()` 的 start 和 step 参数可以是任何可以相加的数值。

> In this example, the start point and steps are `Fraction` objects from the `fraction` module

在这个例子中，起点和步骤是来自分数模块的`fraction`对象。

```python
# 3_26_itertools_count_step.py
import fractions
from itertools import *

start = fractions.Fraction(1, 3)
step = fractions.Fraction(1, 3)

for i in zip(count(start, step), ['a', 'b', 'c']):
    print('{}: {}'.format(*i))

```

```text
1/3: a
2/3: b
1: c
```


> The `cycle()` function returns an iterator that repeats the contents of the arguments it
is given indefinitely. Because it has to remember the entire contents of the input iterator,
it may consume quite a bit of memory if the iterator is long.

`cycle()` 函数返回一个迭代器，它无限期地重复给定参数的内容。
因为它必须记住输入迭代器的全部内容，如果迭代器很长，它可能会消耗相当多的内存。

> A counter variable is used to break out of the loop after a few cycles in this example.

在本例中，计数器变量用于在几个周期后跳出循环。

```python
# 3_27_itertools_cycle.py
from itertools import *

for i in zip(range(7), cycle(['a', 'b', 'c'])):
    print(i)

```

```text
(0, 'a')
(1, 'b')
(2, 'c')
(3, 'a')
(4, 'b')
(5, 'c')
(6, 'a')
```

> The `repeat()` function returns an iterator that produces the same value each time it is
accessed.

`repeat()` 函数返回一个迭代器，每次访问都会产生相同的值

> The iterator returned by `repeat()` keeps returning data forever, unless the optional `times`
argument is provided to limit it.

`repeat()` 返回的迭代器会永远返回数据，除非提供了可选的 `times` 参数来限制它。

```python
# 3_28_itertools_repeat.py
from itertools import *

for i in repeat('over-and-over', 5):
    print(i)

```

```text
over-and-over
over-and-over
over-and-over
over-and-over
over-and-over
```

> It is useful to combine `repeat()` with `zip()` or `map()` when invariant values should be
included with the values from the other iterators.

当不变值应该包含在其他迭代器的值中时，将 `repeat()` 与 `zip()` 或 `map()` 结合起来很有用。

> A counter value is combined with the constant returned by `repeat()` in this example.
 
在此示例中，计数器值与`repeat()`返回的常量相结合。

```python
from itertools import *

for i, s in zip(count(), repeat('over-and-over', 5)):
    print(i, s)

```

```text
0 over-and-over
1 over-and-over
2 over-and-over
3 over-and-over
4 over-and-over

```


> This example uses `map()` to multiply the numbers in the range 0 through 4 by 2.

此示例使用 `map()` 将 0 到 4 范围内的数字乘以 2。

> The `repeat()` iterator does not need to be explicitly limited, since `map()` stops processing
when any of its inputs ends, and the `range()` returns only five elements.

`repeat()` 迭代器不需要明确限制，因为 `map()` 在其任何输入结束时停止处理，并且 `range()` 仅返回五个元素。

```python
# 3_30_itertools_repeat_map.py
from itertools import *

for i in map(lambda x, y: (x, y, x * y), repeat(2), range(5)):
    print('{:d} * {:d} = {:d}'.format(*i))

```

```text
2 * 0 = 0
2 * 1 = 2
2 * 2 = 4
2 * 3 = 6
2 * 4 = 8
```

### 3.2.4 Filtering

> The `dropwhile()` function returns an iterator that produces elements of the input iterator
after a condition becomes false for the first time.

`dropwhile()` 函数返回一个迭代器，该迭代器在条件第一次变为 false 后生成输入迭代器的元素。

> `dropwhile()` does not filter every item of the input. After the condition is false the first
time, all of the remaining items in the input are returned.

```python
# 3_31_itertools_dropwhile.py
from itertools import *


def should_drop(x):
    print('Testing:', x)
    return x < 1


for i in dropwhile(should_drop, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
```

```text
Testing: -1
Testing: 0
Testing: 1
Yielding: 1
Yielding: 2
Yielding: -2
```


> The opposite of `dropwhile()` is `takewhile()`. It returns an iterator that itself returns
items from the input iterator as long as the test function returns true.

`dropwhile()` 的反面是 `takewhile()`。
只要测试函数返回true，它就会返回一个迭代器，该迭代器本身从输入迭代器返回项目。

> As soon as `should_take()` returns false, `takewhile()` stops processing the input.

一旦 `should_take()` 返回 false，`takewhile()` 就会停止处理输入。

```python
# 3_32_itertools_takewhile.py
from itertools import *


def should_take(x):
    print('Testing:', x)
    return x < 2


for i in takewhile(should_take, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)

```

```text
Testing: -1
Yielding: -1
Testing: 0
Yielding: 0
Testing: 1
Yielding: 1
Testing: 2
```


> The built-in function `filter()` returns an iterator that includes only items for which
the test function returns true.

内置函数 `filter()` 返回一个迭代器，它只包含测试函数返回 true 的项目。

> `filter()` differs from `dropwhile()` and `takewhile()` in that every item is tested before it is
returned.

`filter()` 与 `dropwhile()` 和 `takewhile()` 的不同之处在于每个项目在返回之前都经过测试。

这里3_33的代码不需要import模块itertools，与之前来自itertools.py的函数不同，`filter()`函数来自builtins.py

```python
# 3_33_itertools_filter.py
def check_item(x):
    print('Testing:', x)
    return x < 1


for i in filter(check_item, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
```

```text
Testing: -1
Yielding: -1
Testing: 0
Yielding: 0
Testing: 1
Testing: 2
Testing: -2
Yielding: -2
```


> `filterfalse()` returns an iterator that includes only items where the test function
returns false.

`filterfalse()` 返回一个迭代器，它只包含测试函数返回 false 的项目。


> The test expression in `check_item()` is the same, so the results in this example with
`filterfalse()` are the opposite of the results from the previous example.

`check_item()` 中的测试表达式是相同的，所以这个例子中带有 `filterfalse()` 的结果与上一个例子的结果相反。

```python
# 3_34_itertools_filterfalse.py
from itertools import *


def check_item(x):
    print('Testing:', x)
    return x < 1


for i in filterfalse(check_item, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)

```

```text
Testing: -1
Testing: 0
Testing: 1
Yielding: 1
Testing: 2
Yielding: 2
Testing: -2
```


> `compress()` offers another way to filter the contents of an iterable. Instead of calling a
function, it uses the values in another iterable to indicate when to accept a value and when
to ignore it.

`compress()` 提供了另一种过滤可迭代内容的方法。
它不是调用函数，而是使用另一个可迭代对象中的值来指示何时接受值以及何时忽略它。

> The first argument is the data iterable to process. The second argument is a selector iterable
that produces boolean values indicating which elements to take from the data input (a true
value causes the value to be produced; a false value causes it to be ignored).

第一个参数是可迭代处理的数据。
第二个参数是一个可迭代的选择器，它产生布尔值，指示从数据输入中获取哪些元素（真值导致产生该值；假值导致它被忽略）。


```python
# 3_35_itertools_compress.py
from itertools import *

every_third = cycle([False, False, True])
data = range(1, 10)

for i in compress(data, every_third):
    print(i, end=' ')
print()
```

```text
3 6 9

```

