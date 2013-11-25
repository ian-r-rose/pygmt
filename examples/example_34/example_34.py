import pygmt
import numpy as np

fig = pygmt.GMT_Figure('example_34.ps', figure_range='-6/20/35/52', projection='M4.5i', verbosity=2, autopilot=True, portrait=True)
fig.gmtset('FORMAT_GEO_MAP dddF')
fig.pscoast('-FFR,IT+gP300/8 -Glightgray -Baf -BWSne -X2i ')
c = fig.makecpt('-Cglobe -T-5000/5000/500 -Z', 'z.cpt')
gradient = fig.grdgradient('-A15 -Ne0.75 ', input='FR+IT.grd')
fig.grdimage('-Y4.5i -Baf -BWsnE+t\"Franco Italian Union\" ', 'FR+IT.grd', \
              cpt='z.cpt',intensity=gradient)
fig.pscoast('-FFR,IT+gred@60')
fig.close()
