import pygmt
import numpy as np
from scipy.special import sph_harm
from numpy.random import random_sample

#come up with n random points on a sphere
n=10000
x = random_sample(n)-0.5
y = random_sample(n)-0.5
z = random_sample(n)-0.5
lats = np.arccos( z/np.sqrt(x*x+y*y+z*z))
lons = np.arctan2( y, x )+np.pi

#evaluate a spherical harmonic on that sphere
vals = sph_harm(4,9, lons, lats).real
vals = vals/np.amax(vals)

lons = lons*180.0/np.pi
lats = 90.0-lats*180.0/np.pi

#recover the spherical harmonic with contouring
fig = pygmt.GMT_Figure("output.ps", figure_range='g', projection='G-75/41/7i', verbosity=4)
dataset = fig.blockmean('-I5/5 -Rg', [lons,lats,vals])
grid = fig.surface('-I5/5 -Rg', dataset)
c = fig.grd2cpt('-Chot', grid, output=None)
fig.grdimage('-E100i', grid, cpt=c)
fig.grdcontour('-Wthick,black -C0.2', grid)
fig.psxy('-Sp.1c', [lons,lats,vals])

fig.close()
