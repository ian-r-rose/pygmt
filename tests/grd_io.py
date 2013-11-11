import pygmt

fig = pygmt.GMT_Figure('output.ps', figure_range='220/300/20/65', projection='B260/40/20/65/7i',verbosity=1)
fig.grdcut('-R220/300/20/65 -V4', input='geoid.grd', output='namer_geoid.grd')
fig.grdinfo('', 'namer_geoid.grd')

fig.grd2cpt('-Chot', 'namer_geoid.grd', 'pal.cpt')
fig.pscoast('-Bg30 -Dc -Glightbrown -Slightblue')
fig.grdcontour('-C10 -A10+f7p -Gd4i', 'namer_geoid.grd')


g = fig.read_grid('geoid.grd')
fig.grdcontour('-C17 -A10+f7p -Gd4i -Wthick,blue', g)

fig.close()

