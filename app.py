from flask import Flask, render_template, request, redirect
import csv
import os
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "budget.csv"

def init_csv():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Type", "Category", "Amount"])

def read_data():
    with open(DATA_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def add_transaction(t_type, category, amount):
    date = datetime.today().strftime("%Y-%m-%d")
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, t_type, category, amount])

@app.route("/", methods=["GET", "POST"])
def index():
    init_csv()
    if request.method == "POST":
        t_type = request.form["type"]
        category = request.form["category"]
        amount = request.form["amount"]
        add_transaction(t_type, category, amount)
        return redirect("/")

    data = read_data()

    pie_data = defaultdict(float)
    bar_data = defaultdict(float)

    for row in data:
        if row["Type"] == "expense":
            pie_data[row["Category"]] += float(row["Amount"])
        if row["Type"] == "expense":
            month = row["Date"][:7]
            bar_data[month] += float(row["Amount"])

    return render_template("index.html",
                           pie_labels=list(pie_data.keys()),
                           pie_values=list(pie_data.values()),
                           bar_labels=list(bar_data.keys()),
                           bar_values=list(bar_data.values()))

if __name__ == "__main__":
    app.run(debug=True)
