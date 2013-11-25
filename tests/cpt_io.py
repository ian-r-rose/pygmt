import pygmt
import numpy as np


x = np.linspace(0,1, 100)
y = np.linspace(0,1, 100)

X,Y=np.meshgrid(x,y)

fig = pygmt.GMT_Figure('output.ps', figure_range='0/1/0/1', projection='X3i', verbosity=0)

Z = np.cos(np.pi*X)*np.sin(np.pi*Y)
G1 = fig.surface('-I.01/0.01, -R0/1/0/1', input = [X,Y,Z])
c1 = fig.makecpt('-Chot -T-1/1/0.1')
fig.grdimage('', input = G1, cpt = c1)

Z = np.cos(np.pi*X)*np.cos(np.pi*Y)
G2 = fig.surface('-I.01/0.01, -R0/1/0/1', input = [X,Y,Z])
fig.makecpt('-Cjet -T-1/1/0.1', output='c2.cpt')
fig.grdimage('-X3.5i', input = G2, cpt = 'c2.cpt')

Z = np.sin(np.pi*X)*np.cos(np.pi*Y)
G3 = fig.surface('-I.01/0.01, -R0/1/0/1', input = [X,Y,Z])
c3 = fig.grd2cpt('-Cpolar', input=G3)
fig.grdimage('-Y3.5i', input = G3, cpt=c3)

Z = np.sin(np.pi*X)*np.sin(np.pi*Y)
G4 = fig.surface('-I.01/0.01, -R0/1/0/1', input = [X,Y,Z])
c4 = fig.grd2cpt('-Ctopo', input=G4, output='c4.cpt')
fig.grdimage('-X-3.5i', input = G4, cpt = 'c4.cpt')

fig.close()
