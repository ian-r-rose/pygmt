import sys, os
sys.path.insert(1,os.path.abspath('..'))
import pygmt



f = open("test.txt", 'w')
f.write('0.25 0.75 Say test text\n')
f.write('0.5 0.5 three times\n')
f.write('0.75 0.25 fast\n')
f.close()

f = open("test1.txt", 'w')
f.write('0.25 0.7 Say test text\n')
f.write('0.5 0.45 three times\n')
f.write('0.75 0.2 fast\n')
f.close()

f = open("test1.txt", 'r')


fig = pygmt.GMT_Figure("output.ps", figure_range='0/1/0/1', projection='X7i', verbosity=4)
fig.pstext('', 'test.txt')
fig.pstext('', f)
fig.pstext('', ['0.25 0.65 Say test text', '0.5 0.4 three times', '0.75 0.15 fast'])
fig.close()

