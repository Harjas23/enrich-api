from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from enrich import enrich_people

app = FastAPI(
    title="Enrichment API",
    description="Fuzzy people enrichment via Supabase",
    version="1.0"
)


class EnrichRequest(BaseModel):

    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

@app.get("/health")
def health():

    return {"status": "ok"}
@app.post("/skills/enrich_people")

def enrich_endpoint(req: EnrichRequest):

    result = enrich_people(

        name=req.name,
        email=req.email,
        address=req.address
    )

    return {

        "success": True,

        "result": result
    }