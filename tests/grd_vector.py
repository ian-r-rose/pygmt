import pygmt
import numpy as np


lons = np.linspace(-20, 50, 100)
lats = np.linspace(20,70,100)

X,Y = np.meshgrid(lons,lats)

vx = np.sin(Y*np.pi/180.0*5)
vy = -np.cos(X*np.pi/180.0*5)

fig = pygmt.GMT_Figure("output.ps", figure_range='-20/50/20/70', projection='M9i', verbosity=1)
fig.psbasemap('-B0 -P')
fig.pscoast('-Bg30 -Dc -Glightbrown -Slightblue')

gridx = fig.surface('-I3/3 -R-20/50/20/70', [X,Y,vx])
gridy = fig.surface('-I3/3 -R-20/50/20/70', [X,Y,vy])
fig.grdvector('-S.01i -Q0.1i+b+jc  -Wthin',gridx, gridy)

fig.close()
