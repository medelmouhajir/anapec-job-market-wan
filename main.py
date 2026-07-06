import os
import yaml
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import jwt
from typing import Optional

from scraper import scrape_anapec

app = FastAPI(title="ANAPEC Job Market Scraper API")

# Read manifest on startup
with open("isli-skill.yaml", "r", encoding="utf-8") as f:
    manifest = yaml.safe_load(f)

class ScrapeRequest(BaseModel):
    keyword: Optional[str] = None
    region: Optional[str] = None
    sector: Optional[str] = None
    contract_type: Optional[str] = None
    limit: Optional[int] = 50

def verify_jwt(x_internal_auth: str = Header(...)):
    """
    Middleware dependency to verify the ISLI Core JWT.
    """
    secret = os.environ.get("JWT_SECRET")
    if not secret:
        # If secret is not configured, we might be in dev mode, but strictly we should fail.
        # For ISLI v2.0, JWT_SECRET must be present.
        raise HTTPException(status_code=500, detail="JWT_SECRET environment variable not set")
    
    try:
        # We verify the token. The algorithm is typically HS256.
        decoded = jwt.decode(x_internal_auth, secret, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/.well-known/isli-manifest")
def get_manifest():
    return manifest

@app.post("/scrape-jobs")
def api_scrape_jobs(request: ScrapeRequest, token: dict = Depends(verify_jwt)):
    """
    Executes the scraping logic.
    Requires X-Internal-Auth header to be verified.
    """
    try:
        jobs = scrape_anapec(
            keyword=request.keyword,
            region=request.region,
            sector=request.sector,
            contract_type=request.contract_type,
            limit=request.limit
        )
        return {"status": "success", "data": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
