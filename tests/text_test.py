import pygmt



f = open("test.txt", 'w')
f.write('0.25 0.75 Say test text\n')
f.write('0.5 0.5 two times\n')
f.write('0.75 0.25 fast\n')
f.close()


fig = pygmt.GMT_Figure("output.ps", figure_range='0/1/0/1', projection='X7i', verbosity=4)
fig.pstext('', 'test.txt')
fig.pstext('', ['0.25 0.7 Say test text', '0.5 0.45 two times', '0.75 0.2 fast'])
fig.close()

