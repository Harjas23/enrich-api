from fastapi import FastAPI, Query, Body
from typing import Optional, Dict, Any
import asyncio
from enrich import enrich_people

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.api_route("/skills/enrich_people", methods=["GET", "POST"])
async def enrich_people(
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    body: Optional[Dict[str, Any]] = Body(default=None)  # note: default=None
):

    # FastAPI passes JSON body as dict automatically if type=Dict
    if body:
        name = body.get("name", name)
        email = body.get("email", email)
        address = body.get("address", address)

    # handle async or sync enrich logic
    result = enrich_people(name=name, email=email, address=address)
    if asyncio.iscoroutine(result):
        result = await result

    return {
        "input": {
            "name": name,
            "email": email,
            "address": address
        },
        "match": result
    }