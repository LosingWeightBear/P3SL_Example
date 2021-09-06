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


### 4.1.3 Monotonic Clocks

> Because `time()` looks at the system clock, and because the system clock can be changed
by the user or system services for synchronizing clocks across multiple computers, calling
`time()` repeatedly may produce values that go forward and backward. This can result in
unexpected behavior when trying to measure durations or otherwise use those times for
computation. To avoid those situations, use `monotonic()`, which always returns values that
go forward.

因为`time()`查看系统时钟，并且由于用户或系统服务可以更改系统时钟以在多台计算机之间同步时钟，因此重复调用`time()`可能会产生向前和向后的值。
在尝试测量持续时间或以其他方式使用这些时间进行计算时，这可能会导致意外行为。
为了避免这些情况，请使用`monotonic()`，它总是返回前进的值。


> The start point for the monotonic clock is not defined, so return values are useful only
for doing calculations with other clock values. In this example, the duration of the sleep is
measured using `monotonic()`.

单调时钟的起点未定义，因此返回值仅用于使用其他时钟值进行计算。
在这个例子中，睡眠的持续时间是使用 `monotonic()` 来测量的。


```python
# 4_4_time_monotonic.py
import time

start = time.monotonic()
time.sleep(0.1)
end = time.monotonic()
print('start : {:>9.2f}'.format(start))
print('end : {:>9.2f}'.format(end))
print('span : {:>9.2f}'.format(end - start))

```


```text
start :  69087.03
end :  69087.14
span :      0.11

```



### 4.1.4 Processor Clock Time

> While `time()` returns a wall clock time, `clock()` returns a processor clock time. The values
returned from `clock()` reflect the actual time used by the program as it runs.

`time()` 返回挂钟时间，而 `clock()` 返回处理器时钟时间。
从 `clock()` 返回的值反映了程序运行时使用的实际时间。

注意，python 3.8 已不再支持 time.clock，虽然依然包含该方法。

> In this example, the formatted `ctime()` is printed along with the floating-point values
from `time(`)`, and `clock()` for each iteration through the loop.

在此示例中，格式化的 `ctime()` 与循环中每次迭代的 `time(`)` 和 `clock()` 中的浮点值一起打印。

> If you want to run the example on your system, you may have to add more cycles to the inner loop or
work with a larger amount of data to actually see a difference in the times.

如果您想在您的系统上运行该示例，您可能需要向内部循环添加更多周期或使用更大量的数据来实际查看时间上的差异。

```python
# 4_5_time_clock.py
import hashlib
import time

# Data to use to calculate md5 checksums
data = open(__file__, 'rb').read()
for i in range(5):
    h = hashlib.sha1()
    print(time.ctime(), ': {:0.3f} {:0.3f}'.format(time.time(), time.perf_counter()))
    for i in range(300000):
        h.update(data)
    cksum = h.digest()
```

```text
Fri Aug 27 09:48:43 2021 : 1630028923.426 0.079
Fri Aug 27 09:48:43 2021 : 1630028923.632 0.285
Fri Aug 27 09:48:43 2021 : 1630028923.813 0.466
Fri Aug 27 09:48:44 2021 : 1630028924.046 0.699
Fri Aug 27 09:48:44 2021 : 1630028924.242 0.894

```


> Typically, the processor clock does not tick if a program is not doing anything.

通常，如果程序没有做任何事情，处理器时钟不会滴答作响。

> In this example, the loop does very little work by going to sleep after each iteration. The
`time()` value increases even while the application is asleep, but the `clock()` value does not.

在这个例子中，循环通过在每次迭代后进入睡眠状态做很少的工作。
即使在应用程序处于睡眠状态时，`time()` 值也会增加，但 `clock()` 值不会。

注意，python 3.8 已不再支持 time.clock，使用 `process_time()`, 不会计算`sleep()`时间

> Calling `sleep()` yields control from the current thread and asks that thread to wait for
the system to wake it back up. If a program has only one thread, this function effectively
blocks the app so that it does no work.

调用 `sleep()` 会放弃当前线程的控制权，并要求该线程等待系统将其唤醒。
如果一个程序只有一个线程，这个函数会有效地阻塞应用程序，使其无法工作

```python
# 4_6_time_clock_sleep.py
import time

template = '{} - {:0.2f} - {:0.2f}'
print(template.format(
    time.ctime(), time.time(), time.process_time())
)

for i in range(3, 0, -1):
    print('Sleeping', i)
    time.sleep(i)
    print(template.format(
        time.ctime(), time.time(), time.process_time())
    )
```

```text
Fri Aug 27 10:43:36 2021 - 1630032216.53 - 0.09
Sleeping 3
Fri Aug 27 10:43:39 2021 - 1630032219.53 - 0.09
Sleeping 2
Fri Aug 27 10:43:41 2021 - 1630032221.53 - 0.09
Sleeping 1
Fri Aug 27 10:43:42 2021 - 1630032222.54 - 0.09


```


### 4.1.5 Performance Counter

> A high-resolution monotonic clock is essential for measuring performance. Determining
the best clock data source requires platform-specific knowledge, which Python provides
in `perf_counter()`.

高分辨率单调时钟对于测量性能至关重要。
确定最佳时钟数据源需要特定于平台的知识，Python 在 `perf_counter()` 中提供了这些知识。

> As with `monotonic()`, the epoch for `perf_counter()` is undefined, and the values are
meant to be used for comparing and computing values, not as absolute times.

与 `monotonic()` 一样，`perf_counter()` 的纪元是未定义的，这些值旨在用于比较和计算值，而不是绝对时间。


```python
# 4_7_time_perf_counter.py
import hashlib
import time

# Data to use to calculate md5 checksums
data = open(__file__, 'rb').read()

loop_start = time.perf_counter()

for i in range(5):
    iter_start = time.perf_counter()
    h = hashlib.sha1()
    for i in range(300000):
        h.update(data)
    cksum = h.digest()
    now = time.perf_counter()
    loop_elapsed = now - loop_start
    iter_elapsed = now - iter_start
    print(time.ctime(), ': {:0.3f} {:0.3f}'.format(iter_elapsed, loop_elapsed))
```

```text
Fri Aug 27 10:53:40 2021 : 0.273 0.273
Fri Aug 27 10:53:41 2021 : 0.254 0.527
Fri Aug 27 10:53:41 2021 : 0.253 0.780
Fri Aug 27 10:53:41 2021 : 0.254 1.034
Fri Aug 27 10:53:41 2021 : 0.247 1.281

```


### 4.1.6 Time Components

> Storing times as elapsed seconds is useful in some situations, but sometimes a program
needs to have access to the individual fields of a date (e.g., year, month). The `time` module
defines `struct_time` for holding date and time values, with the components being broken
out so they are easy to access. Several functions work with `struct_time` values instead of
floats.

在某些情况下，将时间存储为经过的秒数很有用，但有时程序需要访问日期的各个字段（例如，年、月）。
`time` 模块定义了用于保存日期和时间值的 `struct_time`，组件被分解以便于访问。
几个函数使用 `struct_time` 值而不是浮点数。

> The `gmtime()` function returns the current time in UTC. `localtime()` returns the current
time with the current time zone applied. `mktime()` takes a struct_time and converts it to
the floating-point representation.

`gmtime()` 函数返回 UTC 中的当前时间。
`localtime()` 返回应用当前时区的当前时间。
`mktime()` 接受一个 struct_time 并将其转换为浮点表示。


```python
# 4_8_time_struct.py
import time


def show_struct(s):
    print(' tm_year :', s.tm_year)
    print(' tm_mon :', s.tm_mon)
    print(' tm_mday :', s.tm_mday)
    print(' tm_hour :', s.tm_hour)
    print(' tm_min :', s.tm_min)
    print(' tm_sec :', s.tm_sec)
    print(' tm_wday :', s.tm_wday)
    print(' tm_yday :', s.tm_yday)
    print(' tm_isdst:', s.tm_isdst)


print('gmtime:')
show_struct(time.gmtime())
print('\nlocaltime:')
show_struct(time.localtime())
print('\nmktime:', time.mktime(time.localtime()))
```


```text
gmtime:
 tm_year : 2021
 tm_mon : 8
 tm_mday : 27
 tm_hour : 3
 tm_min : 38
 tm_sec : 10
 tm_wday : 4
 tm_yday : 239
 tm_isdst: 0

localtime:
 tm_year : 2021
 tm_mon : 8
 tm_mday : 27
 tm_hour : 11
 tm_min : 38
 tm_sec : 10
 tm_wday : 4
 tm_yday : 239
 tm_isdst: 0

mktime: 1630035490.0

```


### 4.1.7 Working with Time Zones

> The functions for determining the current time depend on having the time zone set, either
by the program or by using a default time zone set for the system. Changing the time zone
does not change the actual time, just the way it is represented.

用于确定当前时间的函数取决于是否通过程序或使用为系统设置的默认时区设置时区。
更改时区不会更改实际时间，只会更改其表示方式。

> To change the time zone, set the environment variable TZ, and then call tzset(). The
time zone can be specified with a great deal of detail, right down to the start and stop
times for daylight savings time. It is usually easier to use the time zone name and let the
underlying libraries derive the other information, though.

要更改时区，请设置环境变量 TZ，然后调用 tzset()。
可以详细地指定时区，直到夏令时的开始和停止时间。
不过，使用时区名称并让底层库获取其他信息通常更容易。

> The following example changes the time zone to a few different values and shows how
the changes affect other settings in the time module.

以下示例将时区更改为几个不同的值，并显示这些更改如何影响时间模块中的其他设置。

> The default time zone on the system used to prepare the examples is U.S./Eastern. The
other zones in the example change the `tzname`, daylight flag, and `timezone` offset value.

用于准备示例的系统上的默认时区是美国/东部。
示例中的其他区域更改了 `tzname`、日光标志和 `timezone` 偏移值。

注意， `time.tzset()` Unix only

```python
# 4_9_time_timezone.py
import time
import os


def show_zone_info():
    print(' TZ :', os.environ.get('TZ', '(not set)'))
    print(' tzname:', time.tzname)
    print(' Zone : {} ({})'.format(time.timezone, (time.timezone / 3600)))
    print(' DST :', time.daylight)
    print(' Time :', time.ctime())
    print()


print('Default :')

show_zone_info()
ZONES = [
    'GMT',
    'Europe/Amsterdam',
]

for zone in ZONES:
    os.environ['TZ'] = zone
    # time.tzset()
    print(zone, ':')
    show_zone_info()

```

```text
Default :
 TZ : (not set)
 tzname: ('中国标准时间', '中国夏令时')
 Zone : -28800 (-8.0)
 DST : 0
 Time : Fri Aug 27 13:42:52 2021

GMT :
 TZ : GMT
 tzname: ('中国标准时间', '中国夏令时')
 Zone : -28800 (-8.0)
 DST : 0
 Time : Fri Aug 27 13:42:52 2021

Europe/Amsterdam :
 TZ : Europe/Amsterdam
 tzname: ('中国标准时间', '中国夏令时')
 Zone : -28800 (-8.0)
 DST : 0
 Time : Fri Aug 27 13:42:52 2021

```


### 4.1.8 Parsing and Formatting Times

> The functions `strptime()` and `strftime()` convert between `struct_time` and string representations
of time values. The long list of formatting directives supported by both functions
enables input and output in different styles. The complete list is available in the library
documentation for the `time` module.

函数 `strptime()` 和 `strftime()` 在 `struct_time` 和时间值的字符串表示之间进行转换。
这两个函数支持的一长串格式化指令支持不同风格的输入和输出。
完整列表可在`time` 模块的库文档中找到。

> The following example converts the current time from a string to a `struct_time` instance,
and then back to a string.

以下示例将当前时间从字符串转换为 `struct_time` 实例，然后再转换回字符串。

> The output string is not exactly like the input, since the day of the month is prefixed with
a zero.

输出字符串与输入不完全相同，因为月份中的日期以零为前缀。

```python
# 4_10_time_strptime.py
import time


def show_struct(s):
    print(' tm_year :', s.tm_year)
    print(' tm_mon :', s.tm_mon)
    print(' tm_mday :', s.tm_mday)
    print(' tm_hour :', s.tm_hour)
    print(' tm_min :', s.tm_min)
    print(' tm_sec :', s.tm_sec)
    print(' tm_wday :', s.tm_wday)
    print(' tm_yday :', s.tm_yday)
    print(' tm_isdst:', s.tm_isdst)


now = time.ctime(1483391847.433716)
print('Now:', now)
parsed = time.strptime(now)
print('\nParsed:')
show_struct(parsed)
print('\nFormatted:', time.strftime("%a %b %d %H:%M:%S %Y", parsed))

```

````text
Now: Tue Jan  3 05:17:27 2017

Parsed:
 tm_year : 2017
 tm_mon : 1
 tm_mday : 3
 tm_hour : 5
 tm_min : 17
 tm_sec : 27
 tm_wday : 1
 tm_yday : 3
 tm_isdst: -1

Formatted: Tue Jan 03 05:17:27 2017
````


## 4.2 datetime: Date and Time Value Manipulation

> `datetime` contains functions and classes for date and time parsing, formatting, and arithmetic.

datetime` 包含用于日期和时间解析、格式化和算术的函数和类。


### 4.2.1 Times

> Time values are represented with the `time` class. A `time` instance has attributes for `hour`,
`minute`, `second`, and `microsecond`; it can also include time zone information.

时间值用`time` 类表示。
`time` 实例具有 `hour`、`minute`、`second` 和 `microsecond` 的属性；
它还可以包括时区信息。

> The arguments to initialize a time instance are optional, but the default of 0 is unlikely to
be correct.

初始化时间实例的参数是可选的，但默认值 0 不太可能正确。

```python
# 4_11_datetime_time.py
import datetime

t = datetime.time(1, 2, 3)
print(t)
print('hour       :', t.hour)
print('minute     :', t.minute)
print('second     :', t.second)
print('microsecond:', t.microsecond)
print('tzinfo     :', t.tzinfo)

```

```text
01:02:03
hour       : 1
minute     : 2
second     : 3
microsecond: 0
tzinfo     : None

```


> A `time` instance holds only values of time; it does not include a date associated with the
time.

`time` 实例只保存时间值；它不包括与时间相关的日期。


> The `min` and `max` class attributes reflect the valid range of times in a single day.

`min` 和 `max` 类属性反映了一天中的有效时间范围。


```python
# 4_12_datetime_time_minmax.py
import datetime

print('Earliest  :', datetime.time.min)
print('Latest    :', datetime.time.max)
print('Resolution:', datetime.time.resolution)

```

```text
Earliest  : 00:00:00
Latest    : 23:59:59.999999
Resolution: 0:00:00.000001

```


> The resolution for `time` is limited to whole microseconds.

`time` 的分辨率限制为整微秒。


> Floating-point values for microseconds cause a `TypeError`.

微秒的浮点值会导致“TypeError”。

```python
# 4_13_datetime_time_resolution.py
import datetime

for m in [1, 0, 0.1, 0.6]:
    try:
        print('{:02.1f} :'.format(m), datetime.time(0, 0, 0, microsecond=m))
    except TypeError as err:
        print('ERROR:', err)

```


```text
1.0 : 00:00:00.000001
0.0 : 00:00:00
ERROR: integer argument expected, got float
ERROR: integer argument expected, got float

```


### 4.2.2 Dates

> Calendar date values are represented with the `date` class. Instances have attributes for year,
month, and day. It is easy to create a date representing the current date using the `today()`
class method.

日历日期值用`date` 类表示。
实例具有年、月和日的属性。
使用 `today()` 类方法可以轻松创建表示当前日期的日期。

> This example prints the current date in several formats.

此示例以多种格式打印当前日期。


```python
# 4_14_datetime_date.py
import datetime

today = datetime.date.today()
print(today)
print('ctime  :', today.ctime())
tt = today.timetuple()
print('tuple  : tm_year  =', tt.tm_year)
print('         tm_mon   =', tt.tm_mon)
print('         tm_mday  =', tt.tm_mday)
print('         tm_hour  =', tt.tm_hour)
print('         tm_min   =', tt.tm_min)
print('         tm_sec   =', tt.tm_sec)
print('         tm_wday  =', tt.tm_wday)
print('         tm_yday  =', tt.tm_yday)
print('         tm_isdst =', tt.tm_isdst)
print('ordinal:', today.toordinal())
print('Year   :', today.year)
print('Mon    :', today.month)
print('Day    :', today.day)

```

```text
2021-08-30
ctime  : Mon Aug 30 00:00:00 2021
tuple  : tm_year  = 2021
         tm_mon   = 8
         tm_mday  = 30
         tm_hour  = 0
         tm_min   = 0
         tm_sec   = 0
         tm_wday  = 0
         tm_yday  = 242
         tm_isdst = -1
ordinal: 738032
Year   : 2021
Mon    : 8
Day    : 30


```


> There are also class methods for creating instances from POSIX timestamps or integers
representing date values from the Gregorian calendar, where January 1 of the year 1 is
designated as having the value 1 and each subsequent day increments the value by 1.

还有一些类方法可以从 POSIX 时间戳或代表公历日期值的整数创建实例，
其中第 1 年的 1 月 1 日被指定为具有值 1，
并且随后的每一天将该值增加 1。


> This example illustrates the different value types used by `fromordinal()` and
`fromtimestamp()`.

这个例子说明了 `fromordinal()` 和 `fromtimestamp()` 使用的不同值类型。


```python
# 4_15_datetime_date_fromordinal.py
import datetime
import time


o = 733114
print('o               :', o)
print('fromordinal(o)  :', datetime.date.fromordinal(o))

t = time.time()
print('t               :', t)
print('fromtimestamp(t):', datetime.date.fromtimestamp(t))

```

```text
o               : 733114
fromordinal(o)  : 2008-03-13
t               : 1630295598.8341322
fromtimestamp(t): 2021-08-30

```


> As is true with the `time` class, the range of date values supported can be determined
using the `min` and `max` attributes.

与`time` 类一样，支持的日期值范围可以使用`min` 和`max` 属性来确定。


> The resolution for dates is whole days.

日期的分辨率是整天。




```python
# 4_16_datetime_date_minmax.py
import datetime

print('Earliest :', datetime.date.min)
print('Latest :', datetime.date.max)
print('Resolution:', datetime.date.resolution)

```


```text
Earliest : 0001-01-01
Latest : 9999-12-31
Resolution: 1 day, 0:00:00

```


> Another way to create new `date` instances is to use the `replace()` method of an existing
date.

另一种创建新的`date` 实例的方法是使用现有日期的`replace()` 方法。


> This example changes the year, leaving the day and month unmodified.

此示例更改了年份，而未修改日期和月份。


```python
# 4_18_datetime_date_replace.py
import datetime

d1 = datetime.date(2008, 3, 29)
print('d1:', d1.ctime())

d2 = d1.replace(year=2009)
print('d2:', d2.ctime())

```


```text
d1: Sat Mar 29 00:00:00 2008
d2: Sun Mar 29 00:00:00 2009

```


### 4.2.3 timedeltas

> Future and past dates can be calculated using basic arithmetic on two `datetime` objects, or
by combining a `datetime` with a `timedelta`. Subtracting dates produces a `timedelta`, and
a `timedelta` can be also added or subtracted from a date to produce another date. The
internal values for a `timedelta` are stored in days, seconds, and microseconds.

未来和过去的日期可以使用两个 `datetime` 对象的基本算术来计算，或者通过将 `datetime` 与 `timedelta` 组合来计算。
减去日期会产生一个 `timedelta`，并且一个 `timedelta` 也可以从一个日期中添加或减去以产生另一个日期。
`timedelta` 的内部值以天、秒和微秒为单位存储。

> Intermediate-level values passed to the constructor are converted into days, seconds, and
microseconds.

传递给构造函数的中级值被转换为天、秒和微秒。

```python
# 4_18_datetime_timedelta.py
import datetime

print('microseconds:', datetime.timedelta(microseconds=1))
print('milliseconds:', datetime.timedelta(milliseconds=1))
print('seconds     :', datetime.timedelta(seconds=1))
print('minutes     :', datetime.timedelta(minutes=1))
print('hours       :', datetime.timedelta(hours=1))
print('days        :', datetime.timedelta(days=1))
print('weeks       :', datetime.timedelta(weeks=1))

```

```text
microseconds: 0:00:00.000001
milliseconds: 0:00:00.001000
seconds     : 0:00:01
minutes     : 0:01:00
hours       : 1:00:00
days        : 1 day, 0:00:00
weeks       : 7 days, 0:00:00

```


> The full duration of a `timedelta` can be retrieved as a number of seconds using
`total_seconds()`.

可以使用“total_seconds()”以秒数形式检索“timedelta”的完整持续时间。

> The return value is a floating-point number, to accommodate durations of less than 1 second.

返回值是一个浮点数，以适应小于 1 秒的持续时间。

```python
# 4_19_datetime_timedelta_total_seconds.py
import datetime

for delta in [datetime.timedelta(microseconds=1),
              datetime.timedelta(milliseconds=1),
              datetime.timedelta(seconds=1),
              datetime.timedelta(minutes=1),
              datetime.timedelta(hours=1),
              datetime.timedelta(days=1),
              datetime.timedelta(weeks=1),
              ]:
    print('{:15} = {:8} seconds'.format(str(delta), delta.total_seconds()))

```


```text
0:00:00.000001  =    1e-06 seconds
0:00:00.001000  =    0.001 seconds
0:00:01         =      1.0 seconds
0:01:00         =     60.0 seconds
1:00:00         =   3600.0 seconds
1 day, 0:00:00  =  86400.0 seconds
7 days, 0:00:00 = 604800.0 seconds

```


### 4.2.4 Date Arithmetic

> Date math uses the standard arithmetic operators.

日期数学使用标准算术运算符。

> This example with date objects illustrates the use of `timedelta` objects to compute new
dates. In addition, date instances are subtracted to produce `timedelta` objects (including a
negative delta value).

这个带有日期对象的示例说明了使用`timedelta`对象来计算新日期。
此外，减去日期实例以生成`timedelta`对象（包括负增量值）。


```python
# 4_20_datetime_date_math.py
import datetime

today = datetime.date.today()
print('Today :', today)

one_day = datetime.timedelta(days=1)
print('One day :', one_day)

yesterday = today - one_day
print('Yesterday:', yesterday)

tomorrow = today + one_day
print('Tomorrow :', tomorrow)
print()
print('tomorrow - yesterday:', tomorrow - yesterday)
print('yesterday - tomorrow:', yesterday - tomorrow)

```

```text
Today : 2021-08-30
One day : 1 day, 0:00:00
Yesterday: 2021-08-29
Tomorrow : 2021-08-31

tomorrow - yesterday: 2 days, 0:00:00
yesterday - tomorrow: -2 days, 0:00:00

```



> A `timedelta` object also supports arithmetic with integers, floats, and other `timedelta`
instances.

`timedelta` 对象还支持整数、浮点数和其他 `timedelta` 实例的算术运算。


> In this example, several multiples of a single day are computed, with the resulting `timedelta`
holding the appropriate number of days or hours.

在此示例中，计算了一天的多个倍数，结果 `timedelta` 包含适当的天数或小时数。

> The final example demonstrates how to compute values by combining two `timedelta`
objects. In this case, the result is a floating-point number.

最后一个示例演示了如何通过组合两个 `timedelta` 对象来计算值。
在这种情况下，结果是一个浮点数。


```python
# 4_21_datetime_timedelta_math.py
import datetime

one_day = datetime.timedelta(days=1)
print('1 day :', one_day)
print('5 days :', one_day * 5)
print('1.5 days :', one_day * 1.5)
print('1/4 day :', one_day / 4)

# Assume an hour for lunch.
work_day = datetime.timedelta(hours=7)
meeting_length = datetime.timedelta(hours=1)
print('meetings per day :', work_day / meeting_length)

```

```text
1 day : 1 day, 0:00:00
5 days : 5 days, 0:00:00
1.5 days : 1 day, 12:00:00
1/4 day : 6:00:00
meetings per day : 7.0

```


### 4.2.5 Comparing Values

> Both date and time values can be compared using the standard comparison operators to
determine which is earlier or later.

可以使用标准比较运算符来比较日期和时间值，以确定哪个更早或更晚。

> All comparison operators are supported.

支持所有比较运算符。

```python
# 4_22_datetime_comparing.py
import datetime

print('Times:')
t1 = datetime.time(12, 55, 0)
print(' t1:', t1)
t2 = datetime.time(13, 5, 0)
print(' t2:', t2)
print(' t1 < t2:', t1 < t2)

print
print('Dates:')
d1 = datetime.date.today()
print(' d1:', d1)
d2 = datetime.date.today() + datetime.timedelta(days=1)
print(' d2:', d2)
print(' d1 > d2:', d1 > d2)

```


```text
Times:
 t1: 12:55:00
 t2: 13:05:00
 t1 < t2: True
Dates:
 d1: 2021-08-30
 d2: 2021-08-31
 d1 > d2: False

```


### 4.2.6 Combining Dates and Times

> Use the `datetime` class to hold values consisting of both date and time components. As with
`date`, several convenient class methods are available for creating `datetime` instances from
other common values.

使用 `datetime` 类来保存由日期和时间组件组成的值。
与 `date` 一样，有几个方便的类方法可用于从其他常用值创建 `datetime` 实例。

> As might be expected, the `datetime` instance has all of the attributes of both a `date`
object and a `time` object.

正如所料，`datetime` 实例具有`date` 对象和`time` 对象的所有属性。


```python
# 4_23_datetime_datetime.py
import datetime

print('Now :', datetime.datetime.now())
print('Today :', datetime.datetime.today())
print('UTC Now:', datetime.datetime.utcnow())
print

FIELDS = [
    'year', 'month', 'day',
    'hour', 'minute', 'second',
    'microsecond',
]

d = datetime.datetime.now()
for attr in FIELDS:
    print('{:15}: {}'.format(attr, getattr(d, attr)))

```

```text
Now : 2021-08-31 09:28:35.126765
Today : 2021-08-31 09:28:35.126766
UTC Now: 2021-08-31 01:28:35.126765
year           : 2021
month          : 8
day            : 31
hour           : 9
minute         : 28
second         : 35
microsecond    : 126765

```


> Just like `date`, `datetime` provides convenient class methods for creating new instances. It
also includes `fromordinal()` and `fromtimestamp()`.

就像 `date` 一样，`datetime` 提供了方便的类方法来创建新实例。
它还包括`fromordinal()`和`fromtimestamp()`。

> `combine()` creates `datetime` instances from one `date` and one `time` instance.

combine()` 从一个 `date` 和一个 `time` 实例创建 `datetime` 实例。


```python
# 4_24_datetime_datetime_combine.py
import datetime

t = datetime.time(1, 2, 3)
print('t :', t)

d = datetime.date.today()
print('d :', d)

dt = datetime.datetime.combine(d, t)
print('dt:', dt)

```

```text
t : 01:02:03
d : 2021-08-31
dt: 2021-08-31 01:02:03

```


### 4.2.7 Formatting and Parsing

> The default string representation of a datetime object uses the `ISO-8601` format (`YYYY-MMDDTHH:
MM:SS.mmmmmm`). Alternative formats can be generated using `strftime()`.

日期时间对象的默认字符串表示使用 `ISO-8601` 格式（`YYYY-MMDDTHH: MM:SS.mmmmmm`）。
可以使用 `strftime()` 生成其他格式。

> Use `datetime.strptime()` to convert formatted strings to `datetime` instances.

使用 `datetime.strptime()` 将格式化字符串转换为 `datetime` 实例。

```text
ISO : 2021-08-31 14:04:04.726145
strftime: Tue Aug 31 14:04:04 2021
strptime: Tue Aug 31 14:04:04 2021

```


> The same formatting codes can be used with Python’s string formatting mini-language2 by
placing them after the : in the field specification of the format string.

相同的格式代码可以与 Python 的字符串格式 mini-language2 一起使用，方法是将它们放在格式字符串的字段规范中之后。

> Each datetime format code must be prefixed with `%`, and subsequent colons are treated as
literal characters to be included in the output.

每个日期时间格式代码都必须以“%”为前缀，随后的冒号被视为要包含在输出中的文字字符。


```python
# 4_26_datetime_format.py
import datetime

today = datetime.datetime.today()
print('ISO :', today)
print('format(): {:%a %b %d %H:%M:%S %Y}'.format(today))

```


```text
ISO : 2021-08-31 14:12:35.510199
format(): Tue Aug 31 14:12:35 2021

```


### 4.2.8 Time Zones

> Within `datetime`, time zones are represented by subclasses of `tzinfo`. Since `tzinfo` is an
abstract base class, applications need to define a subclass and provide appropriate implementations
for a few methods to make it useful.

在 datetime 中，时区由 tzinfo 的子类表示。
由于 `tzinfo` 是一个抽象基类，应用程序需要定义一个子类并为一些方法提供适当的实现以使其有用

> `datetime` does include a somewhat naive implementation in the class `timezone` that uses
a fixed offset from UTC. This implementation does not support different offset values on
different days of the year, such as where daylight savings time applies, or where the offset
from UTC has changed over time.

`datetime` 确实在类 `timezone` 中包含了一个有点幼稚的实现，它使用与 UTC 的固定偏移量。
此实现不支持一年中不同日期的不同偏移值，例如适用夏令时的地方，或者与 UTC 的偏移量随时间发生变化的地方。

> To convert a `datetime` value from one time zone to another, use `astimezone()`. In the
preceding example, two separate time zones 6 hours on either side of UTC are shown, and
the `utc` instance from `datetime.timezone` is also used for reference. The final output line
shows the value in the system time zone, which was obtained by calling `astimezone()` with
no argument.


要将 `datetime` 值从一个时区转换为另一个时区，请使用 `astimezone()`。
在前面的示例中，显示了 UTC 两侧 6 小时的两个独立时区，并且还使用了来自 `datetime.timezone` 的 `utc` 实例作为参考。
最后的输出行显示了系统时区中的值，该值是通过不带参数调用 `astimezone()` 获得的。


> The third-party module `pytz3` is a better implementation for time zones. It supports named time zones,
and the offset database is kept up-to-date as changes are made by political bodies around the world.

第三方模块`pytz3` 是一个更好的时区实现。
它支持命名时区，并且偏移数据库随着世界各地政治机构的变化而保持最新。


```python
# 4_27_datetime_timezone.py
import datetime

min6 = datetime.timezone(datetime.timedelta(hours=-6))
plus6 = datetime.timezone(datetime.timedelta(hours=6))
d = datetime.datetime.now(min6)

print(min6, ':', d)
print(datetime.timezone.utc, ':', d.astimezone(datetime.timezone.utc))
print(plus6, ':', d.astimezone(plus6))

# Convert to the current system timezone.
d_system = d.astimezone()
print(d_system.tzinfo, ' :', d_system)

```


```text
UTC-06:00 : 2021-08-31 00:25:25.201425-06:00
UTC : 2021-08-31 06:25:25.201425+00:00
UTC+06:00 : 2021-08-31 12:25:25.201425+06:00
中国标准时间  : 2021-08-31 14:25:25.201425+08:00

```


## 4.3 calendar: Work with Dates

> The `calendar` module defines the `Calendar` class, which encapsulates calculations for values
such as the dates of the weeks in a given month or year. In addition, the `TextCalendar` and
`HTMLCalendar` classes can produce preformatted output.

`calendar` 模块定义了 `Calendar` 类，该类封装了对给定月份或年份中的周日期等值的计算。
此外，`TextCalendar` 和 `HTMLCalendar` 类可以生成预先格式化的输出。


### 4.3.1 Formatting Examples

> The `prmonth()` method is a simple function that produces the formatted text output for a
month.

`prmonth()` 方法是一个简单的函数，可以生成一个月的格式化文本输出。

> The example configures `TextCalendar` to start weeks on Sunday, following the U.S. convention.
The default is to use the European convention of starting a week on Monday. The
example produces the following output.

该示例将“TextCalendar”配置为按照美国惯例从星期日开始。
默认是使用从星期一开始一周的欧洲惯例。
该示例产生以下输出。

```python
# 4_28_calendar_textcalendar.py
import calendar

c = calendar.TextCalendar(calendar.SUNDAY)
c.prmonth(2021, 9)

```


```text
   September 2021
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30

```


> A similar HTML table can be produced with `HTMLCalendar` and `formatmonth()`. The
rendered output looks roughly the same as the plain text version, but is wrapped with
HTML tags. Each table cell has a class attribute corresponding to the day of the week, so
the HTML can be styled through CSS.

可以使用`HTMLCalendar` 和`formatmonth()` 生成类似的HTML 表格。
渲染的输出看起来与纯文本版本大致相同，但用 HTML 标签包装。
每个表格单元格都有一个对应星期几的 class 属性，因此可以通过 CSS 对 HTML 进行样式设置。


> To produce output in a format other than one of the defaults, use `calendar` to calculate
the dates and organize the values into week and month ranges, then iterate over the result.
The `weekheader()`, `monthcalendar()`, and `yeardays2calendar()` methods of `Calendar` are
especially useful for this purpose.

要以默认格式以外的格式生成输出，请使用 `calendar` 计算日期并将值组织到周和月范围内，然后迭代结果。
`Calendar` 的 `weekheader()`、`monthcalendar()` 和 `yeardays2calendar()` 方法对于这个目的特别有用。


> Calling `yeardays2calendar()` produces a sequence of “month row” lists. Each list of
months includes each month as another list of weeks. The weeks are lists of tuples made up
of day number (1–31) and weekday number (0–6). Days that fall outside of the month have
a day number of 0.

调用 `yeardays2calendar()` 会生成一系列“月份行”列表。
每个月列表包括每个月作为另一个周列表。
周是由天数 (1-31) 和工作日数 (0-6) 组成的元组列表。
月外的天数为 0

> Calling `yeardays2calendar(2017,3)` returns data for 2017, organized with three months
per row.

调用 `yeardays2calendar(2017,3)` 返回 2017 年的数据，每行组织三个月。

```python
# 4_29_calendar_yeardays2calendar.py
import calendar
import pprint

cal = calendar.Calendar(calendar.SUNDAY)

cal_data = cal.yeardays2calendar(2017, 3)
print('len(cal_data) :', len(cal_data))

top_months = cal_data[0]
print('len(top_months) :', len(top_months))

first_month = top_months[0]
print('len(first_month) :', len(first_month))

print('first_month:')
pprint.pprint(first_month, width=65)

```

```text
len(cal_data) : 4
len(top_months) : 3
len(first_month) : 5
first_month:
[[(1, 6), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5)],
 [(8, 6), (9, 0), (10, 1), (11, 2), (12, 3), (13, 4), (14, 5)],
 [(15, 6), (16, 0), (17, 1), (18, 2), (19, 3), (20, 4), (21, 5)],
 [(22, 6), (23, 0), (24, 1), (25, 2), (26, 3), (27, 4), (28, 5)],
 [(29, 6), (30, 0), (31, 1), (0, 2), (0, 3), (0, 4), (0, 5)]]

```


> This is equivalent to the data used by `formatyear()`.

这相当于`formatyear()`使用的数据。


```python
# 4_30_calendar_formatyear.py
import calendar

cal = calendar.TextCalendar(calendar.SUNDAY)
print(cal.formatyear(2021, 2, 1, 1, 3))

```

```text
                              2021

      January               February               March
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
                1  2      1  2  3  4  5  6      1  2  3  4  5  6
 3  4  5  6  7  8  9   7  8  9 10 11 12 13   7  8  9 10 11 12 13
10 11 12 13 14 15 16  14 15 16 17 18 19 20  14 15 16 17 18 19 20
17 18 19 20 21 22 23  21 22 23 24 25 26 27  21 22 23 24 25 26 27
24 25 26 27 28 29 30  28                    28 29 30 31
31

       April                  May                   June
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
             1  2  3                     1         1  2  3  4  5
 4  5  6  7  8  9 10   2  3  4  5  6  7  8   6  7  8  9 10 11 12
11 12 13 14 15 16 17   9 10 11 12 13 14 15  13 14 15 16 17 18 19
18 19 20 21 22 23 24  16 17 18 19 20 21 22  20 21 22 23 24 25 26
25 26 27 28 29 30     23 24 25 26 27 28 29  27 28 29 30
                      30 31

        July                 August              September
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
             1  2  3   1  2  3  4  5  6  7            1  2  3  4
 4  5  6  7  8  9 10   8  9 10 11 12 13 14   5  6  7  8  9 10 11
11 12 13 14 15 16 17  15 16 17 18 19 20 21  12 13 14 15 16 17 18
18 19 20 21 22 23 24  22 23 24 25 26 27 28  19 20 21 22 23 24 25
25 26 27 28 29 30 31  29 30 31              26 27 28 29 30

      October               November              December
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
                1  2      1  2  3  4  5  6            1  2  3  4
 3  4  5  6  7  8  9   7  8  9 10 11 12 13   5  6  7  8  9 10 11
10 11 12 13 14 15 16  14 15 16 17 18 19 20  12 13 14 15 16 17 18
17 18 19 20 21 22 23  21 22 23 24 25 26 27  19 20 21 22 23 24 25
24 25 26 27 28 29 30  28 29 30              26 27 28 29 30 31
31


```


> The `day_name`, `day_abbr`, `month_name`, and `month_abbr` module attributes are useful for
producing custom-formatted output (e.g., including links in the HTML output). They are
automatically configured correctly for the current locale.

`day_name`、`day_abbr`、`month_name` 和 `month_abbr` 模块属性可用于生成自定义格式的输出（例如，包括 HTML 输出中的链接）。
它们会自动为当前语言环境正确配置。


### 4.3.2 Locales

> To produce a calendar formatted for a locale other than the current default, use `Locale-
TextCalendar` or `LocaleHTMLCalendar`.

要为当前默认设置以外的区域设置格式生成日历，请使用`Locale-TextCalendar`或`LocaleHTMLCalendar`。


> The first day of the week is not part of the locale settings. Instead, its value is taken
from the argument to the calendar class, just as occurs with the regular `TextCalendar` class.

一周的第一天不是区域设置的一部分。
相反，它的值取自日历类的参数，就像常规的`TextCalendar`类一样。


```python
# 4_32_calendar_locale.py
import calendar

c = calendar.LocaleTextCalendar(locale='en_US')
c.prmonth(2021, 7)

print()

c = calendar.LocaleTextCalendar(locale='fr_FR')
c.prmonth(2021, 7)

```

```text
     July 2021
Mo Tu We Th Fr Sa Su
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31

    juillet 2021
lu ma me je ve sa di
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31


```


### 4.3.3 Calculating Dates

> Although the calendar module focuses mostly on printing full calendars in various formats,
it also provides functions useful for working with dates in other ways, such as calculating
dates for a recurring event. For example, the Python Atlanta User’s Group meets on the
second Thursday of every month. To calculate the dates for the meetings for a year, use the
return value of `monthcalendar()`.

尽管日历模块主要侧重于以各种格式打印完整日历，但它也提供了以其他方式处理日期的有用功能，例如计算重复事件的日期。
例如，Python Atlanta 用户组在每个月的第二个星期四开会。
要计算一年的会议日期，请使用`monthcalendar()`的返回值。


> Some days have a 0 value. Those days of the week overlap with the given month, but
are part of another month.

有些日子的值是 0。
一周中的那些日子与给定的月份重叠，但属于另一个月份的一部分。



```python
# 4_32_calendar_monthcalendar.py
import calendar
import pprint

pprint.pprint(calendar.monthcalendar(2021, 7))

```

```text
[[0, 0, 0, 1, 2, 3, 4],
 [5, 6, 7, 8, 9, 10, 11],
 [12, 13, 14, 15, 16, 17, 18],
 [19, 20, 21, 22, 23, 24, 25],
 [26, 27, 28, 29, 30, 31, 0]]

```


> The first day of the week defaults to Monday. It is possible to change that value by
calling `setfirstweekday()`. An even more convenient approach in this case is to skip that
step, since the calendar module includes constants for indexing into the date ranges returned
by `monthcalendar()`.

一周的第一天默认为星期一。
可以通过调用 `setfirstweekday()` 来更改该值。
在这种情况下，更方便的方法是跳过该步骤，因为日历模块包含用于索引到`monthcalendar()`返回的日期范围的常量。


> To calculate the group meeting dates for a year, assuming they are always on the second
Thursday of every month, look at the output of `monthcalendar()` to find the dates on
which Thursdays fall. The first and last weeks of the month are padded with 0 values as
placeholders for the days falling in the preceding and subsequent months, respectively. For
example, if a month starts on a Friday, the value in the first week in the Thursday position
will be 0.

要计算一年的小组会议日期，假设它们总是在每个月的第二个星期四，请查看`monthcalendar()`的输出以找到星期四所在的日期。
该月的第一周和最后一周分别用 0 值作为占位符填充前几个月和后几个月的天数。
例如，如果一个月从星期五开始，则星期四位置的第一周的值将为 0。


```python
# 4_33_calendar_secondthursday.py
import calendar
import sys

year = int(sys.argv[1])

# Show every month.
for month in range(1, 13):
    # Compute the dates for each week that overlaps the month.
    c = calendar.monthcalendar(year, month)
    first_week = c[0]
    second_week = c[1]
    third_week = c[2]

    # If there is a Thursday in the first week,
    # the second Thursday is in the second week.
    # Otherwise, the second Thursday must be in
    # the third week.
    if first_week[calendar.THURSDAY]:
        meeting_date = second_week[calendar.THURSDAY]
    else:
        meeting_date = third_week[calendar.THURSDAY]
    print('{:>3}: {:>2}'.format(calendar.month_abbr[month], meeting_date))

```

> Thus, the meeting schedule for the year is as follows:

因此，今年的会议时间表如下：

```text
python 4_33_calendar_secondthursday.py 2021
Jan: 14
Feb: 11
Mar: 11
Apr:  8
May: 13
Jun: 10
Jul:  8
Aug: 12
Sep:  9
Oct: 14
Nov: 11
Dec:  9

```




