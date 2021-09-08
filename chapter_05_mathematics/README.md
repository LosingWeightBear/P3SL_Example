# Chapter 5  -- Mathematics

> As a general-purpose programming language, Python is frequently used to solve mathematical
problems. It includes built-in types for managing integer and floating-point numbers,
which are suitable for the basic math that might appear in an average application. The
standard library includes modules for more advanced needs.

作为一种通用编程语言，Python 经常用于解决数学问题。
它包括用于管理整数和浮点数的内置类型，适用于可能出现在普通应用程序中的基本数学。
标准库包括满足更高级需求的模块。


> Python’s built-in floating-point numbers use the underlying `double` representation. They
are sufficiently precise for most programs with mathematical requirements, but when more
accurate representations of non-integer values are needed, the `decimal` (page 239) and
`fractions` (page 250) modules will be useful. Arithmetic with decimal and fractional values
retains precision, but is not as fast as the native `float`.

Python 的内置浮点数使用底层的`double`表示。
它们对于大多数有数学要求的程序来说足够精确，但是当需要更准确地表示非整数值时，`decimal`（第 239 页）和`fractions`（第 250 页）模块将很有用。
带有小数和小数值的算术保持精度，但不如原生的`float`快。


> The `random` (page 254) module includes a uniform distribution pseudorandom number
generator, as well as functions for simulating many common non-uniform distributions.

`random`（第 254 页）模块包括一个均匀分布伪随机数生成器，以及用于模拟许多常见非均匀分布的函数。


> The `math` (page 264) module contains fast implementations of advanced mathematical
functions such as logarithms and trigonometric functions. The full complement of IEEE
functions usually found in the native-platform C libraries is available through the module.

`math`（第 264 页）模块包含高级数学函数的快速实现，例如对数和三角函数。
通常在本地平台 C 库中可以找到的完整 IEEE 函数可通过该模块获得。


## 5.1 decimal: Fixed- and Floating-Point Math

> The `decimal` module implements fixed- and floating-point arithmetic using the model familiar
to most people, rather than the IEEE floating-point version implemented by most
computer hardware and familiar to programmers. A `Decimal` instance can represent any
number exactly, be rounded up or down, and apply a limit to the number of significant
digits.

`decimal` 模块使用大多数人熟悉的模型来实现定点和浮点运算，而不是大多数计算机硬件实现的、程序员所熟悉的 IEEE 浮点版本。
`Decimal` 实例可以精确地表示任何数字，可以向上或向下舍入，并对有效数字的数量施加限制。


### 5.1.1 Decimal

> Decimal values are represented as instances of the `Decimal` class. As its argument, the constructor
takes one integer or string. Floating-point numbers can be converted to a string before
being used to create a `Decimal`, thereby letting the caller explicitly deal with the number
of digits for values that cannot be expressed exactly using hardware floating-point representations.
Alternatively, the class method `from_float()` converts a floating-point number
to its exact decimal representation.

十进制值表示为`Decimal`类的实例。
作为它的参数，构造函数接受一个整数或字符串。
浮点数可以在用于创建`Decimal`之前转换为字符串，从而让调用者显式处理无法使用硬件浮点表示精确表达的值的位数。
或者，类方法`from_float()` 将浮点数转换为其精确的十进制表示。


> The floating-point value of 0.1 is not represented as an exact value in binary, so its
representation as a `float` is different from the `Decimal` value. The full string representation
is truncated to 25 characters in the last line of this output.

浮点值 0.1 不表示为二进制的精确值，因此其表示为`float`与`Decimal`值不同。
在此输出的最后一行中，完整的字符串表示被截断为 25 个字符。


```python
# 5_1_decimal_create.py
import decimal

fmt = '{0:<25} {1:<25}'
print(fmt.format('Input', 'Output'))
print(fmt.format('-' * 25, '-' * 25))

# Integer
print(fmt.format(5, decimal.Decimal(5)))

# String
print(fmt.format('3.14', decimal.Decimal('3.14')))

# Float
f = 0.1
print(fmt.format(repr(f), decimal.Decimal(str(f))))
print('{:<0.23g} {:<25}'.format(f, str(decimal.Decimal.from_float(f))[:25]))

```

```text
Input                     Output                   
------------------------- -------------------------
5                         5                        
3.14                      3.14                     
0.1                       0.1                      
0.10000000000000000555112 0.10000000000000000555111

```


> `Decimals` can also be created from tuples containing a sign flag (0 for positive, 1 for
negative), a `tuple` of digits, and an integer exponent.

`Decimals`也可以从包含符号标志（0 表示正，1 表示负）、数字元组和整数指数的元组创建。

> The tuple-based representation is less convenient to create, but offers a portable way of exporting
decimal values without losing precision. The tuple form can be transmitted through
the network or stored in a database that does not support accurate decimal values, then
turned back into a `Decimal` instance later.

基于元组的表示不太方便创建，但提供了一种可移植的方式来导出十进制值而不会损失精度。
元组形式可以通过网络传输或存储在不支持精确十进制值的数据库中，然后再转换回`Decimal`实例。


```python
# 5_2_decimal_tuple.py
import decimal

# Tuple
t = (1, (1, 1), -2)
print('Input :', t)
print('Decimal:', decimal.Decimal(t))

```

```text
Input : (1, (1, 1), -2)
Decimal: -0.11

```


### 5.1.2 Formatting

> `Decimal` responds to Python’s string formatting protocol by using the same syntax and
options as other numerical types.

`Decimal` 使用与其他数字类型相同的语法和选项来响应 Python 的字符串格式化协议。

> The format strings can control the width of the output, the precision (i.e., the number
of significant digits), and the means of padding the value to fill the width.

格式字符串可以控制输出的宽度、精度（即有效位数）以及填充值以填充宽度的方法。

```python
# 5_3_decimal_format.py
import decimal

d = decimal.Decimal(1.1)
print('Precision:')
print('{:.1}'.format(d))
print('{:.2}'.format(d))
print('{:.3}'.format(d))
print('{:.18}'.format(d))

print('\nWidth and precision combined:')
print('{:5.1f} {:5.1g}'.format(d, d))
print('{:5.2f} {:5.2g}'.format(d, d))
print('{:5.2f} {:5.2g}'.format(d, d))

print('\nZero padding:')
print('{:05.1}'.format(d))
print('{:05.2}'.format(d))
print('{:05.3}'.format(d))

```


```python
# 5_3_decimal_format.py
import decimal

d = decimal.Decimal(1.1)
print('Precision:')
print('{:.1}'.format(d))
print('{:.2}'.format(d))
print('{:.3}'.format(d))
print('{:.18}'.format(d))

print('\nWidth and precision combined:')
print('{:5.1f} {:5.1g}'.format(d, d))
print('{:5.2f} {:5.2g}'.format(d, d))
print('{:5.2f} {:5.2g}'.format(d, d))

print('\nZero padding:')
print('{:05.1}'.format(d))
print('{:05.2}'.format(d))
print('{:05.3}'.format(d))

```

```text
Precision:
1
1.1
1.10
1.10000000000000009

Width and precision combined:
  1.1     1
 1.10   1.1
 1.10   1.1

Zero padding:
00001
001.1
01.10

```


### 5.1.3 Arithmetic

> `Decimal` overloads the simple arithmetic operators so instances can be manipulated in much
the same way as the built-in numeric types.

`Decimal` 重载了简单的算术运算符，因此可以以与内置数字类型大致相同的方式操作实例。


> `Decimal` operators also accept integer arguments. In contrast, floating-point values must
be converted to `Decimal` instances before they can be used by these operators.

`Decimal` 运算符也接受整数参数。
相比之下，浮点值必须先转换为“Decimal”实例，然后才能被这些运算符使用。


> Beyond basic arithmetic, `Decimal` includes methods to find base 10 logarithms and natural
logarithms. The return values from `log10()` and `ln()` are Decimal instances, so they
can be used directly in formulas with other values.

除了基本算术，`Decimal`还包括查找以 10 为底的对数和自然对数的方法。
`log10()` 和 `ln()` 的返回值是 Decimal 实例，因此它们可以直接用于具有其他值的公式中。


```python
# 5_4_decimal_operators.py
import decimal

a = decimal.Decimal('5.1')
b = decimal.Decimal('3.14')
c = 4
d = 3.14

print('a =', repr(a))
print('b =', repr(b))
print('c =', repr(c))
print('d =', repr(d))
print()

print('a + b =', a + b)
print('a - b =', a - b)
print('a * b =', a * b)
print('a / b =', a / b)
print()

print('a + c =', a + c)
print('a - c =', a - c)
print('a * c =', a * c)
print('a / c =', a / c)
print()

print('a + d =', end=' ')
try:
    print(a + d)
except TypeError as e:
    print(e)

```

```text
a = Decimal('5.1')
b = Decimal('3.14')
c = 4
d = 3.14

a + b = 8.24
a - b = 1.96
a * b = 16.014
a / b = 1.624203821656050955414012739

a + c = 9.1
a - c = 1.1
a * c = 20.4
a / c = 1.275

a + d = unsupported operand type(s) for +: 'decimal.Decimal' and 'float'

```


### 5.1.4 Special Values

> In addition to the expected numerical values, `Decimal` can represent several special values,
including positive and negative values for infinity, “not a number” (`NaN`), and zero.

除了预期的数值外，`Decimal` 还可以表示几个特殊值，包括无穷大的正负值、“非数字”(`NaN`) 和零。


> Adding to infinite values returns another infinite value. Comparing for equality with `NaN`
always returns false, whereas comparing for inequality with this value always returns true.
Comparing for sort order against `NaN` is undefined and results in an error.

添加到无限值返回另一个无限值。
与`NaN`比较相等总是返回false，而与此值比较不相等总是返回true。
将排序顺序与`NaN`进行比较未定义并导致错误。


```python
# 5_5_decimal_special.py
import decimal

for value in ['Infinity', 'NaN', '0']:
    print(decimal.Decimal(value), decimal.Decimal('-' + value))
print()

# Math with infinity
print('Infinity + 1:', (decimal.Decimal('Infinity') + 1))
print('-Infinity + 1:', (decimal.Decimal('-Infinity') + 1))

# Print comparing NaN
print(decimal.Decimal('NaN') == decimal.Decimal('Infinity'))
print(decimal.Decimal('NaN') != decimal.Decimal(1))

```


```text
Infinity -Infinity
NaN -NaN
0 -0

Infinity + 1: Infinity
-Infinity + 1: -Infinity
False
True


```


### 5.1.5 Context

> So far, all of the examples have used the default behaviors of the `decimal` module. It is
possible to override settings such as the precision maintained, the way in which rounding is
performed, and error handling by using a context. Contexts can be applied for all `Decimal`
instances in a thread or locally within a small code region.

到目前为止，所有示例都使用了 `decimal` 模块的默认行为。
可以使用上下文覆盖设置，例如保持的精度、执行舍入的方式以及错误处理。
上下文可以应用于线程中或本地小代码区域内的所有“十进制”实例。


#### 5.1.5.1 Current Context

> To retrieve the current global context, use `getcontext`.

要检索当前的全局上下文，请使用 `getcontext`。


> The example script shows the public properties of a `Context`.

示例脚本显示了 `Context` 的公共属性。

```python
# 5_6_decimal_getcontext.py
import decimal

context = decimal.getcontext()
print('Emax =', context.Emax)
print('Emin =', context.Emin)
print('capitals =', context.capitals)
print('prec =', context.prec)
print('rounding =', context.rounding)
print('flags =')
for f, v in context.flags.items():
    print(' {}: {}'.format(f, v))
print('traps =')
for t, v in context.traps.items():
    print(' {}: {}'.format(t, v))

```

```text
Emax = 999999
Emin = -999999
capitals = 1
prec = 28
rounding = ROUND_HALF_EVEN
flags =
 <class 'decimal.InvalidOperation'>: False
 <class 'decimal.FloatOperation'>: False
 <class 'decimal.DivisionByZero'>: False
 <class 'decimal.Overflow'>: False
 <class 'decimal.Underflow'>: False
 <class 'decimal.Subnormal'>: False
 <class 'decimal.Inexact'>: False
 <class 'decimal.Rounded'>: False
 <class 'decimal.Clamped'>: False
traps =
 <class 'decimal.InvalidOperation'>: True
 <class 'decimal.FloatOperation'>: False
 <class 'decimal.DivisionByZero'>: True
 <class 'decimal.Overflow'>: True
 <class 'decimal.Underflow'>: False
 <class 'decimal.Subnormal'>: False
 <class 'decimal.Inexact'>: False
 <class 'decimal.Rounded'>: False
 <class 'decimal.Clamped'>: False

```


#### 5.1.5.2 Precision

> The `prec` attribute of the context controls the precision maintained for new values created
as a result of arithmetic. Literal values are maintained as described.

上下文的`prec` 属性控制为算术结果创建的新值保持的精度。
文字值按所述进行维护。


> To change the precision, assign a new value between 1 and decimal.`MAX_PREC` directly
to the attribute.

要更改精度，请直接为属性分配一个介于 1 和小数之间的新值。`MAX_PREC`。


```python
# 5_7_decimal_precision.py
import decimal

d = decimal.Decimal('0.123456')

for i in range(1, 5):
    decimal.getcontext().prec = i
    print(i, ':', d, d * 1)

```

```text
1 : 0.123456 0.1
2 : 0.123456 0.12
3 : 0.123456 0.123
4 : 0.123456 0.1235
```


#### 5.1.5.3 Rounding

> There are several options for rounding to keep values within the desired precision.

有多种四舍五入选项可将值保持在所需的精度范围内。

> `ROUND_CEILING` Always round upward toward infinity.

`ROUND_CEILING` 总是向上舍入到无穷大。

> `ROUND_DOWN` Always round toward zero.

`ROUND_DOWN` 总是向零舍入。

> `ROUND_FLOOR` Always round down toward negative infinity.

`ROUND_FLOOR` 总是向下取整到负无穷大。

> `ROUND_HALF_DOWN` Round away from zero if the last significant digit is greater than or equal
to 5; otherwise, round toward zero.

`ROUND_HALF_DOWN` 如果最后一位有效数字大于或等于 5，则从零开始舍入； 否则，向零舍入。

> `ROUND_HALF_EVEN` Like ROUND_HALF_DOWN except that if the value is 5, then the preceding digit
is examined. Even digits cause the result to be rounded down, and odd digits cause the
result to be rounded up.

`ROUND_HALF_EVEN` 与 ROUND_HALF_DOWN 类似，但如果值为 5，则检查前面的数字。
偶数位导致结果四舍五入，奇数位导致结果四舍五入。

> `ROUND_HALF_UP` Like `ROUND_HALF_DOWN` except that if the last significant digit is 5, the value
is rounded away from zero.

`ROUND_HALF_UP` 与 `ROUND_HALF_DOWN` 类似，但如果最后一位有效数字是 5，则该值从零舍入。

> `ROUND_UP` Round away from zero.

`ROUND_UP` 从零开始舍入。

> `ROUND_05UP` Round away from zero if the last digit is 0 or 5; otherwise, round toward zero.

`ROUND_05UP` 如果最后一位数字是 0 或 5，则从零开始舍入； 否则，向零舍入。


> This program shows the effect of rounding the same value to different levels of precision
using the different algorithms.

该程序显示了使用不同算法将相同值四舍五入到不同精度级别的效果。

```python
# 5_8_decimal_rounding.py
import decimal

context = decimal.getcontext()

ROUNDING_MODES = [
    'ROUND_CEILING',
    'ROUND_DOWN',
    'ROUND_FLOOR',
    'ROUND_HALF_DOWN',
    'ROUND_HALF_EVEN',
    'ROUND_HALF_UP',
    'ROUND_UP',
    'ROUND_05UP',
]

header_fmt = '{:10} ' + ' '.join(['{:^8}'] * 6)

print(header_fmt.format(
    ' ',
    '1/8 (1)', '-1/8 (1)',
    '1/8 (2)', '-1/8 (2)',
    '1/8 (3)', '-1/8 (3)',
))
for rounding_mode in ROUNDING_MODES:
    print('{0:10}'.format(rounding_mode.partition('_')[-1]), end=' ')
    for precision in [1, 2, 3]:
        context.prec = precision
        context.rounding = getattr(decimal, rounding_mode)
        value = decimal.Decimal(1) / decimal.Decimal(8)
        print('{0:^8}'.format(value), end=' ')
        value = decimal.Decimal(-1) / decimal.Decimal(8)
        print('{0:^8}'.format(value), end=' ')
    print()

```

```text
           1/8 (1)  -1/8 (1) 1/8 (2)  -1/8 (2) 1/8 (3)  -1/8 (3)
CEILING      0.2      -0.1     0.13    -0.12    0.125    -0.125  
DOWN         0.1      -0.1     0.12    -0.12    0.125    -0.125  
FLOOR        0.1      -0.2     0.12    -0.13    0.125    -0.125  
HALF_DOWN    0.1      -0.1     0.12    -0.12    0.125    -0.125  
HALF_EVEN    0.1      -0.1     0.12    -0.12    0.125    -0.125  
HALF_UP      0.1      -0.1     0.13    -0.13    0.125    -0.125  
UP           0.2      -0.2     0.13    -0.13    0.125    -0.125  
05UP         0.1      -0.1     0.12    -0.12    0.125    -0.125  

```


#### 5.1.5.4 Local Context

> The context can be applied to a block of code using the `with` statement.

可以使用 `with` 语句将上下文应用于代码块。

> The `Context` supports the context manager API used by `with`, so the settings apply only
within the block.

 `Context` 支持 `with` 使用的上下文管理器 API，因此设置仅适用于块内


```python
# 5_9_decimal_context_manager.py
import decimal

with decimal.localcontext() as c:
        c.prec = 2
        print('Local precision:', c.prec)
        print('3.14 / 3 =', (decimal.Decimal('3.14') / 3))

print()
print('Default precision:', decimal.getcontext().prec)
print('3.14 / 3 =', (decimal.Decimal('3.14') / 3))

```


```text
Local precision: 2
3.14 / 3 = 1.0

Default precision: 28
3.14 / 3 = 1.046666666666666666666666667
```


#### 5.1.5.5 Per-Instance Context

> Contexts also can be used to construct `Decimal` instances, which then inherit the precision
and rounding arguments of the conversion from the context.

上下文还可用于构造`Decimal`实例，然后从上下文继承转换的精度和舍入参数。


> This approach lets an application select the precision of constant values separately from the
precision of user data, for example.

例如，这种方法让应用程序可以与用户数据的精度分开选择常量值的精度。

```python
# 5_10_decimal_instance_context.py
import decimal

# Set up a context with limited precision.
c = decimal.getcontext().copy()
c.prec = 3

# Create our constant.
pi = c.create_decimal('3.1415')

# The constant value is rounded off.
print('PI :', pi)

# The result of using the constant uses the global context.
print('RESULT:', decimal.Decimal('2.01') * pi)

```

```text
PI : 3.14
RESULT: 6.3114
```



#### 5.1.5.6 Threads

> The “global” context is actually thread-local, so each thread can potentially be configured
using different values.

“全局”上下文实际上是线程本地的，因此每个线程都可能使用不同的值进行配置。


> This example creates a new context using the specified values, then installs it within each
thread.

此示例使用指定的值创建一个新上下文，然后将其安装在每个线程中。


```python
# 5_11_decimal_thread_context.py
import decimal
import threading
from queue import PriorityQueue


class Multiplier(threading.Thread):
    def __init__(self, a, b, prec, q):
        self.a = a
        self.b = b
        self.prec = prec
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        c = decimal.getcontext().copy()
        c.prec = self.prec
        decimal.setcontext(c)
        self.q.put((self.prec, a * b))


a = decimal.Decimal('3.14')
b = decimal.Decimal('1.234')
# A PriorityQueue will return values sorted by precision,
# no matter in which order the threads finish.
q = PriorityQueue()
threads = [Multiplier(a, b, i, q) for i in range(1, 6)]
for t in threads:
    t.start()

for t in threads:
    t.join()

for i in range(5):
    prec, value = q.get()
    print('{} {}'.format(prec, value))

```


```text
1 4
2 3.9
3 3.87
4 3.875
5 3.8748

```


## 5.2 fractions: Rational Numbers

> The `Fraction` class implements numerical operations for rational numbers based on the API
defined by `Rational` in the `numbers` module.

`Fraction` 类基于 `numbers` 模块中的 `Rational` 定义的 API 实现有理数的数值运算。


### 5.2.1 Creating Fraction Instances

> As with the `decimal` (page 239) module, new values can be created in several ways. One
easy way is to create them from separate numerator and denominator values.

与 `decimal`（第 239 页）模块一样，可以通过多种方式创建新值。
一种简单的方法是从单独的分子和分母值创建它们。

```python
# 5_12_fractions_create_integers.py
import fractions

for n, d in [(1, 2), (2, 4), (3, 6)]:
    f = fractions.Fraction(n, d)
    print('{}/{} = {}'.format(n, d, f))

```

```text
1/2 = 1/2
2/4 = 1/2
3/6 = 1/2
```



> Another way to create a `Fraction` is using a string representation of `<numerator> /
<denominator>`.

创建 `Fraction` 的另一种方法是使用 ` / ` 的字符串表示。


> The string is parsed to find the numerator and denominator values.

解析字符串以查找分子和分母值。

```python
# 5_13_fractions_create_strings.py
import fractions

for s in ['1/2', '2/4', '3/6']:
    f = fractions.Fraction(s)
    print('{} = {}'.format(s, f))

```


```text
1/2 = 1/2
2/4 = 1/2
3/6 = 1/2
```


> Strings can also use the more usual decimal or floating-point notation of series of digits
separated by a period. Any string that can be parsed by `float()` and that does not represent
`NaN` or an infinite value is supported.

字符串还可以使用更常用的十进制或浮点数表示法，即由句点分隔的一系列数字。
支持任何可以由 `float()` 解析且不代表 `NaN` 或无限值的字符串。

> The numerator and denominator values represented by the floating-point value are computed
automatically.

由浮点值表示的分子和分母值是自动计算的。


```python
# 5_14_fractions_create_strings_floats.py
import fractions

for s in ['0.5', '1.5', '2.0', '5e-1']:
    f = fractions.Fraction(s)
    print('{0:>4} = {1}'.format(s, f))

```

```text
 0.5 = 1/2
 1.5 = 3/2
 2.0 = 2
5e-1 = 1/2
```


> It is also possible to create `Fraction` instances directly from other representations of rational
values, such as `float` or `Decimal`.

也可以直接从其他有理值的表示创建`Fraction`实例，例如`float`或`Decimal`。


> Floating-point values that cannot be expressed exactly may yield unexpected results.

无法准确表达的浮点值可能会产生意外结果。

```python
# 5_15_fractions_from_float.py
import fractions

for v in [0.1, 0.5, 1.5, 2.0]:
    print('{} = {}'.format(v, fractions.Fraction(v)))

```

```text
0.1 = 3602879701896397/36028797018963968
0.5 = 1/2
1.5 = 3/2
2.0 = 2


```


> Using `Decimal` representations of the values gives the expected results.

使用值的`Decimal`表示给出了预期的结果。

> The internal implementation of `Decimal` does not suffer from the precision errors of the
standard floating-point representation.

`Decimal` 的内部实现不会受到标准浮点表示的精度误差的影响

```python
# 5_16_fractions_from_decimal.py
import decimal
import fractions

values = [
    decimal.Decimal('0.1'),
    decimal.Decimal('0.5'),
    decimal.Decimal('1.5'),
    decimal.Decimal('2.0'),
]
for v in values:
    print('{} = {}'.format(v, fractions.Fraction(v)))

```

```text
0.1 = 1/10
0.5 = 1/2
1.5 = 3/2
2.0 = 2
```


### 5.2.2 Arithmetic

> Once the fractions are instantiated, they can be used in mathematical expressions.

一旦分数被实例化，它们就可以用于数学表达式。

> All of the standard operators are supported.

支持所有标准运算符。

```python
# 5_18_fractions_arithmetic.py
import fractions

f1 = fractions.Fraction(1, 2)
f2 = fractions.Fraction(3, 4)

print('{} + {} = {}'.format(f1, f2, f1 + f2))
print('{} - {} = {}'.format(f1, f2, f1 - f2))
print('{} * {} = {}'.format(f1, f2, f1 * f2))
print('{} / {} = {}'.format(f1, f2, f1 / f2))

```


```text
1/2 + 3/4 = 5/4
1/2 - 3/4 = -1/4
1/2 * 3/4 = 3/8
1/2 / 3/4 = 2/3
```


### 5.2.3 Approximating Values

> A useful feature of `Fraction` is the ability to convert a floating-point number to an approximate
rational value.

`Fraction` 的一个有用特性是能够将浮点数转换为近似有理数。

> The value of the fraction can be controlled by limiting the size of the denominator.

分数的值可以通过限制分母的大小来控制。

```python
# 5_18_fractions_limit_denominator.py
import fractions
import math

print('PI =', math.pi)

f_pi = fractions.Fraction(str(math.pi))
print('No limit =', f_pi)

for i in [1, 6, 11, 60, 70, 90, 100]:
    limited = f_pi.limit_denominator(i)
    print('{0:8} = {1}'.format(i, limited))
```

```text
PI = 3.141592653589793
No limit = 3141592653589793/1000000000000000
       1 = 3
       6 = 19/6
      11 = 22/7
      60 = 179/57
      70 = 201/64
      90 = 267/85
     100 = 311/99

```


## 5.3 random: Pseudorandom Number Generators