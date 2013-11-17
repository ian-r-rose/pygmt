import pygmt


fig = pygmt.GMT_Figure('example_09.ps', figure_range='185/250/-68/-42', projection='m0.13i', verbosity=4)

fig.pswiggle('-Ba10f5 -BWSne+g240/255/240 -G+red -G-blue -Z2000 -Wthinnest -S240/-67/500/@~m@~rad --FORMAT_GEO_MAP=dddF', input='tracks.txt')
fig.psxy('-Wthicker', input='ridge.xy')
fig.psxy('-Wthinner', input='fz.xy')
fig.gmtconvert('-El', input='tracks.txt', output="tmp.txt")
fig.pstext('-F+f10p,Helvetica-Bold+a50+jRM+h -D-0.05i/-0.05i', input="tmp.txt")
fig.close()
