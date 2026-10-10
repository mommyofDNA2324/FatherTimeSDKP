import math
from typing import Dict, Any

class AmiyahRoseSmithLawSolver:
    """
    Execution harness for the Amiyah Rose Smith Law: T = S * rho * omega * v
    Governance rule maintaining equilibrium across scale, density, rotation, and translational speed.
    """
    
    # Earth Orbital Speed constant in m/s
    EOS_CONSTANT: float = 29780.0
    
    def __init__(self, scale: float, density: float, omega: float, velocity: float, domain: str = "quantum"):
        self.S = float(scale)
        self.rho = float(density)
        self.omega = float(omega)
        self.v = float(velocity)
        self.domain = domain.lower()  # Options: 'quantum' or 'macro'
        
    def check_boundary_guardrails(self) -> None:
        """
        Prevents ZeroDivisionError, NaN values, and floating-point overflow 
        when scale or packing density approaches near-zero limits (S -> 0, rho -> 0).
        """
        if self.S <= 0.0 or self.rho <= 0.0:
            raise ValueError("Boundary violation: Scale (S) and Density (rho) must be strictly positive non-zero values.")
        if math.isnan(self.S) or math.isnan(self.rho) or math.isnan(self.omega) or math.isnan(self.v):
            raise ArithmeticError("Numerical instability detected: Input variables contain NaN values.")

    def compute_emergent_time(self, normalized_eos: bool = True) -> float:
        """
        Computes dynamic scalar time: T = S * rho * omega * (v / v_EOS)
        """
        self.check_boundary_guardrails()
        
        velocity_factor = (self.v / self.EOS_CONSTANT) if normalized_eos else self.v
        emergent_time = self.S * self.rho * self.omega * velocity_factor
        return emergent_time

    def evaluate_equilibrium_perturbation(
        self, 
        dS: float, 
        drho: float, 
        domega: float, 
        dv: float,
        abs_velocity_tolerance: float = 0.003
    ) -> Dict[str, Any]:
        """
        Evaluates differential equilibrium balance conditions:
        (delta_S / S) + (delta_rho / rho) + (delta_omega / omega) + (delta_v / v) = 0

        Applies strict 0.01% (0.0001) relative error tolerance ONLY in the quantum domain.
        Applies absolute physical baseline tolerances (e.g., LEO dv <= 0.003 m/s) in the macro domain.
        """
        self.check_boundary_guardrails()
        
        if self.omega == 0.0 or self.v == 0.0 or self.S == 0.0 or self.rho == 0.0:
            raise ZeroDivisionError("Kinematic zero-bound error: All base state variables must be non-zero to evaluate differential balance.")
            
        term_S = dS / self.S
        term_rho = drho / self.rho
        term_omega = domega / self.omega
        term_v = dv / self.v
        
        net_variation = term_S + term_rho + term_omega + term_v
        
        # Domain-specific verification logic
        if self.domain == "quantum":
            # 0.01% max variance threshold for quantum state vector fidelity (F = 0.9999)
            is_balanced = abs(net_variation) <= 0.0001
            evaluation_type = "Relative Error (0.01% Quantum Bound)"
        else:
            # Macro scale evaluates velocity shift against absolute LEO baseline (e.g., 0.003 m/s)
            is_balanced = abs(dv) <= abs_velocity_tolerance
            evaluation_type = "Absolute Macro Velocity Baseline (m/s)"
            
        return {
            "domain": self.domain,
            "net_variation": net_variation,
            "is_balanced": is_balanced,
            "evaluation_type": evaluation_type
        }

    def __repr__(self) -> str:
        return f"<AmiyahRoseSmithLawSolver(domain='{self.domain}', S={self.S}, rho={self.rho}, omega={self.omega}, v={self.v})>"
