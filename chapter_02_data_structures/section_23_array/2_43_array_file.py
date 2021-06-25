import array
import binascii
import tempfile
import os

a = array.array('i', range(5))
print('A1:', a)

# Write the array of numbers to a temporary file.
# for Windows close the tmp file before open it again
output = tempfile.NamedTemporaryFile(delete=False) # for windows set delelte as False
a.tofile(output.file) # Must pass an *actual* file
output.flush()
output.close() # close the tmp file

# Read the raw data.
with open(output.name, 'rb') as input:
    raw_data = input.read()
    print('Raw Contents:', binascii.hexlify(raw_data))

    # Read the data into an array.
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print('A2:', a2)


os.remove(output.name) # delete the tmp file