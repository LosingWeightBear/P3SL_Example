# Chapter 1 -- Text

## 1.1 string: Text Constants and Templates

> The `string` module dates from the earliest versions of Python. Many of the functions previously implemented in the module have been moved to methods of `str` objects, but the module retains several useful constants and classes for working with `str` objects.

`string`模块起源于Python的最早期版本。该模块中许多早先的功能已经被移到了`str`对象的方法中，但依旧保留了几个有用的常量和类配合`str`对象使用。

### 1.1.1 Functions
> The function `capwords()` capitalizes all of the words in a string.

`capwords()`函数对字符串中所有单词进行首字母大写。

```python
import string
s = 'The quick brown fox jumped over the lazy dog.'
print(s)
print(string.capwords(s))
```

### 1.1.2 Templates
> String templates were added as part of **PEP 292** and are intended as an alternative to the
built-in interpolation syntax. With `string.Template` interpolation, variables are identified
by prefixing the name with $ (e.g., $var). Alternatively, if necessary to set them off from
surrounding text, they can be wrapped with curly braces (e.g., ${var}).