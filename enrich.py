from supabase import create_client
from dotenv import load_dotenv 
import os
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def enrich_people(
    name=None,
    email=None,
    address=None,
    min_score=0.45   # tune threshold
):

    response = supabase.rpc(
        "match_people",
        {
            "query_name": name,
            "query_email": email,
            "query_address": address,
            "min_score": min_score,
            "match_limit": 3
        }
    ).execute()

    results = response.data

    if not results:
        return None

    top_match = results[0]

    # optional confidence gate
    if top_match["final_score"] < min_score:
        return None

    return {
        "match_found": True,

        "confidence": round(top_match["final_score"], 3),

        "person": {
            "id": top_match["id"],
            "name": top_match["name"],
            "company": top_match["company"],
            "title": top_match["title"],
            "email": top_match["email"],
            "phone": top_match["phone"],
            "address": top_match["address"],
            "linkedin": top_match["linkedin"],
            "industry": top_match["industry"]
        }
    } 