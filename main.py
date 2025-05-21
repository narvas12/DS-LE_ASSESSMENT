from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.bot_service import create_dca_bot
from utils.schemas import BotCreateRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-bot")
async def create_bot(req: BotCreateRequest):
    result = create_dca_bot(
        account_id=req.account_id,
        pair=req.pair,
        name=req.name,
        base_order_volume=req.base_order_volume,
        safety_order_volume=req.safety_order_volume,
        take_profit=req.take_profit,
        max_safety_orders=req.max_safety_orders,
        active_safety_orders_count=req.active_safety_orders_count,
        strategy=req.strategy
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
