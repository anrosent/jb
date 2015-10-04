import fileinput
import json

from jb.parse import browse 

jstr = '\n'.join(fileinput.input())
browse(jstr)
