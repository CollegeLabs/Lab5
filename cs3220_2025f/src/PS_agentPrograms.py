#How do we decide which node from the frontier to expand next?
from src.nodeClass import Node
from queue import PriorityQueue

import math

nodeColors={
    "start":"red",
    "goal": "green",
    "frontier": "orange",
    "expanded":"pink"
}


def A_StarSearchAgentProgram(f=None):
  
    #f=math.dist
    
    def program(problem):
      #print("Hi")
      node_expanded = 0
      p_cost = 0
      node = Node(problem.initial)
      frontier = PriorityQueue()
      h=node.path_cost+round(math.dist(node.state, problem.goal),3)
      frontier.put((h,node))
      reached = {problem.initial:node}

      while frontier:
        print(frontier.queue)
        node = frontier.get()[1]
        print("The node {} is extracted from frontier:".format(node.state))
        node_expanded += 1
        if problem.goal_test(node.state):
          print("We have found our goal: {}".format (node.state))
          print("Path cost = {} and nodes extracted = {}".format(p_cost, node_expanded))
          return node

        #reached.add(node.state)
        for child in node.expand(problem):
            if child.state not in reached or child.path_cost<reached[child.state].path_cost:
                #print(child)
                print("The child node {}.".format(child))
                h=child.path_cost+round(f(child.state, problem.goal),3)
                frontier.put((h,child))
                reached.update({child.state:child})
                p_cost += 1
      return None
    return program



def BestFirstSearchAgentProgram(f=None):
  #with BFS we choose a node, n, with minimum value of some evaluation function, f (n).
    
    def program(problem):
      node = Node(problem.initial)
      #node.color=nodeColors["start"]
      #print(node.state)
      frontier = PriorityQueue()
      frontier.put((1,node))
      print(f"The {node} is being pushed to frontier ...")
      #node.color=nodeColors["frontier"]
      reached = {problem.initial:node}

      while frontier:
        node = frontier.get()[1]
        #node.color=nodeColors["expanded"]
        print(f"The {node} is being extracted from frontier ...")

        if problem.goal_test(node.state):
          node.color=nodeColors["goal"]
          print(f"We have found our goal:  {node}!")
          return node

        #reached.add(node.state)
        for child in node.expand(problem):
            if child.state not in reached or child.path_cost<reached[child.state].path_cost:
                frontier.put((1,child))
                print(f"The child {child} is being pushed to frontier ...")
                #child.color=nodeColors["frontier"]
                reached.update({child.state:child})
            
        #node.color=nodeColors["expanded"]
      return None

    return program
  

def BestFirstSearchAgentProgramForShow(f=None):
  #with BFS we choose a node, n, with minimum value of some evaluation function, f (n).
    
    def program(problem):
      #print(111)
      steps = 0
      allNodeColors = []
      nodeColors = {k : 'white' for k in problem.graph.nodes()}

      node = Node(problem.initial)
      nodeColors[node.state] = "yellow"
      steps += 1
      allNodeColors.append(dict(nodeColors))

      #print(node.state)
      frontier = PriorityQueue()
      frontier.put((1,node))

      nodeColors[node.state] = "orange"
      steps += 1
      allNodeColors.append(dict(nodeColors))



      reached = {problem.initial:node}

      while frontier:
        node = frontier.get()[1]
        nodeColors[node.state] = "red"
        steps += 1
        allNodeColors.append(dict(nodeColors))
        #print(node)

        if problem.goal_test(node.state):
          nodeColors[node.state] = "green"
          steps += 1
          allNodeColors.append(dict(nodeColors))
          return (node,steps,allNodeColors)
          

        #reached.add(node.state)
        for child in node.expand(problem):
            if child.state not in reached or child.path_cost<reached[child.state].path_cost:
                frontier.put((1,child))
                nodeColors[child.state] = "orange"
                steps += 1
                allNodeColors.append(dict(nodeColors))

                reached.update({child.state:child})

        # modify the color of explored nodes to blue
        nodeColors[node.state] = "blue"
        steps += 1
        allNodeColors.append(dict(nodeColors))
            
      return None

    return program
"""
def IDA_StarSearchAgentProgram(f=None):
    if f is None:
        f = lambda s, g: math.dist(s, g)

    
    def program(problem):
        root = Node(problem.initial)
        f_limit = root.path_cost + f(root.state, problem.goal)

        while True:
            solution, new_limit = DFS_Contour(root, f_limit, problem)
            if solution is not None:
                return solution
            if new_limit == float('inf'):
                return None
            f_limit = new_limit
    

    def DFS_Contour(node, f_limit, problem):
        f_cost = node.path_cost + f(node.state, problem.goal)
        if f_cost > f_limit:
            return None, f_cost
        if problem.goal_test(node.state):
            return node, f_limit

        next_f = float('inf')
        for child in node.expand(problem):
            solution, new_limit = DFS_Contour(child, f_limit, problem)
            if solution is not None:
                return solution, f_limit
            next_f = min(next_f, new_limit)

        return None, next_f
    
    return program
"""

def IDA_StarSearchAgentProgram(f=None):
    def program(problem):
        import math
        node_expanded = 0
        p_cost = 0
        node = Node(problem.initial)

        def safe_f(a, b):
            try:
                return f(a, b)
            except (TypeError, ValueError):
                # Fallback for scalar or mismatched-dimension states
                try:
                    return abs(a - b)
                except Exception:
                    # If not numeric, just return 0 as neutral heuristic
                    return 0


        f_limit = node.path_cost + round(safe_f(node.state, problem.goal), 3)
        print("Initial f-limit =", f_limit)

        while True:
            next_f = float("inf")
            print("\nStarting new iteration with f-limit =", f_limit)

            def _state_key(s):
                """Return a stable, hashable key for a state (works for tuple/list/dict/scalars)."""
                try:
                    hash(s)
                    return s
                except TypeError:
                    # list -> tuple, dict -> tuple of items sorted, other -> repr fallback
                    if isinstance(s, list):
                        return tuple(s)
                    if isinstance(s, dict):
                        return tuple(sorted(s.items()))
                    return repr(s)

            def dfs_contour(node, f_limit, path=None):
                nonlocal next_f#, node_expanded, p_cost

                if path is None:
                    path = set()

                key = _state_key(node.state)

                # Loop/cycle detection
                if key in path:
                    # debug print so we can see what's looping
                    print(f"Cycle detected, skipping state: {node.state} (key={key})")
                    return None

                path.add(key)

                # compute f-cost using your safe_f wrapper
                f_cost = node.path_cost + round(safe_f(node.state, problem.goal), 3)
                if f_cost > f_limit:
                    next_f = min(next_f, f_cost)
                    path.remove(key)
                    return None

                if problem.goal_test(node.state):
                    print("We have found our goal:", node.state)
                    #print("Path cost = {} and nodes expanded = {}".format(p_cost, node_expanded))
                    return node

                for child in node.expand(problem):
                    #node_expanded += 1
                    # optional debug to see expansion order
                    # print("Expanding child node:", child.state)

                    result = dfs_contour(child, f_limit, path)
                    #p_cost += 1
                    if result is not None:
                        return result

                # backtrack: remove from path before returning
                path.remove(key)
                return None
    return program

'''
def IDAStartAgentProgram(f=None):
  def program(problem):
    root = Node(initState[problem]) #what does this even mean???
    f_limit = f_cost(root)
    while(1): #is this what I do here??????
      solution, f_limit = DFS_Contour(root, f_limit)
      if (solution != None): return solution
      elif (f_limit == infinity): return None #using None as a null replacement

  def DFS_Contour(node, f_limit):
    if (f_cost[node] > f_limit): return None, f_cost[node] #this feels like an illegal return statement
    if (goal_test[problem](state[node])): return node, f_limit #yes, there is no == or anything in the given diagram
    for node, s in successors[node]:
       solution, new_f = DFS_Contour(s, f_limit)
       if (solution != None): return solution, f_limit
       next_f = min(new_f, next_f)
       return None, next_f
'''