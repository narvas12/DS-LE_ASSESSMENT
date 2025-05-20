from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from services.bot_service import create_dca_bot

app = FastAPI(
    title="3Commas Bot API",
    description="API for managing 3Commas trading bots",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-bot")
async def create_bot(
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
    result = create_dca_bot(
        account_id=account_id,
        pair=pair,
        name=name,
        base_order_volume=base_order_volume,
        safety_order_volume=safety_order_volume,
        take_profit=take_profit,
        max_safety_orders=max_safety_orders,
        active_safety_orders_count=active_safety_orders_count,
        strategy=strategy
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Failed to create bot",
                "error": result["error"],
                "details": result.get("details")
            }
        )
    
    return {"success": True, "data": result}