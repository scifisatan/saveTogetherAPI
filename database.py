from supabase import create_client, Client
from typing import Optional


class Database:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def get_expenses(self) -> Optional[list]:
        response = self.supabase.table("Expenses").select("*").execute()

        return response.data

    def get_savings(self) -> Optional[list]:
        response = self.supabase.table("Savings").select("*").execute()
        return response.data

    def get_total_amount(self) -> Optional[int]:
        expenses = self.supabase.table("Expenses").select("amount").execute()
        totalexpense = sum([expense["amount"] for expense in expenses.data])
        savings = self.supabase.table("Savings").select("amount").execute()
        totalsavings = sum([saving["amount"] for saving in savings.data])
        response = totalsavings - totalexpense
        return response

    def insert_expense(self, expense: dict) -> Optional[dict]:
        response = self.supabase.table("Expenses").insert(expense).execute()
        return response.data

    def insert_saving(self, saving: dict) -> Optional[dict]:
        response = self.supabase.table("Savings").insert(saving).execute()
        return response.data
