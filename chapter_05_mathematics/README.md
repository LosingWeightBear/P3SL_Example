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