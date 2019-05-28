import os
import textwrap

LINE_LENGHT = 65

inputfile = 'test_file.txt'
outputfile = 'wrapped_' + inputfile

with open(inputfile, 'r') as f:
    mail_content = f.read()

twp = textwrap.TextWrapper(
    width=LINE_LENGHT, replace_whitespace=False
)
wrapped_text = twp.fill(mail_content)

with open(outputfile, 'x') as f:
    f.write(wrapped_text)
    # f.writelines(
    #     ('%s\n' % line for line in wrapped_mail)
    # )
