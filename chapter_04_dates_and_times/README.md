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


## 4.1 time: Clock Time

> The `time` module provides access to several types of clocks, each useful for different purposes.
The standard system calls such as `time()` report the system “wall clock” time. The
`monotonic()` clock can be used to measure elapsed time in a long-running process because it
is guaranteed never to move backward, even if the system time is changed. For performance
testing, `perf_counter()` provides access to the clock with the highest available resolution,
which makes short time measurements more accurate. The CPU time is available through
`clock()`, and `process_time()` returns the combined processor time and system time.

`time` 模块提供对多种类型时钟的访问，每种类型用于不同目的。
诸如`time()`之类的标准系统调用报告系统“挂钟”时间。
`monotonic()` 时钟可用于测量长时间运行的进程中经过的时间，因为它保证永远不会向后移动，即使系统时间更改。
对于性能测试，`perf_counter()` 提供对具有最高可用分辨率的时钟的访问，这使得短时间测量更加准确。
CPU时间可通过`clock()`获得，`process_time()`返回处理器时间和系统时间的组合。


> The implementations expose C library functions for manipulating dates and times. Because they are tied
to the underlying C implementation, some details (such as the start of the epoch and the maximum
date value supported) are platform-specific. Refer to the library documentation for complete details.

这些实现公开了用于操作日期和时间的 C 库函数。
因为它们与底层 C 实现相关，所以一些细节（例如纪元的开始和支持的最大日期值）是特定于平台的。
有关完整的详细信息，请参阅库文档。


### 4.1.1 Comparing Clocks

> Implementation details for the clocks vary by platform. Use `get_clock_info()` to access
basic information about the current implementation, including the clock’s resolution.

时钟的实现细节因平台而异。
使用 `get_clock_info()` 访问有关当前实现的基本信息，包括时钟的分辨率。


> The following output for Mac OS X shows that the monotonic and perf_counter clocks
are implemented using the same underlying system call.

Win10 (Mac OS X 是作者使用的系统) 的以下输出显示单调和 perf_counter 时钟是使用相同的底层系统调用实现的。
另外注意，python 3.8 已不再支持 time.clock，虽然依然包含该方法。


```python
# 4_1_time_get_clock_info.py
import textwrap
import time


available_clocks = [
    # ('clock', time.clock),
    ('monotonic', time.monotonic),
    ('perf_counter', time.perf_counter),
    ('process_time', time.process_time),
    ('time', time.time),
]

for clock_name, func in available_clocks:
    print(textwrap.dedent('''\
    {name}:
        adjustable : {info.adjustable}
        implementation: {info.implementation}
        monotonic : {info.monotonic}
        resolution : {info.resolution}
        current : {current}
    ''').format(
        name=clock_name,
        info=time.get_clock_info(clock_name),
        current=func())
    )

```

```text
monotonic:
    adjustable : False
    implementation: GetTickCount64()
    monotonic : True
    resolution : 0.015625
    current : 1106018.359

perf_counter:
    adjustable : False
    implementation: QueryPerformanceCounter()
    monotonic : True
    resolution : 1e-07
    current : 0.0892459

process_time:
    adjustable : False
    implementation: GetProcessTimes()
    monotonic : True
    resolution : 1e-07
    current : 0.0625

time:
    adjustable : True
    implementation: GetSystemTimeAsFileTime()
    monotonic : False
    resolution : 0.015625
    current : 1629943559.23526


```


### 4.1.2 Wall Clock Time

> One of the core functions of the `time` module is `time()`, which returns the number of seconds
since the start of the “epoch” as a floating-point value.

time` 模块的核心函数之一是 `time()`，它以浮点值形式返回自“纪元”开始以来的秒数。


> The epoch is the start of measurement for time, which for Unix systems is 0:00 on January 1,1970. 
Although the value is always a float, the actual precision is platform-dependent.

纪元是时间测量的开始，对于 Unix 系统是 1970 年 1 月 1 日的 0:00。
尽管该值始终是浮点数，但实际精度取决于平台。

```python
# 4_2_time_time.py
import time

print('The time is:', time.time())
```

```text
The time is: 1629946381.8818817
```


> The float representation is highly useful when storing or comparing dates, but less useful
for producing human-readable representations. For logging or printing times, `ctime()` can
be a better choice.

浮点表示在存储或比较日期时非常有用，但对于生成人类可读的表示不太有用。
对于记录或打印时间，`ctime()` 可能是更好的选择。

> The second `print()` call in this example shows how to use `ctime()` to format a time value
other than the current time.

本示例中的第二个 `print()` 调用展示了如何使用 `ctime()` 来格式化当前时间以外的时间值。

```python
# 4_3_time_ctime.py
import time

print('The time is :', time.ctime())
later = time.time() + 15
print('15 secs from now :', time.ctime(later))

```

```text
The time is : Thu Aug 26 11:22:35 2021
15 secs from now : Thu Aug 26 11:22:50 2021
```