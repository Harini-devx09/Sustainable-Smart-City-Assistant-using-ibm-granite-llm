import os
from dotenv import load_dotenv
load_dotenv(override=True)  # ensure vars overwrite anything missing

import uvicorn

if __name__ == "__main__":
    print("✅ LOADED ENV VARS:")
    print("WATSONX_API_KEY:", os.getenv("WATSONX_API_KEY"))
    print("WATSONXAPIKEY:", os.getenv("WATSONXAPIKEY"))

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False  # disable subprocess
    )
