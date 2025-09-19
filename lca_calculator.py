import numpy as np
from typing import Dict, List, Any

class LCACalculator:
    """Handles Life Cycle Assessment calculations for metallurgy processes"""
    
    def __init__(self):
        # Emission factors (kg CO2/kg metal) - industry averages
        self.emission_factors = {
            'aluminium': {
                'raw': 11.5,        # Primary aluminum production
                'recycled': 0.7     # Secondary aluminum production
            },
            'copper': {
                'raw': 3.8,         # Primary copper production
                'recycled': 1.2     # Secondary copper production
            },
            'steel': {
                'raw': 2.3,         # Primary steel production
                'recycled': 0.5     # Secondary steel production
            },
            'other': {
                'raw': 5.0,         # Generic metal average
                'recycled': 1.0     # Generic recycled metal
            }
        }
        
        # Transport emission factor (kg CO2/kg*km)
        self.transport_factor = 0.0001
        
        # Energy emission factor (kg CO2/kWh)
        self.energy_factor = 0.5
        
        # End-of-life factors
        self.eol_factors = {
            'reuse': 0.1,       # Minimal processing required
            'recycle': 0.3,     # Recycling process emissions
            'landfill': 1.0     # Full disposal impact
        }
    
    def calculate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate LCA results for both conventional and circular pathways
        
        Args:
            data: Enhanced input data from AI estimator
            
        Returns:
            Dictionary containing pathway comparisons and metrics
        """
        # Calculate conventional pathway (raw materials, landfill)
        conventional = self._calculate_pathway(
            metal_type=data['metalType'],
            production_route='raw',
            energy_use=data.get('energyUse', 0),
            transport_distance=data.get('transportDistance', 0),
            end_of_life='landfill'
        )
        
        # Calculate circular pathway (recycled materials, reuse/recycle)
        circular_eol = 'reuse' if data['endOfLife'] == 'reuse' else 'recycle'
        circular = self._calculate_pathway(
            metal_type=data['metalType'],
            production_route='recycled',
            energy_use=data.get('energyUse', 0) * 0.6,  # Recycled typically uses less energy
            transport_distance=data.get('transportDistance', 0) * 0.8,  # Often shorter distances
            end_of_life=circular_eol
        )
        
        # Calculate circularity indicators
        conventional['recycled_content'] = 5.0   # Minimal recycled content
        conventional['reuse_potential'] = 10.0   # Low reuse potential
        
        circular['recycled_content'] = 85.0      # High recycled content
        circular['reuse_potential'] = 75.0 if data['endOfLife'] == 'reuse' else 60.0
        
        # Calculate improvement metrics
        co2_reduction = ((conventional['co2_equivalent'] - circular['co2_equivalent']) 
                        / conventional['co2_equivalent'] * 100)
        
        results = {
            'pathways': [
                {
                    'name': 'Conventional Pathway',
                    'co2_equivalent': conventional['co2_equivalent'],
                    'recycled_content': conventional['recycled_content'],
                    'reuse_potential': conventional['reuse_potential']
                },
                {
                    'name': 'Circular Pathway',
                    'co2_equivalent': circular['co2_equivalent'],
                    'recycled_content': circular['recycled_content'],
                    'reuse_potential': circular['reuse_potential']
                }
            ],
            'improvements': {
                'co2_reduction_percent': max(0, co2_reduction),
                'circularity_increase': circular['recycled_content'] - conventional['recycled_content'],
                'reuse_improvement': circular['reuse_potential'] - conventional['reuse_potential']
            }
        }
        
        return results
    
    def _calculate_pathway(self, metal_type: str, production_route: str, 
                          energy_use: float, transport_distance: float, 
                          end_of_life: str) -> Dict[str, float]:
        """Calculate emissions for a specific pathway"""
        
        # Base emissions from metal production
        base_emission = self.emission_factors.get(metal_type, {}).get(production_route, 5.0)
        
        # Energy-related emissions
        energy_emission = energy_use * self.energy_factor if energy_use else 0
        
        # Transport emissions
        transport_emission = transport_distance * self.transport_factor if transport_distance else 0
        
        # End-of-life emissions
        eol_emission = base_emission * self.eol_factors.get(end_of_life, 1.0) * 0.1
        
        total_co2 = base_emission + energy_emission + transport_emission + eol_emission
        
        return {
            'co2_equivalent': round(total_co2, 2),
            'breakdown': {
                'production': base_emission,
                'energy': energy_emission,
                'transport': transport_emission,
                'end_of_life': eol_emission
            }
        }