# COBRApy Skills for LLM Integration

COBRApy is a Python package for constraint-based modeling of metabolic networks. These skills enable LLM agents to interact with genome-scale metabolic models (GEMs).

## Load a Metabolic Model

Load a metabolic model from an SBML file.

```python
import cobra

model = cobra.io.read_sbml_model("path/to/model.xml")

# Or use built-in test model
model = cobra.io.load_model("textbook")
```

**Parameters:**
- `filepath`: Path to SBML (.xml) file

**Returns:** A Model object

---

## Run Flux Balance Analysis (FBA)

Optimize the model to predict metabolic fluxes.

```python
solution = model.optimize()

print(f"Objective value: {solution.objective_value}")
print(f"Status: {solution.status}")
```

**Returns:** 
- `solution.objective_value`: Growth rate or objective function value
- `solution.status`: "optimal", "infeasible", etc.

---

## Get Model Statistics

Retrieve basic information about the model.

```python
print(f"Reactions: {len(model.reactions)}")
print(f"Metabolites: {len(model.metabolites)}")
print(f"Genes: {len(model.genes)}")

model.summary()
```

---

## Query Specific Reactions

Get information about a specific reaction.

```python
reaction = model.reactions.get_by_id("ATPM")

print(f"Name: {reaction.name}")
print(f"Formula: {reaction.reaction}")
print(f"Bounds: {reaction.bounds}")
print(f"Genes: {reaction.genes}")
```

---

## Query Metabolites

Get information about specific metabolites.

```python
metabolite = model.metabolites.get_by_id("atp_c")

print(f"ID: {metabolite.id}")
print(f"Name: {metabolite.name}")
print(f"Formula: {metabolite.formula}")
print(f"Compartment: {metabolite.compartment}")
print(f"Used in {len(metabolite.reactions)} reactions")

# List all reactions using this metabolite
for reaction in metabolite.reactions:
    print(f"  - {reaction.id}: {reaction.name}")
```

**Returns:**
- Metabolite object with formula, compartment, and connected reactions

---

## Modify Reaction Bounds

Simulate different conditions by changing flux bounds.

```python
# Simulate anaerobic conditions
model.reactions.EX_o2_e.lower_bound = 0

solution = model.optimize()
print(f"Anaerobic growth rate: {solution.objective_value}")
```

---

## Flux Variability Analysis (FVA)

Find the minimum and maximum possible flux for reactions.

```python
from cobra.flux_analysis import flux_variability_analysis

# All reactions (can be slow for large models)
fva_result = flux_variability_analysis(model)

# Or analyze specific reactions
reactions_to_analyze = model.reactions[:10]
fva_result = flux_variability_analysis(model, reactions_to_analyze)

print(fva_result)
```

**Returns:** 
- DataFrame with columns: 'minimum', 'maximum'
- Shows flux range for each reaction

**Example output:**
```
           minimum   maximum
ACALD      0.000000  2.500000
ACALDt     0.000000  2.500000
ACKr      -1.000000  1.000000
```

---

## Gene Essentiality Analysis

Identify essential genes by testing knockouts.

```python
from cobra.flux_analysis import single_gene_deletion

deletion_results = single_gene_deletion(model)

# Find essential genes (growth < 1% of wildtype)
essential = deletion_results[deletion_results['growth'] < 0.01]

print(f"Found {len(essential)} essential genes")
print(essential.head())

# Test specific genes
test_genes = ['b0008', 'b0114', 'b0115']
specific_results = single_gene_deletion(model, model.genes.get_by_any(test_genes))
print(specific_results)
```

**Returns:**
- DataFrame with columns: 'ids', 'growth', 'status'

---

## Modify Growth Medium

Simulate different environmental conditions.

```python
medium = model.medium
print("Current medium:")
print(medium)

# Modify specific exchange reaction
model.reactions.EX_glc__D_e.lower_bound = -5

# Or modify the entire medium
medium = model.medium
medium['EX_glc__D_e'] = 5.0
medium['EX_o2_e'] = 0  # anaerobic
model.medium = medium

solution = model.optimize()
print(f"Growth under modified medium: {solution.objective_value}")

# Reset
model.medium = {}
```

**Common exchange reactions:**
- `EX_glc__D_e`: Glucose
- `EX_o2_e`: Oxygen
- `EX_nh4_e`: Ammonium
- `EX_pi_e`: Phosphate

---

## Multiple Gene Knockouts

Test combinations of gene deletions.

```python
from cobra.manipulation import delete_model_genes

with model:
    delete_model_genes(model, ["b0008", "b0114"])
    solution = model.optimize()
    print(f"Double knockout growth: {solution.objective_value}")

# Test multiple combinations
gene_combinations = [
    ["b0008"],
    ["b0114"],
    ["b0008", "b0114"],
    ["b0008", "b0115"]
]

results = []
for genes in gene_combinations:
    with model:
        delete_model_genes(model, genes)
        solution = model.optimize()
        results.append({
            'genes': ','.join(genes),
            'growth': solution.objective_value,
            'status': solution.status
        })

import pandas as pd
df = pd.DataFrame(results)
print(df)
```

---

## Load and Save Models

Work with different file formats.

```python
from cobra.io import read_sbml_model, write_sbml_model
from cobra.io import load_json_model, save_json_model

model = read_sbml_model("path/to/model.xml")
write_sbml_model(model, "output_model.xml")

# JSON is faster for loading
model = load_json_model("model.json")
save_json_model(model, "model.json")

# Built-in models
model = cobra.io.load_model("textbook")
```

---

## Save Model

Export the model to SBML format.

```python
cobra.io.write_sbml_model(model, "output_model.xml")
```

**Note:** This function is now part of the "Load and Save Models" section above.

---

## Gene Knockout Simulation

Simulate the effect of deleting a gene.

```python
# Single gene knockout
with model:
    model.genes.get_by_id("b0008").knock_out()
    solution = model.optimize()
    print(f"Growth rate after knockout: {solution.objective_value}")
```

---

## Common Workflows

### Complete Analysis Pipeline

```python
import cobra

model = cobra.io.read_sbml_model("ecoli_model.xml")
print(f"Model has {len(model.reactions)} reactions")

# Run FBA
solution = model.optimize()
print(f"Growth rate: {solution.objective_value}")

model.summary()

# Test gene knockout
with model:
    model.genes.get_by_id("b0008").knock_out()
    ko_solution = model.optimize()
    print(f"Growth after KO: {ko_solution.objective_value}")
```

### Workflow 2: Environmental Screening

Test growth under different oxygen levels.

```python
import pandas as pd

oxygen_levels = [0, 2, 5, 10, 15, 20]
results = []

for o2 in oxygen_levels:
    with model:
        model.reactions.EX_o2_e.lower_bound = -o2
        solution = model.optimize()
        results.append({
            'oxygen_uptake': o2,
            'growth_rate': solution.objective_value,
            'status': solution.status
        })

df = pd.DataFrame(results)
print(df)

optimal = df.loc[df['growth_rate'].idxmax()]
print(f"\nOptimal oxygen: {optimal['oxygen_uptake']} mmol/gDW/h")
```

### Workflow 3: Knockout Screening

Screen all genes for essentiality.

```python
from cobra.flux_analysis import single_gene_deletion

knockout_results = single_gene_deletion(model)

# Categorize by growth impact
essential = knockout_results[knockout_results['growth'] < 0.01]
reduced = knockout_results[
    (knockout_results['growth'] >= 0.01) & 
    (knockout_results['growth'] < 0.5)
]
non_essential = knockout_results[knockout_results['growth'] >= 0.5]

print(f"Essential genes: {len(essential)}")
print(f"Growth-reducing genes: {len(reduced)}")
print(f"Non-essential genes: {len(non_essential)}")

knockout_results.to_csv('gene_essentiality.csv')
```

### Workflow 4: Reaction Knockout

Test effect of removing reactions.

```python
from cobra.flux_analysis import single_reaction_deletion

reaction_ko = single_reaction_deletion(model)

essential_rxns = reaction_ko[reaction_ko['growth'] < 0.01]
print(f"Essential reactions: {len(essential_rxns)}")
print(essential_rxns.head())
```

---

## Performance Notes

**Typical execution times (E. coli core model, 95 reactions):**
- Model loading from SBML: ~50-100ms
- Model loading from JSON: ~20-50ms
- FBA optimization: ~5-20ms
- FVA (all reactions): ~500ms-2s
- Single gene deletion (all genes): ~2-5s

**For genome-scale models (2000+ reactions):**
- Model loading: 1-5 seconds
- FBA: 50-200ms
- FVA: 10-60 seconds
- Gene essentiality: 1-10 minutes

**Optimization tips:**
- Cache loaded models in memory
- Use JSON format for faster loading
- Limit FVA to reactions of interest
- Use parallel processing for gene deletions

---

## Testing Examples

```python
import cobra
from cobra.io import load_model

def test_model_loading():
    """Test that model loads correctly"""
    model = load_model('textbook')
    assert model.id == 'e_coli_core'
    assert len(model.reactions) == 95
    assert len(model.metabolites) == 72
    assert len(model.genes) == 137

def test_fba_optimization():
    """Test FBA produces expected results"""
    model = load_model('textbook')
    solution = model.optimize()
    assert solution.status == 'optimal'
    assert 0.85 < solution.objective_value < 0.88

def test_gene_knockout():
    """Test gene knockout simulation"""
    model = load_model('textbook')
    
    # Wild-type growth
    wt_growth = model.optimize().objective_value
    
    # Knockout growth
    with model:
        model.genes.get_by_id("b0008").knock_out()
        ko_growth = model.optimize().objective_value
    
    # Should reduce growth
    assert ko_growth < wt_growth

def test_medium_modification():
    """Test changing growth medium"""
    model = load_model('textbook')
    
    # Aerobic growth
    aerobic = model.optimize().objective_value
    
    # Anaerobic growth
    model.reactions.EX_o2_e.lower_bound = 0
    anaerobic = model.optimize().objective_value
    
    # Anaerobic should be lower
    assert anaerobic < aerobic
```

---

## JSON Serialization for APIs

Models and solutions are not directly JSON-serializable. Use these helpers:

```python
import json
import cobra

def model_to_json(model):
    """Convert model to JSON-serializable dict"""
    return {
        "id": model.id,
        "name": model.name,
        "reactions": [r.id for r in model.reactions],
        "metabolites": [m.id for m in model.metabolites],
        "genes": [g.id for g in model.genes],
        "num_reactions": len(model.reactions),
        "num_metabolites": len(model.metabolites),
        "num_genes": len(model.genes),
        "compartments": list(model.compartments.keys())
    }

def solution_to_json(solution):
    """Convert solution to JSON-serializable dict"""
    return {
        "status": solution.status,
        "objective_value": float(solution.objective_value) if solution.objective_value else None,
        "fluxes": {k: float(v) for k, v in solution.fluxes.items()} if solution.fluxes is not None else {}
    }

def reaction_to_json(reaction):
    """Convert reaction to JSON-serializable dict"""
    return {
        "id": reaction.id,
        "name": reaction.name,
        "reaction": reaction.reaction,
        "lower_bound": float(reaction.lower_bound),
        "upper_bound": float(reaction.upper_bound),
        "subsystem": reaction.subsystem,
        "genes": [g.id for g in reaction.genes],
        "metabolites": {m.id: float(coef) for m, coef in reaction.metabolites.items()}
    }

model = cobra.io.load_model('textbook')
solution = model.optimize()

model_data = model_to_json(model)
solution_data = solution_to_json(solution)

print(json.dumps(solution_data, indent=2))
```

---

## Common Error Handling

```python
from cobra.exceptions import OptimizationError

def safe_optimize(model):
    """Safely optimize model with error handling"""
    try:
        solution = model.optimize()
        
        if solution.status == 'optimal':
            return {
                'success': True,
                'growth': solution.objective_value,
                'status': solution.status
            }
        elif solution.status == 'infeasible':
            return {
                'success': False,
                'error': 'Model is infeasible',
                'status': solution.status
            }
        else:
            return {
                'success': False,
                'error': f'Non-optimal status: {solution.status}',
                'status': solution.status
            }
            
    except OptimizationError as e:
        return {
            'success': False,
            'error': f'Optimization error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

result = safe_optimize(model)
if result['success']:
    print(f"Growth rate: {result['growth']}")
else:
    print(f"Error: {result['error']}")
```

---

## Model Caching for MCP Server

```python
from functools import lru_cache
import time
import cobra

# Simple cache
model_cache = {}

def get_cached_model(model_id):
    """Load model with caching"""
    if model_id not in model_cache:
        print(f"Loading {model_id} into cache...")
        model_cache[model_id] = cobra.io.load_model(model_id)
    return model_cache[model_id]

# Or use LRU cache decorator
@lru_cache(maxsize=10)
def load_model_cached(model_id):
    """Load model with LRU caching"""
    return cobra.io.load_model(model_id)

model = get_cached_model('textbook')  # First call loads
model = get_cached_model('textbook')  # Second call from cache
```

---

## References and Resources

- **Official Documentation:** https://cobrapy.readthedocs.io/
- **Tutorial:** https://cobrapy.readthedocs.io/en/latest/getting_started.html
- **BiGG Models Database:** http://bigg.ucsd.edu/ (download genome-scale models)
- **COBRA Methods Paper:** [Nature Protocols 2011](https://doi.org/10.1038/nprot.2011.308)
- **COBRApy Paper:** [BMC Systems Biology 2013](https://doi.org/10.1186/1752-0509-7-74)

---

## Version Information

**Tested with:** COBRApy 0.30.0  
**Python:** 3.8+  
**Last Updated:** 2026-01-28

