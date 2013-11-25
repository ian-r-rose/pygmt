import pygmt

fig = pygmt.GMT_Figure("example_02.ps", figure_range='160/20/220/30r', projection='Oc190/25.5/292/69/4.5i -P', verbosity=1, autopilot=True)
fig.gmtset('FONT_TITLE 30p MAP_ANNOT_OBLIQUE 0')
g = fig.makecpt('-Crainbow -T-2/14/2')
fig.grdimage('-E50 -B10 -X1.0i -Y1.25i', input = 'HI_geoid2.nc', cpt=g)
fig.psscale('-D5.1i/1.35i/2.88i/0.4i -Ac -Bx2+lGEOID -By+lm -E', cpt=g)
t = fig.grd2cpt('-Crelief -Z', 'HI_topo2.nc')
gradient = fig.grdgradient('-A0 -Nt', input='HI_topo2.nc')
fig.grdimage('-B+t\"H@#awaiian @#T@#opo and @#G@#eoid\" -B10 -E50 -Y4.5i --MAP_TITLE_OFFSET=0.5i',\
              input = 'HI_topo2.nc', intensity=gradient, cpt=t)
fig.psscale('-D5.1i/1.35i/2.88i/0.4i -I0.3 -Ac -Bx2+lTOPO -By+lkm', cpt=t)

fig.close()
