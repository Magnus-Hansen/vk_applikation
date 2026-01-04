"""Hovedprogrammet."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router as all_routers

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(all_routers)
