import json
import pandas as pd
from config import *
import re
import json
import pandas as pd


def safe_json_parse(response_str: str) -> dict:
    """
    Parses model output that may include markdown-style code fences or extra escape characters.
    Returns a dictionary with disney_movie, concise_reasoning, and es_LA.
    """
    # Step 1: Remove Markdown-style code fences
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", response_str.strip(), flags=re.IGNORECASE)

    # Step 2: Fix overly escaped quotes if needed (optional for extra safety)
    if isinstance(cleaned, str):
        cleaned = cleaned.replace('\\"', '"')  # unescape any escaped quotes
        cleaned = cleaned.replace("\\'", "'")  # unescape any single quotes

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return None
