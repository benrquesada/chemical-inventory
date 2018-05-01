from configure import Configuration
import argparse, os, re, shutil

parser = argparse.ArgumentParser(description = 'Setup Flask controllers.')

parser.add_argument('-g', '--generate',
                    action = "store_true",
                    help = 'Generate files as opposed to just testing syntax. True or False.')

parser.add_argument('-c', '--config',
                    type = str,
                    help = "Name of the config file to process."
                    )

parser.add_argument('-v', '--verbose',
                    action = "store_true",
                    help = 'Talk a lot.')

args = parser.parse_args()

def error (msg):
  print "OOPS: {0}\n".format(msg)
  exit()

def announce (msg):
  print msg

def hasKey (d, k):
  return isinstance(d, dict) and (k in d)

# http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string
def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

def isDirectoryDictionary (obj):
  return isinstance(obj, dict) and ("directory" in obj)

# http://stackoverflow.com/questions/35784074/does-python-have-andmap-ormap
def isListOfDirectories (layout):
  return  is_sequence(layout) and \
          all(isDirectoryDictionary(obj) for obj in layout)

def check (d):
  #True if hasLayout (cc) else \
  #  error("Top-level should be a 'layout'.")
  #announce("Layout found.") if args.verbose else False
  True if d["fun"]() else error(d["err"]())
  announce(d["aok"]()) if args.verbose else False

def isListOfDictsWithKey (dicts, key):
  return all(map(lambda d: key in d, dicts))

def isListOfObjOfType (ls, t):
  return all(map(lambda o: isinstance(o, t), ls))

def isNonEmptyList (ls):
  return is_sequence(ls) and \
    (len(ls) > 0)

def checkValidMethods (h):
  result = True
  for m in h["methods"]:
    if not m in ["GET", "POST", "PUT", "DELETE"]:
      print "==> {0} is not a valid method.".format(m)
      result = False
  return result

def checkValidRoles (h):
  result = True
  definedRoles = Configuration.from_file('config/roles.yaml').configure()
  for r in h["roles"]:
    if not r in definedRoles:
      print "==> {0} is not a valid role.".format(r)
      result = False
  return result

def findRepeats (ls):
  s = set()
  repeats = set()
  for obj in ls:
    if obj in s:
      repeats.add(obj)
    s.add(obj)
  return repeats

"""
    check ({'fun': lambda: ,
      'err': lambda: "",
      'aok': lambda: ""
    })
"""
def checkSyntax (cc):

  check ({'fun': lambda: cc["layout"],
    'err': lambda: "Top-level should be a 'layout'.",
    'aok': lambda: "Layout found."
  })

  directories = cc["layout"]

  check ({'fun': lambda: isNonEmptyList (directories),
    'err': lambda: "Your directories are not a properly formatted list.",
    'aok': lambda: "Directories are formatted as a list."
  })

  check ({'fun': lambda: isListOfObjOfType (directories, dict),
    'err': lambda: "The file should begin as a list of 'directory' dictionaries.",
    'aok': lambda: "Layout contains a list of 'directory' dictionaries."
  })

  check ({'fun': lambda: isListOfDictsWithKey (directories, "name"),
    'err': lambda: "Every directory should have a 'name' key.",
    'aok': lambda: "All directories have a name."
  })

  # We now know there is a valid list of controllers in every directory
  for d in directories:
    print "------------------"
    print "Checking directory '{0}'".format(d["name"])
    print "------------------"

    controllers = d["controllers"]

    check ({'fun': lambda: isNonEmptyList (controllers),
      'err': lambda: "Directory '{0}' has a non-empty list of controllers.".format(d["name"]),
      'aok': lambda: "Directory '{0}' has a list of controllers.".format(d["name"])
    })

    check ({'fun': lambda: isListOfObjOfType (controllers, dict),
      'err': lambda: "Directory '{0}' has a non-dictionaries in its list of controllers.".format(d["name"]),
      'aok': lambda: "Directory '{0}' has a list of controller dicts.".format(d["name"])
    })

    # Now, we check every controller
    for c in controllers:
      check ({'fun': lambda: hasKey (c, "name"),
        'err': lambda: "Directory '{0}' has a controller missing a 'name'.".format(d["name"]),
        'aok': lambda: "Controller '{0}' has a name.".format(c["name"])
      })

      check ({'fun': lambda: hasKey(c, "handlers"),
        'err': lambda: "'{0}' is missing a 'handlers' key.".format(c["name"]),
        'aok': lambda: "'{0}' has a 'handlers' key.".format(c["name"])
      })

      # We know we have the key now.
      handlers = c["handlers"]
      check ({'fun': lambda: isNonEmptyList (handlers),
        'err': lambda: "Controller '{0}' does not have a list of handlers.".format(c["name"]),
        'aok': lambda: "Controller '{0}' has a list of handlers.".format(c["name"])
      })

      # Check each handler
      for h in handlers:
        check ({'fun': lambda: hasKey (h, "route"),
          'err': lambda: "'{0}' has a handler missing a route.".format(c["name"]),
          'aok': lambda: "Route for '{0}' in '{1}' has a route".format(h["route"], c["name"])
        })

        # Are they all a complete handler
        for key in ["purpose", "route", "methods", "function", "roles"]:
          check ({'fun': lambda: hasKey (h, key),
            'err': lambda: "Handler for route '{0}' is missing '{1}'.".format(h["route"], key),
            'aok': lambda: "Handler for route '{0} has key '{1}'.".format(h["route"], key)
          })

        # Make sure we only have valid methods.
        check ({'fun': lambda: checkValidMethods (h),
          'err': lambda: "Handler for route '{0}' has invalid methods.".format(h["route"]),
          'aok': lambda: "Handler for '{0}' has valid methods.".format(h["route"])
        })

        check ({'fun': lambda: checkValidRoles (h),
          'err': lambda: "Handler for route '{0}' has invalid roles.".format(h["route"]),
          'aok': lambda: "Handler for '{0}' has valid roles.".format(h["route"])
        })

  # Now, make sure none of the routes in any of the controllers are the same

  routes = []
  funs   = []

  print
  print "Looking for repeats of routes and function names."
  print "-------------------------------------------------"
  for d in directories:
    print "Directory {0}".format(d["name"])
    controllers = d["controllers"]
    for c in controllers:
      print "=> Controller: {0}".format(c["name"])
      handlers = c["handlers"]
      for h in handlers:
        print "==> Route {0}".format(h["route"])
        print "==> Func  {0}".format(h["function"])
        print
        routes.append(h["route"])
        funs.append(h["function"])

  print ""
  # Now, do a cute set uniqueness check.
  # http://stackoverflow.com/questions/5278122/checking-if-all-elements-in-a-list-are-unique
  repeats = findRepeats(routes)
  if len(repeats) > 0:
    print "There are repeated routes in your controllers."
    print routes
    print repeats
    for r in repeats:
      print "route: {0}".format(r)
    error("Routes cannot repeat.")

  repeats = findRepeats(funs)
  if len(repeats) > 0:
    print "There are repeated function names in your controllers."
    for f in repeats:
      print "function: {0}".format(f)
    error ("Function names cannot repeat.")

  # If we get here, we pass syntax.
  return True

def createDirectory (dir):
  if not os.path.exists(dir):
    print "Creating directory '{0}'".format(dir)
    os.makedirs(dir)

def touchFile (f):
  open(f, 'a').close()

def copyDefault (src, dest):
  if not os.path.exists(dest):
    print "Copying default file:\n\t'{0}'.".format(src)
    shutil.copy(src, dest)


def touchController(f):
  copyDefault ("config/defaultController.txt", f)

def touchView (f):
  copyDefault ("config/defaultView.txt", f)

def handlerExists (f, h):
  f = open(f, 'r')
  result = False
  for line in f:
    if re.search(h["route"], line):
      print "=> Route '{0}' already exists. Skipping.".format(h["route"])
      result = True
  return result

def getParams(routeString):
  # print "RS: %s" % routeString
  matches = re.findall("<.*?:(.*?)>", routeString)
  if matches:
    return matches
  else:
    return []

def createHandlerInController (controllerFile, d, c, h):
  # If the handler isn't already there
  if not handlerExists(controllerFile, h):
    print "Adding route '{0}' to {1}.".format(h["route"], c["name"])
    cf = open(controllerFile, 'a')
    cf.write("\n")

    cf.write ("# PURPOSE: {0}\n".format(h["purpose"]))
    cf.write ("@app.route('{0}', methods = {1})\n"
      .format (h["route"], h["methods"]))

    for role in h["roles"]:
      cf.write("'{0}')\n".format(role))
    cf.write ("def {0}({1}):\n"
      .format(h["function"],
              ",".join(getParams(h["route"]))
              ))
    cf.write ('  return render_template("views/{0}/{1}View.html", config = config)\n'.format(d["name"], h["function"]))
    cf.write("\n")
    cf.close()

def insertViewName (viewFile, h):
  out = open(viewFile + ".tmp", 'w')
  for line in open(viewFile):
    line = re.sub("VIEWFUNCTION", h["function"], line)
    line = re.sub("VIEWROUTE", h["route"], line)
    out.write(line)
  out.close()
  shutil.copy(viewFile + ".tmp", viewFile)
  os.remove(viewFile + ".tmp")

def insertDefaultInitFile (dir):
  shutil.copy("config/default__init__.txt", dir + "/__init__.py")

def generateFiles (cc):
  directories = cc["layout"]
  for d in directories:
    controllerDir = "application/controllers/" + d["name"]
    viewDir       = "application/templates/views/" + d["name"]
    createDirectory(controllerDir)
    createDirectory(viewDir)
    controllers = d["controllers"]

    for c in controllers:
      controllerFile = controllerDir + "/" + c["name"] + "Controller.py"

      touchController (controllerFile)
      insertDefaultInitFile(controllerDir)

      handlers = c["handlers"]
      for h in handlers:
        createHandlerInController(controllerFile, d, c, h)
        viewFile = viewDir + "/" + h["function"] + "View.html"
        touchView (viewFile)
        insertViewName(viewFile, h)

  # Create the top-level import
  impPath = "application/controllers/__init__.py"
  if os.path.exists(impPath):
    os.remove(impPath)
  imp = open(impPath, 'w')
  for d in directories:
    imp.write("from application.controllers.{0} import *\n".format(d["name"]))
  imp.close()



if __name__ == "__main__":
  if args.config is None:
    cc = Configuration.from_file('config/controllers.yaml').configure()
  else:
    cc = Configuration.from_file(args.config).configure()

  syntaxOK = checkSyntax (cc)

  if syntaxOK:
    print "Syntax checks."

  if syntaxOK and args.generate:
    print
    print "Generating files."
    print "-----------------"
    generateFiles (cc)

