import pytest
import numpy as np
import example_project.expectation as expectation

@pytest.fixture(scope = "class")
def x1():
    return np.random.uniform(0,1,100)

def test_mean(x1):
    assert expectation.mean(x1) == pytest.approx(np.mean(x1))
    
def test_variance(x1):
    assert expectation.variance(x1) == pytest.approx(np.var(x1))
    

@pytest.mark.parametrize("x, expected_result", [([2, 3], 2.5), 
                                                ([-2, -3], -2.5), 
                                                ([-2, 3], 0.5)])
def test_mean2(x, expected_result):
    assert expectation.mean(x) == expected_result