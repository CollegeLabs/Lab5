from src.mazeProblemSolvingAgentClass import MazeProblemSolvingAgent
import collections

class MazeProblemSolvingAgentSMART(MazeProblemSolvingAgent):
  def __init__(self, initial_state=None, dataGraph=None, goal=None, program=None):
    super().__init__(initial_state,dataGraph,goal)
    self.performance=len(dataGraph.nodes())*0.3
    self.path=None

    if program is None or not isinstance(program, collections.abc.Callable):
      print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

      def program(percept):
        return eval(input('Percept={}; action? '.format(percept)))

    self.program = program

  def search(self, problem):
    seq = self.program(problem)
    solution=self.actions_path(seq.path()) if seq else None
    #print("Number of nodes expanded for this path = ".format(len(seq.path())))
    #not sure if the above is what hanna wants, but it gives the number of nodes traveled from start to end
    print("Path cost of solution is: {}".format(len(solution)))
    print("Solution (a sequence of actions) from the initial state to a goal: {}".format(solution))
    self.path=seq.path()
    #problem.initial = self.state #initial solution to change current state when changing goals
    return solution
  
  def actions_path(self, p):
    acts=[]
    for n in p:
      acts.append(n.action)
    return acts[1:]