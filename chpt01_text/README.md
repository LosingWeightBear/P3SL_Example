# Chapter 1 -- Text

[toc]

## 1.1 string: Text Constants and Templates

> The `string` module dates from the earliest versions of Python. Many of the functions previously implemented in the module have been moved to methods of `str` objects, but the module retains several useful constants and classes for working with `str` objects.

`string`模块起源于Python的最早期版本。该模块中许多早先的功能已经被移到了`str`对象的方法中，但依旧保留了几个有用的常量和类配合`str`对象使用。

### 1.1.1 Functions
> The function `capwords()` capitalizes all of the words in a string.
> 
> The results are the same as those obtained by calling `split()`, capitalizing the words in the resulting list, and then calling `join()` to combine the results.

`capwords()`函数对字符串中所有单词进行首字母大写。
其效果等价于：对字符串按**空格**切分为单词列表，再对列表中每个单词进行首字母大写，最后重新组合为字符串。



```python
import string

s = 'I am a Python beginner.'

print(s)
print(string.capwords(s))

# 单词都是大写
ss = 'THIS IS MY FIRST PYTHON CODE!'

print(ss)
print(string.capwords(ss))

# 中文
sss = '我是一名程序员。'

print(sss)
print(string.capwords(sss))

# 中文+英文混合,英文单词前需要有空格才会被首字母大写
ssss = '我是一名初学 python的程序员！'

print(ssss)
print(string.capwords(ssss))

sssss = '我是一名初学python的程序员！'

print(sssss)
print(string.capwords(sssss))
```

```text
I am a Python beginner.
I Am A Python Beginner.
THIS IS MY FIRST PYTHON CODE!
This Is My First Python Code!
我是一名程序员。
我是一名程序员。
我是一名初学 python的程序员！
我是一名初学 Python的程序员！
我是一名初学python的程序员！
我是一名初学python的程序员！
```


### 1.1.2 Templates
> String templates were added as part of **PEP 292** (www.python.org/dev/peps/pep-0292) and are intended as an alternative to the
built-in interpolation syntax. With `string.Template` interpolation, variables are identified by prefixing the name with `$` (e.g., `$var`). Alternatively, if necessary to set them off from surrounding text, they can be wrapped with curly braces (e.g., `${var}`).

字符串模板作为PEP 292的一部分加入，旨在作为一种可选的内建插值语法。
使用`string.Template`插值,通过在名字前增加`$`前缀来识别变量，例如`$var`。或者，变量名如果需要与周围的文本区分开，可以用大括号括起来。

> This example compares a simple template with similar string interpolation using the `%` operator and the new format string syntax using `str.format()`.

这个例子比较简单模板、使用`%`操作符的字符串插值和新的格式化字符串语法`str.format()`。

```python
import string

values = {'var': 'foo'}

t = string.Template("""
Variable        : $var
Escape          : $$
Variable in text: ${var}iable
""")

print('TEMPLATE:', t.substitute(values))

s = """
Variable        : %(var)s
Escape          : %%
Variable in text: %(var)siable
"""

print('INTERPOLATION:', s % values)

s = """
Variable        : {var}
Escape          : {{}}
Variable in text: {var}iable
"""

print('FORMAT:', s.format(**values))
```

```text
TEMPLATE: 
Variable        : foo
Escape          : $
Variable in text: fooiable

INTERPOLATION:
Variable        : foo
Escape          : %
Variable in text: fooiable

FORMAT:
Variable        : foo
Escape          : {}
Variable in text: fooiable
```

> In the first two cases, the trigger character (`$` or `%`) is escaped by repeating it twice. For the format syntax, both `{` and `}` need to be escaped by repeating them.

前两个例子中，通过两次重复触发字符(`$` or `%`)进行转义跳过值替换，显示字符本身。格式化语法中重复左右括号对其转义。
第二个例子中的`%(var)s`表示将`var`的值格式化为字符串，即`%s`的格式化效果。

> One key difference between templates and string interpolation or formatting is that the type of the arguments is not taken into account. The values are converted to strings, and the strings are inserted into the result. No formatting options are available. For example, there is no way to control the number of digits used to represent a floating-point value.

字符串模板与字符串插值或格式化最关键的不同点在于，并不考虑参数的类型。值转为字符串并插入到结果中时，没有格式化选项可以使用。比如，不能控制浮点值的数字位数。


> A benefit, though, is that use of the `safe_substitute()` method makes it possible to avoid exceptions if not all of the values needed by the template are provided as arguments.

如果模板中所需要的值并没有在参数中都给出，那么最好是使用`safe_substitute()`方法来避免例外。


> Since there is no value for `missing` in the values dictionary, a `KeyError` is raised by `substitute()`. Instead of raising the error, `safe_substitute()` catches it and leaves the variable expression alone in the text.

由于变量字典中`missing`的值并未给出，`substitute()`发放抛出一个`KeyError`异常（`Mapping key not found`）。`safe_substitute()` 方法捕获该异常，并在文本中保留没有值的变量表达式。

```python
import string

values = {'var': 'foo'}

t = string.Template("$var is here but $missing is not provided")

try:
    print('substitute() :', t.substitute(values))
except KeyError as err:
    print('ERROR:', str(err))
    
print('safe_substitute():', t.safe_substitute(values))

```

```text
ERROR: 'missing'
safe_substitute(): foo is here but $missing is not provided
```

### 1.1.3 Advanced Templates

> The default syntax for `string.Template` can be changed by adjusting the regular expression patterns it uses to find the variable names in the template body. A simple way to do that is to change the `delimiter` and `idpattern` class attributes.

通过调整匹配模板体中变量名称的正则表达式，可以改变`string.Template`的默认语法。一种简单的方法是改变类属性 `delimiter` 和 `idpattern`。见如下例子：

```python
# 1_4_string_template_advanced.py
import string

class MyTemplate(string.Template):
    delimiter = '%'
    idpattern = '[a-z]+_[a-z]+'


template_text = '''
    Delimiter : %%
    Replaced : %with_underscore
    Ignored : %notunderscored
'''


d = {
    'with_underscore': 'replaced',
    'notunderscored': 'not replaced',
}

t = MyTemplate(template_text)
print('Modified ID pattern:')
print(t.safe_substitute(d))
```

```text
Modified ID pattern:

    Delimiter : %
    Replaced : replaced      
    Ignored : %notunderscored
```

> In this example, the substitution rules are changed so that the delimiter is `%` instead of `$` and variable names must include an underscore somewhere in the middle. The pattern `%notunderscored` is not replaced by anything, because it does not include an underscore character.

上面这个例子中，新的替换规则使用`%`而非默认的`$`作为分隔符，并且变量名称中间必须含有一个下划线。因此不含有下划线的`%notunderscored`没有被替换。

> For even more complex changes, it is possible to override the pattern attribute and define an entirely new regular expression. The pattern provided must contain four named groups for capturing the escaped delimiter, the named variable, a braced version of the variable name, and invalid delimiter patterns.

对于更复杂的更改，可以通过覆盖模式属性来并定义一个全新的正则表达式。新定义的模式必须含有四个命名组用于捕获转义的定界符、变量名、大括号版本的变量名称、无效的定界符模式。

> The value of `t.pattern` is a compiled regular expression, but the original string is available via its `pattern` attribute.

从例子中可以看到，`t.pattern`的值是已编译的正则表达式，可以通过`t.pattern.pattern`访问`pattern`参数的原始字符串。


```python
# 1_5_string_template_defaultpattern.py
import string

t = string.Template('$var')
print(t.pattern)
print('*' * 50)
print(t.pattern.pattern)
```

```text
re.compile('\n            \\$(?:\n              (?P<escaped>\\$)  |   # Escape sequence of two delimiters\n              (?P<named>(?a:[_a-z][_a-z0-9]*))       |   # delimiter and a Python identifier\n          , re.IGNORECASE|re.VERBOSE)
**************************************************

            \$(?:
              (?P<escaped>\$)  |   # Escape sequence of two delimiters
              (?P<named>(?a:[_a-z][_a-z0-9]*))       |   # delimiter and a Python identifier
              {(?P<braced>(?a:[_a-z][_a-z0-9]*))} |   # delimiter and a braced identifier   
              (?P<invalid>)             # Other ill-formed delimiter exprs
            )

```


> This example defines a new pattern to create a new type of template, using `{{var}}` as the
variable syntax.

以下的例子定义了一个新的模式来创建一个新的模板类(`MyTemplate`)，并使用`{{var}}`作为可变语法。

> Both the `named` and `braced` patterns must be provided separately, even though they are
the same. Running the sample program generates the following output:

`named` 和 `braced`模式即使相同，也必须单独提供。执行该样例后生成如下结果。

```python
# 1_6_string_template_newsyntax.py
import re
import string

class MyTemplate(string.Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''

t = MyTemplate('''
{{{{
{{var}}
''')

print('MATCHES:', t.pattern.findall(t.template))
print('SUBSTITUTED:', t.safe_substitute(var='replacement'))
```

```text
MATCHES: [('{{', '', '', ''), ('', 'var', '', '')]
SUBSTITUTED: 
{{
replacement
```

### 1.1.4 Formatter

> The `Formatter` class implements the same layout specification language as the `format()` method of `str`. Its features include type coersion, alignment, attribute and field references, named and positional template arguments, and type-specific formatting options. Most of the time the `format()` method is a more convenient interface to these features, but `Formatter` is provided as a way to build subclasses, for cases where variations are needed.

`Formatter`类实现与`str`类的`format()`方法相同的布局规范语言。其特性包括： 类型约束、对齐、属性和字段引用、命名和位置模板参数、以及特定类型的格式选项。大多数时候，对这些特性，`format()`方法是一个更方便的接口，但`Formatter`提供了构建子类型的方式，应对变化的需要。


### 1.1.5 Constants

> The `string` module includes a number of constants related to ASCII and numerical character
sets.

`string` 模块包含了许多与ASCII和数字字符集相关的常量。

> These constants are useful when working with ASCII data, but since it is increasingly common to encounter non-ASCII text in some form of Unicode, their application is limited.

这些常量在处理ASCII数据很有用，但是由于遇到以Unicode形式出现的非ASCII文本越来越普遍，因此他们的应用受到了限制。

```python
# 1_7_string_constants.py
import inspect
import string

def is_str(value):
    return isinstance(value, str)

for name, value in inspect.getmembers(string, is_str):
    if name.startswith('_'):
        continue
    print('%s=%r\n' % (name, value))
```

```text
ascii_letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

ascii_lowercase='abcdefghijklmnopqrstuvwxyz'

ascii_uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

digits='0123456789'

hexdigits='0123456789abcdefABCDEF'

octdigits='01234567'

printable='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'

punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

whitespace=' \t\n\r\x0b\x0c'
```


## 1.2 textwrap: Formatting Text Paragraphs 
格式化文本段落
* Standard library documentation for textwrap. https://docs.python.org/3.5/library/textwrap.html

> The `textwrap` module can be used to format text for output in situations where pretty-printing is desired. It offers programmatic functionality similar to the paragraph wrapping or filling features found in many text editors and word processors.

`textwrap`模块可用于在需要精美印刷的场景下格式化输出文本。它提供的编程功能类似于许多文本编辑器和文字处理器中的段落换行或填充功能

### 1.2.1 Example Data

> The examples in this section use the module `textwrap_example.py`, which contains a string
`sample_text`.

本节中的示例使用模块`textwrap_example.py`，其中包含字符串`sample_text`。

```python
# textwrap_example.py
sample_text = '''
    The textwrap module can be used to format text for output in
    situations where pretty-printing is desired. It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text editors.
'''
```

### 1.2.2 Filling Paragraphs

> The `fill()` function takes text as input and produces formatted text as output.

 `fill()`函数将文本作为输入，并生成格式化的文本作为输出。

```python
import textwrap
from textwrap_example import sample_text

print(textwrap.fill(sample_text, width=50))
```

```text
     The textwrap module can be used to format 
text for output in     situations where pretty-
printing is desired. It offers     programmatic
functionality similar to the paragraph wrapping
or filling features found in many text editors.
```

> The results are something less than desirable. The text is now left justified, but the first line retains its indent and the spaces from the front of each subsequent line are embedded in the paragraph.

结果有些差强人意。现在，该文本左对齐，但是第一行保留缩进，并且每行后面的空格都嵌入到该段落中。


### 1.2.3 Removing Existing Indentation

> The previous example has embedded tabs and extra spaces mixed into the middle of the output, so it is not formatted very cleanly. Removing the common whitespace prefix from all of the lines in the sample text with `dedent()` produces better results and allows the use of docstrings or embedded multiline strings straight from Python code while removing the formatting of the code itself. The sample string has an artificial indent level introduced for illustrating this feature.

前面的示例在输出的中间有嵌入的制表符和多余的空格，因此它的格式不是很整洁。使用`dedent（)`从示例文本的所有行中删除公共空格前缀会产生更好的结果,并且允许直接从Python代码使用文档字符串或嵌入式多行字符串，同时删除代码本身的格式。

```python
# 1_10_textwrap_dedent.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text)
print('Dedented:')
print(dedented_text)

whitespace_sample_text = '''
 Line one.
   Line two.
 Line three.
'''
dedented_whitespace_sample_text = textwrap.dedent(whitespace_sample_text)
print('Before Dedent:')
print(whitespace_sample_text.replace(' ', chr(765)))
print('After Dedent:')
print(dedented_whitespace_sample_text.replace(' ', chr(765)))
```

```text
Dedented:

The textwrap module can be used to format text for output in
situations where pretty-printing is desired. It offers
programmatic functionality similar to the paragraph wrapping
or filling features found in many text editors.

Before Dedent:

˽Line˽one.
˽˽˽Line˽two.
˽Line˽three.

After Dedent:

Line˽one.
˽˽Line˽two.
Line˽three.
```


> Since “dedent” is the opposite of “indent,” the result is a block of text with the common initial whitespace from each line removed. If one line is already indented more than another, some of the whitespace will not be removed.

由于“dedent”与“缩进”相反，其结果删除一个文本块中每行的公共初始空格。

如果一行的缩进量已超过另一行，则某些空格将不会被删除。（不会删除多余的缩进空格）


### 1.2.4 Combining Dedent and Fill

> Next, the dedented text can be passed through `fill()` with a few different `width` values.
> This produces outputs in the specified widths.


消除缩进的文本与一些不同的宽度值传递给`fill()`。产生指定宽度的输出结果。


```python
# 1_11_textwrap_fill_width.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text).strip()
for width in [45, 60]:
    print('{} Columns:\n'.format(width))
    print(textwrap.fill(dedented_text, width=width))
    print()
```

```text
45 Columns:

The textwrap module can be used to format
text for output in situations where pretty-
printing is desired. It offers programmatic
functionality similar to the paragraph
wrapping or filling features found in many
text editors.

60 Columns:

The textwrap module can be used to format text for output in
situations where pretty-printing is desired. It offers
programmatic functionality similar to the paragraph wrapping
or filling features found in many text editors.

```

### 1.2.5 Indenting Blocks
> Use the `indent()` function to add consistent prefix text to all of the lines in a string. This example formats the same example text as though it was part of an email message being quoted in the reply, using `>` as the prefix for each line.

使用`indent（）`函数向字符串中的所有行添加一致的前缀文本。本示例使用与电子邮件答复中被引用的信息相同的示例文本格式，使用“>”作为每行的前缀。

> The block of text is split on newlines, the prefix is added to each line that contains text, and then the lines are combined back into a new string and returned.

文本块在换行符处进行分割，前缀被添加到包含文本的每一行前，然后这些行重新合并成一个新的字符串并返回。

```python
# 1_12_textwrap_indent.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text)
wrapped = textwrap.fill(dedented_text, width=50)
wrapped += '\n\nSecond paragraph after a blank line.'
final = textwrap.indent(wrapped, '> ')

print('Quoted block:\n')
print(final)
```

```text
Quoted block:

>  The textwrap module can be used to format text
> for output in situations where pretty-printing is
> desired. It offers programmatic functionality
> similar to the paragraph wrapping or filling
> features found in many text editors.

> Second paragraph after a blank line.
```

> To control which lines receive the new prefix, pass a callable as the `predicate` argument to `indent()`. The callable will be invoked for each line of text in turn and the prefix will be added for lines where the return value is true.

要控制哪些行接收新前缀，将可调用对象作为谓词参数`predicate`传递给`indent()`。依次为文本的每一行调用谓词判断，并为返回值为true的行添加前缀。

> This example adds the prefix EVEN to lines that contain an even number of characters.

本示例将前缀EVEN添加到包含偶数个字符的行。

```python
# 1_13_textwrap_indent_predicate.py
import textwrap
from textwrap_example import sample_text

def should_indent(line):
    print('Indent {!r}?'.format(line))
    return len(line.strip()) % 2 == 0

dedented_text = textwrap.dedent(sample_text)
wrapped = textwrap.fill(dedented_text, width=50)
final = textwrap.indent(wrapped, 'EVEN ', predicate=should_indent)

print('\nQuoted block:\n')
print(final)
```

```text
Indent ' The textwrap module can be used to format text\n'?
Indent 'for output in situations where pretty-printing is\n'?
Indent 'desired. It offers programmatic functionality\n'?
Indent 'similar to the paragraph wrapping or filling\n'?
Indent 'features found in many text editors.'?

Quoted block:

EVEN  The textwrap module can be used to format text
for output in situations where pretty-printing is
desired. It offers programmatic functionality
EVEN similar to the paragraph wrapping or filling
EVEN features found in many text editors.
```


### 1.2.6 Hanging Indents

> In the same way that it is possible to set the width of the output, the indent of the first line can be controlled independently of subsequent lines.

以可能设置输出宽度的相同方式，可以独立于后续行来控制第一行的缩进。？？？


> This ability makes it possible to produce a hanging indent, where the first line is indented 
less than the other lines.

此功能可以产生悬挂缩进，其中第一行的缩进少于其他行。


```python
# 1_14_textwrap_hanging_indent.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text).strip()
print(textwrap.fill(dedented_text,
                    initial_indent='', 
                    subsequent_indent=' ' * 4, 
                    width=50,
                    ))
```

```text
The textwrap module can be used to format text for
    output in situations where pretty-printing is
    desired. It offers programmatic functionality
    similar to the paragraph wrapping or filling
    features found in many text editors.
```

> The indent values can include non-whitespace characters, too. The hanging indent can be prefixed with * to produce bullet points, for example.

缩进值也可以包含非空格字符。例如，悬挂的缩进可以以*开头，以产生项目要点。


### 1.2.7 Truncating Long Text

> To truncate text to create a summary or preview, use `shorten()`. All existing whitespace, such as tabs, newlines, and series of multiple spaces, will be standardized to a single space. Then the text will be truncated to a length less than or equal to what is requested, between word boundaries so that no partial words are included.

使用`shorten()`来删减文本以创建摘要或预览。所有现有的空白，例如制表符，换行符和一系列的多个空格，都将被标准化为一个空格。然后，文本将在单词边界之间被截断为小于或等于所请求的长度，因此不包括不完整的单词。



```python
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text)
original = textwrap.fill(dedented_text, width=50)

print('Original:\n')
print(original)

shortened = textwrap.shorten(original, 100)
shortened_wrapped = textwrap.fill(shortened, width=50)

print('\nShortened:\n')
print(shortened_wrapped)
```

```text
Original:

 The textwrap module can be used to format text
for output in situations where pretty-printing is
desired. It offers programmatic functionality
similar to the paragraph wrapping or filling
features found in many text editors.

Shortened:

The textwrap module can be used to format text for
output in situations where pretty-printing [...]
```

> If non-whitespace text is removed from the original text as part of the truncation, it is replaced with a placeholder value. The default value `[...]` can be replaced by providing a `placeholder` argument to `shorten()`.

如果作为截断的一部分从原始文本中删除了非空白文本, 将被占位符值替换。默认的占位符值`[...]`可以通过`shorten()`的`placeholder`参数替换。



## 1.3 re: Regular Expressions