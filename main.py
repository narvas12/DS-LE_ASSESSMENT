from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from services.bot_service import create_dca_bot

app = FastAPI(
    title="3Commas Bot API",
    description="API for managing 3Commas trading bots",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "active", "service": "3Commas Bot API"}

@app.post("/create-bot")
async def create_bot(
    account_id: int = Query(..., description="3Commas account ID"),
    pair: str = Query(..., description="Trading pair (format: BTC_USDT)"),
    name: str = Query("My DCA Bot", description="Bot name"),
    base_order_volume: float = Query(10, description="Base order size in quote currency"),
    safety_order_volume: float = Query(20, description="Safety order size in quote currency"),
    take_profit: float = Query(2, description="Take profit percentage"),
    max_safety_orders: int = Query(3, description="Maximum safety orders"),
    active_safety_orders_count: int = Query(1, description="Active safety orders count"),
    strategy: str = Query("manual", description="Trading strategy")
):
    """
    Create a new DCA bot with the specified parameters.
    
    All parameters are passed as query parameters.
    Example: /create-bot?account_id=123&pair=BTC_USDT&name=MyBot
    """
    try:
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
                    "details": result.get("details", "No additional details")
                }
            )
        
        return {
            "success": True,
            "data": result,
            "message": "Bot created successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Unexpected error occurred",
                "error": str(e)
            }
        )