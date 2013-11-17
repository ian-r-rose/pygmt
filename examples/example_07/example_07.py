import pygmt
import numpy as np

#set up the figure class, tell it the output file, range option and projection
fig = pygmt.GMT_Figure('example_07.ps', figure_range='-50/0/-10/20', projection='M9i', verbosity=0, autopilot=True)

#lay down the coastlines
fig.pscoast('-Slightblue -GP300/26:FtanBdarkbrown -Dl -Wthinnest -B10 --FORMAT_GEO_MAP=dddF')

#plot a bunch of stuff
fig.psxy('-Wthinner,-', 'fz.xy')
fig.psxy('-Wthinnest -Gred -h1 -Sci -i0,1,2s0.01', 'quakes.xym')
fig.psxy('-Wthin,blue', 'isochron.xy')
fig.psxy('-Wthicker,orange', 'ridge.xy')

#make the legend
fig.psxy('-Gwhite -Wthick -A', [ np.array( [-14.5, -2. , -2.,  -14.5] ), \
                                 np.array( [ 15.2,  15.2, 17.8, 17.8] ) ] )
fig.psxy('-Gwhite -Wthinner -A', [ np.array( [-14.35, -2.15 , -2.15,  -14.35] ), \
                                   np.array( [ 15.35,  15.35,  17.65,  17.65] ) ] )
fig.psxy('-Sc0.08i -Gred -Wthinner', [ np.array( [-13.5] ), np.array([16.5]) ] )
fig.pstext('-F+f18p,Times-Italic+jLM', ['-12.5 16.5 ISC Earthquakes',] )

#label the continents
fig.pstext('-F+f30,Helvetica-Bold,white=thin', ['-43 -5 SOUTH' , \
                                                '-43 -8 AMERICA' , \
                                                '-7  11 AFRICA' ] )

#close the figure
fig.close()

