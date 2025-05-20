import hmac
import hashlib
import json
import os
from typing import Dict, Any, Optional

from utils.config import API_SECRET

def create_signature_hmac(method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate HMAC-SHA256 signature required by 3Commas API.
    Signature = HMAC_SHA256(secret, method + /public/api + endpoint + json_string)
    """

    # Full path must start with /public/api
    path = f"/public/api{endpoint}"

    if payload:
        # Ensure alphabetically sorted keys and no spaces
        payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    else:
        payload_str = ""

    string_to_sign = f"{method.upper()}{path}{payload_str}"

    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature

