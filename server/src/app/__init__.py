from azure.functions import AsgiMiddleware

from app.main import app  # Import your FastAPI app

# Wrap the FastAPI app in AsgiMiddleware for Azure Functions
main = AsgiMiddleware(app)
