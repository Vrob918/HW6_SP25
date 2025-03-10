#utilized chatGPT
# region imports
from Fluid import Fluid
from Pipe import Pipe
from Loop import Loop
from PipeNetwork import PipeNetwork
# endregion

# region function definitions
def main():
    '''
    This program analyzes flows in a given pipe network based on the following:
    1. The pipe segments are named by their endpoint node names:  e.g., a-b, b-e, etc.
    2. Flow from the lower letter to the higher letter of a pipe is considered positive.
    3. Pressure decreases in the direction of flow through a pipe.
    4. At each node in the pipe network, mass is conserved.
    5. For any loop in the pipe network, the pressure loss is zero
    Approach to analyzing the pipe network:
    Step 1: build a pipe network object that contains pipe, node, loop and fluid objects
    Step 2: calculate the flow rates in each pipe using fsolve
    Step 3: output results
    Step 4: check results against expected properties of zero head loss around a loop and mass conservation at nodes.
    :return:
    '''
    #instantiate a Fluid object to define the working fluid as water
    water = Fluid(mu=0.00089, rho=1000)  #
    roughness = 0.00025  # in meters

    #instantiate a new PipeNetwork object
    PN = PipeNetwork()  #
    #add Pipe objects to the pipe network (see constructor for Pipe class)
    PN.pipes.append(Pipe('a','b',250, 300, roughness, water))
    PN.pipes.append(Pipe('a','c',100, 200, roughness, water))
    PN.pipes.append(Pipe('b','e',100, 200, roughness, water))
    PN.pipes.append(Pipe('c','d',125, 200, roughness, water))
    PN.pipes.append(Pipe('c','f',100, 150, roughness, water))
    PN.pipes.append(Pipe('d','e',125, 200, roughness, water))
    PN.pipes.append(Pipe('d','g',100, 150, roughness, water))
    PN.pipes.append(Pipe('e','h',100, 150, roughness, water))
    PN.pipes.append(Pipe('f','g',125, 250, roughness, water))
    PN.pipes.append(Pipe('g','h',125, 250, roughness, water))
    #add Node objects to the pipe network by calling buildNodes method of PN object
    PN.buildNodes()

    #update the external flow of certain nodes
    PN.getNode('a').extFlow=60
    PN.getNode('d').extFlow=-30
    PN.getNode('f').extFlow=-15
    PN.getNode('h').extFlow=-15

    #add Loop objects to the pipe network
    PN.loops.append(Loop('A',[PN.getPipe('a-b'), PN.getPipe('b-e'),PN.getPipe('d-e'), PN.getPipe('c-d'), PN.getPipe('a-c')]))
    PN.loops.append(Loop('B',[PN.getPipe('c-d'), PN.getPipe('d-g'),PN.getPipe('f-g'), PN.getPipe('c-f')]))
    PN.loops.append(Loop('C',[PN.getPipe('d-e'), PN.getPipe('e-h'),PN.getPipe('g-h'), PN.getPipe('d-g')]))

    #call the findFlowRates method of the PN (a PipeNetwork object)
    PN.findFlowRates()

    #get output
    PN.printPipeFlowRates()
    print()
    print('Check node flows:')
    PN.printNetNodeFlows()
    print()
    print('Check loop head loss:')
    PN.printLoopHeadLoss()
    #PN.printPipeHeadLosses()
# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregions

