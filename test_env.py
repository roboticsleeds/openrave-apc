from openravepy import *
import openravepy

env = Environment()  # create the environment
env.SetViewer('qtcoin')  # start the viewer
env.Load('amazon_picking_challenge_env.xml')  # load a scene
