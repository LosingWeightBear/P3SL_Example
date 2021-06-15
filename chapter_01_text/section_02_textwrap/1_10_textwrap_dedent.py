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

