# Programmation d'agents avec Python - Projet

Ce dossier contient un projet Python pour un agent IA personnalisé avec accès à
différent **tools**.

## Tech Stack

- Python 3.12
- Langchain
- MCP
- Standard SQL and API request tooling

## Project structure

### agent.py

The `agent.py` file exports a fully usable AI agent:

- `interroger_agent`: prompts the agent and displays the answer
- `creer_agent` creates a new agent with **langchain** library utilites

### tools

The agent has access to a wide range of tools, imported from the `tools/` directory:

- `text`: parsing, formatting and extracting key-words from text input
- `database`: interact with a commercial database: query products and client data 
- `recommendation`: recommend products according to specific criteria
- `public-api`: use an online conversion rates API to convert amounts between currencies
- `finance`: fetch up-to-date data about financial markets and crypto-currencies
- `calculation`: functions to compute common metrics such as taxes, margins and interests

### examples

The `main.py` file contains lots of usage example for the agent, showcasing the
capabilities of the tools.

## Development setup

A Python virtual environment with all dependencies is provided and MUST be used
for working on the project. Dependency version shouldn't be changed under any circumstances.

A minimal **docker compose** setup for a **pgvector** database is also included. It MUST BE launched
with the following **podman** command, as Docker isn't available on this host:

```bash
podman compose up -d
```
