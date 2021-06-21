import string

t = string.Template('$var')
print(t.pattern)
print('*' * 50)
print(t.pattern.pattern)