from fastapi import FastAPI, Request, Query
from typing import Optional, Dict, Any
import asyncio
from enrich import enrich_people_logic  # your existing fuzzy match function

app = FastAPI(title="Enrichment API", version="1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.api_route("/skills/enrich_people", methods=["GET", "POST"])
async def enrich_people(
    request: Request,
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    address: Optional[str] = Query(None)
):
    """
    Supports both GET (query params) and POST (JSON body).
    Returns top fuzzy match only.
    """
    try:
        # --- 1. Read POST JSON body if present ---
        if request.method == "POST":
            try:
                body = await request.json()
                if isinstance(body, dict):
                    name = body.get("name", name)
                    email = body.get("email", email)
                    address = body.get("address", address)
            except Exception:
                # no JSON or invalid, fall back to query params
                pass

        # --- 2. Call enrichment logic ---
        result = enrich_people_logic(name=name, email=email, address=address)

        # support async logic
        if asyncio.iscoroutine(result):
            result = await result

        # --- 3. Ensure JSON serializable ---
        if result is None:
            result = {}
        elif not isinstance(result, (dict, list)):
            try:
                result = dict(result)
            except Exception:
                result = {"value": result}

        # --- 4. Return structured response ---
        return {
            "input": {
                "name": name,
                "email": email,
                "address": address
            },
            "match": result
        }

    except Exception as e:
        # Catch-all for debugging
        return {
            "input": {
                "name": name,
                "email": email,
                "address": address
            },
            "error": str(e)
        }