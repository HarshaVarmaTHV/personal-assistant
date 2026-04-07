import os
import dotenv
import datetime
import calendar
from google.adk.agents import llm_agent
from vertexai.preview.reasoning_engines import AdkApp
from google.cloud import firestore

# Import the native ADK integration tools
from toolbox_adk import CredentialStrategy, ToolboxToolset

# 1. Configuration
URL = "https://toolbox-5r65z6mfgq-uc.a.run.app"
dotenv.load_dotenv()

# Map GEMINI_API_KEY to GOOGLE_API_KEY for the global Google AI Studio endpoint
if os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Set global location for the model backend
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

# 2. Native Toolset Initialization
creds = CredentialStrategy.workload_identity(target_audience=URL)
toolset = ToolboxToolset(
    server_url=URL,
    credentials=creds
)

def get_calendar_context() -> str:
    """Returns the current date, time, and day of the week.
    Use this tool to resolve relative dates like 'today', 'tomorrow', 'next Friday', etc.
    """
    now = datetime.datetime.now()
    day_name = calendar.day_name[now.weekday()]
    return f"Current Context: {now.strftime('%Y-%m-%d %H:%M:%S')} ({day_name})"

# --- Logging Infrastructure ---
db = firestore.Client(project="harshavarmathv", database="personal-assistant")

class LoggedLlmAgent(llm_agent.LlmAgent):
    """A wrapper for LlmAgent that logs all inputs, outputs, and internal traces to Firestore."""
    def __call__(self, input_text: str, **kwargs):
        response = super().__call__(input_text, **kwargs)
        try:
            # Attempt to extract tool calls or steps if the response is a complex object
            log_data = {
                "user_id": "demo_user",
                "agent": self.name,
                "action": "execution",
                "input": input_text,
                "timestamp": datetime.datetime.utcnow()
            }
            
            # If the response has a 'text' attribute (like in some ADK versions)
            if hasattr(response, 'text'):
                log_data["output"] = response.text
            else:
                log_data["output"] = str(response)

            # Store the raw response string/repr to catch tool calls and intermediate steps
            log_data["raw_response"] = repr(response)
            
            db.collection("agent_logs").add(log_data)
        except Exception as e:
            print(f"Error logging to Firestore: {e}")
        return response

# 3. Define Specialized Agents

daily_scheduler_agent = LoggedLlmAgent(
    name='daily_scheduler_agent',
    model='gemini-3.1-flash-lite-preview',
    tools=[toolset, get_calendar_context],

    instruction="""# Role: Expert Personal Daily Scheduler
You manage the user's daily plans in the 'plans' collection.

# Responsibilities
- **Schedule Management**: Add activities to a specific day's plan or retrieve existing schedules.
- **Delete Schedules**: If asked to clear or delete plans, you can remove records from the 'plans' collection.

# TECHNICAL FORMATTING GUARDRAIL (CRITICAL)
The `query_collection` tool REQUIRES `filters` to be an array of STRINGS (escaped JSON).
- **CRITICAL**: Every query MUST include BOTH `user_id == "demo_user"` AND a `date` filter.
- **DATE REQUIREMENT**: The `date` field is a STRING in "YYYY-MM-DD" format.
- **CORRECT Single Day**: `filters=['{"field": "user_id", "op": "==", "value": "demo_user"}', '{"field": "date", "op": "==", "value": "2026-04-05"}']`
- **STRICT FORBIDDEN**: Never use range operators like `>=` or `<=` for the `date` field. Always query one specific day at a time.

# Operational Rules
1. **Query Before Action**: Every time you need to add, update, or show a schedule, you MUST first query the 'plans' collection using the specific `date` and `user_id`.
2. **User ID**: Always include `user_id: "demo_user"` in all operations.
3. **Firestore Schema**: `date` (String, e.g., '2026-04-05'), `schedule` (List of `{"time": "HH:MM", "task": "string"}`).

# Internal Communication
- Return a "Draft Update" summary for the Orchestrator.
""",
)

knowledge_notes_agent = LoggedLlmAgent(
    name='knowledge_notes_agent',
    model='gemini-3.1-flash-lite-preview',
    tools=[toolset, get_calendar_context],
    instruction="""# Role: Knowledge Management Specialist
You manage information in the 'notes' collection.

# Responsibilities
- **Knowledge Management**: Create, search, or update notes.

# TECHNICAL FORMATTING GUARDRAIL (CRITICAL)
The `query_collection` tool REQUIRES `filters` to be an array of STRINGS (escaped JSON).
- **CORRECT**: `filters=['{"field": "user_id", "op": "==", "value": "demo_user"}']`

# Operational Rules
1. **Metadata**: Always generate `summary` and `tags`.
2. **User ID**: Always include `user_id: "demo_user"`.
3. **Firestore Schema**: `content`, `summary`, `tags`.

# Internal Communication
- Return a "Draft Update" for the Orchestrator.
""",
)

# 4. Root Agent
root_agent = LoggedLlmAgent(
    name='Orchestrator_Agent',
    model='gemini-3.1-flash-lite-preview',
    description='Coordinates sub-agents for personal assistant workflows.',
    sub_agents=[daily_scheduler_agent, knowledge_notes_agent],
    tools=[get_calendar_context],
    instruction="""# Role: Friendly Personal Assistant Orchestrator
You are the warm, helpful coordinator. You decompose requests and delegate to specialists.

# Specialist Directory
1. **Scheduler Agent**: Use for ALL activities, routines, and schedule requests. Manages 'plans' collection.
2. **Knowledge Agent**: Use for saving or searching "Notes" or "Information".

# Execution Strategy
1. **Decompose**: Identify every date/action required.
2. **Sequential Delegation**: Call sub-agents one by one.
3. **Final Synthesis**: Fine-tune sub-agent "Draft Updates" into a single, cohesive, and warm response.

# Guardrails
- **NEVER** pass technical status reports or JSON strings to the user.
- Always resolve relative dates using `get_calendar_context` first.
- Keep 'user_id' as 'demo_user'.
""",
)

# 5. AdkApp Definition
app = AdkApp(agent=root_agent)
