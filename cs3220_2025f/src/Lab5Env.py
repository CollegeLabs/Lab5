from src.mazeData import *
from src.maze2025GraphClass import mazeGraph
from pyvis.network import Network
from src.PS_agentPrograms import *
from src.mazeProblemClass import MazeProblem
from src.agents import *
from src.naigationEnvironmentClass import MazeNavigationEnvironment
from src.Lab5Agents import Ghost
from src.environmentClass import Environment
from src.maze2025GraphClass import *

def makeMaze(n):
  size = (n,n)
  proba_0 =0.25 # resulting array will have 25%? of zeros
  proba_Enemy =0.1 # resulting array will have 10%? of enemy
  arrMaze=np.random.choice([0, 1, 2], size=size, p=[proba_0, 1-proba_0-proba_Enemy, proba_Enemy] ) #0=asteroid, 1=open, 2=enemy
  return arrMaze

def MazeCheck(mainMaze, initState, goalState):
  if (initState != 1):
    mainMaze[initState] = 1
  if (goalState != 1):
    mainMaze[goalState] = 1

class Lab5NavEnvironment(Environment):
  def __init__(self, navGraph, maze):
    super().__init__()
    self.status = navGraph
    self.maze = maze

  def execute_action(self, agent, action): 
        '''Check if agent alive, if so, execute action'''
        if self.is_agent_alive(agent):
            """Change agent's location -> agent's state;
            Track performance.
            -1 for each move."""
          
            agent.state=agent.update_state(agent.state, action)
            print(f"Agent in {agent.state} with performance = {agent.performance}")
            x, y = agent.state
            if (self.maze[x][y] == 1): #if the agent is NOT under attack
              agent.performance -= 1
            elif (self.maze[x][y] == 2):
              agent.performance = agent.performance*2
              print(f"Agent in {agent.state} found a food pellet. Performance Doubled!")
              self.maze[x][y] = 1
              #goals.pop()
            else: #the spaceship is under attack (0's are walls, so they're ignored before this)
              print(f"Agent in {agent.state} is under attack!")
              enemy = Ghost(self.status) 
              if (agent.performance <= enemy.power):
                agent.performance = 0 #dies instantly
              else:
                agent.performance = agent.performance*0.9 #removes 10% of performance
            self.update_agent_alive(agent)

  def percept(self, agent):
    #Returns the agent's location, and the location status (Dirty/Clean).
    return agent.state

  def is_agent_alive(self, agent):
    return agent.alive

  def update_agent_alive(self, agent):
    if agent.performance <= 0:
      agent.alive = False
      print("Agent {} is dead.".format(agent))
    elif agent.state==agent.goal or len(agent.seq)==0:
      agent.alive = False
      if len(agent.seq)==0:
        print("Agent reached all goals")
      else:
        print(f"Agent reached the goal: {agent.goal}")
       
  def step(self):
    if not self.is_done():
        actions = []
        for agent in self.agents:
          if agent.alive:
            #with agent.state because for PS Agent we don't need to percive
            action=agent.seq.pop(0)
            print("Agent decided to do {}.".format(action))
            actions.append(action)
          else:
            actions.append("")
            
        for (agent, action) in zip(self.agents, actions):
          self.execute_action(agent, action)
    else:
        print("There is no one here who could work...")
