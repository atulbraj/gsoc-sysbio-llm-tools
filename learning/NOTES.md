# Learning Notes

## COBRApy Exploration - 2026-01-28

### Key Concepts I Learned:
- Models contain reactions, metabolites, and genes
- FBA (Flux Balance Analysis) optimizes for biomass production
- Reactions have bounds (min/max flux)
- Models can be loaded from SBML files
- FVA (Flux Variability Analysis) shows min/max flux ranges
- Gene essentiality can be screened systematically
- Context managers (`with model:`) allow temporary modifications
- Medium composition affects growth predictions

### Key Functions for MCP/SKILLS:
- `cobra.io.read_sbml_model()` - Load model from SBML
- `cobra.io.load_model()` - Load built-in test models
- `model.optimize()` - Run FBA
- `model.reactions` - Access reactions
- `model.metabolites` - Access metabolites  
- `model.genes` - Access genes
- `model.summary()` - Get summary statistics
- `flux_variability_analysis()` - Compute flux ranges
- `single_gene_deletion()` - Test gene essentiality
- `single_reaction_deletion()` - Test reaction essentiality
- `delete_model_genes()` - Multiple gene knockouts

### Advanced Features Documented:
- JSON serialization helpers for API responses
- Model caching strategies for performance
- Error handling for optimization failures
- Testing patterns for model validation
- Performance benchmarks for different model sizes
- Four complete workflow examples

### Questions:
- How to handle large models in API responses? → Use pagination and caching
- What's the most common workflow? → Load → FBA → Gene knockout screening
- Best model format for MCP server? → JSON (faster loading)

### SKILLS.md Statistics:
- **622 lines** of comprehensive documentation
- 16+ main functions documented
- 4 complete workflow examples
- JSON serialization helpers included
- Error handling patterns provided
- Performance benchmarks added
- Testing examples included

### Time Invested:
- COBRApy exploration: 1 hour
- Documentation writing: 3 hours
- Testing and verification: 1 hour
- **Total: ~5 hours**

### Next Steps:
1. Test all code examples in SKILLS.md
2. Create similar documentation for MEMOTE
3. Begin MCP server prototype
4. Add example workflows directory
