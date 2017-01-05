# -*- coding: utf-8 -*-

from collections import deque
from p1_is_complete import *
from p2_is_consistent import *
import sys


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """

    #if assignment is complete then return assignment
    if is_complete(csp):
        return True

    var = select_unassigned_variable(csp)
    domainList = []
    if not var.is_assigned():
        domainList = order_domain_values(csp, var)
    for i in domainList:
        if is_consistent(csp,var,i):
            # add {var = value} to assignment // begin transaction
            csp.variables.begin_transaction()
            var.assign(i)
            if inference(csp,var):
                backtrack(csp)
                if is_complete(csp):
                    return True
            csp.variables.rollback()
            
    return False


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""


    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())
   
    while queue_arcs:        # while queue is not empty
        xi, xj = queue_arcs.popleft()
        if revise(csp, xi, xj):
            if len(xi.domain) == 0:
                return False
            for xk in [c.var2 for c in csp.constraints[xi] if c.var2 != xj]:
                queue_arcs.append((xk, xi))
    
    return True


def revise(csp, xi, xj):
    revised = False
    for x in xi.domain:
        if satisfaction(csp,xi,xj,x) == False:
            xi.domain.remove(x)
            revised = True
    return revised



def satisfaction(csp,variable1,variable2,value):
    for const in csp.constraints[variable1]:
        if const.var2 == variable2:
            for y in variable2.domain:
                if const.is_satisfied(value,y):
                    return True
    return False



#===================================================================================
def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """
    least_num_dom = 100
    least_num_dom_var = None
    for v in ((csp.variables)._variable_list):
        if len(v.domain) > 1:
            if len(v.domain) < least_num_dom:
                least_num_dom = len(v.domain)
                least_num_dom_var = v
            elif len(v.domain) == least_num_dom:
                constListNew = [i for i in csp.constraints[v] if not ((i.var2).is_assigned())] 
                constListOld = [i for i in csp.constraints[least_num_dom_var] if not ((i.var2).is_assigned())]
                if constListOld < constListNew:
                    least_num_dom = len(v.domain)
                    least_num_dom_var = v
    return least_num_dom_var



def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """
    domainList = variable.domain
    constraintNum = []
    for i in domainList:
        number = 0
        constraintList = csp.constraints[variable]
        for j in constraintList:
            if not j.var2.is_assigned():
                for p in j.var2.domain:
                    if not j.is_satisfied(i,p):
                        number += 1
        constraintNum.append(number)
    final = zip(domainList,constraintNum)
    final.sort(key=lambda x: x[1])
    return [i[0] for i in final]




