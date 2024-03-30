import os
import pytz
import uvicorn
from model import *
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from supabase import create_client, Client
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

load_dotenv("./.env")
url: str = os.environ.get("DB_URL")
key: str = os.environ.get("DB_KEY")
supabase: Client = create_client(url, key)

nepal_tz = pytz.timezone("Asia/Kathmandu")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/expenses")
def getExpenses() -> List[Expense]:
    expenses = supabase.table("Expenses").select("*").execute()
    return JSONResponse(content=jsonable_encoder(expenses.data))


@app.get("/savings")
def getSavings() -> List[Saving]:
    savings = supabase.table("Savings").select("*").execute()
    return JSONResponse(content=jsonable_encoder(savings.data))


@app.get("/totalamount")
def getTotalAmount() -> int:
    expenses = supabase.table("Expenses").select("amount").execute()
    totalexpense = sum([expense["amount"] for expense in expenses.data])
    savings = supabase.table("Savings").select("amount").execute()
    totalsavings = sum([saving["amount"] for saving in savings.data])
    return JSONResponse(content={"total": totalsavings - totalexpense})


@app.post("/expenses")
def addExpense(expense: InsertExpense) -> Expense:
    """
    Add an expense to the database
    Expense:
    - amount: int
    - description: str
    - tag: str
    """

    # gmt Asia/Kathmandu
    date = datetime.now(nepal_tz).strftime("%Y-%m-%d %H:%M:%S")
    tempExpense = Expense(
        date=date,
        amount=expense.amount,
        description=expense.description,
        tag=expense.tag,
    )
    try:
        result = supabase.table("Expenses").insert(tempExpense.model_dump()).execute()
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

    return JSONResponse(content=jsonable_encoder(result.data))


@app.post("/savings")
def addSaving(saving: InsertSaving) -> Saving:
    """
    Add a saving to the database
    Saving:
    - amount: int (amount saved individually)
    """
    date = datetime.now(nepal_tz).strftime("%Y-%m-%d %H:%M:%S")
    tempSaving = Saving(
        date=date,
        amount=saving.amount,
    )
    try:
        result = supabase.table("Savings").insert(tempSaving.model_dump()).execute()
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    return JSONResponse(content=jsonable_encoder(result.data))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
