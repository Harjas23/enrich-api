from fastapi import FastAPI, Query, Body
from typing import Optional, Dict, Any
import asyncio
from enrich import enrich_people  # your fuzzy match function

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.api_route("/skills/enrich_people", methods=["GET", "POST"])
async def enrich_people(
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    address: Optional[str] = Query(None),
    body: Optional[Dict[str, Any]] = Body(default=None, embed=True)  # <-- embed=True
):
    try:
        # body is now a proper dict
        if body:
            name = body.get("name", name)
            email = body.get("email", email)
            address = body.get("address", address)

        # call enrich logic
        result = enrich_people(name=name, email=email, address=address)
        if asyncio.iscoroutine(result):
            result = await result

        # ensure JSON serializable
        if not isinstance(result, (dict, list)):
            try:
                result = dict(result)
            except Exception:
                result = {"value": result}

        return {
            "input": {
                "name": name,
                "email": email,
                "address": address
            },
            "match": result
        }

    except Exception as e:
        return {
            "input": {
                "name": name,
                "email": email,
                "address": address
            },
            "error": str(e)
        }