import pyomo.environ as pyo
import unittest
import pyomo_utility as util
import numpy as np


class TestNumpyUtil(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.i_num = 3
        self.j_num = 4

        self.solver=pyo.SolverFactory('gurobi_direct')

        self.model=m = pyo.ConcreteModel()
        m.i = pyo.RangeSet(0,self. i_num - 1)
        m.j = pyo.RangeSet(0, self.j_num - 1)

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

    def test_fill_and_get_value_with_Param(self): 
        m=self.model       
        A_0 = np.random.rand(self.i_num, self.j_num)
        util.fill_value(m.A, A_0)
        A_1=util.value_to_numpy(m.A)
        self.assertTrue(np.all(A_0==A_1))

    def test_fill_and_get_value_with_Var(self): 
        m=self.model       
        A_0 = np.random.rand(self.i_num, self.j_num)
        util.fill_value(m.x, A_0)
        A_1=util.value_to_numpy(m.x)
        self.assertTrue(np.all(A_0==A_1))
    
    def test_suffix_to_numpy(self):
        eps=1e-3
        A_0 = np.random.rand(self.i_num, self.j_num)       
        m=self.model  
        util.fill_value(m.A, A_0)        
        self.solver.solve(m)
        dual = util.suffix_to_numpy(m.dual, m.row_sum_eq_one_con)
        # dual is one the element in A of the corresponding row
        self.assertTrue(np.all(np.sum(np.abs(dual[:,np.newaxis]-A_0)<eps,axis=1)==1))



if __name__ == '__main__':
    unittest.main(verbosity=2)
