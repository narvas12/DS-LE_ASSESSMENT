import requests
from typing import Dict, Any, Optional
from utils.config import API_KEY, BASE_URL
from utils.signer import create_signature_hmac

def make_api_request(
    method: str,
    endpoint: str,
    payload: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"

    headers = {
        "APIKEY": API_KEY,
        "Signature": create_signature_hmac(method, endpoint, payload),
        "Content-Type": "application/json"
    }

    try:
    response = requests.request(
        method,
        url,
        json=payload,
        headers=headers,
        timeout=10
    )

    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Text:", response.text)  # Add this for debugging

    response.raise_for_status()

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "message": "API responded with non-JSON",
            "error": "Non-JSON response",
            "details": response.text
        }



def change_mode(mode: str = "paper") -> Dict[str, Any]:
    endpoint = f"/ver1/users/change_mode?mode={mode}"
    return make_api_request("POST", endpoint)

def create_dca_bot(
    account_id: int,
    pair: str,
    name: str = "My DCA Bot",
    base_order_volume: float = 10,
    safety_order_volume: float = 20,
    take_profit: float = 2,
    max_safety_orders: int = 3,
    active_safety_orders_count: int = 1,
    strategy: str = "manual"
) -> Dict[str, Any]:
    endpoint = "/ver1/bots/create_bot"

    payload = {
        "account_id": account_id,
        "name": name,
        "pairs": [pair], 
        "base_order_volume": base_order_volume,
        "base_order_volume_type": "quote_currency",
        "take_profit": take_profit,
        "take_profit_type": "total",
        "strategy_list": [{"strategy": strategy}],
        "safety_order_step_percentage": 1.5,
        "safety_order_volume": safety_order_volume,
        "safety_order_volume_type": "quote_currency",
        "max_safety_orders": max_safety_orders,
        "active_safety_orders_count": active_safety_orders_count,
        "martingale_volume_coefficient": 1.5,
        "martingale_step_coefficient": 1.2,
        "risk_reduction_percentage": "0",
        "stop_loss_percentage": "0",
        "stop_loss_type": "stop_loss",
        "profit_currency": "quote_currency",
        "start_order_type": "limit",
        "leverage_type": "not_specified"
    }

    return make_api_request("POST", endpoint, payload)
