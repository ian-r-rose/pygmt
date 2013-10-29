import sys,os
sys.path.insert(1,os.path.abspath('..'))
import pygmt.api

session = pygmt.api.GMT_Session("My groovy session")
session.option("R,J")
