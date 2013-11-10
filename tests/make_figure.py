import pygmt

fig = pygmt.GMT_Figure("output.ps", figure_range='g', projection='H7i')
fig.pscoast('-Glightgray -A500')
fig.psbasemap('-B30g30/15g15') 
fig.close()
