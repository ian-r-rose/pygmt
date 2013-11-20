import pygmt 

ps='pygmt_example_12.ps'
fig = pygmt.GMT_Figure(verbosity=4, autopilot=False)

net.xy = fig.triangulate('-M',input='table_5.11')
fig.psxy('-R0/6.5/-0.2/6.5 -JX3.06i/3.15i -B2f1 -BWSNe -Wthinner\
            -P -K -X0.9i -Y4.65i', input=net.xy)
fig.psxy('-R -J -O -K -Sc0.12i -Gwhite -Wthinnest',input=net.xy)
