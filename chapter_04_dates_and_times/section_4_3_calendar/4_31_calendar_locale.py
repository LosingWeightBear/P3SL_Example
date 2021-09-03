import calendar

c = calendar.LocaleTextCalendar(locale='en_US')
c.prmonth(2021, 7)

print()

c = calendar.LocaleTextCalendar(locale='fr_FR')
c.prmonth(2021, 7)
