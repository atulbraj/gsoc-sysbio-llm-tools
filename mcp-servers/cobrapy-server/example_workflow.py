#!/usr/bin/env python3
"""
Example workflow demonstrating LLM agent using COBRApy MCP Server
Simulates how an AI assistant would interact with the server

Author: Atul B Raj
Date: 2026-01-28
"""

import requests
import json

BASE_URL = "http://localhost:5001"

class COBRApyAgent:
    """Simple agent that interacts with COBRApy MCP server"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.loaded_models = set()
    
    def call_tool(self, tool_name, params):
        """Call a tool on the MCP server"""
        response = requests.post(
            f"{self.base_url}/tools/{tool_name}",
            json=params
        )
        return response.json()
    
    def load_model(self, model_id):
        """Load a metabolic model"""
        result = self.call_tool("load_model", {"model_id": model_id})
        if result["success"]:
            self.loaded_models.add(model_id)
        return result
    
    def analyze_model_growth(self, model_id):
        """Analyze model growth potential"""
        # Ensure model is loaded
        if model_id not in self.loaded_models:
            self.load_model(model_id)
        
        # Get basic stats
        stats = self.call_tool("get_model_stats", {"model_id": model_id})
        
        # Run optimization
        fba = self.call_tool("optimize_model", {"model_id": model_id})
        
        return {
            "model": model_id,
            "num_reactions": stats["result"]["num_reactions"],
            "num_metabolites": stats["result"]["num_metabolites"],
            "num_genes": stats["result"]["num_genes"],
            "objective_value": fba["result"]["objective_value"],
            "status": fba["result"]["status"]
        }
    
    def find_essential_genes(self, model_id, sample_genes=None):
        """Test gene essentiality"""
        if model_id not in self.loaded_models:
            self.load_model(model_id)
        
        # Get model genes
        stats = self.call_tool("get_model_stats", {"model_id": model_id})
        all_genes = stats["result"]["genes"]
        
        # Sample some genes to test
        test_genes = sample_genes or all_genes[:5]
        
        essential = []
        non_essential = []
        
        for gene in test_genes:
            result = self.call_tool("gene_knockout", {
                "model_id": model_id,
                "gene_id": gene
            })
            
            if result["success"]:
                growth_rate = result["result"]["knockout_growth_rate"]
                if growth_rate < 0.01:  # Essentially zero
                    essential.append(gene)
                else:
                    non_essential.append(gene)
        
        return {
            "essential_genes": essential,
            "non_essential_genes": non_essential,
            "tested": len(test_genes)
        }
    
    def analyze_reaction_variability(self, model_id):
        """Run FVA to find flexible reactions"""
        if model_id not in self.loaded_models:
            self.load_model(model_id)
        
        fva_result = self.call_tool("run_fva", {"model_id": model_id})
        
        if not fva_result["success"]:
            return {"error": "FVA failed"}
        
        # Analyze variability
        reactions = fva_result["result"]["reactions"]
        
        flexible = []
        blocked = []
        fixed = []
        
        for rxn_id, bounds in reactions.items():
            min_flux = bounds["minimum"]
            max_flux = bounds["maximum"]
            
            # Classify based on flux ranges
            if abs(min_flux) < 1e-6 and abs(max_flux) < 1e-6:
                blocked.append(rxn_id)
            elif abs(max_flux - min_flux) < 1e-6:
                fixed.append(rxn_id)
            else:
                flexible.append(rxn_id)
        
        return {
            "flexible_reactions": len(flexible),
            "blocked_reactions": len(blocked),
            "fixed_reactions": len(fixed),
            "total": len(reactions),
            "examples": {
                "flexible": flexible[:5],
                "blocked": blocked[:5]
            }
        }


def workflow_1_basic_analysis():
    """Workflow 1: Basic model analysis"""
    print("\n" + "="*60)
    print("WORKFLOW 1: Basic Model Analysis")
    print("="*60)
    
    agent = COBRApyAgent()
    
    print("\n1. Loading E. coli textbook model...")
    load_result = agent.load_model("textbook")
    print(f"   Status: {load_result['message']}")
    
    print("\n2. Analyzing growth potential...")
    analysis = agent.analyze_model_growth("textbook")
    print(f"   Model size: {analysis['num_reactions']} reactions, "
          f"{analysis['num_metabolites']} metabolites, "
          f"{analysis['num_genes']} genes")
    print(f"   Growth rate: {analysis['objective_value']:.3f} /h")
    print(f"   Status: {analysis['status']}")


def workflow_2_gene_essentiality():
    """Workflow 2: Gene essentiality screening"""
    print("\n" + "="*60)
    print("WORKFLOW 2: Gene Essentiality Screening")
    print("="*60)
    
    agent = COBRApyAgent()
    
    print("\n1. Testing sample genes for essentiality...")
    test_genes = ["b0008", "b0116", "b0118", "b0720", "b0721"]
    results = agent.find_essential_genes("textbook", test_genes)
    
    print(f"\n   Tested {results['tested']} genes:")
    print(f"   Essential: {len(results['essential_genes'])} genes")
    if results['essential_genes']:
        print(f"      {', '.join(results['essential_genes'])}")
    print(f"   Non-essential: {len(results['non_essential_genes'])} genes")
    if results['non_essential_genes']:
        print(f"      {', '.join(results['non_essential_genes'])}")


def workflow_3_reaction_analysis():
    """Workflow 3: Reaction variability analysis"""
    print("\n" + "="*60)
    print("WORKFLOW 3: Reaction Variability Analysis")
    print("="*60)
    
    agent = COBRApyAgent()
    
    print("\n1. Running Flux Variability Analysis...")
    results = agent.analyze_reaction_variability("textbook")
    
    print(f"\n   Total reactions: {results['total']}")
    print(f"   Flexible: {results['flexible_reactions']} "
          f"({100*results['flexible_reactions']/results['total']:.1f}%)")
    print(f"   Blocked: {results['blocked_reactions']} "
          f"({100*results['blocked_reactions']/results['total']:.1f}%)")
    print(f"   Fixed: {results['fixed_reactions']} "
          f"({100*results['fixed_reactions']/results['total']:.1f}%)")
    
    if results['examples']['flexible']:
        print(f"\n   Example flexible reactions:")
        for rxn in results['examples']['flexible']:
            print(f"      - {rxn}")


def main():
    """Run all example workflows"""
    print("\n" + "="*70)
    print(" COBRApy MCP Server - LLM Agent Workflow Examples")
    print("="*70)
    print("\nThis demonstrates how an LLM agent would interact with the server")
    print("to perform metabolic modeling tasks.")
    
    try:
        # Test connection
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            raise Exception("Server unhealthy")
    except:
        print("\n❌ ERROR: Server not running!")
        print("Please start the server first: python server.py")
        return
    
    # Run workflows
    workflow_1_basic_analysis()
    workflow_2_gene_essentiality()
    workflow_3_reaction_analysis()
    
    print("\n" + "="*70)
    print("✓ All workflows completed successfully!")
    print("="*70)
    print("\nThese examples show how an LLM agent can:")
    print("  • Load and analyze metabolic models")
    print("  • Identify essential genes")
    print("  • Analyze metabolic flexibility")
    print("  • Make multi-step decisions based on results")


if __name__ == "__main__":
    main()
