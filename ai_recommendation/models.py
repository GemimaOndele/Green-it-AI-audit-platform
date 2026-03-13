"""
Data models for the AI recommendation engine.
Aligned with Mike-Brady's energy metrics module.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class DifficultyLevel(Enum):
    """Implementation difficulty levels"""
    EASY = "easy"      # < 1 month, low cost
    MEDIUM = "medium"  # 1-3 months, moderate cost
    HARD = "hard"      # > 3 months, significant investment


class ImpactLevel(Enum):
    """CO2 reduction impact levels"""
    HIGH = "high"      # > 10% CO2 reduction
    MEDIUM = "medium"  # 5-10% reduction
    LOW = "low"        # < 5% reduction


class Category(Enum):
    """Recommendation categories"""
    COOLING = "cooling"
    IT = "it"
    POWER = "power"
    INFRASTRUCTURE = "infrastructure"
    BENCHMARK = "benchmark"


@dataclass
class AuditContext:
    """
    Complete audit context combining Mike-Brady's metrics with UI inputs.
    
    This class is designed to work seamlessly with Mike-Brady's
    `calculate_all_metrics()` function from energy_metrics.
    """
    
    # From Mike-Brady's metrics module (via calculate_all_metrics)
    it_power_kw: float
    it_energy_mwh: float
    total_energy_mwh: float
    carbon_factor_kg_per_kwh: float
    pue: float
    dcie_percent: float
    co2_tonnes_per_year: float
    pue_rating: str
    pue_description: str
    action_needed: bool
    
    # Infrastructure inputs (from UI / document extraction)
    num_servers: int
    cpu_utilization_pct: float
    cooling_setpoint_c: float
    has_aisle_containment: bool
    virtualization_level_pct: float
    cooling_type: str = "air"  # "air", "water", "hybrid", "free"
    
    # Optional fields for advanced rules
    avg_server_age_years: Optional[float] = None
    renewable_energy_pct: Optional[float] = None
    energy_cost_per_kwh: float = 0.12  # Default EUR/kWh
    
    @classmethod
    def from_metrics_and_ui(cls, metrics_dict: Dict[str, Any], ui_inputs: Dict[str, Any]) -> 'AuditContext':
        """
        Create AuditContext from Mike-Brady's metrics dict + UI inputs.
        
        Args:
            metrics_dict: Output from energy_metrics.calculate_all_metrics()
            ui_inputs: Dictionary with UI fields (servers, cpu, cooling, etc.)
        
        Returns:
            AuditContext instance ready for recommendation engine
        """
        # Validate required metrics
        required_metrics = ['it_power_kw', 'it_energy_mwh', 'total_energy_mwh', 
                           'carbon_factor', 'pue', 'dcie_percent', 
                           'co2_tonnes_per_year', 'pue_rating', 
                           'pue_description', 'action_needed']
        
        for field in required_metrics:
            if field not in metrics_dict:
                raise ValueError(f"Missing required metric: {field}")
        
        return cls(
            # From metrics_dict (note: carbon_factor vs carbon_factor_kg_per_kwh)
            it_power_kw=metrics_dict['it_power_kw'],
            it_energy_mwh=metrics_dict['it_energy_mwh'],
            total_energy_mwh=metrics_dict['total_energy_mwh'],
            carbon_factor_kg_per_kwh=metrics_dict['carbon_factor'],
            pue=metrics_dict['pue'],
            dcie_percent=metrics_dict['dcie_percent'],
            co2_tonnes_per_year=metrics_dict['co2_tonnes_per_year'],
            pue_rating=metrics_dict['pue_rating'],
            pue_description=metrics_dict['pue_description'],
            action_needed=metrics_dict['action_needed'],
            
            # From UI inputs with defaults
            num_servers=ui_inputs.get('servers', 0),
            cpu_utilization_pct=ui_inputs.get('cpu_utilization_pct', 0),
            cooling_setpoint_c=ui_inputs.get('cooling_setpoint_c', 20.0),
            has_aisle_containment=ui_inputs.get('has_aisle_containment', False),
            virtualization_level_pct=ui_inputs.get('virtualization_level_pct', 0),
            cooling_type=ui_inputs.get('cooling_type', 'air')
        )
    
    def validate(self) -> List[str]:
        """Validate context data and return list of issues"""
        issues = []
        
        if self.total_energy_mwh <= 0:
            issues.append("total_energy_mwh must be positive")
        
        if self.it_energy_mwh <= 0:
            issues.append("it_energy_mwh must be positive")
        
        if self.carbon_factor_kg_per_kwh <= 0:
            issues.append("carbon_factor_kg_per_kwh must be positive")
        
        if self.pue < 1.0:
            issues.append("pue cannot be less than 1.0")
        
        if self.num_servers < 0:
            issues.append("num_servers cannot be negative")
        
        if not 0 <= self.cpu_utilization_pct <= 100:
            issues.append("cpu_utilization_pct must be between 0 and 100")
        
        if self.cooling_setpoint_c < 10 or self.cooling_setpoint_c > 40:
            issues.append("cooling_setpoint_c outside reasonable range (10-40°C)")
        
        return issues


@dataclass
class Recommendation:
    """
    A single actionable recommendation for the data center.
    Includes both metadata and calculated savings.
    """
    
    # Core identification
    id: str
    title: str
    description: str
    category: str  # "cooling", "it", "power", "infrastructure", "benchmark"
    
    # Savings (relative and absolute)
    estimated_saving_pct: float
    co2_savings_tonnes: float = 0.0  # Will be calculated by engine
    energy_savings_mwh: float = 0.0   # Will be calculated by engine
    cost_savings_eur: float = 0.0     # Will be calculated by engine
    
    # Implementation details
    difficulty: DifficultyLevel
    impact_level: ImpactLevel
    prerequisites: List[str] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    
    # For explainability
    logic_explanation: str
    references: List[str] = field(default_factory=list)
    
    # Optional metadata for simulation
    implementation_time_months: Optional[int] = None
    roi_months: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'saving_pct': self.estimated_saving_pct,
            'co2_savings_tonnes': round(self.co2_savings_tonnes, 2),
            'energy_savings_mwh': round(self.energy_savings_mwh, 2),
            'cost_savings_eur': round(self.cost_savings_eur, 2),
            'difficulty': self.difficulty.value,
            'impact': self.impact_level.value,
            'prerequisites': self.prerequisites,
            'steps': self.steps,
            'explanation': self.logic_explanation,
            'references': self.references,
            'implementation_time_months': self.implementation_time_months,
            'roi_months': self.roi_months
        }


@dataclass
class RecommendationResult:
    """
    Complete output from the recommendation engine.
    Ready for Gemima's frontend and Nandaa's simulation.
    """
    
    recommendations: List[Recommendation]
    summary: Dict[str, Any]
    context: Dict[str, Any]
    target_achievable: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'recommendations': [r.to_dict() for r in self.recommendations],
            'summary': self.summary,
            'context': self.context,
            'target_25pct_achievable': self.target_achievable
        }