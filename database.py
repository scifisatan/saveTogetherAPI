from supabase import create_client, Client
from typing import Optional

class Database:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def get_expenses(self) -> Optional[list]:
        response = self.supabase.tabsupabase.table("Expenses").select("*").execute()
        if response.error:
            print(f"Error fetching expenses: {response.error}")
            return None
        return response.data

    def get_savings(self) -> Optional[list]:
        response = self.supabase.table("Savings").select("*").execute()
        if response.error:
            print(f"Error fetching savings: {response.error}")
            return None
        return response.data

    def get_total_amount(self) -> Optional[int]:
        expenses = self.supabase.table("Expenses").select("amount").execute()
        totalexpense = sum([expense["amount"] for expense in expenses.data])
        savings = self.supabase.table("Savings").select("amount").execute()
        response = sum([saving["amount"] for saving in savings.data])
        if response.error:
            print(f"Error fetching total amount: {response.error}")
            return None
        return sum(item["amount"] for item in response.data)
