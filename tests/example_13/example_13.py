import pygmt
import numpy as np

x = np.linspace(-2,2, 41)
y = np.linspace(-2,2, 41)
X,Y = np.meshgrid(x,y)
Z = X*np.exp(-X*X-Y*Y)

ps = 'example_13.ps'
fig = pygmt.GMT_Figure('example_13.ps', verbosity=4, autopilot=False)
#z = fig.grdmath('-R-2/2/-2/2 -I0.1 X Y R2 NEG EXP X MUL')
z = fig.surface('-R-2/2/-2/2 -I0.1', [X,Y,Z])
dzdx = fig.grdmath(z, 'DDX')
dzdy = fig.grdmath(z, 'DDY')
fig.grdcontour('-JX3i -B1 -BWSne -C0.1 -A0.5 -K -P -Gd2i -S4 -T0.1i/0.03i ->%s' % ps, dzdx)
fig.grdcontour('-J -B -C0.05 -A0.2 -Gd2i -S4 -T0.1i/0.03i -Xa3.45i -K -O ->>%s' % ps, dzdy)
fig.grdcontour('-J -B -C0.05 -A0.1 -Gd2i -S4 -T0.1i/0.03i -Y3.45i -K -O ->>%s' % ps, z)
fig.grdcontour('-J -B -C0.05 -Gd2i -S4 -X3.45i -K -O ->>%s' % ps, z)
fig.grdvector('-I0.2 -J -O -Q0.1i+e+n0.25i -Gblack -W1p -S5i --MAP_VECTOR_SHAPE=0.5 ->>%s' % ps, dzdx, dzdy)
fig.close()
