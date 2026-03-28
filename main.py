from fastapi import FastAPI, Query, Body
from typing import Optional, Dict, Any

from enrich import enrich_people  # your fuzzy match function

app = FastAPI(
    title="Enrichment API",
    description="People enrichment using fuzzy matching",
    version="1.0"
)

# health check (required for Render + debugging)
@app.get("/health")
def health():
    return {"status": "ok"}


# skill endpoint (Claude compatible)
@app.api_route("/skills/enrich_people", methods=["GET", "POST"])
async def enrich_people(
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    body: Optional[Dict[str, Any]] = Body(None)
):

    # if JSON body provided (POST), override query params
    if body:
        name = body.get("name", name)
        email = body.get("email", email)
        address = body.get("address", address)

    # call enrichment logic
    result = enrich_people(
        name=name,
        email=email,
        address=address
    )

    return {
        "input": {
            "name": name,
            "email": email,
            "address": address
        },
        "match": result
    }