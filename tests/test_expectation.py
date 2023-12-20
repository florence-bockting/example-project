import pytest
import numpy as np
import example_project.expectation as expectation

#%% Test mean

@pytest.fixture
def x1():
    return np.random.uniform(0,1,100)

def test_mean(x1):
    assert expectation.mean(x1) == pytest.approx(np.mean(x1))

#%% Test variance

@pytest.fixture
def x2():
    return np.random.normal(0,1,100)

def test_variance(x2):
    assert expectation.variance(x2) == pytest.approx(np.var(x2))