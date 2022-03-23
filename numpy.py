'''
    Shouyuan Shi @ South China University of Technology
'''
import numpy as np

def var_to_numpy(obj):
    shape = tuple(len(s) for s in obj.index_set().subsets())
    val = np.empty(shape)
    for i in obj:
        val[i] = obj[i]()
    return val

def suffix_to_numpy(suf,con):
    shape = tuple(len(s) for s in con.index_set().subsets())
    val = np.empty(shape)
    for i in con:
        val[i] = suf[con[i]]
    return val

def fill_var_value(var,val):
    for i in var:
        val_i=val[i]
        if var[i].has_lb():
            val_i=max(val_i,var[i].lb)
        if var[i].has_ub():
            val_i=min(val_i,var[i].ub)
        var[i].set_value(val_i)

def wrap_as_rule(*data: list, offset: int = 0):
    '''
    Create a Pyomo construction rule for the given data.
    `*data`: One or more list or dict used for the data source.
    `offset`: The first index value that Pyomo is going to pass in. Set to None if it is key rather than numerical index.
    '''

    if len(data) > 1:
        def rule(m, key): return tuple(data[d][key] for d in range(len(data)))
    else:
        def rule(m, key): return data[0][key]
    if offset == None:
        return rule
    else:
        return lambda m, i: rule(m, i-offset)

