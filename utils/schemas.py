from pydantic import BaseModel

class BotCreateRequest(BaseModel):
    account_id: int
    pair: str
    name: str = "My DCA Bot"
    base_order_volume: float = 10
    safety_order_volume: float = 20
    take_profit: float = 2
    max_safety_orders: int = 3
    active_safety_orders_count: int = 1
    strategy: str = "manual"
    mode: str = "paper"
