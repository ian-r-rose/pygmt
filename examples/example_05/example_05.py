import pygmt


f = open('gray.cpt', 'w')
f.write('-5 128 5 128')
f.close()

fig = pygmt.GMT_Figure('example_05.ps', verbosity=4)

sombrero = fig.grdmath('-R-15/15/-15/15 -I0.3 X Y HYPOT DUP 2 MUL PI MUL 8 DIV COS EXCH NEG 10 DIV EXP MUL')
intens = fig.grdgradient('-A225 -Nt0.75', input=sombrero)
fig.grdview('-B5 -Bz0.5 -BSEwnZ -N-1+gwhite -Qs -p120/30 -X1.5i -R-15/15/-15/15 -JX6i -JZ2i', input=sombrero, intensity=intens, cpt='gray.cpt')
fig.pstext('-R0/11/0/8. -Jx1i -F+f50p,ZapfChancery-MediumItalic+jBC', [ '4.1 5.5 z(r) = cos (2@~p@~r/8) @~\327@~e@+-r/10@+'])
fig.close()

