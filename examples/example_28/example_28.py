import pygmt


ps='example_28.ps'
fig = pygmt.GMT_Figure(autopilot=False, verbosity=4)

kilauea = fig.makecpt('-Ccopper -T0/1500/100 -Z')
gradient = fig.grdgradient('-Nt1 -A45', input='Kilauea.utm.nc')
fig.grdimage('-Jx1:160000 -P -K --FORMAT_FLOAT_OUT=%%.10g --FONT_ANNOT_PRIMARY=9p ->%s' % ps, input='Kilauea.utm.nc',\
              intensity=gradient, cpt=kilauea)
fig.pscoast('-RKilauea.utm.nc -Ju5Q/1:160000 -O -K -Df+ -Slightblue -W0.5p -B5mg5m -BNE \
	--FONT_ANNOT_PRIMARY=12p --FORMAT_GEO_MAP=ddd:mmF ->>%s' % ps)
fig.psbasemap(' -R -J -O -K --FONT_ANNOT_PRIMARY=9p -Lf155:07:30W/19:15:40N/19:23N/5k+l1:16,000+u \
	--FONT_LABEL=10p ->>%s' %ps)
fig.psbasemap(' -RKilauea.utm.nc+Uk -Jx1:160 -B5g5+u"@:8:000m" -BWSne -O --FONT_ANNOT_PRIMARY=10p \
	--MAP_GRID_CROSS_SIZE_PRIMARY=0.1i --FONT_LABEL=10p ->>%s' % ps)
fig.close()
