import pygmt

ex_name='pygmt_example_03'

ps1=ex_name+'a.ps'
fig = pygmt.GMT_Figure(verbosity=4, autopilot=False)


report=fig.fitcircle('-L2',input="sat.xyg")

#Stolen from command line until tifcircle works
proj_option = '-C{}/{} -T{}/{} -S -Fpz -Q'.format(\
                330.169184777,18.4206532702,52.7451972868,21.2040074195)

sat_pg  = fig.project(proj_option,input="sat.xyg")
ship_pg = fig.project(proj_option,input="ship.xyg")

R=fig.gmtinfo('-I100/25',input=sat_pg)
fig.psxy('-Rg -JX -O -Sp0.03i -> %s' % ps1, input=ship_pg)
fig.psxy('-Rg -JX -O -Sp0.03i -> %s' % ps1, input=sat_pg)

