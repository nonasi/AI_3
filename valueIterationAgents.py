# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    allStates = mdp.getStates() 
    vPrimes = util.Counter() #  A Counter is a dict with default 0
    
    iteration = 0
    while iteration < iterations:
        
        for s in allStates: 
            if mdp.isTerminal(s):
                vPrimes[s] = mdp.getReward(s, None, s);
            else: 
                sreward = mdp.getReward(s, None, s)
                vPrimes[s] = sreward + discount * self.utilOfBestAction(mdp, s )
               
        for s in allStates:
            self.values[s] = vPrimes[s]
            
        iteration +=1
    
  """Returns the value of the best action to take given that we are
   at state s. 
   s =  current state
  """ 
  def utilOfBestAction (self, mdp, s):
    possibleActions =  mdp.getPossibleActions(s) 
    import sys

    maxUtility = -sys.maxint-1 # equivalent to "-infinity"
    
    
    for action in possibleActions :
            
        transitionStatesAndProbs = mdp.getTransitionStatesAndProbs(s, action)
        
        utilityOfAction = self.getPUsumForGivenAction (mdp, transitionStatesAndProbs, s, action)
        if utilityOfAction >= maxUtility:
            maxUtility = utilityOfAction 
  
    return maxUtility
  
  """ transitionStatesAndProbs a list of (nextState, prob) pairs for a given state
  returns the sum of the probabilities and utilities of each action
  """
  def getPUsumForGivenAction (self, mdp, transitionStatesAndProbs,s, action):
    utilityOfAction = 0 
    for tsAndP in transitionStatesAndProbs:
        nextState = tsAndP[0]
        transitionProbability = tsAndP[1]
        utilityOfAction += (transitionProbability * self.values[nextState]) # 
                
    return utilityOfAction
  
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    qvalue = 0
    for (next_state, probability) in self.mdp.getTransitionStatesAndProbs(state, action):
        qvalue += probability * (self.mdp.getReward(state, action, next_state) + 
                                 self.discount * self.getValue(next_state))
    
    return qvalue
    #util.raiseNotDefined()

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    #this method looks at all the neighboring states, 
    #then returns the action that attempts to goto the state with the highest utility
    print "getPolicy ", state    
    legalActions=self.mdp.getPossibleActions(state)
    
    if len(legalActions)<1:
        print "-getPolicy No legal actions"
        return None

    import sys
    maxValue= -sys.maxint-1 #-infinity
    bestAction = None
    
    for action in legalActions:
        statesReachable=self.mdp.getTransitionStatesAndProbs(state,action)
        
        expectedUtility=0
        for newstate in statesReachable:
            expectedUtility=expectedUtility+newstate[1]*self.getValue(newstate[0])

        if expectedUtility >= maxValue:
            maxValue=expectedUtility
            bestAction=action
    return bestAction

    #util.raiseNotDefined()


  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
