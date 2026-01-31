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

---

## CarveMe Exploration - 2026-01-28

### Key Learnings:
- CarveMe = Automated metabolic model reconstruction
- Command-line tool (primarily)
- Template-based approach using universal model
- Automated gap-filling for biomass production
- RefSeq integration for direct genome download
- Multiple media conditions supported

### Challenges:
- Long-running process (minutes to hours)
- Command-line interface (need subprocess wrappers)
- Async job management essential for API
- Resource intensive (2-8GB memory)

### For MCP Integration:
- Must be async with job queue
- Progress tracking needed
- Timeout management critical
- File cleanup/management important
- Consider caching completed reconstructions

### SKILLS.md Coverage (1041 lines):
- Command-line usage patterns
- Python subprocess wrappers
- Async job management system
- Multiple workflow examples
- Batch reconstruction
- Multi-media testing
- Validation helpers
- Error handling

### Technical Details:
- Typical runtime: 5-60 minutes for bacteria
- Requires internet for RefSeq downloads
- Outputs SBML format models
- Gap-filling configurable

Progress: 3/5 tools complete

---

## MEMOTE Exploration - 2026-01-28

### Key Learnings:
- MEMOTE = Model quality testing tool
- Generates comprehensive HTML reports
- Validates stoichiometry, annotations, structure
- Command-line and Python API
- Provides quality scoring for models

### Technical Issue Encountered:
- Python 3.13 + macOS multiprocessing issue
- `find_blocked_reactions()` uses multiprocessing internally
- Workaround: use `if __name__ == '__main__':` guard
- Not an issue in Linux Docker (production environment)

### For SKILLS.md:
- Document main validation functions
- Quality scoring approach
- Annotation checks
- Mass/charge balance validation
- GPR (Gene-Protein-Reaction) associations
- Note multiprocessing workaround for macOS
- Focus on JSON-serializable results for API

### Main MEMOTE Functions:
- Model validation tests
- Annotation completeness
- Stoichiometric consistency
- Quality report generation
- Programmatic test execution

### Next:
- Create comprehensive MEMOTE SKILLS.md (~500-600 lines)
- Document all quality check functions
- Include workflow examples
- Add JSON serialization helpers
## MCP Server Prototype - 2026-01-28

### What I Built:
- Flask-based REST API server for COBRApy
- Implements Model Context Protocol (MCP) for LLM integration
- 6 core tool endpoints: load, optimize, stats, reaction info, FVA, gene knockout
- In-memory model caching for performance
- Comprehensive error handling with JSON responses
- Validation script to verify functionality without network

### Architecture:
- **Server**: Flask app on port 5001
- **Cache**: Python dictionary for loaded models
- **Endpoints**: RESTful JSON API
- **Tools**: Each endpoint exposes a specific COBRApy capability
- **Error Handling**: Try-except blocks with traceback for debugging

### Files Created:
- `server.py` (~380 lines) - Main Flask application
- `requirements.txt` - Dependencies (flask, cobra)
- `README.md` - Comprehensive documentation with examples
- `test_server.py` - Test suite for all endpoints
- `example_workflow.py` - LLM agent simulation with 3 workflows
- `validate_server.py` - Code validation without network

### Key Design Decisions:
1. **Port 5001**: Avoided conflict with macOS AirPlay on 5000
2. **In-memory cache**: Fast but not persistent (good for prototype)
3. **JSON responses**: Standard format for API communication
4. **Model IDs**: String identifiers for cached models
5. **Error traces**: Include full traceback in development mode

### MCP Protocol Implementation:
- `/health` - Server status check
- `/tools` - List available tools (MCP discovery)
- `/models` - List cached models
- Tool endpoints follow pattern: `/tools/<tool_name>`
- Each tool returns: `{"success": bool, "result": data}` or `{"error": msg}`

### Testing Strategy:
- Validation script: Tests without network (imports, endpoints, COBRApy)
- Test script: Full HTTP testing of all endpoints (requires running server)
- Example workflow: Demonstrates LLM agent patterns

### What It Demonstrates:
- **Integration Skills**: Can wrap existing tools in API
- **MCP Understanding**: Implements protocol for LLM tools
- **Production Thinking**: Includes caching, error handling, validation
- **Documentation**: Clear README with curl + Python examples

### Next Steps for Production:
- Add authentication/API keys
- Use persistent storage (Redis) instead of in-memory cache
- Add rate limiting
- Deploy with gunicorn/uwsgi
- Add more endpoints (medium modification, model comparison)
- WebSocket support for long-running analyses

### Time Invested:
- Planning: 30 min
- Server implementation: 2 hours
- Test scripts: 1 hour
- Documentation: 45 min
- Validation & debugging: 45 min
- **Total: ~5 hours**