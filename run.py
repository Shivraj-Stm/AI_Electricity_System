import uvicorn
import webbrowser
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.main import app

# Get base directory (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Mount frontend folder
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

# Root URL loads dashboard.html
@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8000")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)