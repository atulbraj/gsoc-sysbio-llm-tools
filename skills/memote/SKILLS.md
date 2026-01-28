# MEMOTE Skills for LLM Integration

MEMOTE (Metabolic Model Testing) is a tool for quality control and quality assurance of genome-scale metabolic models (GEMs). It provides standardized tests to evaluate model quality, completeness, and consistency.

**Official Documentation:** https://memote.readthedocs.io/  
**GitHub:** https://github.com/opencobra/memote  
**Paper:** [Nature Biotechnology 2020](https://doi.org/10.1038/s41587-020-0446-y)

---

## Overview

MEMOTE evaluates models based on:
- **Stoichiometric consistency** - Mass and charge balance
- **Annotation quality** - Database cross-references
- **Model structure** - Reactions, metabolites, compartments
- **Metabolite connectivity** - Dead-end metabolites, blocked reactions
- **Gene-Protein-Reaction associations** - GPR completeness

---

## Generate Model Report

Create a comprehensive quality report for a model.

```bash
# Command-line usage
memote report snapshot model.xml --filename report.html

# Generate JSON output
memote report snapshot model.xml --filename report.json --format json
```

**Output:** HTML or JSON report with quality scores and detailed test results

---

## Basic Model Validation

Check if a model can perform basic operations.

```python
from cobra.io import load_model, read_sbml_model

model = load_model('textbook')

# Test optimization
solution = model.optimize()

if solution.status == 'optimal':
    print(f"✓ Model optimizes successfully")
    print(f"  Growth rate: {solution.objective_value:.4f}")
else:
    print(f"✗ Model optimization failed: {solution.status}")

# Check model size
print(f"\nModel statistics:")
print(f"  Reactions: {len(model.reactions)}")
print(f"  Metabolites: {len(model.metabolites)}")
print(f"  Genes: {len(model.genes)}")
print(f"  Compartments: {len(model.compartments)}")
```

---

## Check Annotation Coverage

Verify that model components have proper annotations.

```python
def check_annotations(model):
    """Check annotation completeness"""
    
    reactions_with_annotations = sum(
        1 for r in model.reactions 
        if r.annotation and len(r.annotation) > 0
    )
    
    metabolites_with_annotations = sum(
        1 for m in model.metabolites 
        if m.annotation and len(m.annotation) > 0
    )
    
    genes_with_annotations = sum(
        1 for g in model.genes 
        if g.annotation and len(g.annotation) > 0
    )
    
    total_reactions = len(model.reactions)
    total_metabolites = len(model.metabolites)
    total_genes = len(model.genes)
    
    return {
        "reactions_annotated": reactions_with_annotations,
        "reactions_total": total_reactions,
        "reactions_percent": 100 * reactions_with_annotations / total_reactions if total_reactions > 0 else 0,
        "metabolites_annotated": metabolites_with_annotations,
        "metabolites_total": total_metabolites,
        "metabolites_percent": 100 * metabolites_with_annotations / total_metabolites if total_metabolites > 0 else 0,
        "genes_annotated": genes_with_annotations,
        "genes_total": total_genes,
        "genes_percent": 100 * genes_with_annotations / total_genes if total_genes > 0 else 0
    }

# Usage
model = load_model('textbook')
annotation_stats = check_annotations(model)

print("Annotation Coverage:")
print(f"  Reactions: {annotation_stats['reactions_annotated']}/{annotation_stats['reactions_total']} ({annotation_stats['reactions_percent']:.1f}%)")
print(f"  Metabolites: {annotation_stats['metabolites_annotated']}/{annotation_stats['metabolites_total']} ({annotation_stats['metabolites_percent']:.1f}%)")
print(f"  Genes: {annotation_stats['genes_annotated']}/{annotation_stats['genes_total']} ({annotation_stats['genes_percent']:.1f}%)")
```

---

## Check Formula Completeness

Verify metabolites have chemical formulas.

```python
def check_formulas(model):
    """Check if metabolites have formulas"""
    
    metabolites_with_formula = sum(
        1 for m in model.metabolites 
        if m.formula and len(m.formula) > 0
    )
    
    total_metabolites = len(model.metabolites)
    formula_percent = 100 * metabolites_with_formula / total_metabolites if total_metabolites > 0 else 0
    
    return {
        "metabolites_with_formula": metabolites_with_formula,
        "total_metabolites": total_metabolites,
        "formula_percent": formula_percent,
        "missing_formulas": [
            m.id for m in model.metabolites 
            if not m.formula or len(m.formula) == 0
        ]
    }

# Usage
model = load_model('textbook')
formula_stats = check_formulas(model)

print(f"Metabolites with formula: {formula_stats['metabolites_with_formula']}/{formula_stats['total_metabolites']} ({formula_stats['formula_percent']:.1f}%)")
if formula_stats['missing_formulas'][:5]:
    print(f"Examples missing formula: {formula_stats['missing_formulas'][:5]}")
```

---

## Charge Balance Validation

Check if reactions are charge-balanced.

```python
def check_charge_balance(reaction):
    """Check if a reaction is charge-balanced"""
    
    total_charge = 0
    has_charges = False
    
    for metabolite, coefficient in reaction.metabolites.items():
        if metabolite.charge is not None:
            total_charge += coefficient * metabolite.charge
            has_charges = True
    
    if not has_charges:
        return None  # Cannot determine
    
    return abs(total_charge) < 1e-6

def check_all_charge_balance(model):
    """Check charge balance for all reactions"""
    
    balanced = []
    unbalanced = []
    unknown = []
    
    for reaction in model.reactions:
        result = check_charge_balance(reaction)
        
        if result is None:
            unknown.append(reaction.id)
        elif result:
            balanced.append(reaction.id)
        else:
            unbalanced.append(reaction.id)
    
    return {
        "balanced": len(balanced),
        "unbalanced": len(unbalanced),
        "unknown": len(unknown),
        "total": len(model.reactions),
        "unbalanced_reactions": unbalanced
    }

# Usage
model = load_model('textbook')
charge_stats = check_all_charge_balance(model)

print(f"Charge-balanced reactions: {charge_stats['balanced']}/{charge_stats['total']}")
print(f"Unbalanced: {charge_stats['unbalanced']}")
print(f"Unknown (missing charge data): {charge_stats['unknown']}")
```

---

## Gene-Protein-Reaction (GPR) Validation

Check GPR associations.

```python
def check_gpr_associations(model):
    """Check Gene-Protein-Reaction associations"""
    
    stats = {
        "reactions_with_genes": 0,
        "reactions_without_genes": 0,
        "total_reactions": len(model.reactions),
        "orphan_reactions": []
    }
    
    for reaction in model.reactions:
        if reaction.genes:
            stats["reactions_with_genes"] += 1
        else:
            stats["reactions_without_genes"] += 1
            # Skip exchange/transport reactions
            if not reaction.id.startswith("EX_") and not reaction.id.startswith("DM_"):
                stats["orphan_reactions"].append(reaction.id)
    
    stats["gpr_coverage_percent"] = (
        100 * stats["reactions_with_genes"] / stats["total_reactions"]
        if stats["total_reactions"] > 0 else 0
    )
    
    return stats

# Usage
model = load_model('textbook')
gpr_stats = check_gpr_associations(model)

print("GPR Association Stats:")
print(f"  Reactions with genes: {gpr_stats['reactions_with_genes']}")
print(f"  Reactions without genes: {gpr_stats['reactions_without_genes']}")
print(f"  Coverage: {gpr_stats['gpr_coverage_percent']:.1f}%")
print(f"  Orphan reactions (non-exchange): {len(gpr_stats['orphan_reactions'])}")
```

---

## Check for Duplicate Metabolites

Find potentially duplicate metabolites (same formula in same compartment).

```python
def find_duplicate_metabolites(model):
    """Find metabolites with identical formulas in same compartment"""
    
    from collections import defaultdict
    
    formula_map = defaultdict(list)
    
    for metabolite in model.metabolites:
        if metabolite.formula:
            key = (metabolite.formula, metabolite.compartment)
            formula_map[key].append(metabolite.id)
    
    duplicates = {
        formula: ids 
        for formula, ids in formula_map.items() 
        if len(ids) > 1
    }
    
    return duplicates

# Usage
model = load_model('textbook')
duplicates = find_duplicate_metabolites(model)

print(f"Potential duplicate metabolites: {len(duplicates)}")
if duplicates:
    for (formula, compartment), ids in list(duplicates.items())[:3]:
        print(f"  {formula} in {compartment}: {ids}")
```

---

## Validate Compartments

Check compartment definitions.

```python
def check_compartments(model):
    """Validate model compartments"""
    
    compartments = model.compartments
    
    # Check metabolite distribution
    compartment_counts = {}
    for metabolite in model.metabolites:
        comp = metabolite.compartment
        compartment_counts[comp] = compartment_counts.get(comp, 0) + 1
    
    return {
        "total_compartments": len(compartments),
        "compartment_names": dict(compartments),
        "metabolite_distribution": compartment_counts
    }

# Usage
model = load_model('textbook')
comp_stats = check_compartments(model)

print(f"Compartments: {comp_stats['total_compartments']}")
for comp_id, comp_name in comp_stats['compartment_names'].items():
    metabolite_count = comp_stats['metabolite_distribution'].get(comp_id, 0)
    print(f"  {comp_id} ({comp_name}): {metabolite_count} metabolites")
```

---

## Calculate Quality Score

Create a comprehensive quality score for a model.

```python
def calculate_quality_score(model):
    """Calculate overall model quality score (0-100)"""
    
    score = 0
    max_score = 100
    
    # 1. Optimization (20 points)
    try:
        solution = model.optimize()
        if solution.status == 'optimal':
            score += 20
        elif solution.status == 'feasible':
            score += 10
    except:
        pass
    
    # 2. Annotation coverage (25 points)
    annotation_stats = check_annotations(model)
    annotation_avg = (
        annotation_stats['reactions_percent'] +
        annotation_stats['metabolites_percent'] +
        annotation_stats['genes_percent']
    ) / 3
    score += (25 * annotation_avg / 100)
    
    # 3. Formula completeness (15 points)
    formula_stats = check_formulas(model)
    score += (15 * formula_stats['formula_percent'] / 100)
    
    # 4. GPR coverage (20 points)
    gpr_stats = check_gpr_associations(model)
    score += (20 * gpr_stats['gpr_coverage_percent'] / 100)
    
    # 5. Charge balance (20 points)
    charge_stats = check_all_charge_balance(model)
    if charge_stats['total'] > 0:
        charge_score = 100 * charge_stats['balanced'] / charge_stats['total']
        score += (20 * charge_score / 100)
    
    return round(score, 2)

# Usage
model = load_model('textbook')
quality_score = calculate_quality_score(model)

print(f"Model Quality Score: {quality_score}/100")

# Grade interpretation
if quality_score >= 90:
    grade = "A (Excellent)"
elif quality_score >= 80:
    grade = "B (Good)"
elif quality_score >= 70:
    grade = "C (Acceptable)"
elif quality_score >= 60:
    grade = "D (Needs improvement)"
else:
    grade = "F (Poor)"

print(f"Grade: {grade}")
```

---

## Common Workflows

### Workflow 1: Quick Model Check

```python
from cobra.io import read_sbml_model

def quick_model_check(model_path):
    """Quick validation of a metabolic model"""
    
    model = read_sbml_model(model_path)
    
    print(f"Model: {model.id}")
    print(f"Reactions: {len(model.reactions)}")
    print(f"Metabolites: {len(model.metabolites)}")
    print(f"Genes: {len(model.genes)}")
    
    # Test optimization
    solution = model.optimize()
    print(f"\nOptimization: {solution.status}")
    if solution.status == 'optimal':
        print(f"Growth rate: {solution.objective_value:.4f}")
    
    # Check annotations
    annotation_stats = check_annotations(model)
    print(f"\nAnnotation coverage:")
    print(f"  Reactions: {annotation_stats['reactions_percent']:.1f}%")
    print(f"  Metabolites: {annotation_stats['metabolites_percent']:.1f}%")
    print(f"  Genes: {annotation_stats['genes_percent']:.1f}%")
    
    # Overall score
    score = calculate_quality_score(model)
    print(f"\nQuality Score: {score}/100")
    
    return {
        'status': solution.status,
        'growth': solution.objective_value if solution.status == 'optimal' else None,
        'quality_score': score
    }

# Usage
# results = quick_model_check('path/to/model.xml')
```

### Workflow 2: Detailed Report Generation

```python
import json
from datetime import datetime

def generate_detailed_report(model, output_file='model_report.json'):
    """Generate comprehensive model quality report"""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'model_id': model.id,
        'model_name': model.name,
        'statistics': {
            'reactions': len(model.reactions),
            'metabolites': len(model.metabolites),
            'genes': len(model.genes),
            'compartments': len(model.compartments)
        },
        'optimization': {},
        'annotations': {},
        'formulas': {},
        'gpr': {},
        'charge_balance': {},
        'quality_score': 0
    }
    
    # Optimization
    try:
        solution = model.optimize()
        report['optimization'] = {
            'status': solution.status,
            'objective_value': float(solution.objective_value) if solution.objective_value else None
        }
    except Exception as e:
        report['optimization'] = {'error': str(e)}
    
    # Annotations
    report['annotations'] = check_annotations(model)
    
    # Formulas
    report['formulas'] = check_formulas(model)
    
    # GPR
    report['gpr'] = check_gpr_associations(model)
    
    # Charge balance
    report['charge_balance'] = check_all_charge_balance(model)
    
    # Quality score
    report['quality_score'] = calculate_quality_score(model)
    
    # Save to file
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to: {output_file}")
    return report

# Usage
model = load_model('textbook')
report = generate_detailed_report(model, 'ecoli_report.json')
```

### Workflow 3: Compare Models

```python
def compare_models(model1, model2, model1_name="Model 1", model2_name="Model 2"):
    """Compare quality metrics of two models"""
    
    def get_metrics(model):
        return {
            'reactions': len(model.reactions),
            'metabolites': len(model.metabolites),
            'genes': len(model.genes),
            'quality_score': calculate_quality_score(model),
            'annotation_coverage': check_annotations(model)['reactions_percent'],
            'gpr_coverage': check_gpr_associations(model)['gpr_coverage_percent']
        }
    
    metrics1 = get_metrics(model1)
    metrics2 = get_metrics(model2)
    
    print(f"{'Metric':<25} {model1_name:<20} {model2_name:<20} {'Difference':<15}")
    print("-" * 80)
    
    for key in metrics1:
        val1 = metrics1[key]
        val2 = metrics2[key]
        diff = val2 - val1
        print(f"{key:<25} {val1:<20.2f} {val2:<20.2f} {diff:+<15.2f}")
    
    return {'model1': metrics1, 'model2': metrics2}

# Usage
# model_v1 = read_sbml_model('model_v1.xml')
# model_v2 = read_sbml_model('model_v2.xml')
# comparison = compare_models(model_v1, model_v2, "Version 1", "Version 2")
```

---

## JSON Serialization for APIs

```python
def memote_results_to_json(model):
    """Convert MEMOTE-style checks to JSON format"""
    
    optimization_result = model.optimize()
    annotation_stats = check_annotations(model)
    formula_stats = check_formulas(model)
    gpr_stats = check_gpr_associations(model)
    charge_stats = check_all_charge_balance(model)
    quality_score = calculate_quality_score(model)
    
    return {
        "model_id": model.id,
        "model_name": model.name,
        "size": {
            "reactions": len(model.reactions),
            "metabolites": len(model.metabolites),
            "genes": len(model.genes),
            "compartments": len(model.compartments)
        },
        "optimization": {
            "status": optimization_result.status,
            "objective_value": float(optimization_result.objective_value) if optimization_result.objective_value else None
        },
        "annotations": {
            "reactions_percent": round(annotation_stats['reactions_percent'], 2),
            "metabolites_percent": round(annotation_stats['metabolites_percent'], 2),
            "genes_percent": round(annotation_stats['genes_percent'], 2)
        },
        "formulas": {
            "completeness_percent": round(formula_stats['formula_percent'], 2),
            "missing_count": len(formula_stats['missing_formulas'])
        },
        "gpr": {
            "coverage_percent": round(gpr_stats['gpr_coverage_percent'], 2),
            "orphan_reactions": len(gpr_stats['orphan_reactions'])
        },
        "charge_balance": {
            "balanced": charge_stats['balanced'],
            "unbalanced": charge_stats['unbalanced'],
            "unknown": charge_stats['unknown']
        },
        "quality_score": quality_score
    }

# Usage
import json
model = load_model('textbook')
result = memote_results_to_json(model)
print(json.dumps(result, indent=2))
```

---

## Error Handling

```python
def safe_model_validation(model_path):
    """Safely validate model with comprehensive error handling"""
    
    try:
        model = read_sbml_model(model_path)
    except FileNotFoundError:
        return {'error': 'Model file not found', 'success': False}
    except Exception as e:
        return {'error': f'Failed to load model: {str(e)}', 'success': False}
    
    results = {
        'success': True,
        'model_id': model.id,
        'checks': {}
    }
    
    # Optimization check
    try:
        solution = model.optimize()
        results['checks']['optimization'] = {
            'passed': solution.status == 'optimal',
            'status': solution.status,
            'value': float(solution.objective_value) if solution.objective_value else None
        }
    except Exception as e:
        results['checks']['optimization'] = {
            'passed': False,
            'error': str(e)
        }
    
    # Annotation check
    try:
        annotation_stats = check_annotations(model)
        results['checks']['annotations'] = {
            'passed': annotation_stats['reactions_percent'] > 50,
            'coverage': annotation_stats
        }
    except Exception as e:
        results['checks']['annotations'] = {
            'passed': False,
            'error': str(e)
        }
    
    # Formula check
    try:
        formula_stats = check_formulas(model)
        results['checks']['formulas'] = {
            'passed': formula_stats['formula_percent'] > 80,
            'completeness': formula_stats['formula_percent']
        }
    except Exception as e:
        results['checks']['formulas'] = {
            'passed': False,
            'error': str(e)
        }
    
    return results

# Usage
# result = safe_model_validation('path/to/model.xml')
# print(json.dumps(result, indent=2))
```

---

## Testing Examples

```python
def test_model_optimization():
    """Test model can optimize"""
    model = load_model('textbook')
    solution = model.optimize()
    assert solution.status == 'optimal'
    assert solution.objective_value > 0.8

def test_annotation_coverage():
    """Test annotation coverage is reasonable"""
    model = load_model('textbook')
    stats = check_annotations(model)
    assert stats['reactions_percent'] > 0
    assert stats['metabolites_percent'] > 0

def test_formula_completeness():
    """Test metabolites have formulas"""
    model = load_model('textbook')
    stats = check_formulas(model)
    assert stats['formula_percent'] > 90  # E. coli core should be complete

def test_quality_score():
    """Test quality score is calculated"""
    model = load_model('textbook')
    score = calculate_quality_score(model)
    assert 0 <= score <= 100
    assert score > 70  # E. coli core should score well

def test_gpr_coverage():
    """Test GPR associations exist"""
    model = load_model('textbook')
    stats = check_gpr_associations(model)
    assert stats['gpr_coverage_percent'] > 50
```

---

## Performance Notes

**Execution times (E. coli core model):**
- Quick validation: ~100-200ms
- Annotation check: ~50ms
- Formula check: ~30ms
- Charge balance check: ~100ms
- Full quality report: ~500ms-1s
- Official MEMOTE report: 5-30 minutes (comprehensive)

**For genome-scale models (2000+ reactions):**
- Quick validation: ~500ms-2s
- Full quality report (JSON): ~2-5s
- Official MEMOTE HTML report: 30-60+ minutes

**Optimization tips:**
- Cache model loading
- Run checks in parallel when possible
- Use JSON format for faster processing
- Skip time-intensive tests for quick checks

---

## Platform Notes

**macOS with Python 3.13+:**

Some COBRApy functions use multiprocessing and require proper guards on macOS:

```python
if __name__ == '__main__':
    from cobra.flux_analysis import find_blocked_reactions
    model = load_model('textbook')
    blocked = find_blocked_reactions(model)
```

This is not an issue in production Linux Docker containers.

---

## Integration with MEMOTE CLI

Wrap command-line MEMOTE for programmatic use:

```python
import subprocess
import json

def run_memote_report(model_path, output_format='json'):
    """Run MEMOTE command-line tool and return results"""
    
    output_file = f"memote_report.{output_format}"
    
    cmd = [
        'memote', 'report', 'snapshot',
        model_path,
        '--filename', output_file,
        '--format', output_format
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )
        
        if result.returncode == 0:
            if output_format == 'json':
                with open(output_file, 'r') as f:
                    return json.load(f)
            return {'success': True, 'output_file': output_file}
        else:
            return {'error': result.stderr, 'success': False}
            
    except subprocess.TimeoutExpired:
        return {'error': 'MEMOTE report generation timed out', 'success': False}
    except Exception as e:
        return {'error': str(e), 'success': False}

# Usage
# result = run_memote_report('path/to/model.xml', 'json')
```

---

## References

- **MEMOTE Documentation:** https://memote.readthedocs.io/
- **MEMOTE Paper:** [Nature Biotechnology 2020](https://doi.org/10.1038/s41587-020-0446-y)
- **MEMOTE GitHub:** https://github.com/opencobra/memote
- **Model Standards:** https://github.com/opencobra/memote/tree/develop/memote/suite/tests

---

## Version Information

**Tested with:** MEMOTE 0.17.0, COBRApy 0.30.0  
**Python:** 3.8+  
**Last Updated:** 2026-01-28
