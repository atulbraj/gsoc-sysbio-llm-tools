# CarveMe Skills for LLM Integration

CarveMe is an automated tool for genome-scale metabolic model reconstruction from genome sequences.

**Version Tested:** 1.5.1  
**Documentation:** https://carveme.readthedocs.io/  
**GitHub:** https://github.com/cdanielmachado/carveme  
**Paper:** [Nucleic Acids Research 2018](https://doi.org/10.1093/nar/gky537)

---

## Overview

CarveMe automates metabolic model reconstruction:
- **Input:** Protein sequences (FASTA) or RefSeq accession
- **Process:** Gene annotation → Reaction mapping → Gap-filling
- **Output:** Genome-scale metabolic model (SBML format)
- **Time:** Minutes to hours depending on genome size

Key advantages:
- Fully automated workflow
- High-quality template-based reconstruction
- Built-in gap-filling
- Multiple media conditions
- RefSeq database integration

---

## Basic Model Reconstruction

Reconstruct a metabolic model from protein sequences.

```bash
# From protein FASTA file
carve proteins.faa -o model.xml

# With specific organism name
carve proteins.faa -o model.xml --name "Escherichia coli"

# Specify gram type for better reconstruction
carve proteins.faa -o model.xml --gram-positive
carve proteins.faa -o model.xml --gram-negative
```

**Input:**
- `proteins.faa`: Protein sequences in FASTA format
- Can also use genome nucleotide sequences (`.fna`)

**Output:**
- `model.xml`: SBML format metabolic model

**Typical runtime:** 5-30 minutes for bacterial genomes

---

## Reconstruct from RefSeq

Use NCBI RefSeq accession for automatic genome download.

```bash
# Using RefSeq accession
carve --refseq GCF_000005845.2 -o ecoli_model.xml

# With organism name
carve --refseq GCF_000005845.2 -o model.xml --name "E. coli K-12"

# Multiple genomes
carve --refseq GCF_000005845.2 --refseq GCF_000006945.2 -o models/
```

**Common RefSeq examples:**
- E. coli K-12: `GCF_000005845.2`
- B. subtilis: `GCF_000009045.1`
- S. cerevisiae: `GCF_000146045.2`

**Note:** Requires internet connection for genome download

---

## Specify Growth Medium

Define media conditions for gap-filling.

```bash
# Use pre-defined medium
carve proteins.faa -o model.xml --mediadb M9

# Rich medium (LB)
carve proteins.faa -o model.xml --mediadb LB

# Multiple media (tests all)
carve proteins.faa -o model.xml --mediadb M9,LB

# Custom medium from file
carve proteins.faa -o model.xml --media custom_media.csv
```

**Pre-defined media:**
- `M9`: Minimal glucose medium
- `M9[glycerol]`: M9 with glycerol
- `LB`: Luria-Bertani (rich medium)
- `TSB`: Tryptic Soy Broth

**Custom medium format (CSV):**
```csv
compound,flux
glc__D_e,10
o2_e,20
nh4_e,10
pi_e,10
```

---

## Gap-Filling Options

Control the gap-filling process.

```bash
# Enable gap-filling (default)
carve proteins.faa -o model.xml --gapfill default

# No gap-filling (draft model only)
carve proteins.faa -o model.xml --gapfill none

# Use specific solver
carve proteins.faa -o model.xml --solver cplex
carve proteins.faa -o model.xml --solver glpk

# Set time limit for gap-filling
carve proteins.faa -o model.xml --timelimit 300  # 5 minutes
```

**Gap-filling strategies:**
- `default`: Standard gap-filling for growth
- `none`: No gap-filling, draft model only
- Custom: Advanced gap-filling with specific constraints

---

## Universe and Templates

Specify reaction universe and templates.

```bash
# Use specific universe
carve proteins.faa -o model.xml --universe bacteria

# Custom universe file
carve proteins.faa -o model.xml --universe-file custom_universe.xml

# Eukaryotic reconstruction
carve proteins.faa -o model.xml --universe eukaryota
```

**Available universes:**
- `bacteria`: Bacterial reaction universe (default)
- `eukaryota`: Eukaryotic reaction universe
- `archaea`: Archaeal reaction universe

---

## Output Options

Control output format and details.

```bash
# Verbose output
carve proteins.faa -o model.xml --verbose

# Quiet mode
carve proteins.faa -o model.xml --quiet

# Save intermediate files
carve proteins.faa -o model.xml --debug

# Specify output directory
carve proteins.faa -o outputs/model.xml

# JSON format output
carve proteins.faa -o model.json --format json
```

---

## Python API Usage

Use CarveMe programmatically from Python.

```python
from carveme import config, project_dir
from carveme.reconstruction.carving import carve_model
from carveme.reconstruction.utils import load_media_db

def reconstruct_model(fasta_file, output_file, media='M9'):
    """
    Reconstruct model using CarveMe Python API
    
    Parameters:
    - fasta_file: Path to protein FASTA
    - output_file: Path for output SBML
    - media: Growth medium name
    """
    
    # Load universe model
    universe_file = project_dir + config.get('generated', 'universe')
    
    # Load media database
    media_db = load_media_db()
    
    # Get specific medium
    if media in media_db:
        medium_comp = media_db[media]
    else:
        raise ValueError(f"Medium {media} not found")
    
    # Carve model
    model = carve_model(
        fasta_file=fasta_file,
        universe_file=universe_file,
        outputfile=output_file,
        media=medium_comp,
        gapfill=True
    )
    
    return model

# Usage
# model = reconstruct_model('ecoli.faa', 'ecoli_model.xml', 'M9')
```

---

## Wrapper for Command-Line Execution

Execute CarveMe as subprocess for API integration.

```python
import subprocess
import os
import json
from pathlib import Path

def run_carveme_reconstruction(
    input_file=None,
    refseq_id=None,
    output_file='model.xml',
    media='M9',
    gram_type=None,
    gapfill=True,
    verbose=False
):
    """
    Run CarveMe reconstruction via subprocess.
    
    Parameters:
    - input_file: Path to FASTA file (if not using RefSeq)
    - refseq_id: RefSeq accession (if not using file)
    - output_file: Output SBML file path
    - media: Growth medium
    - gram_type: 'positive' or 'negative'
    - gapfill: Enable gap-filling
    - verbose: Verbose output
    
    Returns: dict with status and paths
    """
    
    cmd = ['carve']
    
    # Input source
    if refseq_id:
        cmd.extend(['--refseq', refseq_id])
    elif input_file:
        if not os.path.exists(input_file):
            return {'success': False, 'error': f'Input file not found: {input_file}'}
        cmd.append(input_file)
    else:
        return {'success': False, 'error': 'Must provide input_file or refseq_id'}
    
    # Output
    cmd.extend(['-o', output_file])
    
    # Media
    if media:
        cmd.extend(['--mediadb', media])
    
    # Gram type
    if gram_type == 'positive':
        cmd.append('--gram-positive')
    elif gram_type == 'negative':
        cmd.append('--gram-negative')
    
    # Gap-filling
    if not gapfill:
        cmd.extend(['--gapfill', 'none'])
    
    # Verbose
    if verbose:
        cmd.append('--verbose')
    
    # Run command
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode == 0:
            return {
                'success': True,
                'model_file': output_file,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        else:
            return {
                'success': False,
                'error': result.stderr,
                'stdout': result.stdout
            }
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Reconstruction timed out (> 1 hour)'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Usage
# result = run_carveme_reconstruction(
#     refseq_id='GCF_000005845.2',
#     output_file='ecoli_model.xml',
#     media='M9'
# )
# if result['success']:
#     print(f"Model created: {result['model_file']}")
```

---

## Async Job Management

Handle long-running reconstructions asynchronously.

```python
import uuid
import threading
import time
from datetime import datetime
from enum import Enum

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# Global job registry
jobs = {}

class ReconstructionJob:
    def __init__(self, job_id, params):
        self.job_id = job_id
        self.params = params
        self.status = JobStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        self.progress = 0

def start_reconstruction_async(input_file=None, refseq_id=None, **kwargs):
    """
    Start reconstruction in background thread.
    
    Returns: job_id for tracking
    """
    
    job_id = str(uuid.uuid4())
    
    params = {
        'input_file': input_file,
        'refseq_id': refseq_id,
        **kwargs
    }
    
    job = ReconstructionJob(job_id, params)
    jobs[job_id] = job
    
    # Start background thread
    thread = threading.Thread(
        target=_run_reconstruction_job,
        args=(job,)
    )
    thread.daemon = True
    thread.start()
    
    return job_id

def _run_reconstruction_job(job):
    """Background worker for reconstruction"""
    
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now()
    
    try:
        # Run reconstruction
        result = run_carveme_reconstruction(**job.params)
        
        if result['success']:
            job.status = JobStatus.COMPLETED
            job.result = result
        else:
            job.status = JobStatus.FAILED
            job.error = result.get('error', 'Unknown error')
            
    except Exception as e:
        job.status = JobStatus.FAILED
        job.error = str(e)
    
    job.completed_at = datetime.now()
    job.progress = 100

def get_job_status(job_id):
    """Get status of reconstruction job"""
    
    if job_id not in jobs:
        return {'error': 'Job not found'}
    
    job = jobs[job_id]
    
    return {
        'job_id': job_id,
        'status': job.status.value,
        'created_at': job.created_at.isoformat(),
        'started_at': job.started_at.isoformat() if job.started_at else None,
        'completed_at': job.completed_at.isoformat() if job.completed_at else None,
        'progress': job.progress,
        'result': job.result,
        'error': job.error
    }

def get_job_result(job_id):
    """Get result of completed job"""
    
    if job_id not in jobs:
        return {'error': 'Job not found'}
    
    job = jobs[job_id]
    
    if job.status != JobStatus.COMPLETED:
        return {'error': f'Job not completed (status: {job.status.value})'}
    
    return job.result

# Usage
# job_id = start_reconstruction_async(refseq_id='GCF_000005845.2')
# print(f"Job started: {job_id}")
# 
# # Check status later
# status = get_job_status(job_id)
# print(f"Status: {status['status']}")
#
# # Get result when done
# if status['status'] == 'completed':
#     result = get_job_result(job_id)
```

---

## Validate Reconstructed Model

Check quality of reconstructed model.

```python
from cobra.io import read_sbml_model

def validate_carveme_model(model_file):
    """
    Validate CarveMe reconstruction output.
    
    Returns: dict with validation results
    """
    
    try:
        model = read_sbml_model(model_file)
    except Exception as e:
        return {'valid': False, 'error': f'Failed to load model: {str(e)}'}
    
    validation = {
        'valid': False,
        'model_id': model.id,
        'statistics': {
            'reactions': len(model.reactions),
            'metabolites': len(model.metabolites),
            'genes': len(model.genes)
        },
        'checks': {},
        'warnings': []
    }
    
    # Check model can optimize
    try:
        solution = model.optimize()
        validation['checks']['optimization'] = {
            'status': solution.status,
            'objective_value': float(solution.objective_value) if solution.objective_value else None
        }
        
        if solution.status != 'optimal':
            validation['warnings'].append(f"Model optimization status: {solution.status}")
        
    except Exception as e:
        validation['checks']['optimization'] = {'error': str(e)}
        validation['warnings'].append(f"Optimization failed: {str(e)}")
    
    # Check for minimum number of reactions
    if len(model.reactions) < 100:
        validation['warnings'].append(f"Low reaction count: {len(model.reactions)}")
    
    # Check for genes
    if len(model.genes) == 0:
        validation['warnings'].append("No genes in model")
    
    # Overall validation
    validation['valid'] = (
        len(model.reactions) > 0 and
        len(model.metabolites) > 0 and
        validation['checks'].get('optimization', {}).get('status') == 'optimal'
    )
    
    return validation

# Usage
# validation = validate_carveme_model('reconstructed_model.xml')
# if validation['valid']:
#     print("Model is valid!")
#     print(f"Reactions: {validation['statistics']['reactions']}")
# else:
#     print("Issues found:")
#     for warning in validation['warnings']:
#         print(f"  - {warning}")
```

---

## Common Workflows

### Workflow 1: Basic Reconstruction Pipeline

Complete workflow from genome to validated model.

```python
def complete_reconstruction_pipeline(
    genome_file=None,
    refseq_id=None,
    organism_name=None,
    output_dir='outputs'
):
    """
    Complete reconstruction pipeline.
    
    Steps:
    1. Reconstruct model
    2. Validate model
    3. Return summary
    """
    
    import os
    from pathlib import Path
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Set output file
    if organism_name:
        safe_name = organism_name.replace(' ', '_').lower()
        output_file = f"{output_dir}/{safe_name}_model.xml"
    else:
        output_file = f"{output_dir}/model.xml"
    
    print(f"Starting reconstruction...")
    print(f"Output: {output_file}")
    
    # Run reconstruction
    result = run_carveme_reconstruction(
        input_file=genome_file,
        refseq_id=refseq_id,
        output_file=output_file,
        media='M9'
    )
    
    if not result['success']:
        return {
            'success': False,
            'error': result['error']
        }
    
    print("Reconstruction complete!")
    print("Validating model...")
    
    # Validate
    validation = validate_carveme_model(output_file)
    
    return {
        'success': True,
        'model_file': output_file,
        'validation': validation,
        'reconstruction_output': result.get('stdout', '')
    }

# Usage
# result = complete_reconstruction_pipeline(
#     refseq_id='GCF_000005845.2',
#     organism_name='E. coli K12'
# )
```

### Workflow 2: Batch Reconstruction

Reconstruct multiple genomes.

```python
def batch_reconstruction(genome_list, output_dir='batch_models'):
    """
    Reconstruct models for multiple genomes.
    
    Parameters:
    - genome_list: List of dicts with 'refseq' or 'file' and optional 'name'
    - output_dir: Directory for output models
    
    Returns: Summary of all reconstructions
    """
    
    from pathlib import Path
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for i, genome_info in enumerate(genome_list, 1):
        print(f"\n[{i}/{len(genome_list)}] Processing {genome_info.get('name', 'Unknown')}")
        
        name = genome_info.get('name', f'model_{i}')
        safe_name = name.replace(' ', '_').lower()
        output_file = f"{output_dir}/{safe_name}.xml"
        
        result = run_carveme_reconstruction(
            input_file=genome_info.get('file'),
            refseq_id=genome_info.get('refseq'),
            output_file=output_file,
            media='M9'
        )
        
        results.append({
            'name': name,
            'output_file': output_file if result['success'] else None,
            'success': result['success'],
            'error': result.get('error')
        })
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    summary = {
        'total': len(results),
        'successful': successful,
        'failed': failed,
        'results': results
    }
    
    print(f"\n=== Batch Reconstruction Complete ===")
    print(f"Total: {summary['total']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    
    return summary

# Usage
# genomes = [
#     {'refseq': 'GCF_000005845.2', 'name': 'E. coli K-12'},
#     {'refseq': 'GCF_000009045.1', 'name': 'B. subtilis'},
#     {'file': 'custom_genome.faa', 'name': 'Custom organism'}
# ]
# summary = batch_reconstruction(genomes)
```

### Workflow 3: Reconstruction with Multiple Media

Test reconstruction under different growth conditions.

```python
def multi_media_reconstruction(
    input_file=None,
    refseq_id=None,
    media_list=['M9', 'LB'],
    output_dir='multi_media_models'
):
    """
    Reconstruct models under multiple media conditions.
    
    Useful for comparing gap-filling under different conditions.
    """
    
    from pathlib import Path
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    for medium in media_list:
        print(f"\nReconstructing with {medium} medium...")
        
        output_file = f"{output_dir}/model_{medium}.xml"
        
        result = run_carveme_reconstruction(
            input_file=input_file,
            refseq_id=refseq_id,
            output_file=output_file,
            media=medium
        )
        
        if result['success']:
            validation = validate_carveme_model(output_file)
            results[medium] = {
                'success': True,
                'model_file': output_file,
                'reactions': validation['statistics']['reactions'],
                'genes': validation['statistics']['genes'],
                'growth': validation['checks']['optimization'].get('objective_value')
            }
        else:
            results[medium] = {
                'success': False,
                'error': result['error']
            }
    
    # Compare results
    print("\n=== Media Comparison ===")
    for medium, data in results.items():
        if data['success']:
            print(f"{medium}: {data['reactions']} reactions, growth={data['growth']:.3f}")
        else:
            print(f"{medium}: Failed - {data['error']}")
    
    return results

# Usage
# results = multi_media_reconstruction(
#     refseq_id='GCF_000005845.2',
#     media_list=['M9', 'LB', 'M9[glycerol]']
# )
```

---

## JSON Serialization for APIs

Format reconstruction results for API responses.

```python
import json
from datetime import datetime

def reconstruction_to_json(reconstruction_result, validation_result=None):
    """
    Convert reconstruction results to JSON format.
    
    Suitable for API responses.
    """
    
    response = {
        'timestamp': datetime.now().isoformat(),
        'reconstruction': {
            'success': reconstruction_result['success'],
            'model_file': reconstruction_result.get('model_file'),
            'error': reconstruction_result.get('error')
        }
    }
    
    if validation_result:
        response['validation'] = {
            'valid': validation_result['valid'],
            'model_id': validation_result.get('model_id'),
            'statistics': validation_result.get('statistics', {}),
            'optimization': validation_result.get('checks', {}).get('optimization', {}),
            'warnings': validation_result.get('warnings', [])
        }
    
    return response

# Usage
# result = run_carveme_reconstruction(refseq_id='GCF_000005845.2')
# if result['success']:
#     validation = validate_carveme_model(result['model_file'])
#     json_response = reconstruction_to_json(result, validation)
#     print(json.dumps(json_response, indent=2))
```

---

## Error Handling

Robust error handling for production use.

```python
def safe_reconstruction(input_file=None, refseq_id=None, **kwargs):
    """
    Safely run reconstruction with comprehensive error handling.
    """
    
    result = {
        'success': False,
        'stage': None,
        'error': None,
        'warnings': []
    }
    
    # Validate inputs
    result['stage'] = 'input_validation'
    
    if not input_file and not refseq_id:
        result['error'] = 'Must provide input_file or refseq_id'
        return result
    
    if input_file and not os.path.exists(input_file):
        result['error'] = f'Input file not found: {input_file}'
        return result
    
    # Check CarveMe installation
    result['stage'] = 'tool_check'
    
    try:
        subprocess.run(['carve', '--version'], capture_output=True, check=True)
    except FileNotFoundError:
        result['error'] = 'CarveMe not installed or not in PATH'
        return result
    except Exception as e:
        result['error'] = f'CarveMe check failed: {str(e)}'
        return result
    
    # Run reconstruction
    result['stage'] = 'reconstruction'
    
    try:
        recon_result = run_carveme_reconstruction(
            input_file=input_file,
            refseq_id=refseq_id,
            **kwargs
        )
        
        if not recon_result['success']:
            result['error'] = recon_result['error']
            return result
        
        result['model_file'] = recon_result['model_file']
        
    except Exception as e:
        result['error'] = f'Reconstruction failed: {str(e)}'
        return result
    
    # Validate output
    result['stage'] = 'validation'
    
    try:
        validation = validate_carveme_model(result['model_file'])
        result['validation'] = validation
        
        if not validation['valid']:
            result['warnings'].extend(validation['warnings'])
        
    except Exception as e:
        result['error'] = f'Validation failed: {str(e)}'
        return result
    
    # Success
    result['success'] = True
    result['stage'] = 'complete'
    
    return result

# Usage
# result = safe_reconstruction(refseq_id='GCF_000005845.2')
# if result['success']:
#     print(f"Model created: {result['model_file']}")
#     if result['warnings']:
#         print(f"Warnings: {result['warnings']}")
# else:
#     print(f"Failed at {result['stage']}: {result['error']}")
```

---

## Performance Notes

**Reconstruction Times:**
- Small bacterial genome (< 2000 genes): 5-15 minutes
- Medium bacterial genome (2000-5000 genes): 15-30 minutes
- Large bacterial genome (> 5000 genes): 30-60 minutes
- Eukaryotic genomes: 1-3+ hours

**Factors affecting speed:**
- Genome size (number of genes)
- Media complexity
- Gap-filling settings
- Solver performance (CPLEX faster than GLPK)

**Resource requirements:**
- Memory: 2-8 GB depending on genome size
- CPU: Benefits from multiple cores
- Disk: ~100-500 MB per model

**Optimization tips:**
- Use `--gapfill none` for faster draft models
- Limit `--timelimit` for time-critical applications
- Use CPLEX solver if available (much faster than GLPK)
- Cache results - don't reconstruct same genome repeatedly

---

## Testing Examples

```python
import pytest
import tempfile
from pathlib import Path

def test_carveme_command_builder():
    """Test command building"""
    result = run_carveme_reconstruction(
        refseq_id='GCF_000005845.2',
        output_file='test.xml',
        media='M9'
    )
    # Should not crash (might fail without CarveMe installed)
    assert 'success' in result

def test_async_job_creation():
    """Test async job management"""
    job_id = start_reconstruction_async(refseq_id='GCF_000005845.2')
    assert isinstance(job_id, str)
    assert len(job_id) > 0
    
    status = get_job_status(job_id)
    assert status['job_id'] == job_id
    assert 'status' in status

def test_validation_with_invalid_file():
    """Test validation handles missing files"""
    result = validate_carveme_model('nonexistent.xml')
    assert result['valid'] == False
    assert 'error' in result

def test_json_serialization():
    """Test results are JSON-serializable"""
    import json
    
    result = {
        'success': True,
        'model_file': 'test.xml'
    }
    
    json_response = reconstruction_to_json(result)
    json_str = json.dumps(json_response)
    assert len(json_str) > 0
```

---

## Integration with Other Tools

CarveMe models work seamlessly with other tools:

```python
from cobra.io import read_sbml_model

# Load CarveMe model
model = read_sbml_model('carveme_model.xml')

# Analyze with COBRApy
solution = model.optimize()
print(f"Growth rate: {solution.objective_value}")

# Quality check with MEMOTE
# memote report snapshot carveme_model.xml

# Gap-fill with other tools
# Can use refineGEMs or other curation tools

# Visualize with Cytoscape
# Export to formats compatible with Cytoscape
```

---

## References and Resources

- **CarveMe Documentation:** https://carveme.readthedocs.io/
- **CarveMe Paper:** [Nucleic Acids Research 2018](https://doi.org/10.1093/nar/gky537)
- **CarveMe GitHub:** https://github.com/cdanielmachado/carveme
- **NCBI RefSeq:** https://www.ncbi.nlm.nih.gov/refseq/
- **BiGG Models:** http://bigg.ucsd.edu/

---

## Version Information

**Tested with:** CarveMe 1.5.1, COBRApy 0.30.0  
**Python:** 3.8+  
**Author:** Atul B Raj  
**Last Updated:** 2026-01-28

---

## Notes for MCP Server Implementation

When building the MCP server for CarveMe:

1. **Async architecture is critical** - Reconstructions take minutes to hours
2. **Job queue system** - Use Celery, RQ, or similar
3. **Progress tracking** - Parse CarveMe output for progress updates
4. **Resource limits** - Set timeouts and memory limits
5. **Caching** - Cache completed reconstructions by genome hash
6. **File management** - Clean up old files, manage storage
7. **Error recovery** - Handle partial failures gracefully

**Example API endpoints:**

```
POST   /carveme/reconstruct      → Start reconstruction job
GET    /carveme/jobs/:id         → Get job status
GET    /carveme/jobs/:id/result  → Download completed model
GET    /carveme/jobs/:id/logs    → View reconstruction logs
DELETE /carveme/jobs/:id         → Cancel/delete job
```

**Job lifecycle:**
```
PENDING → RUNNING → COMPLETED
                  ↘ FAILED
```
