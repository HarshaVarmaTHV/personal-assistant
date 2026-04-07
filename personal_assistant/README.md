# Personal Assistant Agent (ADK & MCP)

This project is a multi-agent personal assistant built using the Google ADK (Agent Development Kit) and Vertex AI. It coordinates specialized agents to manage a user's daily schedule and knowledge base using a Firestore MCP (Model Context Protocol) server.

## Architecture

The system uses a **Hub-and-Spoke** orchestration model:

- **Orchestrator Agent (Root)**: The central entry point. It decomposes user requests, delegates tasks to specialists sequentially, and synthesizes their technical drafts into friendly, natural language responses.
- **Daily Scheduler Agent**: Manages the `plans` collection. It handles all time-based activities (gym, meetings, routines). It follows a "Query-then-Update" pattern to maintain structured daily timelines.
- **Knowledge Notes Agent**: Manages the `notes` collection. It captures unstructured information, auto-generates summaries/tags, and handles knowledge retrieval.

## Technical Requirements & Constraints

### 1. Database Schema (Firestore)
- **Collection: `plans`**: Stores daily schedules.
  - `user_id`: "demo_user" (Mandatory)
  - `date`: "YYYY-MM-DD" (Used for indexing)
  - `schedule`: List of `{"time": "HH:MM", "task": "string"}`
- **Collection: `notes`**: Stores personal knowledge.
  - `user_id`: "demo_user"
  - `content`, `summary`, `tags`

### 2. MCP Tooling (Firestore)
The agent interacts with Firestore via an MCP server. All queries (`query_collection`) **MUST** follow these strict rules:
- **String Filtering**: Filters must be an array of **escaped JSON strings**, NOT dictionaries.
- **Mandatory Filters**: Every `plans` query must filter by both `user_id` and `date`.
- **Composite Indexes**: Composite indexes are required for `user_id` + `date` (plans) and `user_id` + `due_date` (tasks/history).

## Setup & Execution

1. **Environment**: Ensure `.env` contains necessary credentials and the `URL` for the Cloud Run Toolbox.
2. **Initialization**: Run `firestore_data.py` to seed the initial collections and structure.
3. **Agent Loop**: The `agent.py` defines the `AdkApp` which can be deployed to Vertex AI Reasoning Engines.

## Communication Protocol
- **Sub-agents**: Provide "Draft Updates" (helpful but technical summaries) to the Orchestrator.
- **Orchestrator**: Fine-tunes these drafts into a warm, professional personal assistant persona for the end user.



# Run the deployment command
uvx --from google-adk \
adk deploy cloud_run \
  --project=harshavarmathv \
  --region=us-central1 \
  --service_name=personal-assistant \
  --with_ui \
  .