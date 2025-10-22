import pytest
from MetricsClass import Metrics  # assuming your file is metrics.py

@pytest.fixture
def m():
    return Metrics()

def test_default_values(m):
    assert m.prestige == 51
    assert m.budget == 450000000
    assert m.sHappiness == 75
    assert m.aHappiness == 60
    assert m.security == 50
    assert m.academics == 80

def test_prestige(m):
    m.prestige = m.prestige + 10
    assert m.prestige == 61

def test_budget(m):
    m.budget = m.budget + 1000000
    assert m.budget == 451000000

def test_shappiness(m):
    m.sHappiness = m.sHappiness + 5
    assert m.sHappiness == 80

def test_ahappiness(m):
    m.aHappiness = m.aHappiness + 10
    assert m.aHappiness == 70

def test_security(m):
    m.security = m.security - 5
    assert m.security == 45

def test_academics(m):
    m.academics = m.academics + m.academics + 5
    assert m.academics == 85

@pytest.mark.parametrize("attr", [
    "prestige", "budget", "sHappiness", "aHappiness", "security", "academics"
])
def test_negative_values_raise(m, attr):
    with pytest.raises(ValueError):
        setattr(m, attr, -1)

