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
      path_cost = 0
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
          print("Path cost = {} and nodes extracted = {}".format(path_cost, node_expanded))
          return node

        #reached.add(node.state)
        for child in node.expand(problem):
            if child.state not in reached or child.path_cost<reached[child.state].path_cost:
                #print(child)
                print("The child node {}.".format(child))
                h=child.path_cost+round(f(child.state, problem.goal),3)
                frontier.put((h,child))
                reached.update({child.state:child})
                path_cost += 1
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
    if f is None:
        f = lambda s, g: math.dist(s, g)

    # --- Iterative (stack-based) DFS_Contour: no recursion anywhere ---
    def DFS_Contour(root, f_limit, problem):
        # Each frame: (node, children_iterator, state_of_node, f_cost)
        # children_iterator yields child Node objects from node.expand(problem)
        frame_children = lambda node: iter(node.expand(problem))

        stack = []
        path_set = set()            # states currently on the path (like call stack)
        best_next_limit = float('inf')

        # push root
        stack.append((root, frame_children(root), root.state, root.path_cost + f(root.state, problem.goal)))
        path_set.add(root.state)

        while stack:
            node, children_it, state, f_cost = stack[-1]

            # If the f_cost was not computed (or children changed), ensure it's current:
            # (we compute once when frame is pushed, so this is fine)

            # If node exceeds current contour limit, update best_next_limit and backtrack
            if f_cost > f_limit:
                best_next_limit = min(best_next_limit, f_cost)
                # pop and remove from path
                stack.pop()
                path_set.discard(state)
                continue

            # Goal test
            if problem.goal_test(state):
                return node, f_limit

            # Try to get next child from iterator
            try:
                child = next(children_it)
            except StopIteration:
                # finished exploring this node, backtrack
                stack.pop()
                path_set.discard(state)
                continue

            # skip children that are already on current path (avoid cycles)
            if child.state in path_set:
                # skip to next child (do not push)
                continue

            # prepare child's f_cost and push frame
            child_f_cost = child.path_cost + f(child.state, problem.goal)
            # push child frame (LIFO) — note we make children iterator lazily via expand
            stack.append((child, frame_children(child), child.state, child_f_cost))
            path_set.add(child.state)
            # loop continues, we will process the child next iteration

        return None, best_next_limit

    # --- Main program (outer closure) ---
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