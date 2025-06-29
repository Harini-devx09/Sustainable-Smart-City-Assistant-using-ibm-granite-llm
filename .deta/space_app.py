import sys
import os
from Project_Files.main import app  # this should point to your FastAPI app

# Required for Deta Space to run your FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

