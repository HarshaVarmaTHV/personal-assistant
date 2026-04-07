from google.cloud import firestore
from datetime import datetime

# Initialize Firestore client
db = firestore.Client(project="harshavarmathv",database="personal-assistant")

# Common user_id for hackathon
USER_ID = "demo_user"

# ---------------------------
# USERS COLLECTION
# ---------------------------
def create_users():
    users_ref = db.collection("users").document(USER_ID)
    users_ref.set({
        "user_id": USER_ID,
        "name": "Demo User",
        "created_at": datetime.utcnow()
    })
    print("✅ users collection initialized")


# ---------------------------
# NOTES COLLECTION
# ---------------------------
def create_notes():
    notes = [
        {
            "content": "Discussed claim settlement with broker",
            "summary": "Meeting about claim settlement",
            "tags": ["insurance", "meeting"]
        },
        {
            "content": "Need to optimize claim processing pipeline",
            "summary": "Improve pipeline efficiency",
            "tags": ["work", "tech"]
        }
    ]

    for note in notes:
        db.collection("notes").add({
            "user_id": USER_ID,
            **note,
            "created_at": datetime.utcnow()
        })

    print("✅ notes collection initialized")


# ---------------------------
# PLANS COLLECTION
# ---------------------------
def create_plans():
    db.collection("plans").add({
        "user_id": USER_ID,
        "date": "2026-04-05",
        "schedule": [
            {"time": "07:00", "task": "Go to gym"},
            {"time": "18:00", "task": "Finish report"}
        ],
        "created_at": datetime.utcnow()
    })

    print("✅ plans collection initialized")


# ---------------------------
# AGENT LOGS COLLECTION
# ---------------------------
def create_agent_logs():
    db.collection("agent_logs").add({
        "user_id": USER_ID,
        "agent": "planner_agent",
        "action": "generated_plan",
        "input": "Plan my day",
        "output": "Generated schedule",
        "timestamp": datetime.utcnow()
    })

    print("✅ agent_logs collection initialized")


# ---------------------------
# MAIN EXECUTION
# ---------------------------
if __name__ == "__main__":
    print("🚀 Initializing Firestore collections...")

    create_users()
    create_notes()
    create_plans()
    create_agent_logs()

    print("🎉 All collections created successfully!")