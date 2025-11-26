import json
import os

from src.api.main import app

"""
Utility script to regenerate the OpenAPI schema based on the current FastAPI app.
Writes to interfaces/openapi.json so other containers (e.g., frontend) can consume it.
"""

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
