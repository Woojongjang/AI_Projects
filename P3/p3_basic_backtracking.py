# -*- coding: utf-8 -*-

from p1_is_complete import *
from p2_is_consistent import *

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    For P3, *you do not need to modify this method.*
    """
    return next((variable for variable in csp.variables if not variable.is_assigned()))

def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    For P3, *you do not need to modify this method.*
    """
    return [value for value in variable.domain]


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P3, *you do not need to modify this method.*
    """
    return True


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P3, *you do not need to modify this method.*
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
    domainList = order_domain_values(csp, var)
    for i in domainList:
        if is_consistent(csp,var,i):
            csp.variables.begin_transaction()
            var.assign(i)
            if inference(csp,var):
                backtrack(csp)
                if is_complete(csp):
                    return True
            csp.variables.rollback()
    return False



    #for each value in Order-Domain-Values(var,assignment,csp) do
    #    if value is consistent with assignment then
    #        add {var = value} to assignment //begin transaction
    #        inferences <- Inference(csp,var,value)
    #        if inferences =/= failure then
    #            add inferences to assignment
    #            result <- BACKTRACK(assignment, csp)
    #            if result =/= failure then
    #                return result
    #    remove{var = value} and inferences from assignment // rollback
    #return failure


