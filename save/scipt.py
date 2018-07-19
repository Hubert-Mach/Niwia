### This is ugly workaround to make importing from parent dir possible
### Think of using environmental PATH as solution
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from niwia import *
import time

# Template 1
# Your code goes here.
p = Player()
for i in range(0,5):
    p.move_down()
    time.sleep(1)
