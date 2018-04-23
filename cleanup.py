#!/usr/bin/python3
# this should get rid of the docs in /docs
# QUESTION: use it with the real program?
import os
import send2trash
from datetime import datetime
os.chdir('./docs')
# TODO: needs a while loop if i want it in the finished program.
print(os.getcwd() + ': ' + str(os.listdir())) # FIXME: needs a time check (every first of month in 20:00)
for i in os.listdir():
    send2trash.send2trash(i)
    print('sent %s to trash' % i)
