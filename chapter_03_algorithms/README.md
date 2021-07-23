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


Process finished with exit code 0

```