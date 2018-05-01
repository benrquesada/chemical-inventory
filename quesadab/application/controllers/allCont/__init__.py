import glob, os

controllers = []

directoryOfThisFile = os.path.dirname(os.path.realpath(__file__))
# print "cwd: {0} thisFile: {1}".format(os.getcwd(), directoryOfThisFile)

for file in glob.glob(directoryOfThisFile + "/*Controller.py"):
    # print "File: {0}".format(file)
    controllers.append(os.path.splitext(os.path.basename(file))[0])
      
# print "Found controllers: {0}".format(controllers)
__all__ = controllers

