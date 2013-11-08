import sys,os
sys.path.insert(1,os.path.abspath('..'))
import pygmt

#recover the spherical harmonic with contouring
ps = 'example_01.ps'
fig = pygmt.GMT_Figure(verbosity=4, autopilot=False)
fig.psbasemap('-R0/6.5/0/7.5 -Jx1i -B0 -P -K ->%s' % ps)

fig.pscoast('-Rg -JH0/6i -X0.25i -Y0.2i -Bg30 -Dc -Glightbrown -Slightblue -K -O ->>%s' % ps)
fig.grdcontour_test('-JH0/6i -C10 -A50+f7p -Gd4i -L-1000/-1 -Wcthinnest,- -Wathin,- -T0.1i/0.02i -K -O ->>%s' % ps, 'geoid.grd')
fig.grdcontour_test('-JH0/6i -C10 -A50+f7p -Gd4i -L-1/1000 -T0.1i/0.02i -K -O ->>%s' % ps, 'geoid.grd')

fig.pscoast('-Rg -JH6i -Y3.4i -Bg30 -B+tLowOrderGeoid -Dc -Glightbrown -Slightblue -K -O ->>%s' % ps)
fig.grdcontour_test('-JH6i -C10 -A50+f7p -Gd4i -L-1000/-1 -Wcthinnest,- -Wathin,- -T0.1i/0.02i -K -O ->>%s' % ps, 'geoid.grd')
fig.grdcontour_test('-JH6i -C10 -A50+f7p -Gd4i -L-1/1000 -T0.1i/0.02i -O ->>%s' % ps, 'geoid.grd')

