# Chapter 4 -- Dates and Times

[toc]


> Python does not include native types for dates and times as it does for `int`, `float`,
and `str`, but it provides three modules for manipulating date and time values in several
representations.

Python 不像`int`、`float` 和`str` 那样包含日期和时间的本机类型，但它提供了三个模块来操作多种表示形式的日期和时间值。

> The `time` (page 211) module exposes the time-related functions from the underlying C
library. It includes functions for retrieving the clock time and the processor run time, as
well as basic parsing and string formatting tools.
 
time`（第 211 页）模块从底层 C 库中暴露与时间相关的函数。
它包括用于检索时钟时间和处理器运行时间的函数，以及基本的解析和字符串格式化工具。

> The `datetime` (page 221) module provides a higher-level interface for date, time, and
combined values. The classes in `datetime` support arithmetic, comparison, and time zone
configuration.

`datetime`（第 221 页）模块为日期、时间和组合值提供了更高级别的接口。
`datetime` 中的类支持算术、比较和时区配置。

> The `calendar` (page 233) module creates formatted representations of weeks, months,
and years. It can also be used to compute recurring events, the day of the week for a given
date, and other calendar-based values.

`calendar`（第 233 页）模块创建周、月和年的格式化表示。
它还可以用于计算重复事件、给定日期的星期几以及其他基于日历的值。