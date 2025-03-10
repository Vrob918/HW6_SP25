#region imports
from scipy.optimize import fsolve
import numpy as np
from Fluid import Fluid
from Node import Node
#endregion
# region class definitions
class PipeNetwork():
    #region constructor
    def __init__(self, Pipes=[], Loops=[], Nodes=[], fluid=Fluid()):
        '''
        The pipe network is built from pipe, node, loop, and fluid objects.
        :param Pipes: a list of pipe objects
        :param Loops: a list of loop objects
        :param Nodes: a list of node objects
        :param fluid: a fluid object
        '''
        #region attributes
        self.loops=Loops
        self.nodes=Nodes
        self.Fluid=fluid
        self.pipes=Pipes
        #endregion
    #endregion

    #region methods
    def findFlowRates(self):
        '''
        a method to analyze the pipe network and find the flow rates in each pipe
        given the constraints of: i) no net flow into a node and ii) no net pressure drops in the loops.
        :return: a list of flow rates in the pipes
        '''
        #see how many nodes and loops there are, this is how many equation results I will return
        N=len(self.nodes)+len(self.loops)
        # build an initial guess for flow rates in the pipes.
        # note that I only have 10 pipes, but need 11 variables because of the degenerate node equation at b.
        Q0=np.full(N,10)
        def fn(q):
            """
            This is used as a callback for fsolve.  The mass continuity equations at the nodes and the loop equations
            are functions of the flow rates in the pipes.  Hence, fsolve will search for the roots of these equations
            by varying the flow rates in each pipe.
            :param q: an array of flowrates in the pipes + 1 extra value b/c of node b
            :return: L an array containing flow rates at the nodes and  pressure losses for the loops
            """
            #update the flow rate in each pipe object
            for i in range(len(self.pipes)):
                self.pipes[i].Q = q[i]  # set volumetric flow rate from input argument q
            #calculate the net flow rate for the node objects
            # note:  when flow rates in pipes are correct, the net flow into each node should be zero.
            L = self.getNodeFlowRates()  # call the getNodeFlowRates function of this class
            #calculate the net head loss for the loop objects
            # note: when the flow rates in pipes are correct, the net head loss for each loop should be zero.
            L += self.getLoopHeadLosses()  # call the getLoopHeadLosses function of this class
            return L
        #using fsolve to find the flow rates
        FR=fsolve(fn,Q0)
        return FR

    def getNodeFlowRates(self):
        #each node object is responsible for calculating its own net flow rate
        qNet=[n.getNetFlowRate() for n in self.nodes]
        return qNet

    def getLoopHeadLosses(self):
        #each loop object is responsible for calculating its own net head loss
        lhl=[l.getLoopHeadLoss() for l in self.loops]
        return lhl

    def getPipe(self, name):
        #returns a pipe object by its name
        for p in self.pipes:
            if name == p.Name():
                return p

    def getNodePipes(self, node):
        #returns a list of pipe objects that are connected to the node object
        l=[]
        for p in self.pipes:
            if p.oContainsNode(node):
                l.append(p)
        return l

    def nodeBuilt(self, node):
        #determines if I have already constructed this node object (by name)
        for n in self.nodes:
            if n.name==node:
                return True
        return False

    def getNode(self, name):
        #returns one of the node objects by name
        for n in self.nodes:
            if n.name==name:
                return n

    def buildNodes(self):
        #automatically create the node objects by looking at the pipe ends
        for p in self.pipes:
            if self.nodeBuilt(p.startNode)==False:
                #instantiate a node object and append it to the list of nodes
                self.nodes.append(Node(p.startNode,self.getNodePipes(p.startNode)))
            if self.nodeBuilt(p.endNode)==False:
                #instantiate a node object and append it to the list of nodes
                self.nodes.append(Node(p.endNode,self.getNodePipes(p.endNode)))

    def printPipeFlowRates(self):
        for p in self.pipes:
            p.printPipeFlowRate()

    def printNetNodeFlows(self):
        for n in self.nodes:
            print('net flow into node {} is {:0.2f}'.format(n.name, n.getNetFlowRate()))

    def printLoopHeadLoss(self):
        for l in self.loops:
            print('head loss for loop {} is {:0.2f}'.format(l.name, l.getLoopHeadLoss()))
    #endregion
# endregion