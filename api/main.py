"""
FastAPI Main Application Module
Entry point for the GWC-SIEM REST API
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="GWC-SIEM API",
    description="Security Information and Event Management System API",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "GWC-SIEM API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200, content={"status": "healthy", "service": "gwc-siem-api"}
    )


def start_server():
    """Entry point for console script"""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_server()
