import sys,os
sys.path.insert(1,os.path.abspath('..'))
import pygmt
import numpy as np

lats = np.linspace(0,45, 100)
lons = np.linspace(0,45, 100)
size = np.linspace(0.1,0.3, 100)


#produce the same figure in three different ways
fig = pygmt.GMT_Figure("output.ps", range='g', projection='H7i', verbose=True)
fig.pscoast('-Glightgray -A500')
fig.psbasemap('-B30g30/15g15') 

#First, pass the numpy arrays
fig.psxy('-Sci', [lons+50,lats,size])

#second, pass a text string indicating a file
np.savetxt("test.txt", zip(lons+100,lats,size))
fig.psxy('-Sci', "test.txt")


#third, pass a python file which is open for reading
np.savetxt("test.txt", zip(lons+150,lats,size))
f = open("test.txt")
fig.psxy('-Sci', f)


fig.close()
