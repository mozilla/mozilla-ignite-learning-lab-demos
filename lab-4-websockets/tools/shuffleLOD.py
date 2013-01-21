"""
Andor Salga

This script is intended to be used with the "House of Cards" dataset created by Radiohead.

Place the script in the same directory as the .CSV files.

The script will first rearrange the data in each file so the points are evenly distributed
instead of in a linear top-down order. When the data is in this order, we can effectively truncate
parts of the file while still keeping the general 'shape' of the point cloud. This will create our
different LODs (Levels of Detail).

The script will then create several directories and copy a certain percent of the original data from each 
file/frame and place that subset of data into the respective directory.

For exampple, if 4 was passed in as an argument for numLevels, 4 directories will be created: 
25-percent, 50-percent, 75-percent and 100-percent. Within 25-percent, all the frames will be present, however  
each frame will only contain 25 percent of the original data.

"""

import random
import sys
import os

# Usage: python shuffleLOD.py 4
if (len(sys.argv) < 2):
  print "Usage: python shuffleLOD.py numLevels\n"
else:
    # Find out how many files we need to create for every input file
    numLevels = float(sys.argv[1])

    # Seperate the increasing levels of detail in directories so swapping
    # between LODs is as easy as changing a directory in the rendering script
    folder = 1.0
    while folder <= numLevels:
      dirName = str(int(folder/numLevels * 100.0)) + "-percent"

      if not os.path.exists(dirName):
        os.mkdir(dirName)
      folder = folder + 1

    # Iterate over every frame/file
    # Instead of this magic number, we should first find out how many
    # .CSV files there are in the directory.
    currFrame = 1
    while currFrame <= 2101:
      
      # Read the file into an array and shuffle it
      arr = []
      file = open(str(currFrame) + ".csv")
      while 1:
        line = file.readline()
        arr.append(line)
        if not line: break 
      file.close()
      random.shuffle(arr);

      # Iterate over each level of detail and write out a file to the respective
      # folder. If 4 was pass in as numLevels argument, folder 25percent will have
      # all the files and each file will contain 25 percent of the original data
      currLOD = 1.0
      while currLOD <= numLevels:

        # Find out how much of the file we want
        percent = currLOD/numLevels
        linesToCopy = int(percent * len(arr))

        dirName = str(int(percent * 100.0)) + "-percent"
        FILE = open( dirName + "/" + str(currFrame) + ".csv", "w")
        i = 0
        while i < linesToCopy:
          FILE.write(str(arr[i]))
          i = i + 1
        FILE.close()

        currLOD = currLOD + 1
      currFrame = currFrame + 1
