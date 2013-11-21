import pygmt

fig = pygmt.GMT_Figure("output.ps", figure_range='g', projection='H7i', verbosity=4, autopilot=True)
report=fig.fitcircle('-L2 -V4',input='sat.xyg')
fig.pstext('-F+a30 -N -Gred',report)

fig.fitcircle('-L2 -V4',input='sat.xyg', output='tmp.txt')
fig.pstext('-F+a80 -N -Gblue',input='tmp.txt')

fig.close() 

