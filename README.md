# Personal Assistant Project

This project consists of two main components that work together to provide a multi-agent personal assistant experience with Firestore integration.

## Project Structure

- [**mcp-toolbox**](./mcp-toolbox): A Model Context Protocol (MCP) toolset configured to interact with Google Cloud Firestore. It exposes Firestore operations as tools for AI agents.
- [**personal_assistant**](./personal_assistant): A multi-agent personal assistant built using the Google ADK (Agent Development Kit) and Vertex AI. It coordinates specialized agents to manage a user's daily schedule and knowledge base.

---

## [MCP Toolbox](./mcp-toolbox)

This component contains a Model Context Protocol (MCP) toolset configured to interact with Google Cloud Firestore. It uses the `mcp-toolbox` to expose Firestore operations as tools for AI agents.

### Configuration (`tools.yaml`)

The `tools.yaml` file is configured with:
- **Project ID**: `harshavarmathv`
- **Database**: `personal-assistant`
- **Toolset**: `firestore_full_access` (includes CRUD operations and collection queries).

### Deployment to Google Cloud

The toolbox is designed to be deployed to Google Cloud Run, allowing MCP-compatible clients to interact with your Firestore database securely.

---

## [Personal Assistant Agent](./personal_assistant)

The personal assistant uses a **Hub-and-Spoke** orchestration model to manage schedules and notes.

### Architecture

- **Orchestrator Agent (Root)**: Central entry point that decomposes requests and delegates tasks.
- **Daily Scheduler Agent**: Manages the `plans` collection for time-based activities.
- **Knowledge Notes Agent**: Manages the `notes` collection for unstructured information.

### Communication Protocol
- **Sub-agents**: Provide "Draft Updates" to the Orchestrator.
- **Orchestrator**: Synthesizes these drafts into a warm, professional persona for the end user.

---

## Getting Started

Refer to the individual `README.md` files in each directory for specific setup and deployment instructions:
- [MCP Toolbox Setup](./mcp-toolbox/README.md)
- [Personal Assistant Agent Setup](./personal_assistant/README.md)

- ## Links post deployment
- mcp : https://toolbox-296956655568.us-central1.run.app
- adk agent : https://personal-assistant-296956655568.us-central1.run.app
