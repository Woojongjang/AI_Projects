#!/usr/bin/env python

from BayesianNetwork import *
from pprint import pprint
# 
#   * Creates and tests the alarm network as given in the book.
#   
class TestNetwork(object):
    """ generated source for class TestNetwork """
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        guilty = BayesianNetwork()
        #  Add variables to network
        BrokeElectionLaw = RandomVariable("Broke Election Law")
        PoliticallyMotivatedProsecutor = RandomVariable("Politically Motivated Prosecutor")
        Indicted = RandomVariable("Indicted")
        FoundGuilty = RandomVariable("Found Guilty")
        Jailed = RandomVariable("Jailed")

        guilty.addVariable(BrokeElectionLaw)
        guilty.addVariable(PoliticallyMotivatedProsecutor)
        guilty.addVariable(Indicted)
        guilty.addVariable(FoundGuilty)
        guilty.addVariable(Jailed)
        #  Add edges to network
        guilty.addEdge(BrokeElectionLaw, Indicted)
        guilty.addEdge(BrokeElectionLaw, FoundGuilty)
        guilty.addEdge(Indicted, FoundGuilty)
        guilty.addEdge(PoliticallyMotivatedProsecutor, Indicted)
        guilty.addEdge(PoliticallyMotivatedProsecutor, FoundGuilty)
        guilty.addEdge(FoundGuilty, Jailed)
        #  Initialize probability tables
        BrokeElectionLawProbs = [0.9]
        PoliticallyMotivatedProsecutorProbs = [0.1]
        IndictedProbs = [0.9, 0.5, 0.5, 0.1]
        FoundGuiltyProbs = [0.9, 0.8, 0.0, 0.0, 0.2, 0.1, 0.0, 0.0]
        JailedProbs = [0.9, 0.0]
        guilty.setProbabilities(BrokeElectionLaw, BrokeElectionLawProbs)
        guilty.setProbabilities(PoliticallyMotivatedProsecutor, PoliticallyMotivatedProsecutorProbs)
        guilty.setProbabilities(Indicted, IndictedProbs)
        guilty.setProbabilities(FoundGuilty, FoundGuiltyProbs)
        guilty.setProbabilities(Jailed, JailedProbs)
        
        
        #  Perform sampling tests
        #  P(J = 1|B = 1, M = 0) and P(M = 1|J = 1)
        #  ----------------------
        #  P(J = 1|B = 1, M = 0)
        runs = [10,100,1000,10000,100000,1000000]
        for i in runs:
            print "#####################################"
            print "NUMBER OF SAMPLES: " + str(i)
            print("Test 1: P(J = 1|B = 1, M = 0)")
            given1 = {}
            given1[BrokeElectionLaw]= True
            given1[PoliticallyMotivatedProsecutor]=False
            print("rejection sampling: " +str(guilty.performRejectionSampling(Jailed, given1, i)))
            print("weighted sampling: " + str(guilty.performWeightedSampling(Jailed, given1, i)))
            print("gibbs sampling: " + str(guilty.performGibbsSampling(Jailed, given1, i)))
            #  P(M = 1|J = 1)
            print("Test 2: P(M = 1|J = 1)")
            given2 = {}
            given2[Jailed]=True
            print("rejection sampling: " + str(guilty.performRejectionSampling(PoliticallyMotivatedProsecutor, given2, i)))
            print("weighted sampling: " + str(guilty.performWeightedSampling(PoliticallyMotivatedProsecutor, given2, i)))
            print("gibbs sampling: " + str(guilty.performGibbsSampling(PoliticallyMotivatedProsecutor, given2, i)))
        
if __name__ == '__main__':
    import sys
    TestNetwork.main(sys.argv)
import sys
TestNetwork.main(sys.argv)