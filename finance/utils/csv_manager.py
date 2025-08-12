# finance/utils/csv_manager.py

import base64
import io
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from django.conf import settings
import os


# CSV_FILE = "/finance/data/finance_data.csv"
# Correct path construction
CSV_FILE = os.path.join(settings.BASE_DIR, 'finance',
                        'data', 'finance_data.csv')
COLUMNS = ["date", "amount", "category", "description"]
FORMAT = "%Y-%m-%d"


class CSVManager:
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
            writer.writerow(new_entry)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=FORMAT)
        start_date = datetime.strptime(start_date, FORMAT)
        end_date = datetime.strptime(end_date, FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        return filtered_df

    @staticmethod
    def plot_transactions(df):
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        income_df = (
            df[df["category"] == "Income"]
            .resample("D")
            .sum()
            .reindex(df.index, fill_value=0)
        )
        expense_df = (
            df[df["category"] == "Expense"]
            .resample("D")
            .sum()
            .reindex(df.index, fill_value=0)
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(income_df.index,
                income_df["amount"], label="Income", color="g")
        ax.plot(expense_df.index,
                expense_df["amount"], label="Expense", color="r")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount")
        ax.set_title("Income and Expenses Over Time")
        ax.legend()
        ax.grid(True)

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight")
        plt.close(fig)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode("utf-8")
        return graphic
