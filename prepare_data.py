import pandas as pd
import sqlite3


# Read data
df = pd.read_excel("Online Retail.xlsx")


# Make invoice numbers text
df["InvoiceNo"] = df["InvoiceNo"].astype(str)


# Find return records
returns = df[
    (
        df["InvoiceNo"].str.startswith("C")
    )
    | (df["Quantity"] < 0)
].copy()


# Fill missing data
returns["Description"] = returns["Description"].fillna(
    "Unknown product"
)

returns["CustomerID"] = returns["CustomerID"].fillna(
    "Unknown customer"
)


# Reset row numbers
returns = returns.reset_index(drop=True)


# Calculate return quantity
returns["ReturnQty"] = returns["Quantity"].abs()


# Calculate return value
returns["ReturnValue"] = (
    returns["ReturnQty"] * returns["UnitPrice"]
)


# Create case IDs
returns["CaseID"] = [
    "Case" + str(i).zfill(5)
    for i in range(1, len(returns) + 1)
]


# Set case type
returns["CaseType"] = "RMA"

returns.loc[
    returns.index % 5 == 0,
    "CaseType"
] = "RTV"


# Set case status
returns["Status"] = "Open"

returns.loc[
    returns.index % 3 == 0,
    "Status"
] = "In Progress"

returns.loc[
    returns.index % 7 == 0,
    "Status"
] = "Closed"


# Add case fields
returns["Priority"] = "Medium"
returns["Reason"] = "Product return"

returns["ProcessingDays"] = (
    returns.index % 15
) + 1


# Save clean data
returns.to_csv(
    "rma_rtv_cases.csv",
    index=False
)


# Open database
conn = sqlite3.connect("rma_rtv.db")


# Save data to SQLite
returns.to_sql(
    "cases",
    conn,
    if_exists="replace",
    index=False
)


# Count cases by status
status_query = """
SELECT
    Status,
    COUNT(*) AS CaseCount
FROM cases
GROUP BY Status;
"""

status_summary = pd.read_sql_query(
    status_query,
    conn
)

print("Case Status Summary:")
print(status_summary)


# Count cases by type
case_type_query = """
SELECT
    CaseType,
    COUNT(*) AS CaseCount,
    SUM(ReturnValue) AS TotalReturnValue
FROM cases
GROUP BY CaseType;
"""

case_type_summary = pd.read_sql_query(
    case_type_query,
    conn
)

print("\nCase Type Summary:")
print(case_type_summary)


# Check database tables
tables = conn.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
    """
).fetchall()

print("\nDatabase Tables:")
print(tables)


# Close database
conn.close()

print("\nData preparation completed.")