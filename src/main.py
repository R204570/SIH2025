"""
Main application entry point
"""
import uvicorn
from src.api import app
from src.config import settings

def main():
    """Run the application"""
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=4
    )

if __name__ == "__main__":
    main()
