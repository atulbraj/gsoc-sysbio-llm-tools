# Project Structure

## Current Organization

```
gsoc-sysbio-llm-tools/
├── skills/              # SKILLS.md documentation for each tool
│   ├── cobrapy/
│   │   └── SKILLS.md (596 lines) ✓
│   ├── memote/
│   │   └── SKILLS.md (804 lines) ✓
│   ├── carveme/
│   │   └── SKILLS.md (1,041 lines) ✓
│   ├── refinegems/
│   └── cytoscape/
├── mcp-servers/         # MCP server implementations
│   └── cobrapy-server/  ✓
│       ├── server.py (380 lines)
│       ├── test_server.py
│       ├── example_workflow.py
│       ├── validate_server.py
│       ├── requirements.txt
│       └── README.md
├── examples/            # Example workflows and use cases
│   └── (to be added)
├── learning/            # Personal learning notes and explorations
│   ├── cobrapy_exploration.py
│   ├── memote_exploration.py
│   ├── carveme_exploration.py
│   └── NOTES.md
├── docs/                # Additional documentation
│   └── (to be added)
├── LICENSE
└── README.md
```

## Progress Summary

### Completed Work:
- ✅ **COBRApy SKILLS.md** (596 lines) - Committed & pushed
- ✅ **MEMOTE SKILLS.md** (804 lines) - Committed & pushed  
- ✅ **CarveMe SKILLS.md** (1,041 lines) - Local only
- ✅ **MCP Server Prototype** (cobrapy-server) - Local only

### Total Documentation: 2,441 lines across 3 tools
### Total Code: ~380 lines Flask server + test scripts

## Roadmap

### Phase 1: Documentation (Weeks 1-2)
- [x] COBRApy SKILLS.md (596 lines)
- [x] MEMOTE SKILLS.md (804 lines)
- [x] CarveMe SKILLS.md (1,041 lines)
- [ ] refineGEMs SKILLS.md (optional)
- [ ] Cytoscape SKILLS.md (optional)

### Phase 2: MCP Servers (Weeks 3-6)
- [x] COBRApy MCP server prototype ← **YOU ARE HERE**
### Phase 4: Proof of Concept (Weeks 11-12)
- [ ] Bacterial network reconstruction
- [ ] Analysis workflow
- [ ] Documentation
