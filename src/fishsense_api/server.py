"""FishSense API Server"""

from fastapi import FastAPI

from fishsense_api.__version__ import __version__

app = FastAPI(version=__version__)


@app.get("/")
def home():
    """Home endpoint providing basic API information."""

    return {
        "message": "Welcome to the FishSense API!",
        "docs": "/docs",
        "version": __version__,
    }
