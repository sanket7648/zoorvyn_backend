from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, records, dashboard, users

app = FastAPI(
    title="Finance Dashboard API",
    description="Backend API for managing financial records and user roles.",
    version="1.0.0"
)

# Configure CORS (Important for frontend connectivity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api")
app.include_router(records.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Finance Dashboard API. Visit /docs for the API Swagger documentation."}