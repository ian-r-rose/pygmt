import pygmt
import numpy as np

ps='pygmt_example_03.ps'
fig = pygmt.GMT_Figure(verbosity=4, autopilot=False)
report=fig.fitcircle('-L2',input='sat.xyg')
