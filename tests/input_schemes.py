import pygmt
import numpy as np

lats = np.linspace(0,45, 100)
lons = np.linspace(0,45, 100)
size = np.linspace(0.1,0.3, 100)


#produce the same figure in three different ways
fig = pygmt.GMT_Figure("output.ps", figure_range='g', projection='H7i', verbosity=4)
fig.pscoast('-Glightgray -A500')
fig.psbasemap('-B30g30/15g15') 

#First, pass the numpy arrays
fig.psxy('-Sci', pygmt.GMT_Vector([lons+50,lats,size]))
fig.pswiggle('-W -Z1c', [lons+200,lats,size])

#second, pass a text string indicating a file
np.savetxt("test.txt", zip(lons+100,lats,size))
fig.psxy('-Sci', "test.txt")


fig.close()
