#!/usr/bin/env python
from application.models import Mess
from application.config import *
from httplib import *
from urllib import *
from uuid import *

import string
import random

def generate (size = 6, chars = string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
numInserts = 1000

for stringSize in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 4096, 65536]:
  myID = uuid4()
  s = "x"
  for i in range (numInserts):
    conn      = HTTPConnection(config.sys.host, config.sys.port)
    # print("String generated: {0}".format(s))
    # print "Insert #{0}".format(i)
    params = urlencode({'id': myID, 'data': s})
    conn.request("POST", "insert", params, headers)
    response = conn.getresponse()
    if response.status != 200:
      print "Error on insert {0}: {1} {2}".format(i, response.status, response.reason)
  print "Done with {0} inserts on string size {1}".format(numInserts, stringSize)
