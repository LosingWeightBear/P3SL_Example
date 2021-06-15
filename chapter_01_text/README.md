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

> Regular expressions are text matching patterns described with a formal syntax. The patterns are interpreted as a set of instructions, which are then executed with a string as input to produce a matching subset or modified version of the original. The term “regular expressions” is frequently shortened to “regex” or “regexp” in conversation. Expressions can include literal text matching, repetition, pattern composition, branching, and other sophisticated rules. A large number of parsing problems are easier to solve with a regular expression than by creating a special-purpose lexer and parser.

正则表达式是用正式语法描述的文本匹配模式。这些模式被解释为一组说明，然后用字符串作为输入执行，以生成原始字符串的匹配子集或修改版本。术语“正则表达式”在上下文中经常缩写为“regex”或“regexp”。表达式可以包括文字文本匹配、重复、模式组合、分支和其他复杂的规则。与创建特殊用途的词法分析程序和解析器相比，大量解析问题使用正则表达式更容易解决。


> Regular expressions are typically used in applications that involve a lot of text processing. For example, they are commonly used as search patterns in text editing programs used by developers, including vi, emacs, and modern IDEs. They are also an integral part of Unix command-line utilities such as sed, grep, and awk. Many programming languages include support for regular expressions in the language syntax (Perl, Ruby, Awk, and Tcl). Other languages, such as C, C++, and Python, support regular expressions through extension libraries.


正则表达式通常用于处涉及理大量文本的应用中。例如，经常被用于开发人员的文本编辑软件中作为搜索模式，包括vi，emacs，以及现代的那些IDE。它们也是 Unix 命令行实用程序的组成部分，比如sed，grep和awk。许多编程语言在语言语法中包括对正则表达式的支持（Perl, Ruby, Awk, and Tcl）。其他语言通过扩展库支持正则表达式，如C,C++和python。


> Multiple open source implementations of regular expressions exist, each sharing a common core syntax but with different extensions or modifications to their advanced features. The syntax used in Python’s `re` module is based on the syntax used for regular expressions in Perl, with a few Python-specific enhancements.

正则表达式存在多个开源实现，他们公用一个核心语法，但对其他高级功能有不同的扩展或修改。python的`re`模块基于Perl的正则表达式语法，并具有一些 Python 特定的增强功能。


### 1.3.1 Finding Patterns in Text

> The most common use for `re` is to search for patterns in text. The `search()` function takes the pattern and text to scan, and returns a `Match` object when the pattern is found. If the pattern is not found, `search()` returns `None`.
Each `Match` object holds information about the nature of the match, including the original input string, the regular expression used, and the location within the original string where the pattern occurs.

`re` 最常见的用途是在文本中搜索模式。`search()` 函数扫描接受的模式和文本后，并在找到时返回一个 `Match` 对象。如果没有找到模式，返回`None`。

> The `start()` and `end()` methods give the indexes into the string showing where the text
matched by the pattern occurs.

`start()`和`end()`方法给出字符串的索引，显示匹配的文本在字符串中出现的位置。

```python
# 1_16_re_simple_match.py
import re
pattern = 'this'
text = 'Does this text match the pattern?'

match = re.search(pattern, text)

s = match.start()
e = match.end()

print('Found "{}"\nin "{}"\nfrom {} to {} ("{}")'.format(match.re.pattern, match.string, s, e, text[s:e]))
```


```text
Found "this"
in "Does this text match the pattern?"
from 5 to 9 ("this")
```


### 1.3.2 Compiling Expressions
> Although `re` includes module-level functions for working with regular expressions as text strings, it is more efficient to compile the expressions a program uses frequently. The `compile()` function converts an expression string into a `RegexObject`.

尽管 `re` 包含用于将正则表达式作为文本字符串处理的模块级函数，将表达式编译为经常使用的程序会更有效。`compile()` 函数将表达式字符串转换为 `RegexObject`。

> The module-level functions maintain a cache of compiled expressions, but the size of the cache is limited and using compiled expressions directly avoids the overhead associated with cache lookup. Another advantage of using compiled expressions is that by precompiling all of the expressions when the module is loaded, the compilation work is shifted to application start time, instead of occurring at a point where the program may be responding to a user action.

模块级功能维护已编译表达式的高速缓存，但是高速缓存的大小受到限制，并且直接使用已编译表达式可以避免与高速缓存查找相关的开销。使用编译表达式的另一个优点是，通过在加载模块时预编译所有表达式，编译工作转移到应用程序启动时间，而不是发生在程序可能响应用户操作的时刻。


```python
# 1_17_re_simple_compiled.py
import re
# Precompile the patterns.
regexes = [
    re.compile(p)
    for p in ['this', 'that']
]
text = 'Does this text match the pattern?'

print('Text: {!r}\n'.format(text))

for regex in regexes:
    print('Seeking "{}" ->'.format(regex.pattern), end=' ')
    if regex.search(text):
        print('match!')
    else:
        print('no match')
```

```text
Text: 'Does this text match the pattern?'

Seeking "this" -> match!
Seeking "that" -> no match
```

### 1.3.3 Multiple Matches

> So far, the example patterns have all used `search()` to look for single instances of literal text strings. The `findall()` function returns all of the substrings of the input that match the pattern without overlapping.

到目前为止，示例模式都使用了`search()` 来查找文字文本字符串的单个实例。`findall()` 函数返回输入中与模式匹配的所有不重叠的子字符串。

> There are two instances of `ab` in the input string.

输入字符串中有两个 `ab` 实例。

```python
# 1_18_re_findall.py
import re

text = 'abbaaabbbbaaaaa'
pattern = 'ab'

for match in re.findall(pattern, text):
    print('Found {!r}'.format(match))
```

```text
Found 'ab'
Found 'ab'
```

> `finditer()` returns an iterator that produces Match instances instead of the strings returned by `findall()`.

`finditer()` 返回一个迭代器，它产生 Match 实例而不是 `findall()` 返回的字符串。

> This example finds the same two occurrences of `ab`, and the `Match` instance shows where they are found in the original input.

此示例查找到ab出现了两次，并且Match实例显示了它们在原始输入字符串中被找到的位置。

```python
# 1_19_re_finditer.py
import re

text = 'abbaaabbbbaaaaa'

pattern = 'ab'

for match in re.finditer(pattern, text):
    s = match.start()
    e = match.end()
    print('Found {!r} at {:d}:{:d}'.format(text[s:e], s, e))
```

```text
Found 'ab' at 0:2
Found 'ab' at 5:7
```

### 1.3.4 Pattern Syntax
> Regular expressions support more powerful patterns than simple literal text strings. Patterns can repeat, can be anchored to different logical locations within the input, and can be expressed in compact forms that do not require every literal character to be present in the pattern. All of these features are used by combining literal text values with `meta-characters` that are part of the regular expression pattern syntax implemented by `re`.

正则表达式比简单的文字文本字符串支持更强大的模式。模式可以重复，可以锚定到输入中的不同逻辑位置，并且可以用不需要每个文字字符都出现在模式中的紧凑形式表达。所有这些功能都是通过将文字文本值与元字符组合来使用的，元字符是`re`实现的正则表达式模式语法的一部分。

> The following examples use `test_patterns()` to explore how variations in patterns change the way they match the same input text. The output shows the input text and the substring range from each portion of the input that matches the pattern.

以下示例使用`test_patterns()` 来探索模式的变化如何改变它们匹配相同输入文本的方式。 输出结果显示输入的文本和与模式匹配的部分的子字符串范围。


```python
# 1_20_re_test_patterns.py
import re

def test_patterns(text, patterns):
    """Given source text and a list of patterns, look for
    matches for each pattern within the text and print
    them to stdout.
    """
    # Look for each pattern in the text and print the results.
    for pattern, desc in patterns:
        print("'{}' ({})\n".format(pattern, desc))
        print(" '{}'".format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count('\\')
            prefix = '.' * (s + n_backslashes)
            print(" {}'{}'".format(prefix, substr))
        print()
    return

if __name__ == '__main__':
    test_patterns('abbaaabbbbaaaaa',[('ab', "'a' followed by 'b'"),])
```

```text
'ab' ('a' followed by 'b')

 'abbaaabbbbaaaaa'
 'ab'
 .....'ab'

```


#### 1.3.4.1 Repetition

> There are five ways to express repetition in a pattern. A pattern followed by the metacharacter * is repeated zero or more times (allowing a pattern to repeat zero times means it does not need to appear at all to match). If the * is replaced with +, the pattern must appear at least once. Using `?` means the pattern appears zero or one time. For a specific number of occurrences, use `{m}` after the pattern, where `m` is the number of times the pattern should repeat. Finally, to allow a variable but limited number of repetitions, use `{m,n}`, where `m` is the minimum number of repetitions and `n` is the maximum. Leaving out `n` (`{m,}`) means the value must appear at least `m` times, with no maximum.

在模式中有五种方法可以表达重复。模式后的通配符 `*` 表示重复零次或多次（允许模式重复零次意味着它根本不需要出现）。`+`表示模式至少出现一次。`?`表示该模式出现零次或一次。对于特定的出现次数，在模式后使用 `{m}`，其中 `m` 是模式应该重复的次数。最后，要允许可变但有限的重复次数，请使用`{m,n}`，其中`m`是最小重复次数，`n`是最大重复次数。省略`n` (`{m,}`) 意味着匹配的值必须至少出现 `m` 次，没有最大值。

> In this example, there are more matches for `ab*` and `ab?` than `ab+`.

例子中，`ab*` 和 `ab?` 的匹配结果比`ab+`多。



```python
# 1_21_re_repetition.py
from re_test_patterns import test_patterns

test_patterns(
    'abbaabbba',
    [('ab*', 'a followed by zero or more b'),
    ('ab+', 'a followed by one or more b'),
    ('ab?', 'a followed by zero or one b'),
    ('ab{3}', 'a followed by three b'),
    ('ab{2,3}', 'a followed by two to three b')],
)
```

```text
'ab*' (a followed by zero or more b)

 'abbaabbba'
 'abb'      
 ...'a'     
 ....'abbb' 
 ........'a'

'ab+' (a followed by one or more b)

 'abbaabbba'
 'abb'
 ....'abbb'

'ab?' (a followed by zero or one b)

 'abbaabbba'
 'ab'
 ...'a'
 ....'ab'
 ........'a'

'ab{3}' (a followed by three b)

 'abbaabbba'
 ....'abbb'

'ab{2,3}' (a followed by two to three b)

 'abbaabbba'
 'abb'
 ....'abbb'

```


> When processing a repetition instruction, `re` will usually consume as much of the input as possible while matching the pattern. This so-called `greedy` behavior may result in fewer individual matches, or the matches may include more of the input text than intended. Greediness can be turned off by following the repetition instruction with `?`.

在处理重复指令时，`re` 通常会在匹配模式时消耗尽可能多的输入。这种所谓的“贪婪”行为可能会导致更少的单独匹配，或者或者匹配可能包含比预期更多的输入文本。可以通过在重复通配符后使用`?`关闭贪婪模式。

> Disabling greedy consumption of the input for any of the patterns where zero occurrences of `b` are allowed means the matched substring does not include any `b` characters.

对于允许`b` 出现零次的任何模式，禁用输入的贪婪消耗意味着匹配的子字符串不包含任何`b`字符。

```python
# 1_22_re_repetition_non_greedy.py
from re_test_patterns import test_patterns

test_patterns(
    'abbaabbba',
    [('ab*?', 'a followed by zero or more b'),
    ('ab+?', 'a followed by one or more b'),
    ('ab??', 'a followed by zero or one b'),
    ('ab{3}?', 'a followed by three b'),
    ('ab{2,3}?', 'a followed by two to three b')],
)
```

```text
'ab*?' (a followed by zero or more b)

 'abbaabbba'
 'a'
 ...'a'
 ....'a'
 ........'a'

'ab+?' (a followed by one or more b)

 'abbaabbba'
 'ab'
 ....'ab'

'ab??' (a followed by zero or one b)

 'abbaabbba'
 'a'
 ...'a'
 ....'a'
 ........'a'

'ab{3}?' (a followed by three b)

 'abbaabbba'
 ....'abbb'

'ab{2,3}?' (a followed by two to three b)

 'abbaabbba'
 'abb'
 ....'abb'

```


#### 1.3.4.2 Character Sets

> A *character set* is a group of characters, any one of which can match at that point in the pattern. For example, `[ab]` would match either `a` or `b`.

字符集是一组字符，其中任何一个都可以匹配模式中那个位置。例如，`[ab]` 将匹配 `a` 或 `b`。

> The greedy form of the expression (`a[ab]+`) consumes the entire string because the first letter is `a` and every subsequent character is either `a` or `b`.

表达式 (`a[ab]+`) 的贪婪形式会消耗整个字符串，因为第一个字母是 `a`，随后的每个字符都是 `a` 或 `b`。

```python
# 1_23_re_charset.py
from re_test_patterns import test_patterns

test_patterns(
    'abbaabbba',
    [('[ab]', 'either a or b'),
    ('a[ab]+', 'a followed by 1 or more a or b'),
    ('a[ab]+?', 'a followed by 1 or more a or b, not greedy')],
)
```


```text
'[ab]' (either a or b)

 'abbaabbba'
 'a'        
 .'b'       
 ..'b'      
 ...'a'     
 ....'a'    
 .....'b'   
 ......'b'  
 .......'b' 
 ........'a'

'a[ab]+' (a followed by 1 or more a or b)

 'abbaabbba'
 'abbaabbba'

'a[ab]+?' (a followed by 1 or more a or b, not greedy)

 'abbaabbba'
 'ab'
 ...'aa'

```


> A character set can also be used to exclude specific characters. The carat (`^`) means to look for characters that are not in the set following the carat.

字符集还可以用于排除特点字符， 脱字符(`^`) 表示查找不在脱字符之后的集合中的字符。(注：这里`^`符号的英文应该是**caret**，而不是carat)

> This pattern finds all of the substrings that do not contain the characters `-`, `.`, or a space.

此模式查找所有不包含字符 `-`、`.` 或空格的子字符串。

```python
# 1_24_re_charset_exclude.py
from re_test_patterns import test_patterns

test_patterns(
    'This is some text -- with punctuation.',
    [('[^-. ]+', 'sequences without -, ., or space')],
)
```

```text
'[^-. ]+' (sequences without -, ., or space)

 'This is some text -- with punctuation.'
 'This'
 .....'is'
 ........'some'
 .............'text'
 .....................'with'
 ..........................'punctuation'
```

> As character sets grow larger, typing every character that should (or should not) match becomes tedious. A more compact format using *character ranges* can be used to define a character set to include all of the contiguous characters between the specified start and stop points.

随着字符集变得越来越大，键入每个应该（或不应该）匹配的字符变得单调乏味。使用字符范围这一更紧凑的格式，可用于定义字符集以包含指定开始点和停止点之间的所有连续字符。

> Here the range `a-z` includes the lowercase ASCII letters, and the range `A-Z` includes the uppercase ASCII letters. The ranges can also be combined into a single character set.

这里范围`a-z` 包括小写的ASCII字母，范围`A-Z`包括大写的ASCII 字母。多个字符范围也可以合并成一个字符集。

```python
# 1_25_re_charset_ranges.py
from re_test_patterns import test_patterns

test_patterns(
    'This is some text -- with punctuation.',
    [('[a-z]+', 'sequences of lowercase letters'),
    ('[A-Z]+', 'sequences of uppercase letters'),
    ('[a-zA-Z]+', 'sequences of lower- or uppercase letters'),
    ('[A-Z][a-z]+', 'one uppercase followed by lowercase')],
)
```

```text
'[a-z]+' (sequences of lowercase letters)

 'This is some text -- with punctuation.'
 .'his'
 .....'is'
 ........'some'
 .............'text'
 .....................'with'
 ..........................'punctuation'

'[A-Z]+' (sequences of uppercase letters)

 'This is some text -- with punctuation.'
 'T'

'[a-zA-Z]+' (sequences of lower- or uppercase letters)

 'This is some text -- with punctuation.'
 'This'
 .....'is'
 ........'some'
 .............'text'
 .....................'with'
 ..........................'punctuation'

'[A-Z][a-z]+' (one uppercase followed by lowercase)

 'This is some text -- with punctuation.'
 'This'

```

> As a special case of a character set, the meta-character dot, or period (`.`), indicates that the pattern should match any single character in that position.

作为字符集的特殊情况，元字符点, 即句点符 (`.`)， 表示该模式在该位置应该匹配任何单个字符。

> Combining the dot with repetition can result in very long matches, unless the non-greedy form is used.

除非使用非贪婪形式，否则将句点符与重复组合会导致很长的匹配。

```python
# 1_26_re_charset_dot.py
from re_test_patterns import test_patterns

test_patterns(
    'abbaabbba',
    [('a.', 'a followed by any one character'),
    ('b.', 'b followed by any one character'),
    ('a.*b', 'a followed by anything, ending in b'),
    ('a.*?b', 'a followed by anything, ending in b')],
)
```

```text
'a.' (a followed by any one character)

 'abbaabbba'
 'ab'
 ...'aa'

'b.' (b followed by any one character)
\\
 'abbaabbba'
 .'bb'
 .....'bb'
 .......'ba'

'a.*b' (a followed by anything, ending in b)

 'abbaabbba'
 'abbaabbb'

'a.*?b' (a followed by anything, ending in b)

 'abbaabbba'
 'ab'
 ...'aab'

```


#### 1.3.4.3 Escape Codes

> An even more compact representation uses escape codes for several predefined character sets. The escape codes recognized by `re` are listed in Table 1.1.

使用转义码可以更简洁的表示一些预定义的字符集。`re`可识别的转义码如下：


|Code|Meaning| |
|--|--|--|
| `\d` | A digit | 数字 |
| `\D` | A non-digit | 非数字 |
| `\s` | Whitespace (tab, space, newline, etc.) | 空白（制表符、空格、换行等） | `\S` | Non-whitespace | 非空 |
| `\w` | Alphanumeric | 字母数字 |
| `\W` | Non-alphanumeric | 非字母数字 |

> Escapes are indicated by prefixing the character with a backslash (`\`). Unfortunately, a backslash must itself be escaped in normal Python strings, and that results in difficult-to-read expressions. Using raw strings, which are created by prefixing the literal value with `r`, eliminates this problem and maintains readability.

在字符前加上反斜杠 (`\`) 来表示转义。不幸的是，反斜杠本身必须在普通 Python 字符串中进行转义，这会导致难以阅读的表达式。通过在文字值前面加上 `r` 来创建原始字符串，可以消除这个问题并保持代码的可读性。

> These sample expressions combine escape codes with repetition to find sequences of like characters in the input string.

这些示例表达式将转义码与重复组合在一起，以查找输入字符串中相似的字符序列。

```python
# 1_27_re_escape_codes.py
from re_test_patterns import test_patterns

test_patterns(
    'A prime #1 example!',
    [(r'\d+', 'sequence of digits'),
    (r'\D+', 'sequence of non-digits'),
    (r'\s+', 'sequence of whitespace'),
    (r'\S+', 'sequence of non-whitespace'),
    (r'\w+', 'alphanumeric characters'),
    (r'\W+', 'non-alphanumeric')],
)
```

```text
'\d+' (sequence of digits)

 'A prime #1 example!'        
 .........'1'

'\D+' (sequence of non-digits)

 'A prime #1 example!'
 'A prime #'
 ..........' example!'

'\s+' (sequence of whitespace)

 'A prime #1 example!'
 .' '
 .......' '
 ..........' '

'\S+' (sequence of non-whitespace)

 'A prime #1 example!'
 'A'
 ..'prime'
 ........'#1'
 ...........'example!'

'\w+' (alphanumeric characters)

 'A prime #1 example!'
 'A'
 ..'prime'
 .........'1'
 ...........'example'

'\W+' (non-alphanumeric)

 'A prime #1 example!'
 .' '
 .......' #'
 ..........' '
 ..................'!'
```

> To match the characters that are part of the regular expression syntax, escape the characters in the search pattern.

要匹配作为正则表达式语法一部分的字符，请对搜索模式中的字符进行转义。

> The pattern in this example escapes the backslash and plus characters, since both are meta-characters and have special meaning in a regular expression.

此示例中的模式转义了反斜纹和加号，因为两者都是元字符，在常规表达中具有特殊含义。

```python
# 1_28_re_escape_escapes.py
from re_test_patterns import test_patterns

test_patterns(
    r'\d+ \D+ \s+',
    [(r'\\.\+', 'escape code')],
)
```

```text
'\\.\+' (escape code)

 '\d+ \D+ \s+'
 '\d+'
 .....'\D+'
 ..........'\s+'
```


#### 1.3.4.4 Anchoring

> In addition to describing the content of a pattern to match, the relative location can be specified in the input text where the pattern should appear by using anchoring instructions. Table 1.2 lists valid anchoring codes.

除了描述要匹配的模式的内容外，还可以在输入文本中通过锚定指令指定模式应该出现的相关位置。表1.2 列出了有效的锚定代码。

|Code|Meaning||
|--|--|--|
| `^` | Start of string, or line | 字符串或行的开始 |
| `$` | End of string, or line| 字符串或行的末尾 |
| `\A` | Start of string | 字符串开始 |
| `\Z` | End of string | 字符串末尾 |
| `\b` | Empty string at the beginning or end of a word | 单词开头或结尾的空字符串 |
| `\B` | Empty string not at the beginning or end of a word | 不在单词的开头或结尾的空字符串 |

> The patterns in the example for matching words at the beginning and the end of the string are different because the word at the end of the string is followed by punctuation to terminate the sentence. The pattern `\w+$` would not match, since `.` is not considered an alphanumeric character.

示例中，在字符串开头和末尾匹配单词的模式不同，因为在字符串末尾的单词后面跟着标点符号来终止句子。模式`\w+$`将不匹配，因为`.`不被视为字母数字字符。

```python
# 1_29_re_anchoring.py
from re_test_patterns import test_patterns

test_patterns(
    'This is some text -- with punctuation.',
    [(r'^\w+', 'word at start of string'),
    (r'\A\w+', 'word at start of string'),
    (r'\w+\S*$', 'word near end of string'),
    (r'\w+\S*\Z', 'word near end of string'),
    (r'\w*t\w*', 'word containing t'),
    (r'\bt\w+', 't at start of word'),
    (r'\w+t\b', 't at end of word'),
    (r'\Bt\B', 't, not start or end of word')],
)
```

```text
'^\w+' (word at start of string)

 'This is some text -- with punctuation.'
 'This'

'\A\w+' (word at start of string)

 'This is some text -- with punctuation.'
 'This'

'\w+\S*$' (word near end of string)

 'This is some text -- with punctuation.'
 ..........................'punctuation.'

'\w+\S*\Z' (word near end of string)

 'This is some text -- with punctuation.'
 ..........................'punctuation.'

'\w*t\w*' (word containing t)

 'This is some text -- with punctuation.'
 .............'text'
 .....................'with'
 ..........................'punctuation'

'\bt\w+' (t at start of word)

 'This is some text -- with punctuation.'
 .............'text'

'\w+t\b' (t at end of word)

 'This is some text -- with punctuation.'
 .............'text'

'\Bt\B' (t, not start or end of word)

 'This is some text -- with punctuation.'
 .......................'t'
 ..............................'t'
 .................................'t'

```



### 1.3.5 Constraining the Search

> In situations where it is known in advance that only a subset of the full input should be searched, the regular expression match can be further constrained by telling `re` to limit the search range. For example, if the pattern must appear at the front of the input, then using `match()` instead of `search()` will anchor the search without having to explicitly include an
anchor in the search pattern.

如果事先知道只应搜索完整输入的子集，则可以通过告诉`re`限制搜索范围来进一步限制正则表达式匹配。例如，如果模式必须出现在输入的前面，则使用`match()`而不是`search()`将锚定搜索，而不必在搜索模式中明确包含锚点。

> Since the literal text `is` does not appear at the start of the input text, it is not found using `match()`. The sequence appears two other times in the text, though, so `search()` finds it.

由于输入文本开头没有显示字面文本`is`，因此不会使用`match()`找到。不过，该序列在文本中还显示了另外两次，因此`search()`会找到它。

```python
# 1_30_re_match.py
import re

text = 'This is some text -- with punctuation.'
pattern = 'is'

print('Text :', text)
print('Pattern:', pattern)

m = re.match(pattern, text)
print('Match :', m)
s = re.search(pattern, text)
print('Search :', s)
```

```text
Text : This is some text -- with punctuation.
Pattern: is
Match : None
Search : <re.Match object; span=(2, 4), match='is'>
```



> The `fullmatch()` method requires that the entire input string match the pattern.

`fullmatch()`方法要求整个输入字符串与模式匹配。

> Here `search()` shows that the pattern does appear in the input, but it does not consume all of the input so `fullmatch()` does not report a match.

本例中`search()`显示模式确实出现在输入中，但它不消耗所有的输入，所以`fullmatch()`不报告匹配。

```python
# 1_31_re_fullmatch.py
import re

text = 'This is some text -- with punctuation.'
pattern = 'is'

print('Text :', text)
print('Pattern :', pattern)

m = re.search(pattern, text)
print('Search :', m)

s = re.fullmatch(pattern, text)
print('Full match :', s)
```

```text
Text : This is some text -- with punctuation.
Pattern : is
Search : <re.Match object; span=(2, 4), match='is'>
Full match : None
```


> The `search()` method of a compiled regular expression accepts optional start and end position parameters to limit the search to a substring of the input.

编译后的正则表达式的`search()`方法接受可选的开始和结束位置参数，以将搜索限制为输入的子字符串。


> This example implements a less efficient form of `iterall()`. Each time a match is found, the end position of that match is used for the next search.

此示例实现了效率较低的`iterall()`。每次找到匹配项时，该匹配的最终位置被用于下一次搜索。


```python
# 1_32_re_search_substring.py
import re

text = 'This is some text -- with punctuation.'
pattern = re.compile(r'\b\w*is\w*\b')

print('Text:', text)
print()

pos = 0
while True:
    match = pattern.search(text, pos)
    if not match:
        break
    s = match.start()
    e = match.end()
    print(' {:>2d} : {:>2d} = "{}"'.format(s, e - 1, text[s:e]))
    # Move forward in text for the next search.
    pos = e
```

```text
Text: This is some text -- with punctuation.

  0 :  3 = "This"
  5 :  6 = "is"
```


### 1.3.6 Dissecting Matches with Groups

> Searching for pattern matches is the basis of the powerful capabilities provided by regular expressions. Adding *groups* to a pattern isolates parts of the matching text, expanding those capabilities to create a parser. Groups are defined by enclosing patterns in parentheses.

搜索模式匹配是正则表达式提供的强大功能的基础。将组添加到模式可以隔离匹配文本的部分，扩展这些功能以创建解析器。组是通过将模式括在括号中来定义的。

> Any complete regular expression can be converted to a group and nested within a larger expression. All of the repetition modifiers can be applied to a group as a whole, requiring the entire group pattern to repeat.

任何完整的正则表达式均可以转换为组并嵌套在更大的表达式中。所有重复修饰符都可以作为一个整体应用于一个组，需要整个组模式重复。



```python
# 1_33_re_groups.py
from re_test_patterns import test_patterns

test_patterns(
    'abbaaabbbbaaaaa',
    [('a(ab)', 'a followed by literal ab'),
    ('a(a*b*)', 'a followed by 0-n a and 0-n b'),
    ('a(ab)*', 'a followed by 0-n ab'),
    ('a(ab)+', 'a followed by 1-n ab')],
)
```

```text
'a(ab)' (a followed by literal ab)

 'abbaaabbbbaaaaa'
 ....'aab'

'a(a*b*)' (a followed by 0-n a and 0-n b)

 'abbaaabbbbaaaaa'
 'abb'
 ...'aaabbbb'
 ..........'aaaaa'

'a(ab)*' (a followed by 0-n ab)

 'abbaaabbbbaaaaa'
 'a'
 ...'a'
 ....'aab'
 ..........'a'
 ...........'a'
 ............'a'
 .............'a'
 ..............'a'

'a(ab)+' (a followed by 1-n ab)

 'abbaaabbbbaaaaa'
 ....'aab'

```


> To access the substrings matched by the individual groups within a pattern, use the `groups()`
method of the `Match` object.

要访问模式中各个组匹配的子字符串，使用`Match`对象的`groups()`方法。

> `Match.groups()` returns a sequence of strings in the order of the groups within the
expression that matches the string.

`Match.groups()`按照表达式中与字符串匹配的组的顺序返回字符串序列。

```python
# 1_34_re_groups_match.py
import re

text = 'This is some text -- with punctuation.'

print(text)
print()

patterns = [
    (r'^(\w+)', 'word at start of string'),
    (r'(\w+)\S*$', 'word at end, with optional punctuation'),
    (r'(\bt\w+)\W+(\w+)', 'word starting with t, another word'),
    (r'(\w+t)\b', 'word ending with t'),
]

for pattern, desc in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}' ({})\n".format(pattern, desc))
    print(' ', match.groups())
    print()
```

```text
This is some text -- with punctuation.

'^(\w+)' (word at start of string)

  ('This',)

'(\w+)\S*$' (word at end, with optional punctuation)

  ('punctuation',)

'(\bt\w+)\W+(\w+)' (word starting with t, another word)

  ('text', 'with')

'(\w+t)\b' (word ending with t)

  ('text',)

```


> To ask for the match of a single group, use the `group()` method. This is useful when grouping is being used to find parts of the string, but some of the parts matched by groups are not needed in the results.

要请求单个组的匹配，请使用 `group()` 方法。这在使用分组查找字符串部分时很有用，但结果中不需要某些与组匹配的部分。


> Group `0` represents the string matched by the entire expression, and subgroups are numbered starting with `1` in the order that their left parenthesis appears in the expression.

组“0”代表整个表达式匹配的字符串，子组从“1”开始按其左括号出现在表达式中的顺序编号。


```python
# 1_35_re_groups_individual.py
import re

text = 'This is some text -- with punctuation.'

print('Input text :', text)

# Word starting with 't' then another word
regex = re.compile(r'(\bt\w+)\W+(\w+)')
print('Pattern :', regex.pattern)

match = regex.search(text)
print('Entire match :', match.group(0))
print('Word starting with "t":', match.group(1))
print('Word after "t" word :', match.group(2))
```


```text
Input text : This is some text -- with punctuation.
Pattern : (\bt\w+)\W+(\w+)
Entire match : text -- with
Word starting with "t": text
Word after "t" word : with
```


> Python extends the basic grouping syntax to add named groups. Using names to refer to groups makes it easier to modify the pattern over time, without having to also modify the code using the match results. To set the name of a group, use the syntax (`?P<name>pattern`).

Python 扩展了基本分组语法以添加命名组。使用名称来引用组可以更轻松地随时间修改模式，而不必在使用匹配结果时修改代码。使用如下语法设置组名字：`?P<name>pattern`。

> Use `groupdict()` to retrieve the dictionary mapping group names to substrings from the match. Named patterns are included in the ordered sequence returned by `groups()` as well.

使用`groupdict()` 从匹配中检索将组名映射到子字符串的字典。命名模式也包含在`groups()` 返回的有序序列中。



```python
# 1_36_re_groups_named.py
import re

text = 'This is some text -- with punctuation.'

print(text)

print()
patterns = [
    r'^(?P<first_word>\w+)',
    r'(?P<last_word>\w+)\S*$',
    r'(?P<t_word>\bt\w+)\W+(?P<other_word>\w+)',
    r'(?P<ends_with_t>\w+t)\b',
]

for pattern in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}'".format(pattern))
    print(' ', match.groups())
    print(' ', match.groupdict())
    print()
```


```text
This is some text -- with punctuation.

'^(?P<first_word>\w+)'
  ('This',)
  {'first_word': 'This'}

'(?P<last_word>\w+)\S*$'
  ('punctuation',)
  {'last_word': 'punctuation'}

'(?P<t_word>\bt\w+)\W+(?P<other_word>\w+)'
  ('text', 'with')
  {'t_word': 'text', 'other_word': 'with'}

'(?P<ends_with_t>\w+t)\b'
  ('text',)
  {'ends_with_t': 'text'}

```


> An updated version of `test_patterns()` that shows the numbered and named groups matched by a pattern will make the following examples easier to follow.

显示与模式匹配的编号和命名组的`test_patterns()`的更新版本将使以下示例更容易理解。


```python
# re_test_patterns.py
import re

def test_patterns(text, patterns):
    """Given source text and a list of patterns, look for
    matches for each pattern within the text and print
    them to stdout.
    """
    # Look for each pattern in the text and print the results.
    for pattern, desc in patterns:
        print('{!r} ({})\n'.format(pattern, desc))
        print(' {!r}'.format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            prefix = ' ' * (s)
            print(' {}{!r}{} '.format(prefix,text[s:e],' ' * (len(text) - e)),end=' ',)
            print(match.groups())
            if match.groupdict():
                print('{}{}'.format(' ' * (len(text) - s),match.groupdict()),)
        print()
    return

```

> Since a group is itself a complete regular expression, groups can be nested within other
groups to build even more complicated expressions.

由于组本身就是一个完整的正则表达式，因此组可以嵌套在其他组中以构建更复杂的表达式。

> In this case, the group (`a*`) matches an empty string, so the return value from `groups()` includes that empty string as the matched value.

在这种情况下，组 (`a*`) 匹配一个空字符串，因此`groups()`的返回值包括该空字符串作为匹配值。

```python
# 1_38_re_groups_nested.py
from re_test_patterns_groups import test_patterns

test_patterns(
    'abbaabbba',
    [(r'a((a*)(b*))', 'a followed by 0-n a and 0-n b')],
)
```

```text
'a((a*)(b*))' (a followed by 0-n a and 0-n b)

 'abbaabbba'
 'abb'        ('bb', '', 'bb')
    'aabbb'   ('abbb', 'a', 'bbb')
         'a'  ('', '', '')

```


> Groups are also useful for specifying alternative patterns. Use the pipe symbol (`|`) to indicate that either pattern should match. Consider the placement of the pipe carefully, though. The first expression in this example matches a sequence of `a` followed by a sequence consisting entirely of a single letter, `a` or `b`. The second pattern matches `a` followed by a sequence that may include either `a` or `b`. The patterns are similar, but the resulting matches are completely different.

组对于指定替代模式也很有用。使用竖线符号 (`|`) 表示任一模式都应匹配。仔细考虑管道的放置。此示例中的第一个表达式匹配一个序列“a”，后跟一个完全由单个字母“a”或“b”组成的序列。第二个模式匹配 `a` 后跟一个可能包含 `a` 或 `b` 的序列。模式相似，但结果匹配完全不同。


> When an alternative group is not matched, but the entire pattern does match, the return value of `groups()` includes a `None` value at the point in the sequence where the alternative group should appear.

当替代组不匹配，但整个模式确实匹配时，`groups()` 的返回值在替代组应该出现的序列点处包括一个 `None` 值。


```python
# 1_39_re_groups_alternative.py
from re_test_patterns_groups import test_patterns

test_patterns(
    'abbaabbba',
    [(r'a((a+)|(b+))', 'a then seq. of a or seq. of b'),
    (r'a((a|b)+)', 'a then seq. of [ab]')],
)
```

```text
'a((a+)|(b+))' (a then seq. of a or seq. of b)

 'abbaabbba'
 'abb'        ('bb', None, 'bb') 
    'aa'      ('a', 'a', None)   

'a((a|b)+)' (a then seq. of [ab])

 'abbaabbba'
 'abbaabbba'  ('bbaabbba', 'a')  

```


> Defining a group containing a subpattern is also useful in cases where the string matching the subpattern is not part of what should be extracted from the full text. These kinds of groups are called non-capturing. Non-capturing groups can be used to describe repetition patterns or alternatives, without isolating the matching portion of the string in the value returned. To create a non-capturing group, use the syntax (`?:pattern`).

在匹配子模式的字符串不是应从全文中提取的内容的一部分的情况下，定义包含子模式的组也很有用。这些类型的组称为非捕获组。非捕获组可用于描述重复模式或替代方案，而无需隔离返回值中字符串的匹配部分。要创建非捕获组，使用语法`?:pattern`。

> In the following example, compare the groups returned for the capturing and noncapturing forms of a pattern that matches the same results.

通过以下示例中，比较捕获和非捕获形式返回的组匹配相同结果的。

```python
# 1_40_re_groups_noncapturing.py
from re_test_patterns_groups import test_patterns

test_patterns(
    'abbaabbba',
    [(r'a((a+)|(b+))', 'capturing form'),
    (r'a((?:a+)|(?:b+))', 'noncapturing')],
)
```


```text
'a((a+)|(b+))' (capturing form)

 'abbaabbba'
 'abb'        ('bb', None, 'bb')
    'aa'      ('a', 'a', None)

'a((?:a+)|(?:b+))' (noncapturing)

 'abbaabbba'
 'abb'        ('bb',)
    'aa'      ('a',)

```


### 1.3.7 Search Options

> Option flags are used to change the way the matching engine processes an expression. The flags can be combined using a bitwise OR operation, then passed to `compile()`, `search()`, `match()`, and other functions that accept a pattern for searching.
 
选项标志用于更改匹配引擎处理表达式的方式。这些标志可以使用按位 OR 操作组合，然后传递给 `compile()`、`search()`、`match()` 和其他接受模式进行搜索的函数。

#### 1.3.7.1 Case-Insensitive Matching

> **IGNORECASE** causes literal characters and character ranges in the pattern to match both uppercase and lowercase characters.

IGNORECASE使模式中的文字字符和字符范围同时匹配大写和小写字符。

> Since the pattern includes the literal `T`, if **IGNORECASE** is not set, the only match is the word `This`. When case is ignored, `text` also matches.

由于模式包含文字`T`，如果未设置IGNORECASE，则唯一匹配的是单词`This`当忽略大小写时，`text` 也匹配。

```python
# 1_41_re_flags_ignorecase.py
import re

text = 'This is some text -- with punctuation.'
pattern = r'\bT\w+'
with_case = re.compile(pattern)
without_case = re.compile(pattern, re.IGNORECASE)

print('Text:\n {!r}'.format(text))
print('Pattern:\n {}'.format(pattern))
print('Case-sensitive:')
for match in with_case.findall(text):
    print(' {!r}'.format(match))
print('Case-insensitive:')
for match in without_case.findall(text):
    print(' {!r}'.format(match))
```

```text
Text:
 'This is some text -- with punctuation.'
Pattern:
 \bT\w+
Case-sensitive:
 'This'
Case-insensitive:
 'This'
 'text'
```

#### 1.3.7.2 Input with Multiple Lines

> Two flags affect how searching in multiline input works: **MULTILINE** and **DOTALL**. The
**MULTILINE** flag controls how the pattern matching code processes anchoring instructions
for text containing newline characters. When multiline mode is turned on, the anchor rules
for `^` and `$` apply at the beginning and end of each line, in addition to the entire string.

有两个标志会影响在多行输入中搜索的工作方式：**MULTILINE** 和 **DOTALL**。**MULTILINE** 标志控制模式匹配代码如何处理包含换行符的文本的锚定指令。当打开多行模式时，`^` 和 `$` 的锚规则适用于每行的开头和结尾，以及整个字符串。

> The pattern in the example matches the first or last word of the input. It matches `line.` at the end of the string, even though there is no newline.

示例中的模式匹配输入的第一个或最后一个单词。它匹配字符串末尾的 `line.`，即使没有换行符。

```python
# 1_42_re_flags_multiline.py
import re

text = 'This is some text -- with punctuation.\nA second line.'
pattern = r'(^\w+)|(\w+\S*$)'
single_line = re.compile(pattern)
multiline = re.compile(pattern, re.MULTILINE)

print('Text:\n {!r}'.format(text))
print('Pattern:\n {}'.format(pattern))
print('Single Line :')
for match in single_line.findall(text):
    print(' {!r}'.format(match))
print('Multline :')
for match in multiline.findall(text):
    print(' {!r}'.format(match))
```


```text
Text:
 'This is some text -- with punctuation.\nA second line.'
Pattern:
 (^\w+)|(\w+\S*$)
Single Line :
 ('This', '')
 ('', 'line.')
Multline :
 ('This', '')
 ('', 'punctuation.')
 ('A', '')
 ('', 'line.')
```

> **DOTALL** is the other flag related to multiline text. Normally, the dot character (`.`) matches everything in the input text except a newline character. The flag allows the dot to match newlines as well.

**DOTALL** 是另一个与多行文本相关的标志。通常，点字符 (`.`) 匹配输入文本中除换行符之外的所有内容。该标志也允许点匹配换行符。

> Without the flag, each line of the input text matches the pattern separately. Adding the flag causes the entire string to be consumed.

如果没有标志，输入文本的每一行都分别与模式匹配。添加标志会导致消耗整个字符串。


```python
# 1_43_re_flags_dotall.py
import re

text = 'This is some text -- with punctuation.\nA second line.'
pattern = r'.+'
no_newlines = re.compile(pattern)
dotall = re.compile(pattern, re.DOTALL)

print('Text:\n {!r}'.format(text))
print('Pattern:\n {}'.format(pattern))
print('No newlines :')
for match in no_newlines.findall(text):
    print(' {!r}'.format(match))
print('Dotall :')
for match in dotall.findall(text):
    print(' {!r}'.format(match))
```


```text
Text:
 'This is some text -- with punctuation.\nA second line.'
Pattern:
 .+
No newlines :
 'This is some text -- with punctuation.'
 'A second line.'
Dotall :
 'This is some text -- with punctuation.\nA second line.'
```


#### 1.3.7.3 Unicode

> Under Python 3, `str` objects use the full Unicode character set, and regular expression processing on a `str` assumes that the pattern and input text are both Unicode. The escape codes described earlier are defined in terms of Unicode by default. Those assumptions mean that the pattern `\w+` will match both the words “French” and “Français”. To restrict escape codes to the ASCII character set, as was the default in Python 2, use the `ASCII` flag when compiling the pattern or when calling the module-level functions `search()` and `match()`.

在 Python 3 下，`str` 对象使用完整的 Unicode 字符集，并且对 `str` 的正则表达式处理假定模式和输入文本都是 Unicode。默认情况下，前面描述的转义码是根据 Unicode 定义的。这些假设意味着模式`\w+` 将匹配单词“French”和“Français”。要将转义码限制为 ASCII 字符集，这是 Python 2 中的默认设置，请在编译模式或调用模块级函数 `search()` 和 `match()` 时使用 `ASCII` 标志。


> The other escape sequences (`\W`, `\b`, `\B`, `\d`, `\D`, `\s`, and `\S`) are also processed differently for ASCII text. Instead of consulting the Unicode database to find the properties of each character, `re` uses the `ASCII` definition of the character set identified by the escape sequence.

对于 ASCII 文本，其他转义序列（`\W`、`\b`、`\B`、`\d`、`\D`、`\s` 和 `\S`）也有不同的处理方式。`re` 不是通过查询 Unicode 数据库来查找每个字符的属性，而是使用由转义序列标识的字符集的 `ASCII` 定义。

```python
# 1_44_re_flags_ascii.py
import re

text = u'Français łzoty Österreich'
pattern = r'\w+'
ascii_pattern = re.compile(pattern, re.ASCII)
unicode_pattern = re.compile(pattern)

print('Text :', text)
print('Pattern :', pattern)
print('ASCII :', list(ascii_pattern.findall(text)))
print('Unicode :', list(unicode_pattern.findall(text)))
```

```text
Text : Français łzoty Österreich
Pattern : \w+
ASCII : ['Fran', 'ais', 'zoty', 'sterreich'] 
Unicode : ['Français', 'łzoty', 'Österreich']
```


#### 1.3.7.4 Verbose Expression Syntax

> The compact format of regular expression syntax can become a hindrance as expressions grow more complicated. As the number of groups in an expression increases, it will be more work to keep track of why each element is needed and how exactly the parts of the expression interact. Using named groups helps mitigate these issues, but a better solution is to use *verbose mode expressions*, which allow comments and extra whitespace to be embedded in the pattern.

> A pattern to validate email addresses will illustrate how verbose mode makes working with regular expressions easier. The first version recognizes addresses that end in one of three top-level domains: `.com`, `.org`, or `.edu`.


随着表达式变得越来越复杂，正则表达式语法的紧凑格式可能会成为一个障碍。随着表达式中组数的增加，跟踪为什么需要每个元素以及表达式的各个部分如何准确交互将需要更多的工作。使用命名组有助于缓解这些问题，但更好的解决方案是使用*详细模式表达式*，它允许在模式中嵌入注释和额外的空格。

验证电子邮件地址的模式将说明详细模式如何使使用正则表达式更容易。第一个版本识别以三个顶级域之一结尾的地址：`.com`、`.org` 或`.edu`。

> This expression is already complex. There are several character classes, groups, and repetition expressions.

这个表达已经很复杂了。有多个字符类、组和重复表达式。

```python
# 1_45_re_email_compact.py
import re
address = re.compile('[\w\d.+-]+@([\w\d.]+\.)+(com|org|edu)')

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
]
for candidate in candidates:
    match = address.search(candidate)
    print('{:<30} {}'.format(candidate, 'Matches' if match else 'No match'))
```

```text
first.last@example.com         Matches
first.last+category@gmail.com  Matches
valid-address@mail.example.com Matches
not-valid@example.foo          No match
```


> Converting the expression to a more verbose format will make it easier to extend.

将表达式转换为更详细的格式将使其更易于扩展。

> The expression matches the same inputs, but in this extended format it is easier to read. The comments also help identify different parts of the pattern so that it can be expanded to match more inputs.

该表达式匹配相同的输入，但在这种扩展格式中更易于阅读。注释还有助于识别模式的不同部分，以便可以对其进行扩展以匹配更多输入。

```python
# 1_46_re_email_verbose.py
import re

address = re.compile(
    '''
    [\w\d.+-]+ # Username
    @
    ([\w\d.]+\.)+ # Domain name prefix
    (com|org|edu) # TODO: support more top-level domains
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
]

for candidate in candidates:
    match = address.search(candidate)
    print('{:<30} {}'.format(candidate, 'Matches' if match else 'No match'),)
```


```text
first.last@example.com         Matches
first.last+category@gmail.com  Matches      
valid-address@mail.example.com Matches      
not-valid@example.foo          No match 
```


> This expanded version parses inputs that include a person’s name and email address, as might appear in an email header. The name comes first and stands on its own, and the email address follows, surrounded by angle brackets (`<` and `>`).

此扩展版本解析包含个人姓名和电子邮件地址的输入，这些输入可能会出现在电子邮件标题中。名称首先出现并独立存在，然后是电子邮件地址，并用尖括号（`<` 和 `>`）括起来。

> As with other programming languages, the ability to insert comments into verbose regular expressions helps with their maintainability. This final version includes implementation notes to future maintainers and whitespace to separate the groups from each other and highlight their nesting level.

与其他编程语言一样，在冗长的正则表达式中插入注释的能力有助于它们的可维护性。这个最终版本包括对未来维护者的实现说明和空格，以将组彼此分开并突出它们的嵌套级别。

```python
# 1_47_re_email_with_name.py
import re

address = re.compile(
    '''
    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    ((?P<name>
    ([\w.,]+\s+)*[\w.,]+)
    \s*
    # Email addresses are wrapped in angle
    # brackets < >, but only if a name is
    # found, so keep the start bracket in this
    # group.
    <
    )? # The entire name is optional.
    # The address itself: username@domain.tld
    (?P<email>
    [\w\d.+-]+ # Username
    @
    ([\w\d.]+\.)+ # Domain name prefix
    (com|org|edu) # Limit the allowed top-level domains.
    )
    >? # Optional closing angle bracket.
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'First Last',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
    u'<first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print(' Name :', match.groupdict()['name'])
        print(' Email:', match.groupdict()['email'])
    else:
        print(' No match')
```

```text
Candidate: first.last@example.com
 Name : None
 Email: first.last@example.com
Candidate: first.last+category@gmail.com 
 Name : None
 Email: first.last+category@gmail.com    
Candidate: valid-address@mail.example.com
 Name : None
 Email: valid-address@mail.example.com
Candidate: not-valid@example.foo
 No match
Candidate: First Last <first.last@example.com>
 Name : First Last
 Email: first.last@example.com
Candidate: No Brackets first.last@example.com
 Name : None
 Email: first.last@example.com
Candidate: First Last
 No match
Candidate: First Middle Last <first.last@example.com>
 Name : First Middle Last
 Email: first.last@example.com
Candidate: First M. Last <first.last@example.com>
 Name : First M. Last
 Email: first.last@example.com
Candidate: <first.last@example.com>
 Name : None
 Email: first.last@example.com
```


#### 1.3.7.5 Embedding Flags in Patterns

> In situations where flags cannot be added when compiling an expression, such as when a pattern is passed as an argument to a library function that will compile it later, the flags can be embedded inside the expression string itself. For example, to turn case-insensitive matching on, add (`?i`) to the beginning of the expression.

在编译表达式时无法添加标志的情况下，例如当模式作为参数传递给稍后将编译它的库函数时，可以将标志嵌入表达式字符串本身中。例如，要打开不区分大小写的匹配，将 (`?i`) 添加到表达式的开头。


> Because the options control the way the entire expression is evaluated or parsed, they should always appear at the beginning of the expression.

由于选项控制整个表达式的求值或解析方式，因此它们应始终出现在表达式的开头。


```python
# 1_48_re_flags_embedded.py
import re

text = 'This is some text -- with punctuation.'
pattern = r'(?i)\bT\w+'
regex = re.compile(pattern)

print('Text :', text)
print('Pattern :', pattern)
print('Matches :', regex.findall(text))
```

```text
Text : This is some text -- with punctuation.
Pattern : (?i)\bT\w+
Matches : ['This', 'text']
```


> The abbreviations for all of the flags are listed in Table 1.3. (Table 1.3: Regular Expression Flag
Abbreviations)
Embedded flags can be combined by placing them within the same group. For example, (`?im`) turns on case-insensitive matching for multiline strings.

嵌入的标志可以通过将它们放在同一组中来组合。例如， (`?im`) 为多行字符串打开不区分大小写的匹配。


|Flag|Abbreviation|
|----| :----: |
|ASCII|a|
|IGNORECASE|i|
|MULTILINE|m|
|DOTALL|s|
|VERBOSE|x|


### 1.3.8 Looking Ahead or Behind

> In many cases, it is useful to match a part of a pattern only if some other part will also match. For example, in the email parsing expression, the angle brackets were marked as optional. Realistically, the brackets should be paired, and the expression should match only if both are present, or neither is. This modified version of the expression uses a positive look ahead assertion to match the pair. The look ahead assertion syntax is (`?=pattern`).

在许多情况下，仅当其他部分也匹配时才匹配模式的一部分是有用的。例如，在电子邮件解析表达式中，尖括号被标记为可选。实际上，括号应该成对出现，并且表达式应该只在两者都存在或都不存在时匹配。该表达式的修改版本使用积极的前瞻断言来匹配该对。前瞻断言语法是 (`?=pattern`)。

> There are several important changes in this version of the expression. First, the name portion is no longer optional. That means stand-alone addresses do not match, but it also prevents improperly formatted name/address combinations from matching. The positive look ahead rule after the “name” group asserts that either the remainder of the string is wrapped with a pair of angle brackets, or there is not a mismatched bracket; either both or neither of the brackets is present. The look ahead is expressed as a group, but the match for a look ahead group does not consume any of the input text, so the rest of the pattern picks up from the same spot after the look ahead matches.

这个版本的表达式有几个重要的变化。首先，名称部分不再是可选的。这意味着独立地址不匹配，但它也防止格式不正确的名称/地址组合匹配。“name”组后的正向前瞻规则断言字符串的其余部分用一对尖括号括起来，或者没有不匹配的括号。要么两个括号都存在，要么都不存在。预读表示为一个组，但预读组的匹配不消耗任何输入文本，因此在预读匹配后，模式的其余部分从同一位置选取。

```python
import re

address = re.compile(
    '''
    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    ((?P<name>
    ([\w.,]+\s+)*[\w.,]+
    )
    \s+
    ) # The name is no longer optional.
    # LOOKAHEAD
    # Email addresses are wrapped in angle brackets, but only
    # if both are present or neither is.
    (?= (<.*>$) # Remainder wrapped in angle brackets
    |
    ([^<].*[^>]$) # Remainder *not* wrapped in angle brackets
    )
    <? # Optional opening angle bracket
    # The address itself: username@domain.tld
    (?P<email>
    [\w\d.+-]+ # Username
    @
    ([\w\d.]+\.)+ # Domain name prefix
    (com|org|edu) # Limit the allowed top-level domains.
    )
    >? # Optional closing angle bracket
    ''',
    re.VERBOSE)

candidates = [
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'Open Bracket <first.last@example.com',
    u'Close Bracket first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print(' Name :', match.groupdict()['name'])
        print(' Email:', match.groupdict()['email'])
    else:
        print(' No match')
```

```text
Candidate: First Last <first.last@example.com>
 Name : First Last
 Email: first.last@example.com
Candidate: No Brackets first.last@example.com   
 Name : No Brackets
 Email: first.last@example.com
Candidate: Open Bracket <first.last@example.com 
 No match
Candidate: Close Bracket first.last@example.com>
 No match
```


> A negative look ahead assertion (`(?!pattern)`) says that the pattern does not match
the text following the current point. For example, the email recognition pattern could
be modified to ignore the `noreply` mailing addresses commonly used by automated
systems.

否定前瞻断言 (`(?!pattern)`) 表示该模式与当前点之后的文本不匹配。例如，可以修改电子邮件识别模式以忽略自动化系统常用的`noreply`邮寄地址。

> The address starting with `noreply` does not match the pattern, since the look ahead assertion fails.

以`noreply`开头的地址与模式不匹配，因为前瞻断言失败。

```python
import re

address = re.compile(
    '''
    ^
    # An address: username@domain.tld
    # Ignore noreply addresses.
    (?!noreply@.*$)
    [\w\d.+-]+ # Username
    @
    ([\w\d.]+\.)+ # Domain name prefix
    (com|org|edu) # Limit the allowed top-level domains.
    $
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print(' Match:', candidate[match.start():match.end()])
    else:
        print(' No match')
```

```text
Candidate: first.last@example.com
 Match: first.last@example.com
Candidate: noreply@example.com
 No match
```


> Instead of looking ahead for noreply in the username portion of the email address, the pattern can alternatively be written using a negative look behind assertion after the username is matched using the syntax `(?<!pattern)`.

与在电子邮件地址的用户名部分中查找 noreply 不同，该模式也可以在使用语法匹配用户名后使用否定回溯断言来编写。

> Looking backward works a little differently than looking ahead, in that the expression must use a fixed-length pattern. Repetitions are allowed, as long as there is a fixed number of them (no wildcards or ranges).

向后看与向前看有点不同，因为表达式必须使用固定长度的模式。允许重复，只要它们的数量是固定的（没有通配符或范围）。

```python
import re
address = re.compile(
    '''
    ^

    # An address: username@domain.tld

    [\w\d.+-]+ # Username

    # Ignore noreply addresses.
    (?<!noreply)

    @
    ([\w\d.]+\.)+ # Domain name prefix
    (com|org|edu) # Limit the allowed top-level domains.

    $
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print(' Match:', candidate[match.start():match.end()])
    else:   
        print(' No match')
```

```text
Candidate: first.last@example.com
 Match: first.last@example.com
Candidate: noreply@example.com
 No match
```



> A positive look behind assertion can be used to find text following a pattern using the syntax `(?<=pattern)`. In the following example, the expression finds Twitter handles.

断言背后的积极查找可用于使用语法`(?<=pattern)` 来查找遵循模式的文本。在以下示例中，表达式查找 Twitter 句柄。

> The pattern matches sequences of characters that can make up a Twitter handle, as long as they are preceded by an `@`.

该模式匹配可以构成 Twitter 句柄的字符序列，只要它们前面有一个 `@`。

```python
# 1_52_re_look_behind.py
import re

twitter = re.compile(
    '''
    # A twitter handle: @username
    (?<=@)
    ([\w\d_]+) # Username
    ''',
    re.VERBOSE)

text = '''This text includes two Twitter handles.
One for @ThePSF, and one for the author, @doughellmann.
'''

print(text)
for match in twitter.findall(text):
    print('Handle:', match)
```

```text
This text includes two Twitter handles.
One for @ThePSF, and one for the author, @doughellmann.

Handle: ThePSF      
Handle: doughellmann
```



### 1.3.9 Self-Referencing Expressions

> Matched values can be used in later parts of an expression. For example, the email example can be updated to match only addresses composed of the first and last names of the person by including back-references to those groups. The easiest way to achieve this is by referring to the previously matched group by ID number, using `\num`.

匹配值可用于表达式的后面部分。例如，可以更新电子邮件示例以通过包括对这些组的反向引用来仅匹配由该人的名字和姓氏组成的地址。实现这一点的最简单方法是通过 ID 号引用先前匹配的组，使用 `\num`。

> Although the syntax is simple, creating back-references by numerical ID has a few disadvantages. From a practical standpoint, as the expression changes, the groups must be counted again and every reference may need to be updated. Another disadvantage is that only 99 references can be made using the standard back-reference syntax `\n`, because if the ID number is three digits long, it will be interpreted as an octal character value instead of a group reference. Of course, if there are more than 99 groups in an expression, there will be more serious maintenance challenges than simply not being able to refer to all of them.

尽管语法很简单，但通过数字 ID 创建反向引用有一些缺点。从实际的角度来看，随着表达式的变化，必须再次对组进行计数，并且可能需要更新每个引用。另一个缺点是使用标准的反向引用语法“\n”只能进行 99 次引用，因为如果 ID 号是三位数长，它将被解释为八进制字符值而不是组引用。当然，如果一个表达式中有超过 99 个组，那么维护方面的挑战会比简单地不能引用所有这些组更严重。

```python
import re

address = re.compile(
    r'''

    # The regular name
    (\w+) # First name
    \s+
    (([\w.]+)\s+)? # Optional middle name or initial
    (\w+) # Last name

    \s+

    <

    # The address: first_name.last_name@domain.tld
    (?P<email>
    \1 # First name
    \.
    \4 # Last name
    @
    ([\w\d.]+\.)+ # Domain name prefix
    (com|org|edu) # Limit the allowed top-level domains.
    )

    >
    ''',
    re.VERBOSE | re.IGNORECASE)

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print(' Match name :', match.group(1), match.group(4))
        print(' Match email:', match.group(5))
    else:
        print(' No match')
```


```text
Candidate: First Last <first.last@example.com>
 Match name : First Last
 Match email: first.last@example.com
Candidate: Different Name <first.last@example.com>
 No match
Candidate: First Middle Last <first.last@example.com>
 Match name : First Last
 Match email: first.last@example.com
Candidate: First M. Last <first.last@example.com>
 Match name : First Last
 Match email: first.last@example.com
```


> Python’s expression parser includes an extension that uses `(?P=name)` to refer to the value of a named group matched earlier in the expression.

Python 的表达式解析器包含一个扩展，它使用 `(?P=name)` 来引用表达式中较早匹配的命名组的值。

> The address expression is compiled with the `IGNORECASE` flag on, since proper names are normally capitalized but email addresses are not.

地址表达式编译时打开了 `IGNORECASE` 标志，因为专有名称通常大写，但电子邮件地址不是。

```python
# 1_54_re_refer_to_named_group.py
import re

address = re.compile(
    '''

    # The regular name
    (?P<first_name>\w+)
    \s+
    (([\w.]+)\s+)? # Optional middle name or initial
    (?P<last_name>\w+)

    \s+
    
    <

    # The address: first_name.last_name@domain.tld
    (?P<email>
    (?P=first_name)
    \.
    (?P=last_name)
    @
    ([\w\d.]+\.)+ # Domain name prefix
    (com|org|edu) # Limit the allowed top-level domains.
    )
    
    >
    ''',
    re.VERBOSE | re.IGNORECASE)

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print(' Match name :', match.groupdict()['first_name'],end=' ')
        print(match.groupdict()['last_name'])
        print(' Match email:', match.groupdict()['email'])
    else:
        print(' No match')
```

```text
Candidate: First Last <first.last@example.com>
 Match name : First Last
 Match email: first.last@example.com
Candidate: Different Name <first.last@example.com>
 No match
Candidate: First Middle Last <first.last@example.com>
 Match name : First Last
 Match email: first.last@example.com
Candidate: First M. Last <first.last@example.com>
 Match name : First Last
 Match email: first.last@example.com
```



> The other mechanism for using back-references in expressions chooses a different pattern based on whether a previous group matched. The email pattern can be corrected so that the angle brackets are required if a name is present, and not required if the email address is by itself. The syntax for testing whether a group has matched is `(?(id)yes-expression|no-expression)`, where `id` is the group name or number, `yes-expression` is the pattern to use if the group has a value, and `no-expression` is the pattern to use otherwise.


在表达式中使用反向引用的另一种机制根据前一组是否匹配来选择不同的模式。可以更正电子邮件模式，以便在名称存在时需要尖括号，如果电子邮件地址本身不需要尖括号。
测试组是否匹配的语法是 `(?(id)yes-expression|no-expression)`，其中 `id` 是组名或编号，`yes-expression` 是如果组匹配使用的模式有一个值，并且 `no-expression` 是其他情况下要使用的模式。



> This version of the email address parser uses two tests. If the `name` group matches, then the look ahead assertion requires both angle brackets and sets up the `brackets` group. If `name` is not matched, the assertion requires the rest of the text to not have angle brackets around it. Later, if the `brackets` group is set, the actual pattern matching code consumes the brackets in the input using literal patterns; otherwise, it consumes any blank space.

此版本的电子邮件地址解析器使用两个测试。如果 `name` 组匹配，则前瞻断言需要两个尖括号并设置 `brackets` 组。如果 `name` 不匹配，则断言要求文本的其余部分周围没有尖括号。稍后，如果设置了 `brackets` 组，则实际的模式匹配代码使用文字模式消耗输入中的括号；否则，它会消耗任何空白空间。



```python
# 1_55_re_id.py
import re
address = re.compile(
    '''
    ^

    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    (?P<name>
    ([\w.]+\s+)*[\w.]+
    )?
    \s*

    # Email addresses are wrapped in angle brackets, but
    # only if a name is found.
    (?(name)
    # Remainder wrapped in angle brackets because
    # there is a name
    (?P<brackets>(?=(<.*>$)))
    |
    # Remainder does not include angle brackets without name
    (?=([^<].*[^>]$))
    )

    # Look for a bracket only if the look-ahead assertion
    # found both of them.
    (?(brackets)<|\s*)
    
    # The address itself: username@domain.tld
    (?P<email>
    [\w\d.+-]+ # Username
    @
    ([\w\d.]+\.)+ # Domain name prefix
    (com|org|edu) # Limit the allowed top-level domains.
    )
    
    # Look for a bracket only if the look-ahead assertion
    # found both of them.
    (?(brackets)>|\s*)

    $
    ''',
    re.VERBOSE)

candidates = [
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'Open Bracket <first.last@example.com',
    u'Close Bracket first.last@example.com>',
    u'no.brackets@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print(' Match name :', match.groupdict()['name'])
        print(' Match email:', match.groupdict()['email'])
    else:
        print(' No match')
```

```text
Candidate: First Last <first.last@example.com>
 Match name : First Last
 Match email: first.last@example.com
Candidate: No Brackets first.last@example.com
 No match
Candidate: Open Bracket <first.last@example.com
 No match
Candidate: Close Bracket first.last@example.com>
 No match
Candidate: no.brackets@example.com
 Match name : None
 Match email: no.brackets@example.com
```


### 1.3.10 Modifying Strings with Patterns


> In addition to searching through text, `re` supports modifying text using regular expressions as the search mechanism, and the replacements can reference groups matched in the pattern as part of the substitution text. Use `sub()` to replace all occurrences of a pattern with another string.

除了搜索文本之外，`re` 支持使用正则表达式作为搜索机制修改文本，并且替换可以引用模式中匹配的组作为替换文本的一部分。使用 `sub()` 用另一个字符串替换所有出现的模式。

> References to the text matched by the pattern can be inserted using the `\num` syntax used for back-references.

可以使用用于反向引用的 `\num` 语法插入对与模式匹配的文本的引用。


```python
# 1_56_re_sub.py
import re

bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**. This **too**.'

print('Text:', text)
print('Bold:', bold.sub(r'<b>\1</b>', text))
```


```text
Text: Make this **bold**. This **too**.
Bold: Make this <b>bold</b>. This <b>too</b>.
```


> To use named groups in the substitution, use the syntax `\g<name>`.

要在替换中使用命名组，使用语法 `\g`。

> The `\g<name>` syntax also works with numbered references, and using it eliminates any ambiguity between group numbers and surrounding literal digits.

`\g<name>`语法也适用于编号引用，使用它可以消除组编号和周围文字数字之间的任何歧义。


```python
# 1_57_re_sub_named_groups.py
import re

bold = re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}')

text = 'Make this **bold**. This **too**.'

print('Text:', text)
print('Bold:', bold.sub(r'<b>\g<bold_text></b>', text))
```

```text
Text: Make this **bold**. This **too**.
Bold: Make this <b>bold</b>. This <b>too</b>.
```


> Pass a value to `count` to limit the number of substitutions performed.

将值传递给 `count` 以限制执行的替换次数。

> Only the first substitution is made because `count` is 1.

因为 `count` 是 1，所以只进行了第一次替换。

```python
# 1_58_re_sub_count.py
import re

bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**. This **too**.'

print('Text:', text)
print('Bold:', bold.sub(r'<b>\1</b>', text, count=1))
```

```text
Text: Make this **bold**. This **too**.
Bold: Make this <b>bold</b>. This **too**.
```

> `subn()` works just like `sub()` except that it returns both the modified string and the count of substitutions made.

`subn()` 的工作方式与 `sub()` 类似，不同之处在于它返回修改后的字符串和替换的次数。

> The search pattern matches twice in the example.

示例中的搜索模式匹配两次。

```python
# 1_59_re_subn.py
import re

bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**. This **too**.'

print('Text:', text)
print('Bold:', bold.subn(r'<b>\1</b>', text))
```


```text
Text: Make this **bold**. This **too**.
Bold: ('Make this <b>bold</b>. This <b>too</b>.', 2)
```

### 1.3.11 Splitting with Patterns

> `str.split()` is one of the most frequently used methods for breaking apart strings to parse them. It supports only the use of literal values as separators, though, and sometimes a regular expression is necessary if the input is not consistently formatted. For example, many plain text markup languages define paragraph separators as two or more newline (`\n`) characters. In this case, `str.split()` cannot be used because of the “or more” part of the definition.

`str.split()` 是最常用的用于拆分字符串以解析它们的方法之一。但是，它仅支持使用文字值作为分隔符，如果输入格式不一致，有时需要正则表达式。例如，许多纯文本标记语言将段落分隔符定义为两个或多个换行符 (`\n`)。在这种情况下，不能使用 `str.split()` 因为定义的“或更多”部分。

> A strategy for identifying paragraphs using `findall()` would use a pattern like
`(.+?)\n{2,}`.

使用 `findall()` 识别段落的策略将使用类似 `(.+?)\n{2,}` 的模式。

> That pattern fails for paragraphs at the end of the input text, as illustrated by the fact that “Paragraph three.” is not part of the output.

该模式对于输入文本末尾的段落失败，如“段落三”这一事实所示。不是输出的一部分。

```python
# 1_60_re_paragraphs_findall.py
import re

text = '''Paragraph one
on two lines.

Paragraph two.


Paragraph three.'''

for num, para in enumerate(re.findall(r'(.+?)\n{2,}',text,flags=re.DOTALL)):
    print(num, repr(para))
    print()
```

```text
0 'Paragraph one\non two lines.'

1 'Paragraph two.'

```


> Extending the pattern to say that a paragraph ends with two or more newlines or the end of input fixes the problem, but makes the pattern more complicated. Converting to `re.split()` instead of `re.findall()` handles the boundary condition automatically and keeps the pattern simpler.

通过扩展模式来描述一个段落以两个或更多换行符结尾或输入结束可以解决问题，但会使模式更加复杂。转换为 `re.split()` 而不是 `re.findall()` 会自动处理边界条件并使模式更简单。

> The pattern argument to `split()` expresses the markup specification more precisely. Two or more newline characters mark a separator point between paragraphs in the input string.

`split()` 的模式参数更精确地表达了标记规范。两个或多个换行符标记输入字符串中段落之间的分隔点。

```python
# 1_61_re_split.py
import re

text = '''Paragraph one
on two lines.

Paragraph two.


Paragraph three.'''

print('With findall:')
for num, para in enumerate(re.findall(r'(.+?)(\n{2,}|$)',text,flags=re.DOTALL)):
    print(num, repr(para))
    print()

print()
print('With split:')
for num, para in enumerate(re.split(r'\n{2,}', text)):
    print(num, repr(para))
    print()
```


```text
With findall:
0 ('Paragraph one\non two lines.', '\n\n')

1 ('Paragraph two.', '\n\n\n')

2 ('Paragraph three.', '')


With split:
0 'Paragraph one\non two lines.'

1 'Paragraph two.'

2 'Paragraph three.'

```

> Enclosing the expression in parentheses to define a group causes `split()` to work more like `str.partition()`, so it returns the separator values as well as the other parts of the string.

将表达式括在括号中以定义组会使得 `split()` 更像 `str.partition()`，因此它返回分隔符值以及字符串的其他部分。

> The output now includes each paragraph, as well as the sequence of newlines separating them.

输出现在包括每个段落，以及分隔它们的换行符序列。

```python
# 1_62_re_split_groups.py
import re
text = '''Paragraph one
on two lines.

Paragraph two.


Paragraph three.'''

print('With split:')
for num, para in enumerate(re.split(r'(\n{2,})', text)):
    print(num, repr(para))
    print()
```

```text
With split:
0 'Paragraph one\non two lines.'

1 '\n\n'

2 'Paragraph two.'

3 '\n\n\n'

4 'Paragraph three.'

```

## 1.4 difflib: Compare Sequences

> The `difflib` module contains tools for computing and working with differences between sequences. It is especially useful for comparing text, and includes functions that produce reports using several common difference formats.

`difflib` 模块包含用于计算和处理序列之间差异的工具。它对于比较文本特别有用，并且包括使用几种常见差异格式生成报告的功能。

> The examples in this section will all use the following common test data in the `difflib_data.py` module.

本节中的示例都将使用 difflib_data.py 模块中的以下常见测试数据。

### 1.4.1 Comparing Bodies of Text

> The `Differ` class works on sequences of text lines and produces human-readable deltas, or change instructions, including differences within individual lines. The default output produced by `Differ` is similar to the `diff` command-line tool under Unix. It includes the original input values from both lists, including common values, and markup data to indicate which changes were made.

> * Lines prefixed with `-` were in the first sequence, but not the second.
> * Lines prefixed with `+` were in the second sequence, but not the first.
> * If a line has an incremental difference between versions, an extra line prefixed with `?` is used to highlight the change within the new version.
> * If a line has not changed, it is printed with an extra blank space on the left column so that it is aligned with the other output that may have differences.


`Differ` 类处理文本行序列并生成人类可读的增量或更改指令，包括单个行内的差异。`Differ` 产生的默认输出类似于 Unix 下的 `diff` 命令行工具。它包括来自两个列表的原始输入值（包括公共值）和标记数据以指示进行了哪些更改。

* 以`-` 为前缀的行在第一个序列中，但不在第二个序列中。
* 以`+`为前缀的行在第二个序列中，但不是第一个。
* 如果某行在版本之间存在增量差异，则使用带有`?`前缀的额外行来突出显示新版本中的更改。
* 如果一行没有改变，它会在左列打印一个额外的空格，以便与可能有差异的其他输出对齐。
  


> The beginning of both text segments in the sample data is the same, so the first line is
printed without any extra annotation.

示例数据中两个文本段的开头相同，因此打印第一行没有任何额外的注释。

> The third line of the data has been changed to include a comma in the modified text. Both versions of the line are printed, with the extra information on line 5 showing the column where the text was modified, including the fact that the `,` character was added.

数据的第三行已更改为在修改后的文本中包含逗号。该行的两个版本都被打印出来，第5行的额外信息显示了文本被修改的列，包括添加了`,`字符的事实。

> The next few lines of the output show that an extra space was removed.

输出的接下来几行显示删除了一个额外的空格。

> Next, a more complex change was made, replacing several words in a phrase.

接下来，进行了更复杂的更改，替换了短语中的几个单词。


> The last sentence in the paragraph was changed significantly, so the difference is represented by removing the old version and adding the new.

段落中最后一句有明显改动，所以区别是去掉旧版本加新版本。

> The `ndiff()` function produces essentially the same output. The processing is specifically tailored for working with text data and eliminating “noise” in the input.

`ndiff()` 函数产生基本相同的输出。该处理是专门为处理文本数据和消除输入中的“噪音”而量身定制的。

```python
# 1_64_difflib_differ.py
import difflib
from difflib_data import *

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print('\n'.join(diff))
```


```text
  Lorem ipsum dolor sit amet, consectetuer adipiscing
  elit. Integer eu lacus accumsan arcu fermentum euismod. Donec 
- pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis 
+ pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
?         +

  pharetra tortor. In nec mauris eget magna consequat
- convalis. Nam sed sem vitae odio pellentesque interdum. Sed   
?                 - --

+ convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
?               +++ +++++   +

  consequat viverra nisl. Suspendisse arcu metus, blandit quis,
  rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
  molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
  tristique vel, mauris. Curabitur vel lorem id nisl porta
- adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
- tristique enim. Donec quis lectus a justo imperdiet tempus.
+ adipiscing. Duis vulputate tristique enim. Donec quis lectus a
+ justo imperdiet tempus. Suspendisse eu lectus. In nu
```

#### 1.4.1.1 Other Output Formats

> While the Differ class shows all of the input lines, a unified diff includes only the modified lines and a bit of context. The `unified_diff()` function produces this sort of output.

虽然 Differ 类显示所有输入行，但统一的 diff 仅包括修改后的行和一些上下文。 `unified_diff()` 函数产生这种输出。

> The `lineterm` argument is used to tell `unified_diff()` to skip appending newlines to the control lines that it returns because the input lines do not include them. Newlines are added to all of the lines when they are printed. The output should look familiar to users of many popular version-control tools.

`lineterm` 参数用于告诉 `unified_diff()` 跳过将换行符附加到它返回的控制行，因为输入行不包含它们。打印时会在所有行中添加换行符。对于许多流行的版本控制工具的用户来说，输出应该看起来很熟悉。

> Using `context_diff()` produces similar readable output.

使用 `context_diff()` 会产生类似的可读输出。



```python
# 1_65_difflib_unified.py
import difflib
from difflib_data import *

diff = difflib.unified_diff(
    text1_lines,
    text2_lines,
    lineterm='',
)
print('\n'.join(list(diff)))
```

```text
--- 
+++
@@ -1,11 +1,11 @@
 Lorem ipsum dolor sit amet, consectetuer adipiscing
 elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
-pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
+pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
 pharetra tortor. In nec mauris eget magna consequat
-convalis. Nam sed sem vitae odio pellentesque interdum. Sed
+convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
 consequat viverra nisl. Suspendisse arcu metus, blandit quis,
 rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
 molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
 tristique vel, mauris. Curabitur vel lorem id nisl porta
-adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
-tristique enim. Donec quis lectus a justo imperdiet tempus.
+adipiscing. Duis vulputate tristique enim. Donec quis lectus a
+justo imperdiet tempus. Suspendisse eu lectus. In nunc.
```


### 1.4.2 Junk Data

> All of the functions that produce difference sequences accept arguments to indicate which lines should be ignored and which characters within a line should be ignored. These parameters can be used to skip over markup or whitespace changes in two versions of a file, for example.

所有产生差异序列的函数都接受参数来指示应忽略哪些行以及应忽略行中的哪些字符。例如，这些参数可用于跳过文件的两个版本中的标记或空白更改。


> The default for `Differ` is to not ignore any lines or characters explicitly, but rather to rely on the ability of `SequenceMatcher` to detect noise. The default for `ndiff()` is to ignore space and tab characters.

“Differ”的默认设置是不明确忽略任何行或字符，而是依赖“SequenceMatcher”检测噪声的能力。`ndiff()` 的默认值是忽略空格和制表符。

```python
# 1_66_difflib_junk.py
# This example is adapted from the source for difflib.py.

from difflib import SequenceMatcher


def show_results(match):
    print(' a = {}'.format(match.a))
    print(' b = {}'.format(match.b))
    print(' size = {}'.format(match.size))
    i, j, k = match
    print(' A[a:a+size] = {!r}'.format(A[i:i + k]))
    print(' B[b:b+size] = {!r}'.format(B[j:j + k]))

A = " abcd"
B = "abcd abcd"

print('A = {!r}'.format(A))
print('B = {!r}'.format(B))

print('\nWithout junk detection:')
s1 = SequenceMatcher(None, A, B)
match1 = s1.find_longest_match(0, len(A), 0, len(B))
show_results(match1)

print('\nTreat spaces as junk:')
s2 = SequenceMatcher(lambda x: x == " ", A, B)
match2 = s2.find_longest_match(0, len(A), 0, len(B))
show_results(match2)
```

```text
A = ' abcd'
B = 'abcd abcd'

Without junk detection:
 a = 0
 b = 4
 size = 5
 A[a:a+size] = ' abcd'
 B[b:b+size] = ' abcd'

Treat spaces as junk:
 a = 1
 b = 0
 size = 4
 A[a:a+size] = 'abcd'
 B[b:b+size] = 'abcd'
```


### 1.4.3 Comparing Arbitrary Types

> The `SequenceMatcher` class compares two sequences of any types, as long as the values are hashable. It uses an algorithm to identify the longest contiguous matching blocks from the sequences, eliminating “junk” values that do not contribute to the real data.

`SequenceMatcher` 类比较任何类型的两个序列，只要值是可散列的。它使用一种算法从序列中识别最长的连续匹配块，消除对真实数据没有贡献的“垃圾”值。


> The funct `get_opcodes()` returns a list of instructions for modifying the first sequence to make it match the second. The instructions are encoded as five-element tuples, including a string instruction (the “opcode”) and two pairs of start and stop indexes into the sequences (denoted as `i1`, `i2`, `j1`, and `j2`) as shown in Table 1.4.

函数`get_opcodes()` 返回一个指令列表，用于修改第一个序列以使其与第二个序列匹配。指令被编码为五元素元组，包括一个字符串指令（“操作码”）和两对序列的开始和停止索引（表示为`i1`、`i2`、`j1`和`j2`），如表 1.4 所示。

|Opcode|Definition|
|:----:|----|
|`'replace'`|Replace `a[i1:i2]` with `b[j1:j2]`.|
|`'delete'`|Remove `a[i1:i2]` entirely.|
|`'insert'`|Insert `b[j1:j2]` at `a[i1:i1]`.|
|`'equal'`|The subsequences are already equal.|

> This example compares two lists of integers and uses `get_opcodes()` to derive the instructions for converting the original list into the newer version. The modifications are applied in reverse order so that the list indexes remain accurate after items are added and removed.

此示例比较两个整数列表，并使用 `get_opcodes()` 来导出将原始列表转换为更新版本的指令。修改以相反的顺序应用，以便在添加和删除项目后列表索引保持准确。

> `SequenceMatcher` works with custom classes, as well as built-in types, as long as they are hashable.

`SequenceMatcher` 适用于自定义类以及内置类型，只要它们是可散列的。

```python
# 1_67_difflib_seq.py
import difflib

s1 = [1, 2, 3, 5, 6, 4]
s2 = [2, 3, 5, 4, 6, 1]

print('Initial data:')
print('s1 =', s1)
print('s2 =', s2)
print('s1 == s2:', s1 == s2)
print()

matcher = difflib.SequenceMatcher(None, s1, s2)
for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):

    if tag == 'delete':
        print('Remove {} from positions [{}:{}]'.format(s1[i1:i2], i1, i2))
        print(' before =', s1)
        del s1[i1:i2]

    elif tag == 'equal':
        print('s1[{}:{}] and s2[{}:{}] are the same'.format(i1, i2, j1, j2))

    elif tag == 'insert':
        print('Insert {} from s2[{}:{}] into s1 at {}'.format(s2[j1:j2], j1, j2, i1))
        print(' before =', s1)
        s1[i1:i2] = s2[j1:j2]

    elif tag == 'replace':
        print(('Replace {} from s1[{}:{}] ''with {} from s2[{}:{}]').format(s1[i1:i2], i1, i2, s2[j1:j2], j1, j2))
        print(' before =', s1)
        s1[i1:i2] = s2[j1:j2]

    print(' after =', s1, '\n')

print('s1 == s2:', s1 == s2)
```

```text
Initial data:
s1 = [1, 2, 3, 5, 6, 4]
s2 = [2, 3, 5, 4, 6, 1]
s1 == s2: False

Replace [4] from s1[5:6] with [1] from s2[5:6]
 before = [1, 2, 3, 5, 6, 4]
 after = [1, 2, 3, 5, 6, 1]

s1[4:5] and s2[4:5] are the same
 after = [1, 2, 3, 5, 6, 1]

Insert [4] from s2[3:4] into s1 at 4
 before = [1, 2, 3, 5, 6, 1]
 after = [1, 2, 3, 5, 4, 6, 1]

s1[1:4] and s2[0:3] are the same
 after = [1, 2, 3, 5, 4, 6, 1]

Remove [1] from positions [0:1]
 before = [1, 2, 3, 5, 4, 6, 1]
 after = [2, 3, 5, 4, 6, 1]

s1 == s2: True
```