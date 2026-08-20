import os
import google.auth
import vertexai

_, project_id = google.auth.default()
if not project_id or project_id == "cloudshell-gca":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-03-ef713aa8c2c9")

location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

print(f"Creating Memory Bank in project: {project_id}, location: {location}...")

client = vertexai.Client(project=project_id, location=location)

# Create a Memory Bank instance (an Agent Engine instance configured for memory)
memory_bank = client.agent_engines.create()

resource_name = memory_bank.api_resource.name
memory_bank_id = resource_name.split("/")[-1]

print("==========================================")
print("SUCCESSFULLY CREATED MEMORY BANK INSTANCE!")
print("MEMORY_BANK_ID:", memory_bank_id)
print("RESOURCE_NAME:", resource_name)
print("==========================================")

# Write MEMORY_BANK_ID to .env file for local usage
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
with open(env_path, "a") as f:
    f.write(f"\nMEMORY_BANK_ID={memory_bank_id}\n")
    f.write(f"GOOGLE_CLOUD_LOCATION={location}\n")
