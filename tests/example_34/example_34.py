import pygmt
import numpy as np

fig = pygmt.GMT_Figure('example_34.ps', figure_range='-6/20/35/52', projection='M4.5i -P', verbosity=2, autopilot=True)
fig.gmtset('FORMAT_GEO_MAP dddF')
fig.pscoast('-FFR,IT+gP300/8 -Glightgray -Baf -BWSne -X2i ')
fig.makecpt('-Cglobe -T-5000/5000/500', 'pal.cpt')
fig.grdgradient('-A15 -Ne0.75 ', input='FR+IT.grd', output='FR+IT_int.grd')
fig.grdimage('-IFR+IT_int.grd -Cpal.cpt -Y4.5i -Baf -BWsnE+t\"Franco-Italian-Union\" ', 'FR+IT.grd')
fig.pscoast('-FFR,IT+gred@60')
fig.close()
