# -*- coding: utf-8 -*-

from collections import deque
from p2_is_consistent import *



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













