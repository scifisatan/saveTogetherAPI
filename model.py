from pydantic import BaseModel

class InsertSaving(BaseModel):
    amount: int

class InsertExpense(BaseModel):
    amount: int
    description: str
    tag: str | None
    
class Expense(BaseModel):
    date: str
    amount: int
    description: str
    tag: str | None

class Saving(BaseModel):
    date: str
    amount: int

class Duo(BaseModel):
    id: int
    startDate: str