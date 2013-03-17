# textDisplay.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import pacman, time

DRAW_EVERY = 1
SLEEP_TIME = 0 # This can be overwritten by __init__
DISPLAY_MOVES = False
QUIET = False # Supresses output

class NullGraphics:
  def initialize(self, state, isBlue = False):
    pass
  
  def update(self, prevState):
    pass
  
  def pause(self):
    time.sleep(SLEEP_TIME)
    
  def draw(self, state):
    print state
  
  def finish(self):
    pass

class PacmanGraphics:
  def __init__(self, speed=None):
    if speed != None:
      global SLEEP_TIME
      SLEEP_TIME = speed
  
  def initialize(self, state, isBlue = False):
    self.draw(state)
    self.pause()
    self.turn = 0
    self.agentCounter = 0
    
  def update(self, prevState):
    numAgents = len(prevState.agentStates)
    self.agentCounter = (self.agentCounter + 1) % numAgents
    if self.agentCounter == 0:
      self.turn += 1
      if DISPLAY_MOVES:
        ghosts = [pacman.nearestPoint(prevState.getGhostPosition(i)) for i in range(1, numAgents)]
        print "%4d) P: %-8s" % (self.turn, str(pacman.nearestPoint(prevState.getPacmanPosition()))),'| Score: %-5d' % prevState.score,'| Ghosts:', ghosts
      if self.turn % DRAW_EVERY == 0:
        self.draw(prevState)
        self.pause()
    if prevState._win or prevState._lose:
      self.draw(prevState)
    
  def pause(self):
    time.sleep(SLEEP_TIME)
    
  def draw(self, state):
    print state
  
  def finish(self):
    pass
