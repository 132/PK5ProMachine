import os
filename = "f1.txt"
statbuf = os.stat(filename)
print("Modification time: {}".format(statbuf.st_mtime))
