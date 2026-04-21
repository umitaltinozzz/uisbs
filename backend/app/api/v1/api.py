"""
Main API router for UISBS v1 endpoints.
Combines all API routes into a single router.
"""

from fastapi import APIRouter

from .endpoints import auth, users, pharmacies, drugs, stocks, search, admin

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(pharmacies.router, prefix="/pharmacies", tags=["Pharmacies"])
api_router.include_router(drugs.router, prefix="/drugs", tags=["Drugs"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["Drug Stocks"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administration"]) 