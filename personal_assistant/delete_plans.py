from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client(project="harshavarmathv", database="personal-assistant")

def delete_collection(coll_ref, batch_size=100):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f"Deleting doc {doc.id}...")
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

if __name__ == "__main__":
    print("🗑️  Deleting all documents in 'plans' collection...")
    plans_ref = db.collection("plans")
    delete_collection(plans_ref)
    print("✅ 'plans' collection cleared.")
