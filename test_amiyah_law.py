import pytest
from amiyah_law_solver import AmiyahRoseSmithLawSolver

def test_quantum_domain_equilibrium():
    # Initialize solver in quantum domain
    solver = AmiyahRoseSmithLawSolver(scale=1e-9, density=1.0, omega=1e3, velocity=10.0, domain="quantum")
    
    # Test valid perturbation within 0.01% relative error bound (0.0001)
    result = solver.evaluate_equilibrium_perturbation(dS=1e-13, drho=1e-7, domega=1e-2, dv=1e-4)
    assert result["is_balanced"] is True
    assert result["domain"] == "quantum"

def test_quantum_domain_violation():
    solver = AmiyahRoseSmithLawSolver(scale=1e-9, density=1.0, omega=1e3, velocity=10.0, domain="quantum")
    
    # Test perturbation exceeding 0.01% relative error bound
    result = solver.evaluate_equilibrium_perturbation(dS=1e-10, drho=1e-4, domega=1.0, dv=0.5)
    assert result["is_balanced"] is False

def test_macro_domain_equilibrium():
    # Initialize solver in macro domain
    solver = AmiyahRoseSmithLawSolver(scale=1.0, density=1.225, omega=7.2921e-5, velocity=29780.0, domain="macro")
    
    # Test macro velocity shift within LEO absolute baseline (<= 0.003 m/s)
    result = solver.evaluate_equilibrium_perturbation(dS=0.0, drho=0.0, domega=0.0, dv=0.0015, abs_velocity_tolerance=0.003)
    assert result["is_balanced"] is True
    assert result["domain"] == "macro"

def test_boundary_guardrails_zero_division():
    solver = AmiyahRoseSmithLawSolver(scale=0.0, density=1.0, omega=1.0, velocity=1.0)
    
    with pytest.raises(ValueError):
        solver.check_boundary_guardrails()

def test_emergent_time_calculation():
    solver = AmiyahRoseSmithLawSolver(scale=2.0, density=1.5, omega=4.0, velocity=29780.0)
    time_val = solver.compute_emergent_time(normalized_eos=True)
    assert time_val == 12.0
