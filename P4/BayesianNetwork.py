#!/usr/bin/env python
""" generated source for module BayesianNetwork """
from Assignment4 import *
import random
from pprint import pprint
import numpy as np
# 
#  * A bayesian network
#  * @author Woo-Jong
#  
class BayesianNetwork(object):
    """ generated source for class BayesianNetwork """
    # 
    #     * Mapping of random variables to nodes in the network
    #     
    varMap = None

    # 
    #     * Edges in this network
    #     
    edges = None

    # 
    #     * Nodes in the network with no parents
    #     
    rootNodes = None

    # 
    #     * Default constructor initializes empty network
    #     
    def __init__(self):
        """ generated source for method __init__ """
        self.varMap = {}
        self.edges = []
        self.rootNodes = []

    # 
    #     * Add a random variable to this network
    #     * @param variable Variable to add
    #     
    def addVariable(self, variable):
        """ generated source for method addVariable """
        node = Node(variable)
        self.varMap[variable]=node
        self.rootNodes.append(node)

    # 
    #     * Add a new edge between two random variables already in this network
    #     * @param cause Parent/source node
    #     * @param effect Child/destination node
    #     
    def addEdge(self, cause, effect):
        """ generated source for method addEdge """
        source = self.varMap.get(cause)
        dest = self.varMap.get(effect)
        self.edges.append(Edge(source, dest))
        source.addChild(dest)
        dest.addParent(source)
        if dest in self.rootNodes:
            self.rootNodes.remove(dest)

    # 
    #     * Sets the CPT variable in the bayesian network (probability of
    #     * this variable given its parents)
    #     * @param variable Variable whose CPT we are setting
    #     * @param probabilities List of probabilities P(V=true|P1,P2...), that must be ordered as follows.
    #       Write out the cpt by hand, with each column representing one of the parents (in alphabetical order).
    #       Then assign these parent variables true/false based on the following order: ...tt, ...tf, ...ft, ...ff.
    #       The assignments in the right most column, P(V=true|P1,P2,...), will be the values you should pass in as probabilities here.
    #     
    def setProbabilities(self, variable, probabilities):
        """ generated source for method setProbabilities """
        probList = []
        for probability in probabilities:
            probList.append(probability)
        self.varMap.get(variable).setProbabilities(probList)
    
    def topologicalOrder(self, outgoingNode, NodeEdges):
        for i in NodeEdges:
            if i.source in outgoingNode and i.dest not in outgoingNode:
                outgoingNode.append(i.dest)

    def priorSampleTrue(self, givenVars):
        sampleOut = {}
        givenSampList = Sample()
        startTopNode = []

        startTopNode = self.rootNodes

        self.topologicalOrder(startTopNode, self.edges)
        for i in startTopNode:
            x = i.getProbability(givenSampList.assignments, True)
            y = random.random()
            if (y <= x):
                givenSampList.setAssignment(i.getVariable().getName(),True)
            else:
                givenSampList.setAssignment(i.getVariable().getName(),False)
        return givenSampList.assignments
        

    def sampleGoodReal(self, sample, givenVars):
        for i in givenVars:
            if givenVars[i] != sample[i.getName()]:
                return False
        return True
        
        
    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using rejection sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of rejection samples to perform
    #     
    def performRejectionSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performRejectionSampling """
        #  TODO
        freq = 0.0
        freqNot = 0.0
        numTaken = 0.0
        times = 0
        count = 0                                   # for that query
        query = {9:0,99:0,999:0,9999:0,99999:0,999999:0}
        for i in range(numSamples):
            sample = self.priorSampleTrue(givenVars)
            if self.sampleGoodReal(sample, givenVars):
                if random.random() <= sample[queryVar.getName()]:
                    freq += 1.0
                numTaken += 1.0
            if count in list(query.keys()):
                query[count] = (freq / (numTaken+0.00000000000000001))
            count = count + 1
        if numTaken == 0.0:
            return -1
        return freq / numTaken

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using weighted sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of weighted samples to perform
    #     
    def performWeightedSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performWeightedSampling """
        
        W = {}
        startTopNode = []                                   # getting topological order
        startTopNode = self.rootNodes
        self.topologicalOrder(startTopNode, self.edges)
        for node in startTopNode:
            W[node.getVariable()] = 0 
        wat = 0
        count = 0                                   # for that query
        query = {9:0,99:0,999:0,9999:0,99999:0,999999:0}
        number_of_times_this_thang_is_True = 0
        for i in range(numSamples):
            x, weight = self.weighted_sample(givenVars)
            if x[queryVar.getName()] == True:
                number_of_times_this_thang_is_True = number_of_times_this_thang_is_True + 1
                wat = wat+weight
            ## check if the given variables are what the given variables are
            W[queryVar] = W[queryVar]+weight
            if count in list(query.keys()):
                query[count] = (float(wat)/float(W[queryVar]))
            count = count + 1
                
        return str(float(wat)/float(W[queryVar]))


    def weighted_sample(self, givenVars):
        givenSL = Sample()
        for i in givenVars:
            givenSL.setAssignment(i.getName(), givenVars[i])
            
        startTopNode = []                                   # getting topological order
        startTopNode = self.rootNodes
        self.topologicalOrder(startTopNode, self.edges)

        for node in startTopNode:                                                                        # going in topological order
        
            node_variable = node.getVariable()
            node_name = node_variable.getName()

            if node.getVariable() in givenVars:                                                          # if node is evidence var with value x in e
                
                node_probability = node.getProbability(givenSL.assignments,givenSL.assignments[node_name])
                givenSL.setWeight(givenSL.getWeight()*node_probability)


            else:  
                
                random_var = random.random()
                node_probability_true = node.getProbability(givenSL.assignments, True)

                
                if (random_var <= node_probability_true):                                                           # Sampling the unknown
                    givenSL.setAssignment(node_name, True)
                else:
                    givenSL.setAssignment(node_name, False)
        return givenSL.assignments, givenSL.getWeight()

    #======================GIBBS SAMPLING==================       
    def performGibbsSampling(self, queryVar, givenVars, numTrials):
        """ generated source for method performGibbsSampling """

        givenSampList = Sample()
        for i in givenVars:
            givenSampList.setAssignment(i.getName(), float(givenVars[i]))

        nonGiven = {}
        nonGivenName = []
        nonGivenVar = {}
        for ng in self.varMap:
            if ng not in givenVars:
                nonGiven[ng.getName()] = ng
                nonGivenVar[ng] = ng.getName()
                nonGivenName.append(ng.getName())

        gotTrue = 0.0
        gotFalse = 0.0

        count = 0                                   # for that query
        query = {9:0,99:0,999:0,9999:0,99999:0,999999:0}
        for i in range(numTrials):
            if random.random() <= float(self.fuckYouMarkov(queryVar, givenVars)):
                gotTrue += 1.0
            else:
                gotFalse += 1.0
            if count in list(query.keys()):
                query[count] = (gotTrue / numTrials)
            count = count + 1

        if gotTrue == 0:
            return -1
        return gotTrue / numTrials


    def priorSample(self, givenVars):
        sampleOut = {}
        givenSampList = Sample()
        for i in givenVars:
            givenSampList.setAssignment(i.getName(), givenVars[i])

        startTopNode = []

        startTopNode = self.rootNodes

        self.topologicalOrder(startTopNode, self.edges)

        for i in startTopNode:
            x = i.getProbability(givenSampList.assignments, True)
            if(i.getVariable() not in givenVars):
                if (random.random() <= 0.5): 
                    givenSampList.setAssignment(i.getVariable().getName(),True)
                else:
                    givenSampList.setAssignment(i.getVariable().getName(),False)
            sampleOut[i.getVariable().getName()] = x
        return sampleOut


    def fuckYouMarkov(self, queryVar, givenVars):
        sampleT = self.priorSample(givenVars)
        sampleF = self.priorSample(givenVars)

        pSample1 = Sample()
        pSample2 = Sample()

        for i in self.varMap.get(queryVar).getParents():
            if random.random() <= sampleT[i.getVariable().getName()]:
                pSample1.setAssignment(i.getVariable().getName(), True)
            else:
                pSample1.setAssignment(i.getVariable().getName(), False)
            
        pXTrue = self.varMap.get(queryVar).getProbability(pSample1.assignments, True)

        for i in self.varMap.get(queryVar).getParents():
            if random.random() <= sampleF[i.getVariable().getName()]:
                pSample2.setAssignment(i.getVariable().getName(), True)
            else:
                pSample2.setAssignment(i.getVariable().getName(), False)
        
        pxFalse = self.varMap.get(queryVar).getProbability(pSample2.assignments, False)

        pchildT = 1
        pCHSample1 = Sample()
        for ch in self.varMap.get(queryVar).getChildren():
            for chparent in self.varMap.get(ch.getVariable()).getParents():
                if random.random() <= sampleT[chparent.getVariable().getName()]:
                    pCHSample1.setAssignment(chparent.getVariable().getName(), True)
                else:
                    pCHSample1.setAssignment(chparent.getVariable().getName(), False)
            pchildT *= self.varMap.get(ch.getVariable()).getProbability(pCHSample1.assignments, True)

        pchildF = 1
        pCHSample2 = Sample()
        for ch in self.varMap.get(queryVar).getChildren():
            for chparent in self.varMap.get(ch.getVariable()).getParents():
                if random.random() <= sampleF[chparent.getVariable().getName()]:
                    pCHSample2.setAssignment(chparent.getVariable().getName(), True)
                else:
                    pCHSample2.setAssignment(chparent.getVariable().getName(), False)
            pchildF *= self.varMap.get(ch.getVariable()).getProbability(pCHSample2.assignments, True)

        probTrue = pXTrue * pchildT
        probFalse = pxFalse * pchildF
        return (probTrue / (probTrue + probFalse + 0.000000000000000000000001))
