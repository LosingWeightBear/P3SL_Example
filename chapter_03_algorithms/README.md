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

### 3.2.5 Grouping Data

> The `groupby()` function returns an iterator that produces sets of values organized by a
common key. This example illustrates grouping of related values based on an attribute.

`groupby()` 函数返回一个迭代器，该迭代器生成由公共键组织的值集。
此示例说明了基于属性对相关值进行分组。

> The input sequence needs to be sorted on the key value so that the groupings will work
out as expected.

输入序列需要根据键值进行排序，以便按预期进行分组。

```python
# 3_36_itertools_groupby_seq.py
import functools
from itertools import *
import operator
import pprint


@functools.total_ordering
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)


# Create a data set of Point instances.
data = list(map(Point, cycle(islice(count(), 3)), islice(count(), 7)))
print('Data:')
pprint.pprint(data, width=35)
print()

# Try to group the unsorted data based on X values.
print('Grouped, unsorted:')
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
print()

# Sort the data.
data.sort()
print('Sorted:')
pprint.pprint(data, width=35)
print()

# Group the sorted data based on X values.
print('Grouped, sorted:')
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
print()

```

```text
Data:
[(0, 0),
 (1, 1),
 (2, 2),
 (0, 3),
 (1, 4),
 (2, 5),
 (0, 6)]

Grouped, unsorted:
0 [(0, 0)]
1 [(1, 1)]
2 [(2, 2)]
0 [(0, 3)]
1 [(1, 4)]
2 [(2, 5)]
0 [(0, 6)]

Sorted:
[(0, 0),
 (0, 3),
 (0, 6),
 (1, 1),
 (1, 4),
 (2, 2),
 (2, 5)]

Grouped, sorted:
0 [(0, 0), (0, 3), (0, 6)]
1 [(1, 1), (1, 4)]
2 [(2, 2), (2, 5)]


Process finished with exit code 0

```


### 3.2.6 Combining Inputs

> The `accumulate()` function processes the input iterable, passing the nth and n+1st item
to a function and producing the return value instead of either input. The default function
used to combine the two values adds them, so `accumulate()` can be used to produce the
cumulative sum of a series of numerical inputs.


`accumulate()` 函数处理输入可迭代对象，将第 n 项和第 n+1 项传递给函数并生成返回值而不是任一输入。
用于组合两个值的默认函数将它们相加，因此 `accumulate()` 可用于生成一系列数字输入的累积总和。


> When used with a sequence of non-integer values, the results depend on what it means to
“add” two items together. The second example in this script shows that when `accumulate()`
receives a string input, each response is a progressively longer prefix of that string.

当与一系列非整数值一起使用时，结果取决于将两个项目“相加”在一起的含义。
此脚本中的第二个示例显示，当 `accumulate()` 接收字符串输入时，每个响应都是该字符串的逐渐变长的前缀。

```python
# 3_37_itertools_accumulate.py
from itertools import *

print(list(accumulate(range(5))))
print(list(accumulate('abcde')))

```

```text
[0, 1, 3, 6, 10]
['a', 'ab', 'abc', 'abcd', 'abcde']

```

> `accumulate()` may be combined with any other function that takes two input values to
achieve different results.

`accumulate()` 可以与任何其他需要两个输入值的函数结合使用以获得不同的结果。

> This example combines the string values in a way that makes a series of (nonsensical)
palindromes. Each step of the way when `f()` is called, it prints the input values passed to
it by `accumulate()`.

此示例以形成一系列（无意义的）回文的方式组合字符串值。
当`f()` 被调用时，每一步都会打印`accumulate()` 传递给它的输入值。


```python
# 3_38_itertools_accumulate_custom.py
from itertools import *


def f(a, b):
    print(a, b)
    return b + a + b


print(list(accumulate('abcde', f)))

```

```text
a b
bab c
cbabc d
dcbabcd e
['a', 'bab', 'cbabc', 'dcbabcd', 'edcbabcde']

```

> Nested `for` loops that iterate over multiple sequences can often be replaced with
`product()`, which produces a single iterable whose values are the Cartesian product of the
set of input values.

迭代多个序列的嵌套 `for` 循环通常可以替换为 `product()`，它生成一个可迭代对象，其值是输入值集的笛卡尔积


> The values produced by `product()` are tuples, with the members taken from each of
the iterables passed in as arguments in the order they are passed. The first tuple returned
includes the first value from each iterable. The last iterable passed to `product()` is processed
first, followed by the next-to-last, and so on. The result is that the return values are in order
based on the first iterable, then the next iterable, and so on.
In this example, the cards are ordered first by value and then by suit.

`product()` 产生的值是元组，其成员从作为参数传入的每个可迭代对象中获取，并按照它们的传递顺序进行。
返回的第一个元组包含每个可迭代对象的第一个值。
传递给 `product()` 的最后一个可迭代对象首先被处理，然后是倒数第二个，依此类推。
结果是返回值按第一个可迭代对象的顺序排列，然后是下一个可迭代对象，依此类推。

在此示例中，卡片首先按价值排序，然后按花色排序。

```python
# 3_39_itertools_product.py
from itertools import *
import pprint

FACE_CARDS = ('J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')

DECK = list(
    product(
        chain(range(2, 11), FACE_CARDS),
        SUITS,
    )
)

for card in DECK:
    print('{:>2}{}'.format(*card), end=' ')
    if card[1] == SUITS[-1]:
        print()

```

```text
 2H  2D  2C  2S 
 3H  3D  3C  3S 
 4H  4D  4C  4S 
 5H  5D  5C  5S 
 6H  6D  6C  6S 
 7H  7D  7C  7S 
 8H  8D  8C  8S 
 9H  9D  9C  9S 
10H 10D 10C 10S 
 JH  JD  JC  JS 
 QH  QD  QC  QS 
 KH  KD  KC  KS 
 AH  AD  AC  AS 

```


> To change the order of the cards, change the order of the arguments to `product()`.

要更改卡片的顺序，改变`product()`的参数的顺序 。


> The print loop in this example looks for an ace card, instead of the spade suit, and then
adds a newline to break up the output.

此示例中的打印循环查找 ace 卡，而不是黑桃花色，然后添加换行符以拆分输出。

```python
# 3_40_itertools_product_ordering.py
from itertools import *
import pprint

FACE_CARDS = ('J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')

DECK = list(
    product(
        SUITS,
        chain(range(2, 11), FACE_CARDS),
    )
)

for card in DECK:
    print('{:>2}{}'.format(card[1], card[0]), end=' ')
    if card[1] == FACE_CARDS[-1]:
        print()

```


```text
 2H  3H  4H  5H  6H  7H  8H  9H 10H  JH  QH  KH  AH 
 2D  3D  4D  5D  6D  7D  8D  9D 10D  JD  QD  KD  AD 
 2C  3C  4C  5C  6C  7C  8C  9C 10C  JC  QC  KC  AC 
 2S  3S  4S  5S  6S  7S  8S  9S 10S  JS  QS  KS  AS 
 
```


> To compute the product of a sequence with itself, specify how many times the input should
be repeated.

要计算序列与其自身的乘积，请指定应重复输入的次数。

> Since repeating a single iterable is like passing the same iterable multiple times, each tuple
produced by `product()` will contain a number of items equal to the repeat counter.

由于重复单个迭代就像多次传递相同的迭代，“product()”生成的每个元组将包含与重复计数器相等的项目数。

```python
# 3_41_itertools_product_repeat.py
from itertools import *


def show(iterable):
    for i, item in enumerate(iterable, 1):
        print(item, end=' ')
        if (i % 3) == 0:
            print()
    print()


print('Repeat 2:\n')
show(list(product(range(3), repeat=2)))

print('Repeat 3:\n')
show(list(product(range(3), repeat=3)))

```

```text
Repeat 2:

(0, 0) (0, 1) (0, 2) 
(1, 0) (1, 1) (1, 2) 
(2, 0) (2, 1) (2, 2) 

Repeat 3:

(0, 0, 0) (0, 0, 1) (0, 0, 2) 
(0, 1, 0) (0, 1, 1) (0, 1, 2) 
(0, 2, 0) (0, 2, 1) (0, 2, 2) 
(1, 0, 0) (1, 0, 1) (1, 0, 2) 
(1, 1, 0) (1, 1, 1) (1, 1, 2) 
(1, 2, 0) (1, 2, 1) (1, 2, 2) 
(2, 0, 0) (2, 0, 1) (2, 0, 2) 
(2, 1, 0) (2, 1, 1) (2, 1, 2) 
(2, 2, 0) (2, 2, 1) (2, 2, 2) 

```


> The `permutations()` function produces items from the input iterable combined in the
possible permutations of the given length. It defaults to producing the full set of all permutations.

`permutations()` 函数从输入迭代中生成项目，该输入迭代组合在给定长度的可能排列中。
它默认生成所有排列的完整集合。

> Use the `r` argument to limit the length and number of the individual permutations returned.

使用 `r` 参数来限制返回的单个排列的长度和数量。

```python
# 3_42_itertools_permutations.py
from itertools import *


def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('All permutations:\n')
show(permutations('abcd'))

print('\nPairs:\n')
show(permutations('abcd', r=2))

```


```text
All permutations:

abcd abdc acbd acdb adbc adcb 
bacd badc bcad bcda bdac bdca 
cabd cadb cbad cbda cdab cdba 
dabc dacb dbac dbca dcab dcba 

Pairs:

ab ac ad 
ba bc bd 
ca cb cd 
da db dc 

```


> To limit the values to unique combinations rather than permutations, use
`combinations()`. As long as the members of the input are unique, the output will not
include any repeated values.

要将值限制为唯一组合而不是排列，请使用`combinations()`。
只要输入的成员是唯一的，输出就不会包含任何重复的值。

> Unlike with permutations, the `r` argument to `combinations()` is required.

与排列不同，`combinations()` 的 `r` 参数是必需的。

```python
# 3_43_itertools_combinations.py
from itertools import *


def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('Unique pairs:\n')
show(combinations('abcd', r=2))

```

```text
Unique pairs:

ab ac ad 
bc bd 
cd 

```


> While `combinations()` does not repeat individual input elements, sometimes it is useful
to consider combinations that do include repeated elements. For those cases, use
`combinations_with_replacement()`.

虽然`combinations()` 不会重复单个输入元素，但有时考虑包含重复元素的组合是有用的。
对于这些情况，请使用`combinations_with_replacement()`。

> In this output, each input item is paired with itself as well as all of the other members of
the input sequence.

在此输出中，每个输入项与其自身以及输入序列的所有其他成员配对。

```python
# 3_44_itertools_combinations_with_replacement.py
from itertools import *


def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('Unique pairs:\n')
show(combinations_with_replacement('abcd', r=2))

```

```text
Unique pairs:

aa ab ac ad 
bb bc bd 
cc cd 
dd 

```

## 3.3 operator: Functional Interface to Built-In Operators

> Programming using iterators occasionally requires creating small functions for simple
expressions. Sometimes, these can be implemented as `lambda` functions, but for some
operations new functions are not needed at all. The `operator` module defines functions that
correspond to the built-in arithmetic, comparison, and other operations for the standard
object APIs.

使用迭代器编程有时需要为简单表达式创建小函数。
有时，这些可以实现为 `lambda` 函数，但对于某些操作，根本不需要新函数。
`operator` 模块定义了与标准对象 API 的内置算术、比较和其他操作相对应的函数。


### 3.3.1 Logical Operations

> Functions are provided for determining the boolean equivalent for a value, negating a value
to create the opposite boolean value, and comparing objects to see if they are identical.

提供了用于确定值的布尔等效值、否定值以创建相反的布尔值以及比较对象以查看它们是否相同的函数。

> `not_()` includes a trailing underscore because `not` is a Python keyword. `truth()` applies
the same logic used when testing an expression in an `if` statement or converting an expression
to a `bool. is_()` implements the same check used by the `is` keyword, and `is_not()`
does the same test and returns the opposite answer.

`not_()` 包含一个尾随下划线，因为 `not` 是一个 Python 关键字。
`truth()` 应用在测试 `if` 语句中的表达式或将表达式转换为 `bool 时使用的相同逻辑。
is_()` 实现了与 `is` 关键字使用的相同的检查，而 `is_not()` 执行相同的测试并返回相反的答案。


```python
# 3_45_operator_boolean.py
from operator import *


a = -1
b = 5

print('a =', a)
print('b =', b)
print()

print('not_(a) :', not_(a))
print('truth(a) :', truth(a))
print('is_(a, b) :', is_(a, b))
print('is_not(a, b):', is_not(a, b))

```

```text
a = -1
b = 5

not_(a) : False
truth(a) : True
is_(a, b) : False
is_not(a, b): True

```

### 3.3.2 Comparison Operators

> All of the rich comparison operators are supported.

支持所有丰富的比较运算符。

> The functions are equivalent to the expression syntax using <, <=, ==, >=, and >.

这些函数等效于使用 <、<=、==、>= 和 > 的表达式语法。


```python
# 3_46_operator_comparisons.py
from operator import *

a = 1
b = 5.0

print('a =', a)
print('b =', b)
for func in (lt, le, eq, ne, ge, gt):
    print('{}(a, b): {}'.format(func.__name__, func(a, b)))

```

```text
a = 1
b = 5.0
lt(a, b): True
le(a, b): True
eq(a, b): False
ne(a, b): True
ge(a, b): False
gt(a, b): False

```


### 3.3.3 Arithmetic Operators

> The arithmetic operators for manipulating numerical values are also supported.

支持操作数值的算术运算符。

> Two different division operators are provided: `floordiv()` (integer division as implemented
in Python before version 3.0) and `truediv()` (floating-point division).

提供了两种不同的除法运算符：`floordiv()`（在 Python 3.0 之前版本中实现的整数除法）和 `truediv()`（浮点除法）。


```python
# 3_47_operator_math.py
from operator import *

a = -1
b = 5.0
c = 2
d = 6

print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)

print('\nPositive/Negative:')
print('abs(a):', abs(a))
print('neg(a):', neg(a))
print('neg(b):', neg(b))
print('pos(a):', pos(a))
print('pos(b):', pos(b))

print('\nArithmetic:')
print('add(a, b) :', add(a, b))
print('floordiv(a, b):', floordiv(a, b))
print('floordiv(d, c):', floordiv(d, c))
print('mod(a, b) :', mod(a, b))
print('mul(a, b) :', mul(a, b))
print('pow(c, d) :', pow(c, d))
print('sub(b, a) :', sub(b, a))
print('truediv(a, b) :', truediv(a, b))
print('truediv(d, c) :', truediv(d, c))

print('\nBitwise:')
print('and_(c, d) :', and_(c, d))
print('invert(c) :', invert(c))
print('lshift(c, d):', lshift(c, d))
print('or_(c, d) :', or_(c, d))
print('rshift(d, c):', rshift(d, c))
print('xor(c, d) :', xor(c, d))
```

```text
a = -1
b = 5.0
c = 2
d = 6

Positive/Negative:
abs(a): 1
neg(a): 1
neg(b): -5.0
pos(a): -1
pos(b): 5.0

Arithmetic:
add(a, b) : 4.0
floordiv(a, b): -1.0
floordiv(d, c): 3
mod(a, b) : 4.0
mul(a, b) : -5.0
pow(c, d) : 64
sub(b, a) : 6.0
truediv(a, b) : -0.2
truediv(d, c) : 3.0

Bitwise:
and_(c, d) : 2
invert(c) : -3
lshift(c, d): 128
or_(c, d) : 6
rshift(d, c): 1
xor(c, d) : 4
```


### 3.3.4 Sequence Operators

> The operators for working with sequences can be organized into four groups: building
up sequences, searching for items, accessing contents, and removing items from
sequences.

处理序列的操作符可以分为四组：建立序列、搜索项目、访问内容和从序列中删除项目。

> Some of these operations, such as s`etitem()` and `delitem()`, modify the sequence in
place and do not return a value.

其中一些操作，例如 s`etitem()` 和 `delitem()`，就地修改序列并且不返回值。


```python
# 3_48_operator_sequences.py
from operator import *

a = [1, 2, 3]
b = ['a', 'b', 'c']

print('a =', a)
print('b =', b)

print('\nConstructive:')
print(' concat(a, b):', concat(a, b))

print('\nSearching:')
print(' contains(a, 1)  :', contains(a, 1))
print(' contains(b, "d"):', contains(b, "d"))
print(' countOf(a, 1)   :', countOf(a, 1))
print(' countOf(b, "d") :', countOf(b, "d"))
print(' indexOf(a, 5)   :', indexOf(a, 1))

print('\nAccess Items:')
print(' getitem(b, 1)                  :', getitem(b, 1))
print(' getitem(b, slice(1, 3))        :', getitem(b, slice(1, 3)))

print(' setitem(b, 1, "d")             :', end=' ')
setitem(b, 1, "d")
print(b)
print(' setitem(a, slice(1, 3), [4, 5]):', end=' ')
setitem(a, slice(1, 3), [4, 5])
print(a)

print('\nDestructive:')
print(' delitem(b, 1)          :', end=' ')
delitem(b, 1)
print(b)
print(' delitem(a, slice(1, 3)):', end=' ')
delitem(a, slice(1, 3))
print(a)

```

```text
a = [1, 2, 3]
b = ['a', 'b', 'c']

Constructive:
 concat(a, b): [1, 2, 3, 'a', 'b', 'c']

Searching:
 contains(a, 1)  : True
 contains(b, "d"): False
 countOf(a, 1)   : 1
 countOf(b, "d") : 0
 indexOf(a, 5)   : 0

Access Items:
 getitem(b, 1)                  : b
 getitem(b, slice(1, 3))        : ['b', 'c']
 setitem(b, 1, "d")             : ['a', 'd', 'c']
 setitem(a, slice(1, 3), [4, 5]): [1, 4, 5]

Destructive:
 delitem(b, 1)          : ['a', 'c']
 delitem(a, slice(1, 3)): [1]

```



### 3.3.5 In-Place Operators

> In addition to the standard operators, many types of objects support “in-place” modification
through special operators such as +=. Equivalent functions are available for in-place
modifications as well.

除了标准运算符之外，许多类型的对象都支持通过特殊运算符（例如 +=）进行“就地”修改。
等效函数也可用于就地修改。

> These examples demonstrate just a few of the functions. Refer to the standard library
documentation for complete details.

这些示例仅演示了其中的几个功能。
有关完整的详细信息，请参阅标准库文档。


```python
# 3_49_operator_inplace.py
from operator import *

a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']
print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)
print()

a = iadd(a, b)
print('a = iadd(a, b) =>', a)
print()

c = iconcat(c, d)
print('c = iconcat(c, d) =>', c)
```


```text
a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']

a = iadd(a, b) => 4.0

c = iconcat(c, d) => [1, 2, 3, 'a', 'b', 'c']

```


### 3.3.6 Attribute and Item "Getters"

> One of the most unusual features of the `operator` module is the concept of getters. These
callable objects are constructed at runtime and retrieve attributes of objects or contents from
sequences. Getters are especially useful when working with iterators or generator sequences,
as they incur less overhead than a `lambda` or Python function.

`operator` 模块最不寻常的特性之一是 getter 的概念。
这些可调用对象是在运行时构造的，并从序列中检索对象或内容的属性。
Getter 在使用迭代器或生成器序列时特别有用，因为它们比 `lambda` 或 Python 函数产生更少的开销。

> Attribute getters work like `lambda x,n='attrname': getattr(x,n):`


```python
# 3_50_operator_attrgetter.py
from operator import *


class MyObj:
    """example class for attrgetter"""

    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def __repr__(self):
        return 'MyObj({})'.format(self.arg)


l = [MyObj(i) for i in range(5)]
print('objects :', l)
# Extract the 'arg' value from each object.
g = attrgetter('arg')
vals = [g(i) for i in l]
print('arg values:', vals)
# Sort using arg.
l.reverse()
print('reversed :', l)
print('sorted :', sorted(l, key=g))


```


```text
objects : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
arg values: [0, 1, 2, 3, 4]
reversed : [MyObj(4), MyObj(3), MyObj(2), MyObj(1), MyObj(0)]
sorted : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
```


> Item getters work like `lambda x,y=5: x[y]:`


> Item getters work with mappings as well as sequences.

可以处理映射和序列


```python
# 3_51_operator_itemgetter.py
from operator import *

l = [dict(val=-1 * i) for i in range(4)]
print('Dictionaries:')
print(' original:', l)
g = itemgetter('val')
vals = [g(i) for i in l]
print(' values:', vals)
print(' sorted:', sorted(l, key=g))

print
l = [(i, i * -2) for i in range(4)]
print('\nTuples:')
print(' original:', l)
g = itemgetter(1)
vals = [g(i) for i in l]
print(' values:', vals)
print(' sorted:', sorted(l, key=g))

```

```text
Dictionaries:
 original: [{'val': 0}, {'val': -1}, {'val': -2}, {'val': -3}]
 values: [0, -1, -2, -3]
 sorted: [{'val': -3}, {'val': -2}, {'val': -1}, {'val': 0}]

Tuples:
 original: [(0, 0), (1, -2), (2, -4), (3, -6)]
 values: [0, -2, -4, -6]
 sorted: [(3, -6), (2, -4), (1, -2), (0, 0)]

```


### 3.3.7 Combining Operators and Custom Classes

> The functions in the `operator` module work via the standard Python interfaces when performing
their operations. Thus, they work with user-defined classes as well as the built-in
types.

`operator` 模块中的函数在执行操作时通过标准 Python 接口工作。
因此，它们可以使用用户定义的类以及内置类型。


> Refer to the Python reference guide for a complete list of the special methods used by
each operator.

有关每个运算符使用的特殊方法的完整列表，请参阅 Python 参考指南。

```python
# 3_52_operator_classes.py
from operator import *


class MyObj:
    """Example for operator overloading"""

    def __init__(self, val):
        super(MyObj, self).__init__()
        self.val = val

    def __str__(self):
      return 'MyObj({})'.format(self.val)

    def __lt__(self, other):
        """compare for less-than"""
        print('Testing {} < {}'.format(self, other))
        return self.val < other.val

    def __add__(self, other):
        """add values"""
        print('Adding {} + {}'.format(self, other))
        return MyObj(self.val + other.val)


a = MyObj(1)
b = MyObj(2)

print('Comparison:')
print(lt(a, b))

print('\nArithmetic:')
print(add(a, b))
```


```text
Comparison:
Testing MyObj(1) < MyObj(2)
True

Arithmetic:
Adding MyObj(1) + MyObj(2)
MyObj(3)

```


## 3.4 contextlib: Context Manager Utilities

> The `contextlib` module contains utilities for working `with` context managers and the with
statement.

`contextlib` 模块包含用于处理上下文管理器和 `with` 语句的实用程序。


### 3.4.1 Context Manager API

> A `context` manager is responsible for a resource within a code block, possibly creating it
when the block is entered and then cleaning it up after the block is exited. For example, files
support the context manager API, which ensures that the files are closed after all reading
or writing is done.

`context` 管理器负责代码块中的资源，可能在进入该块时创建它，然后在退出该块后清理它。
例如，文件支持上下文管理器 API，它确保在所有读取或写入完成后关闭文件。

```python
# with open('/tmp/pymotw.txt', 'wt') as f:
# below works for Windows
with open('C:/tmp/pymotw.txt', 'wt') as f:
    f.write('contents go here')
# File is automatically closed

```

> A context manager is enabled by the `with` statement, and the API involves two methods.
The `__enter__()` method is run when execution flow enters the code block inside the `with`
statement. It returns an object to be used within the context. When execution flow leaves
the `with` block, the `__exit__()` method of the context manager is called to clean up any
resources that were used.

上下文管理器由 `with` 语句启用，API 涉及两种方法。
`__enter__()` 方法在执行流程进入 `with` 语句内的代码块时运行。
它返回要在上下文中使用的对象。
当执行流程离开 `with` 块时，会调用上下文管理器的 `__exit__()` 方法来清理任何使用过的资源。

> Combining a context manager and the `with` statement is a more compact way of writing
a `try:finally` block, since the context manager’s `__exit__()` method is always called, even
if an exception is raised.

结合上下文管理器和 `with` 语句是编写 `try:finally` 块的更紧凑的方式，因为上下文管理器的 `__exit__()` 方法总是被调用，即使引发异常。

```python
# 3_54_contexlib_api.py
class Context:

    def __init__(self):
        print('__init__()')

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')


with Context():
    print('Doing work in the context')

```

```text
__init__()
__enter__()
Doing work in the context
__exit__()

```


> The `__enter__()` method can return any object to be associated with a name specified
in the `as` clause of the `with` statement. In this example, the `Context` returns an object that
uses the open context.

`__enter__()` 方法可以返回与 `with` 语句的 `as` 子句中指定的名称相关联的任何对象。
在这个例子中，`Context` 返回一个使用开放上下文的对象。

> The value associated with the variable c is the object returned by `__enter__()`, which is
not necessarily the `Context` instance created in the `with` statement.

与变量 c 关联的值是 `__enter__()` 返回的对象，它不一定是 `with` 语句中创建的 `Context` 实例。


```python
# 3_55_contextlib_api_other_object.py
class WithinContext:

    def __init__(self, context):
        print('WithinContext.__init__({})'.format(context))

    def do_something(self):
        print('WithinContext.do_something()')

    def __del__(self):
        print('WithinContext.__del__')


class Context:

    def __init__(self):
        print('Context.__init__()')

    def __enter__(self):
        print('Context.__enter__()')
        return WithinContext(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Context.__exit__()')


with Context() as c:
    c.do_something()

```


```text
Context.__init__()
Context.__enter__()
WithinContext.__init__(<__main__.Context object at 0x000001D4FD609FD0>)
WithinContext.do_something()
Context.__exit__()
WithinContext.__del__

```


> The `__exit__()` method receives arguments containing details of any exception raised
in the `with` block.

`__exit__()` 方法接收包含 `with` 块中引发的任何异常的详细信息的参数。


> If the context manager can handle the exception, `__exit__()` should return a true value
to indicate that the exception does not need to be propagated. Returning a false value
causes the exception to be raised again after `__exit__()` returns.

如果上下文管理器可以处理异常，`__exit__()` 应该返回一个真值以指示不需要传播异常。
返回 false 值会导致在 `__exit__()` 返回后再次引发异常。

```python
# 3_56_contextlib_api_error.py
class Context:

    def __init__(self, handle_error):
        print('__init__({})'.format(handle_error))
        self.handle_error = handle_error

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')
        print(' exc_type =', exc_type)
        print(' exc_val =', exc_val)
        print(' exc_tb =', exc_tb)
        return self.handle_error


with Context(True):
    raise RuntimeError('error message handled')

print()

with Context(False):
    raise RuntimeError('error message propagated')
```

```text
__init__(True)
__enter__()
__exit__()
 exc_type = <class 'RuntimeError'>
 exc_val = error message handled
 exc_tb = <traceback object at 0x00000162C77B6980>

__init__(False)
__enter__()
__exit__()
 exc_type = <class 'RuntimeError'>
 exc_val = error message propagated
 exc_tb = <traceback object at 0x00000162C7100B80>
Traceback (most recent call last):
  File "C:\Users\ABCX1C\MyProjects\P3SL_Example\chapter_03_algorithms\section_3_4_contextlib\3_56_contextlib_api_error.py", line 25, in <module>
    raise RuntimeError('error message propagated')
RuntimeError: error message propagated
```



### 3.4.2 Context Managers as Function Decorators

> The class `ContextDecorator` adds support to regular context manager classes so that they
can be used as function decorators as well as context managers.

类 ContextDecorator 增加了对常规上下文管理器类的支持，以便它们可以用作函数装饰器和上下文管理器。

> One difference that arises when using the context manager as a decorator is that the
value returned by `__enter__()` is not available inside the function being decorated, unlike the
case when `with` and `as` are used. Arguments passed to the decorated function are available
in the usual way.

使用上下文管理器作为装饰器时出现的一个区别是，`__enter__()` 返回的值在被装饰的函数内不可用，这与使用 `with` 和 `as` 的情况不同。
传递给装饰函数的参数以通常的方式可用。


```python
# 3_57_contexlib_decorator.py
import contextlib


class Context(contextlib.ContextDecorator):

    def __init__(self, how_used):
        self.how_used = how_used
        print('__init__({})'.format(how_used))

    def __enter__(self):
        print('__enter__({})'.format(self.how_used))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({})'.format(self.how_used))


@Context('as decorator')
def func(message):
    print(message)


print()

with Context('as context manager'):
    print('Doing work in the context')

print()
func('Doing work in the wrapped function')
```

```text
__init__(as decorator)

__init__(as context manager)
__enter__(as context manager)
Doing work in the context
__exit__(as context manager)

__enter__(as decorator)
Doing work in the wrapped function
__exit__(as decorator)

```



### 3.4.3 From Generator to Context Manager

> Creating context managers the traditional way—that is, by writing a class with `__enter__()`
and `__exit__()` methods—is not difficult. Nevertheless, writing everything out fully creates
extra overhead when only a trivial bit of context is being managed. In those sorts of situations,
the best approach is to use the `contextmanager()` decorator to convert a generator
function into a context manager.

以传统方式创建上下文管理器——也就是说，通过使用 `__enter__()` 和 `__exit__()` 方法编写一个类——并不困难。
然而，当只管理一小部分上下文时，将所有内容完全写出来会产生额外的开销。
在这种情况下，最好的方法是使用 `contextmanager()` 装饰器将生成器函数转换为上下文管理器。

> The generator should initialize the context, invoke yield exactly one time, and then clean
up the context. The value yielded, if any, is bound to the variable in the `as` clause of the `with`
statement. Exceptions from within the `with` block are raised again inside the generator, so
they can be handled there.

生成器应该初始化上下文，只调用一次 yield，然后清理上下文。
产生的值（如果有）绑定到 `with` 语句的 `as` 子句中的变量。
`with` 块中的异常在生成器中再次引发，因此它们可以在那里处理。

```python
# 3_58_contextlib_contextmanager.py
import contextlib


@contextlib.contextmanager
def make_context():
    print(' entering')
    try:
        yield {}
    except RuntimeError as err:
        print(' ERROR:', err)
    finally:
        print(' exiting')


print('Normal:')
with make_context() as value:
    print(' inside with statement:', value)

print('\nHandled error:')
with make_context() as value:
    raise RuntimeError('showing example of handling an error')

print('\nUnhandled error:')
with make_context() as value:
    raise ValueError('this exception is not handled')

```


```text
Normal:
 entering
 inside with statement: {}
 exiting

Handled error:
 entering
 ERROR: showing example of handling an error
 exiting

Unhandled error:
 entering
 exiting
Traceback (most recent call last):
  File "C:\Users\ABCX1C\MyProjects\P3SL_Example\chapter_03_algorithms\section_3_4_contextlib\3_58_contextlib_contextmanager.py", line 25, in <module>
    raise ValueError('this exception is not handled')
ValueError: this exception is not handled

```


> The context manager returned by `contextmanager()` is derived from `ContextDecorator`,
so it also works as a function decorator.

`contextmanager()` 返回的上下文管理器是从 `ContextDecorator` 派生的，因此它也可以作为函数装饰器使用。

> As shown in the preceding `ContextDecorator` example, when the context manager is used
as a decorator, the value yielded by the generator is not available inside the function being
decorated. Arguments passed to the decorated function are still available, as demonstrated
by `throw_error()` in this example.

如前面的 `ContextDecorator` 示例所示，当上下文管理器用作装饰器时，生成器产生的值在被装饰的函数内部不可用。
传递给装饰函数的参数仍然可用，如本示例中的“throw_error()”所示。


```python
# 3_59_contextlib_contextmanager_decorator.py
import contextlib


@contextlib.contextmanager
def make_context():
    print(' entering')
    try:
        # Yield control, but not a value, because any value
        # yielded is not available when the context manager
        # is used as a decorator.
        yield
    except RuntimeError as err:
        print(' ERROR:', err)
    finally:
        print(' exiting')


@make_context()
def normal():
    print(' inside with statement')


@make_context()
def throw_error(err):
    raise err


print('Normal:')
normal()

print('\nHandled error:')
throw_error(RuntimeError('showing example of handling an error'))

print('\nUnhandled error:')
throw_error(ValueError('this exception is not handled'))

```

```text
Traceback (most recent call last):
  File "C:\Users\ABCX1C\MyProjects\P3SL_Example\chapter_03_algorithms\section_3_4_contextlib\3_59_contextlib_contextmanager_decorator.py", line 35, in <module>
    throw_error(ValueError('this exception is not handled'))
  File "C:\Users\ABCX1C\AppData\Local\Programs\Python\Python39\lib\contextlib.py", line 79, in inner
    return func(*args, **kwds)
  File "C:\Users\ABCX1C\MyProjects\P3SL_Example\chapter_03_algorithms\section_3_4_contextlib\3_59_contextlib_contextmanager_decorator.py", line 25, in throw_error
    raise err
ValueError: this exception is not handled
Normal:
 entering
 inside with statement
 exiting

Handled error:
 entering
 ERROR: showing example of handling an error
 exiting

Unhandled error:
 entering
 exiting

Process finished with exit code 1

```


### 3.4.4 Closing Open Handles

> The `file` class supports the context manager API directly, but some other objects that
represent open handles do not. The example given in the standard library documentation
for `contextlib` is the object returned from `urllib.urlopen()`. Some other legacy classes use
a `close()` method but do not support the context manager API. To ensure that a handle
is closed, use `closing()` to create a context manager for it.

`file` 类直接支持上下文管理器 API，但其他一些表示打开句柄的对象不支持。
`contextlib` 的标准库文档中给出的示例是从 `urllib.urlopen()` 返回的对象。
其他一些遗留类使用 `close()` 方法，但不支持上下文管理器 API。
为确保句柄已关闭，请使用 `closure()` 为其创建上下文管理器。


> The handle is closed whether there is an error in the `with` block or not.

无论 `with` 块中是否存在错误，句柄都会关闭。

```python
# 3_60_contextlib_closing.py
import contextlib


class Door:

    def __init__(self):
        print(' __init__()')
        self.status = 'open'

    def close(self):
        print(' close()')
        self.status = 'closed'


print('Normal Example:')
with contextlib.closing(Door()) as door:
    print(' inside with statement: {}'.format(door.status))
print(' outside with statement: {}'.format(door.status))

print('\nError handling example:')
try:
    with contextlib.closing(Door()) as door:
        print(' raising from inside with statement')
        raise RuntimeError('error message')
except Exception as err:
    print(' Had an error:', err)

```

```text
Normal Example:
 __init__()
 inside with statement: open
 close()
 outside with statement: closed

Error handling example:
 __init__()
 raising from inside with statement
 close()
 Had an error: error message

```


### 3.4.5 Ignoring Exceptions

> It is frequently useful to ignore exceptions raised by libraries, because the error indicates
that the desired state has already been achieved or can otherwise be ignored. The most
common way to ignore exceptions is with a `try:except` statement that includes only a `pass`
statement in the `except` block.

忽略库引发的异常通常很有用，因为错误表明已达到或可以忽略所需的状态。
忽略异常的最常见方法是使用 `try:except` 语句，该语句在 `except` 块中只包含一个 `pass` 语句。


> In this case, the operation fails and the error is ignored.

在这种情况下，操作失败并忽略错误。

```python
# 3_61_contextlib_ignore_error.py
import contextlib


class NonFatalError(Exception):
    pass


def non_idempotent_operation():
    raise NonFatalError(
        'The operation failed because of existing state'
    )


try:
    print('trying non-idempotent operation')
    non_idempotent_operation()
    print('succeeded!')
except NonFatalError:
    pass

print('done')

```

```text
trying non-idempotent operation
done

```

> The `try:except` form can be replaced with `contextlib.suppress()` to more explicitly
suppress a class of exceptions happening anywhere within the `with` block.

`try:except` 形式可以替换为 `contextlib.suppress()`，以更明确地抑制发生在 `with` 块内任何地方的一类异常。

> In this updated version, the exception is discarded entirely.

在这个更新版本中，异常被完全丢弃。

```python
# 3_63_contextlib_suppress.py
import contextlib


class NonFatalError(Exception):
    pass


def non_idempotent_operation():
    raise NonFatalError(
        'The operation failed because of existing state'
    )


with contextlib.suppress(NonFatalError):
    print('trying non-idempotent operation')
    non_idempotent_operation()
    print('succeeded!')

print('done')

```


```text
trying non-idempotent operation
done

```


### 3.4.6 Redirecting Output Streams

> Poorly designed library code may write directly to `sys.stdout` or `sys.stderr`, without providing
arguments to configure different output destinations. The `redirect_stdout()` and
`redirect_stderr()` context managers can be used to capture output from these kinds of
functions, for which the source cannot be changed to accept a new output argument.

设计不佳的库代码可能会直接写入 `sys.stdout` 或 `sys.stderr`，而不提供参数来配置不同的输出目的地。
`redirect_stdout()` 和 `redirect_stderr()` 上下文管理器可用于捕获来自这些类型函数的输出，对于这些函数，源不能更改为接受新的输出参数。


> In this example, `misbehaving_function()` writes to both `stdout` and `stderr`, but the two
context managers send that output to the same `io.StringIO` instance, where it is saved for
later use.

在这个例子中，`misbesharing_function()` 写入`stdout` 和`stderr`，
但是两个上下文管理器将该输出发送到同一个`io.StringIO` 实例，在那里保存以备后用。

> Both `redirect_stdout()` and `redirect_stderr()` modify the global state by replacing objects in
the `sys` (page 1178) module; for this reason, they should be used with care. The functions are not really
thread-safe, so calling them in a multithreaded application will have nondeterministic results. They also
may interfere with other operations that expect the standard output streams to be attached to terminal
devices.

`redirect_stdout()` 和 `redirect_stderr()` 都通过替换 `sys`（第 1178 页）模块中的对象来修改全局状态；
因此，应谨慎使用它们。
这些函数并不是真正的线程安全的，因此在多线程应用程序中调用它们将产生不确定的结果。
它们还可能干扰其他期望将标准输出流附加到终端设备的操作。

```python
# 3_63_contextlib_redirect.py
from contextlib import redirect_stdout, redirect_stderr
import io
import sys


def misbehaving_function(a):
    sys.stdout.write('(stdout) A: {!r}\n'.format(a))
    sys.stderr.write('(stderr) A: {!r}\n'.format(a))


capture = io.StringIO()
with redirect_stdout(capture), redirect_stderr(capture):
    misbehaving_function(5)

print(capture.getvalue())

```

```text
(stdout) A: 5
(stderr) A: 5

```



### 3.4.7 Dynamic Context Manager Stacks

> Most context managers operate on one object at a time, such as a single file or database
handle. In these cases, the object is known in advance and the code using the context
manager can be built around that one object. In other cases, a program may need to create
an unknown number of objects within a context, with all of those objects expected to be
cleaned up when control flow exits the context. `ExitStack` was created to handle these more
dynamic cases.

大多数上下文管理器一次对一个对象进行操作，例如单个文件或数据库句柄。
在这些情况下，对象是预先知道的，并且可以围绕该对象构建使用上下文管理器的代码。
在其他情况下，程序可能需要在上下文中创建未知数量的对象，当控制流退出上下文时，所有这些对象都将被清除。 
`ExitStack` 的创建是为了处理这些更动态的情况。


> An `ExitStack` instance maintains a stack data structure of cleanup callbacks. The callbacks
are populated explicitly within the context, and any registered callbacks are called
in the reverse order when control flow exits the context. The result is similar to having
multiple nested `with` statements, except they are established dynamically.

`ExitStack` 实例维护一个清理回调的堆栈数据结构。
回调在上下文中显式填充，当控制流退出上下文时，任何注册的回调都以相反的顺序调用。
结果类似于具有多个嵌套的 `with` 语句，只是它们是动态建立的。


#### 3.4.7.1 Stacking Context Managers

> Several approaches may be used to populate the `ExitStack`. This example uses `enter_
context()` to add a new context manager to the stack.

可以使用多种方法来填充`ExitStack`。
此示例使用 `enter_ context()` 将一个新的上下文管理器添加到堆栈中。


> `enter_context()` first calls `__enter__()` on the context manager. It then registers its
`__exit__()` method as a callback to be invoked as the stack is undone.

`enter_context()` 首先在上下文管理器上调用 `__enter__()`。
然后它注册它的 `__exit__()` 方法作为一个回调，当堆栈被撤消时被调用。


```python
# 3_64_contextlib_exitstack_enter_context.py
import contextlib


@contextlib.contextmanager
def make_context(i):
    print('{} entering'.format(i))
    yield {}
    print('{} exiting'.format(i))


def variable_stack(n, msg):
    with contextlib.ExitStack() as stack:
        for i in range(n):
            stack.enter_context(make_context(i))
        print(msg)


variable_stack(2, 'inside context')

```

```text
0 entering
1 entering
inside context
1 exiting
0 exiting

```


> The context managers given to `ExitStack` are treated as though they appear within a
series of nested `with` statements. Errors that happen anywhere within the context propagate
through the normal error handling of the context managers. The following context manager
classes illustrate the way errors propagate.

赋予 `ExitStack` 的上下文管理器被视为出现在一系列嵌套的 `with` 语句中。
上下文中任何地方发生的错误通过上下文管理器的正常错误处理传播。
以下上下文管理器类说明了错误传播的方式。


> The following examples using these classes are based on `variable_stack()`, which uses
the context managers passed to construct an `ExitStack`, building up the overall context in
a step-by-step manner. The examples pass different context managers to explore the error
handling behavior. The first example presents the normal case of no exceptions.

以下使用这些类的示例基于 `variable_stack()`，它使用传递的上下文管理器来构造一个 `ExitStack`，以逐步的方式构建整体上下文。
这些示例通过不同的上下文管理器来探索错误处理行为。
第一个例子展示了没有异常的正常情况。


```python
print('No errors:')
variable_stack([
    HandleError(1),
    PassError(2),
])
```

> The next example illustrates handling exceptions within the context managers at the end
of the stack, in which all of the open contexts are closed as the stack is unwound.

下一个示例说明在堆栈末尾的上下文管理器中处理异常，其中所有打开的上下文在堆栈展开时关闭。

```python
print('\nError at the end of the context stack:')
variable_stack([
    HandleError(1),
    HandleError(2),
    ErrorOnExit(3),
])
```

> In the next example, exceptions are handled within the context managers in the middle of
the stack. The error does not occur until some contexts are already closed, so those contexts
do not see the error.

在下一个示例中，异常在堆栈中间的上下文管理器中处理。
在某些上下文已经关闭之前不会发生错误，因此这些上下文看不到错误。


```python
print('\nError in the middle of the context stack:')
variable_stack([
    HandleError(1),
    PassError(2),
    ErrorOnExit(3),
    HandleError(4),
])
```

> The final example shows the case in which the exception remains unhandled and propagates
up to the calling code.

最后一个示例显示了异常未处理并传播到调用代码的情况。

```python
try:
    print('\nError ignored:')
    variable_stack([
        PassError(1),
        ErrorOnExit(2),
    ])
except RuntimeError:
    print('error handled outside of context')
```

> If any context manager in the stack receives an exception and returns a `True` value, it
prevents that exception from propagating up to any other context managers.

如果堆栈中的任何上下文管理器收到异常并返回“True”值，它会阻止该异常传播到任何其他上下文管理器。


```text
No errors:
 HandleError(1): entering
 PassError(2): entering
 PassError(2): exiting
 HandleError(1): exiting False
 outside of stack, any errors were handled

Error at the end of the context stack:
 HandleError(1): entering
 HandleError(2): entering
 ErrorOnExit(3): entering
 ErrorOnExit(3): throwing error
 HandleError(2): handling exception RuntimeError('from 3')
 HandleError(2): exiting True
 HandleError(1): exiting False
 outside of stack, any errors were handled

Error in the middle of the context stack:
 HandleError(1): entering
 PassError(2): entering
 ErrorOnExit(3): entering
 HandleError(4): entering
 HandleError(4): exiting False
 ErrorOnExit(3): throwing error
 PassError(2): passing exception RuntimeError('from 3')
 PassError(2): exiting
 HandleError(1): handling exception RuntimeError('from 3')
 HandleError(1): exiting True
 outside of stack, any errors were handled

Error ignored:
 PassError(1): entering
 ErrorOnExit(2): entering
 ErrorOnExit(2): throwing error
 PassError(1): passing exception RuntimeError('from 2')
 PassError(1): exiting
 error handled outside of context

Process finished with exit code 0

```


#### 3.4.7.2 Arbitrary Context Callbacks

> `ExitStack` also supports arbitrary callbacks for closing a context, making it easy to clean
up resources that are not controlled via a context manager.

`ExitStack` 还支持关闭上下文的任意回调，从而可以轻松清理不受上下文管理器控制的资源。

> Just as with the `__exit__()` methods of full context managers, the callbacks are invoked in
the reverse order that they are registered.

就像完整上下文管理器的 `__exit__()` 方法一样，回调的调用顺序与它们注册的顺序相反。

```python
# 3_66_contextlib_exitstack_callbacks.py
import contextlib


def callback(*args, **kwds):
    print('closing callback({}, {})'.format(args, kwds))


with contextlib.ExitStack() as stack:
    stack.callback(callback, 'arg1', 'arg2')
    stack.callback(callback, arg3='val3')
```


```text
closing callback((), {'arg3': 'val3'})
closing callback(('arg1', 'arg2'), {})
```


> The callbacks are invoked regardless of whether an error occurred, and they are not given
any information about whether an error occurred. Their return value is ignored.

无论是否发生错误，都会调用回调，并且不会向它们提供有关是否发生错误的任何信息。
它们的返回值被忽略。

> Because they do not have access to the error, callbacks are unable to prevent exceptions
from propagating through the rest of the stack of context managers.

因为它们无权访问错误，回调无法阻止异常通过上下文管理器堆栈的其余部分传播。


```python
# 3_67_contextlib_exitstack_callbacks_error.py
import contextlib


def callback(*args, **kwds):
    print('closing callback({}, {})'.format(args, kwds))


try:
    with contextlib.ExitStack() as stack:
        stack.callback(callback, 'arg1', 'arg2')
        stack.callback(callback, arg3='val3')
        raise RuntimeError('thrown error')
except RuntimeError as err:
    print('ERROR: {}'.format(err))
```

```text
closing callback((), {'arg3': 'val3'})
closing callback(('arg1', 'arg2'), {})
ERROR: thrown error

```


> Callbacks offer a convenient way to clearly define cleanup logic without the overhead
of creating a new context manager class. To improve code readability, that logic can be
encapsulated in an inline function, and `callback()` can be used as a decorator.

回调提供了一种方便的方法来明确定义清理逻辑，而无需创建新的上下文管理器类。
为了提高代码可读性，可以将该逻辑封装在一个内联函数中，并且`callback()` 可以用作装饰器。

> There is no way to specify the arguments for functions registered using the decorator
form of `callback()`. However, if the cleanup callback is defined inline, scope rules give it
access to variables defined in the calling code.

无法为使用“callback()”的装饰器形式注册的函数指定参数。
但是，如果清理回调是内联定义的，作用域规则允许它访问调用代码中定义的变量。


```python
# 3_68_contextlib_exitstack_callbacks_decorator.py
import contextlib


with contextlib.ExitStack() as stack:

    @stack.callback
    def inline_cleanup():
        print('inline_cleanup()')
        print('local_resource = {!r}'.format(local_resource))

    local_resource = 'resource created in context'
    print('within the context')

```

```text
within the context
inline_cleanup()
local_resource = 'resource created in context'

```


#### 3.4.7.3 Partial Stacks

> Sometimes when building complex contexts, it is useful to be able to abort an operation if
the context cannot be completely constructed, but to delay the cleanup of all resources until
a later time if they can all be set up properly. For example, if an operation needs several
long-lived network connections, it may be best to not start the operation if one connection
fails. However, if all of the connections can be opened, they need to stay open longer than
the duration of a single context manager. The `pop_all()` method of `ExitStack` can be used
in this scenario.

有时在构建复杂的上下文时，如果上下文不能完全构建，可以中止操作是有用的，但如果它们都可以正确设置，则将所有资源的清理延迟到稍后的时间。
例如，如果一项操作需要多个长期存在的网络连接，如果一个连接失败，最好不要启动该操作。
但是，如果所有连接都可以打开，则它们需要保持打开状态的时间长于单个上下文管理器的持续时间。
在这种情况下可以使用`ExitStack`的`pop_all()`方法。

> `pop_all()` clears all of the context managers and callbacks from the stack on which it
is called, and returns a new stack prepopulated with those same context managers and
callbacks. The `close()` method of the new stack can be invoked later, after the original
stack is gone, to clean up the resources.

`pop_all()` 从调用它的堆栈中清除所有上下文管理器和回调，并返回一个预先填充了这些相同上下文管理器和回调的新堆栈。
新堆栈的`close()`方法可以在原堆栈消失后调用，以清理资源。


> This example uses the same context manager classes defined earlier, but `ErrorOnEnter`
produces an error on `__enter__()` instead of `__exit__()`. Inside `variable_stack()`, if all
of the contexts are entered without error, then the `close()` method of a new `ExitStack`
is returned. If a handled error occurs, `variable_stack()` returns `None` to indicate that the
cleanup work has already been done. If an unhandled error occurs, the partial stack is
cleaned up and the error is propagated. 

此示例使用之前定义的相同上下文管理器类，但 `ErrorOnEnter` 会在 `__enter__()` 而不是 `__exit__()` 上产生错误。
在 `variable_stack()` 内部，如果所有上下文都没有错误地输入，则返回新的 `ExitStack` 的 `close()` 方法。
如果发生处理错误，`variable_stack()` 返回 `None` 表示清理工作已经完成。
如果发生未处理的错误，则会清除部分堆栈并传播错误。

```python
# 3_69_contextlib_exitstack_pop_all.py
import contextlib

from contextlib_context_managers import *


def variable_stack(contexts):
    with contextlib.ExitStack() as stack:
        for c in contexts:
            stack.enter_context(c)
        # Return the close() method of a new stack as a clean-up
        # function.
        return stack.pop_all().close
    # Explicitly return None, indicating that the ExitStack could
    # not be initialized cleanly but that cleanup has already
    # occurred.
    return None


print('No errors:')
cleaner = variable_stack([
    HandleError(1),
    HandleError(2),
])
cleaner()

print('\nHandled error building context manager stack:')
try:
    cleaner = variable_stack([
        HandleError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error {}'.format(err))
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')

print('\nUnhandled error building context manager stack:')
try:
    cleaner = variable_stack([
        PassError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error {}'.format(err))
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')

```


````text
No errors:
 HandleError(1): entering
 HandleError(2): entering
 HandleError(2): exiting False
 HandleError(1): exiting False

Handled error building context manager stack:
 HandleError(1): entering
 ErrorOnEnter(2): throwing error on enter
 HandleError(1): handling exception RuntimeError('from 2')
 HandleError(1): exiting True
no cleaner returned

Unhandled error building context manager stack:
 PassError(1): entering
 ErrorOnEnter(2): throwing error on enter
 PassError(1): passing exception RuntimeError('from 2')
 PassError(1): exiting
caught error from 2

Process finished with exit code 0

````