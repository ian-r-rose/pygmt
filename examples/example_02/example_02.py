import pygmt

fig = pygmt.GMT_Figure("example_02.ps", figure_range='160/20/220/30r', projection='Oc190/25.5/292/69/4.5i -P', verbosity=0, autopilot=True)
fig.gmtset('FONT_TITLE 30p MAP_ANNOT_OBLIQUE 0')
fig.makecpt('-Crainbow -T-2/14/2', 'g.cpt')
fig.grdimage('-E50 -B10 -Cg.cpt -X1.0i -Y1.25i', 'HI_geoid2.nc')
fig.psscale('-Cg.cpt -D5.1i/1.35i/2.88i/0.4i -Ac -Bx2+lGEOID -By+lm -E')
fig.grd2cpt('-Crelief -Z', 'HI_topo2.nc', 't.cpt')
fig.grdgradient('-A0 -Nt', input='HI_topo2.nc', output='HI_topo2_int.nc')
fig.grdimage('-IHI_topo2_int.nc -B+t\"H@#awaiian @#T@#opo and @#G@#eoid\" -B10 -E50 -Ct.cpt -Y4.5i --MAP_TITLE_OFFSET=0.5i', 'HI_topo2.nc')
fig.psscale('-Ct.cpt -D5.1i/1.35i/2.88i/0.4i -I0.3 -Ac -Bx2+lTOPO -By+lkm')

fig.close()
