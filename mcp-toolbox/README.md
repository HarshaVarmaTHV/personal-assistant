# MCP Toolbox - Installation

mkdir mcp-toolbox

cd mcp-toolbox

export VERSION=0.23.0
curl -O https://storage.googleapis.com/genai-toolbox/v$VERSION/linux/amd64/toolbox
chmod +x toolbox


# Firestore MCP Toolbox - Deployment Guide

This project contains a Model Context Protocol (MCP) toolset configured to interact with Google Cloud Firestore. It uses the `mcp-toolbox` to expose Firestore operations as tools for AI agents.

## Project Structure

- `toolbox`: The `mcp-toolbox` binary.
- `tools.yaml`: Configuration file defining Firestore sources and tools.
- `readme.txt`: Quick start for local execution.

## Configuration (`tools.yaml`)

The `tools.yaml` file is configured with:
- **Project ID**: `harshavarmathv`
- **Database**: `personal-assistant`
- **Toolset**: `firestore_full_access` (includes CRUD operations and collection queries).

## Local Execution

To run the toolbox locally with a UI for testing:
```bash
./toolbox --tools-file "tools.yaml" --ui
```

---

## Deployment to Google Cloud

Based on the [MCP Toolbox Cloud Run Guide](https://mcp-toolbox.dev/documentation/deploy-to/cloud-run/), the following steps were used to deploy this toolset.

### 1. Prerequisites
- Google Cloud CLI installed and initialized (`gcloud init`).
- APIs enabled: `run.googleapis.com`, `cloudbuild.googleapis.com`, `secretmanager.googleapis.com`.

### 2. Service Account & Permissions
Create a service account for the toolbox to run as:
```bash
gcloud iam service-accounts create toolbox-identity
```

Grant it permissions to access Firestore and Secret Manager:
```bash
# For Firestore access
gcloud projects add-iam-policy-binding harshavarmathv \
    --member="serviceAccount:toolbox-identity@harshavarmathv.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

# For reading the configuration secret
gcloud projects add-iam-policy-binding harshavarmathv \
    --member="serviceAccount:toolbox-identity@harshavarmathv.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### 3. Store Configuration in Secret Manager
Upload your `tools.yaml` to Secret Manager so it can be securely mounted in the cloud environment:
```bash
gcloud secrets create mcp-tools-config --data-file=tools.yaml
```

### 4. Deployment

####  Deploy to Cloud Run (Recommended)
```bash
gcloud run deploy firestore-mcp-toolbox \
    --image us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest \
    --service-account toolbox-identity@harshavarmathv.iam.gserviceaccount.com \
    --set-secrets "/app/tools.yaml=mcp-tools-config:latest" \
    --args="--config=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
    --region us-central1 \
    --allow-unauthenticated
```

### 5. Accessing the Tools
Once deployed, the service URL can be used by an MCP-compatible client (like Claude Desktop or a custom agent) to interact with your Firestore database.
