# -*- coding: utf-8 -*-

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
    final.sort(key=lambda x: x[0])
    final.sort(key=lambda x: x[1])
    return [i[0] for i in final]




