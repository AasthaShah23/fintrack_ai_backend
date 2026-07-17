from pydantic import BaseModel
from app.schemas.category_schema import CategoryResponse
class CreateBudgetRequest(BaseModel):
    budget: float

    model_config = {
        "from_attributes": True
    }

class BudgetResponse(BaseModel):
    id: int
    monthly_budget: int

    class Config:
        from_attributes = True

class GetBudgetResponse(BaseModel):
    id: int
    monthly_budget: float
    category: CategoryResponse

    model_config = {
        "from_attributes": True
    }