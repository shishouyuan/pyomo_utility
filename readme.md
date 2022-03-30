# Pyomo Utility
Utility functions for Pyomo.
## 1. Function List
### value_to_numpy
Return a `numpy` array containning each element value of `obj` at the corresponding position.

### suffix_to_numpy
Return a `numpy` array containning the suffix `suf` value of each element of constraint `con` at the corresponding position.

### fill_value
Set the value of each element in `obj` with the corresponding item in `val`.

## 2. Example
```python
import pyomo.environ as pyo
import numpy as np
import pyomo_utility as util

i_num = 3
j_num = 4

m = pyo.ConcreteModel()
m.i = pyo.RangeSet(0, i_num - 1)
m.j = pyo.RangeSet(0, j_num - 1)

# variable
m.x = pyo.Var(m.i, m.j, bounds=(0, 1))

# parameter
m.A = pyo.Param(m.i, m.j, default=0, mutable=True)

# constraint
m.row_sum_eq_one_con = pyo.Constraint(
    m.i, rule=lambda p, i:
    pyo.quicksum(p.x[i, :]) == 1
)

# objective
m.obj = pyo.Objective(expr=pyo.sum_product(m.A, m.x))

# suffix for dual
m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

A_0 = np.random.rand(i_num, j_num)

# fill parameter A with A_0
util.fill_value(m.A, A_0)

solver = pyo.SolverFactory('gurobi_direct')
solver.solve(m)

# get value of variable x
x = util.value_to_numpy(m.x)
print(f'x = {x}')
# x = [[0. 0. 0. 1.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]]

# get dual of constraint con
dual = util.suffix_to_numpy(m.dual, m.row_sum_eq_one_con)

print(f'dual = {dual}')
# dual = [0.06459462 0.27276094 0.07508348]


# fill variable x with x_0
x_0 = np.random.rand(i_num, j_num)
util.fill_value(m.x, x_0)
```