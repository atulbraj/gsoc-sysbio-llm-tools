Provide established Metabolic Systems Biology tooling for reconstruction and analysis for LLMs 

### Background
Reconstruction and subsequent network analysis are the fundamental processes of the systems biology of genome-scale metabolic models (GEMs). A plethora of tools exist in this space, and some of them emerged as the de facto standards (specifically [COBRApy](), [CarveMe](), [MEMOTE](), [Cytoscape](). The skillful and creative usage of these tools is a prerequisite for reliable knowledge extraction and fruitful hypothesis generation using GEMs.

GEMs are graph data structures that are well-suited for loading to and querying from a graph database. Consequently, tooling to load SBML into Neo4J ([Neo4JSBML](https://github.com/brsynth/neo4jsbml) has been developed.
 
The dominant open standards for LLM tool usage currently are the Model Context Protocol (MCP) and the SKILLS.md mechanism. These standards are designed as lightweight mechanisms to allow LLM agents to call external software tools in pursuit of a given goal. MCP server-based tools suffer from a context bloat problem that can be mitigated using dynamic tool detection. The most important software tools in systems biology currently have no integrations available to make them available to LLM agents. Neo4J has an official MCP server that allows an LLM to query and manipulate graph databases.

GEMs, like all formal models, have large potentials as curated, focused organism databases, as well as hypothesis generating oracles. Unlike with LLMs, their "responses" are fundamentally deterministic and mechanistic, grounded in knowledge. Their accessibility and usability however is severely limited by the sheer complexity and number of tools and databases involved. Furthermore, the idiosyncratic nature of lines of inquiry into a model usually means each analysis is (at least partially) as unique a gem as the GEM it investigates.

### Goal

1. MCP Servers and/or SKILLS.md documentation for at least these reconstruction and analysis tools are made available:
- CarveMe
- COBRApy
- MEMOTE
- refineGEMs
- Cytoscape

2. A portable project setup (docker-compose.yml in case of MCP, clonable repo in case of skills + Neo4J database and MCP container setup) is made available, to enable users to start using these tools as a framework for interacting with GEMs using LLMs with minimal setup.

3.  This setup is used in conjunction with the OpenCode LLM agent framework that supports both MCP and SKILLS.md. A proof of concept reconstruction and analysis of a bacterial metabolic network are performed.

### Difficulty Level: Easy/Medium/Hard
**Easy**.

MCP servers are fundamentally HTTP wrappers around given functionality and their implementation is usually easy. SKILLS.md fundamentally uses documentation of tools, which can to a large degree be extracted and adapted from existing documentation. Both processes lend themselves exceedingly well to LLM-assistance.

The greatest difficulty in the project lies in the understanding and evaluation of the LLM output and sufficient understanding of the underlying tools and data structures to properly prompt it.

### Size and Length of Project
- medium: 175
- 12 weeks

### Skills

**Essential skills:** 
- Programming proficiency (pref. Python)
- HTTP APIs (i.e. fundamental HTTP concepts (methods, routes), JSON, some experience programming a server, for example using Flask)
**Nice to have skills:**
- Docker
- Proficiency with at least one visualization library (pref. ggplot or Vega-Lite)
- OpenAPI/Swagger (for Cytoscape REST)

### AI Usage Policy
We welcome the use of AI tools by users who are capable and have proven expertise in the field they are using AIs for. We care first and foremost about the characteristics of the software artifact. That is, code needs to do exactly what it is supposed to, not "be written by a human". It needs to be maintainable, not "be pretty".

We therefore explicitly encourage participants to use AI tools, as long as they are capable and prepared to responsibly review and integrate the generated code.
