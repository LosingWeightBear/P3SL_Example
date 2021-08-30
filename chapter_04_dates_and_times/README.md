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

