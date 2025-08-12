import os
from django.shortcuts import render
from .models import Expense, Income
from django.shortcuts import render, redirect
from .forms import TransactionForm
from .utils.csv_manager import CSVManager, FORMAT
from finance.utils import csv_manager
from datetime import datetime
import pandas as pd
from django.contrib import messages
# from django.http import FileResponse, Http404
from django.conf import settings
from datetime import datetime
import csv
from django.http import HttpResponse


#! finance/views.py

def balance_view(request):
    CSVManager.initialize_csv()

    try:
        df = pd.read_csv(csv_manager.CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=["date", "amount", "category", "description"])

    if not df.empty:
        df["amount"] = df["amount"].astype(float)
        df["date"] = pd.to_datetime(df["date"], errors='coerce')

        # Separate expenses and incomes as lists of dicts for template iteration
        expenses_df = df[df["category"] == "Expense"]
        incomes_df = df[df["category"] == "Income"]

        total_income = incomes_df["amount"].sum()
        total_expense = expenses_df["amount"].sum()
        balance = total_income - total_expense

        expenses = expenses_df.to_dict(orient="records")
        incomes = incomes_df.to_dict(orient="records")
    else:
        total_income = total_expense = balance = 0
        expenses = []
        incomes = []

    context = {
        "expenses": expenses,
        "incomes": incomes,
        # total sum of incomes (optional for display)
        "income": total_income,
        "expenses_total": total_expense,  # total sum of expenses (optional)
        "balance": balance,
    }

    return render(request, "index.html", context)


def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"] or datetime.today()
            CSVManager.initialize_csv()
            CSVManager.add_entry(
                date.strftime(FORMAT),
                form.cleaned_data["amount"],
                form.cleaned_data["category"],
                form.cleaned_data["description"]
            )

            # ? Store just-added transaction in session
            request.session["last_transaction"] = {
                "date": date.strftime(FORMAT),
                "amount": form.cleaned_data["amount"],
                "category": form.cleaned_data["category"],
                "description": form.cleaned_data["description"]
            }

            messages.success(request, "Transaction added.")
            return redirect("add_transaction")
    else:
        form = TransactionForm()

     # * Retrieve last transaction if present
    last_transaction = request.session.pop("last_transaction", None)

    return render(request, "add_transaction.html", {"form": form,  "last_transaction": last_transaction})


def view_summary(request):
    transactions = None
    summary = {}

    if request.method == "POST":
        raw_start_date = request.POST.get("start_date")
        raw_end_date = request.POST.get("end_date")

        if raw_start_date and raw_end_date:
            try:
                # Change this format if needed
                # start_date = datetime.strptime(raw_start_date, "%Y-%m-%d")
                # end_date = datetime.strptime(raw_end_date, "%Y-%m-%d")

                df = CSVManager.get_transactions(raw_start_date, raw_end_date)
                transactions = df.to_dict("records")

                total_income = df[df["category"] == "Income"]["amount"].sum()
                total_expense = df[df["category"] == "Expense"]["amount"].sum()

                summary = {
                    "total_income": total_income,
                    "total_expense": total_expense,
                    "net_savings": total_income - total_expense,
                }
            except ValueError as e:
                # Optional: add error logging or pass an error message to template
                print(f"[ERROR] Invalid date format: {e}")

    return render(request, "view_summary.html", {"transactions": transactions, "summary": summary})


def transaction_chart(request):
    # Example: replace with your actual data source
    csv_path = os.path.join(settings.BASE_DIR, 'finance',
                            'data', 'finance_data.csv')
    df = pd.read_csv(csv_path)
    # df = pd.read_csv("/data/finance_data.csv")  # or fetch from DB
    chart = CSVManager.plot_transactions(df)
    return render(request, "chart.html", {"chart": chart})


#! download file
def download_financial_data(request):
    CSVManager.initialize_csv()

    try:
        df = pd.read_csv(csv_manager.CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "amount", "category", "description"])

    # Ensure correct data types
    if not df.empty:
        df["amount"] = df["amount"].astype(float)
        df["date"] = pd.to_datetime(df["date"], errors='coerce')

    # Prepare HTTP response for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="finance_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Amount', 'Category', 'Description'])  # Header row

    for _, row in df.iterrows():
        writer.writerow([
            row["date"].strftime("%Y-%m-%d") if not pd.isnull(row["date"]) else "",
            row["amount"],
            row["category"],
            row["description"]
        ])

    return response
# def download_financial_data(request):
#     CSVManager.initialize_csv()

#     try:
#         df = pd.read_csv(csv_manager.CSV_FILE)
#     except FileNotFoundError:
#         df = pd.DataFrame(
#             columns=["date", "amount", "category", "description"])

#     # Prepare HTTP response for CSV download
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="finance_data.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Date', 'Amount', 'Category', 'Description'])  # Header

#     for _, row in df.iterrows():
#         writer.writerow([
#             row['date'],
#             row['amount'],
#             row['category'],
#             row['description']
#         ])

#     return response
