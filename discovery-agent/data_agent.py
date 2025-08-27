#!/usr/bin/env python3
"""
Banking Data Agent (synthetic) — DeepAgents + LangGraph

- Spin up in-memory DuckDB with synthetic banking data
- Tools:
  1) list_assets()       -> table of tables/columns
  2) sql(query, limit)   -> run safe SELECT; returns table artifact
  3) profile(table)      -> column stats; returns table artifact
  4) dq_check(rule, ...) -> simple DQ checks; returns table artifact

Artifacts follow LangChain “content_and_artifact” contract so UIs (e.g., deep-agents-ui)
can render results directly from LangGraph thread messages.

Requires:
  pip install deepagents duckdb pandas pyarrow "langchain-core>=0.2.19"
"""

from __future__ import annotations

import os
import re
import math
import json
import time
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional

import duckdb
import pandas as pd
from langchain_core.tools import tool
from deepagents import create_deep_agent 
from azure_openai_model import azure_openai_model

# -------------------------------
# Synthetic data generation
# -------------------------------

def _rng_choice(rng: random.Random, seq):
    return seq[rng.randrange(0, len(seq))]

def make_synthetic_banking(seed: int = 7,
                           n_customers: int = 500,
                           months: int = 12) -> dict[str, pd.DataFrame]:
    rng = random.Random(seed)

    # Customers
    cust_ids = [f"C{100000+i}" for i in range(n_customers)]
    segments = ["Mass", "Mass Affluent", "HNW", "SME"]
    ages = [rng.randint(19, 78) for _ in cust_ids]
    customers = pd.DataFrame({
        "customer_id": cust_ids,
        "name": [f"Cust {i}" for i in range(n_customers)],
        "age": ages,
        "segment": [ _rng_choice(rng, segments) for _ in cust_ids ],
        "kyc_status": [ _rng_choice(rng, ["complete", "partial", "missing"]) for _ in cust_ids ],
    })

    # Accounts (1–3 per customer)
    acct_rows = []
    acct_types = ["CHECKING", "SAVINGS", "CREDIT_CARD"]
    today = pd.Timestamp("2025-06-30")
    a_id = 200000
    for cid in cust_ids:
        for _ in range(1 + rng.randint(0, 2)):
            a_id += 1
            open_date = today - pd.Timedelta(days=rng.randint(30, 1200))
            acct_rows.append({
                "account_id": f"A{a_id}",
                "customer_id": cid,
                "account_type": _rng_choice(rng, acct_types),
                "open_date": open_date.date(),
                "balance": round(max(0.0, rng.gauss(3000, 2500)), 2),
                "credit_limit": round(max(0.0, rng.gauss(8000, 5000)), 2),
                "status": _rng_choice(rng, ["active", "blocked", "closed"])
            })
    accounts = pd.DataFrame(acct_rows)

    # Monthly transactions (random)
    start_month = (today - pd.DateOffset(months=months-1)).normalize() + pd.offsets.MonthBegin(0)
    months_list = pd.period_range(start=start_month, periods=months, freq="M")
    txn_rows = []
    for _, row in accounts.iterrows():
        # ~40–120 txns per account across months
        n_txn = rng.randint(40, 120)
        for _ in range(n_txn):
            month = _rng_choice(rng, months_list)
            # transactions around +/- 150 with some variability
            amt = rng.gauss(0, 150)
            # bias: more negative amounts (spend)
            if rng.random() < 0.6:
                amt = -abs(amt)
            else:
                amt = abs(amt)
            txn_rows.append({
                "txn_id": f"T{rng.randint(10_000_000, 99_999_999)}",
                "account_id": row["account_id"],
                "post_date": month.to_timestamp(how="end").date(),
                "merchant_category": _rng_choice(rng, ["GROCERY","DINING","TRAVEL","UTILITIES","RENT","FUEL","OTHER"]),
                "amount": round(amt, 2),
                "currency": "USD"
            })
    transactions = pd.DataFrame(txn_rows)

    # Loans (subset of customers)
    loan_rows = []
    for cid in rng.sample(cust_ids, k=max(50, n_customers // 5)):
        principal = round(max(1000, rng.gauss(9000, 6000)), 2)
        rate = round(max(1.5, rng.gauss(8.5, 3.0)), 2)
        term_m = _rng_choice(rng, [12, 24, 36, 48, 60])
        delinquent = _rng_choice(rng, [0, 0, 0, 1])  # ~25% chance
        loan_rows.append({
            "loan_id": f"L{rng.randint(10000,99999)}",
            "customer_id": cid,
            "principal": principal,
            "interest_rate_apr": rate,
            "term_months": term_m,
            "is_delinquent": delinquent,
            "start_date": (today - pd.DateOffset(months=rng.randint(1,60))).date()
        })
    loans = pd.DataFrame(loan_rows)

    # Cards (only for CREDIT_CARD accounts)
    card_rows = []
    for _, row in accounts[accounts["account_type"] == "CREDIT_CARD"].iterrows():
        limit = max(500, row["credit_limit"])
        utilization = max(0.0, min(0.98, abs(rng.gauss(0.35, 0.2))))
        outstanding = round(limit * utilization, 2)
        card_rows.append({
            "card_id": f"CC{rng.randint(100000,999999)}",
            "account_id": row["account_id"],
            "credit_limit": limit,
            "outstanding_balance": outstanding,
            "status": _rng_choice(rng, ["active","blocked","closed"]),
        })
    cards = pd.DataFrame(card_rows)

    return {
        "customers": customers,
        "accounts": accounts,
        "transactions": transactions,
        "loans": loans,
        "cards": cards,
    }

# -------------------------------
# Engine (DuckDB) bootstrap
# -------------------------------

@dataclass
class DataEnv:
    con: duckdb.DuckDBPyConnection

def init_env() -> DataEnv:
    con = duckdb.connect(database=":memory:")
    dfs = make_synthetic_banking()
    for name, df in dfs.items():
        con.register(name, df)   # virtual view pointing to pandas
        # also create a physical table to enable information_schema
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM {name}")
    return DataEnv(con=con)

ENV = init_env()

# -------------------------------
# Utilities
# -------------------------------

READ_ONLY = re.compile(r"^\s*select\b", re.IGNORECASE | re.DOTALL)

def _is_safe_select(sql: str) -> bool:
    return bool(READ_ONLY.match(sql)) and (";" not in sql)

def _to_rows(df: pd.DataFrame, max_rows: Optional[int] = None) -> List[Dict[str, Any]]:
    if max_rows is not None:
        df = df.head(max_rows)
    # ensure JSON-serializable (duckdb types -> py)
    return json.loads(df.to_json(orient="records", date_format="iso"))

def _schema(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    return con.execute("""
        SELECT table_name, column_name, data_type, ordinal_position
        FROM information_schema.columns
        WHERE table_schema = 'main'
        ORDER BY table_name, ordinal_position
    """).df()

# -------------------------------
# Tools (with artifacts)
# -------------------------------

@tool(response_format="content_and_artifact")
def list_assets() -> Tuple[str, Dict[str, Any]]:
    """List available datasets and columns in the in-memory banking catalog."""
    df = _schema(ENV.con)
    content = f"Found {df['table_name'].nunique()} tables and {len(df)} columns."
    artifact = {
        "type": "table.json",
        "title": "Catalog: Tables & Columns",
        "inline": {
            "data": _to_rows(df),
        },
        "limits": {"truncated": False}
    }
    return content, artifact

@tool(response_format="content_and_artifact")
def sql(query: str, limit: int = 1000) -> Tuple[str, Dict[str, Any]]:
    """Execute a safe SELECT query against the banking data (DuckDB)."""
    if not _is_safe_select(query):
        return (
            "Only read-only SELECT queries without semicolons are allowed.",
            {
                "type": "table.json",
                "title": "SQL Error",
                "inline": {"data": []},
                "limits": {"truncated": False, "note": "Unsafe or non-SELECT query."}
            },
        )

    # Inject LIMIT if caller didn't specify one explicitly (best-effort)
    q_norm = query.strip()
    if re.search(r"\blimit\s+\d+\b", q_norm, flags=re.IGNORECASE) is None:
        q_exec = f"SELECT * FROM ({q_norm}) AS t LIMIT {int(limit)}"
    else:
        q_exec = q_norm

    df = ENV.con.execute(q_exec).df()
    content = f"Returned {min(len(df), limit)} row(s) from query."
    artifact = {
        "type": "table.json",
        "title": "SQL result",
        "inline": {
            "data": _to_rows(df, max_rows=limit),
        },
        "limits": {"truncated": len(df) > limit, "row_cap": limit}
    }
    return content, artifact

@tool(response_format="content_and_artifact")
def profile(table: str) -> Tuple[str, Dict[str, Any]]:
    """Profile a table: dtype, nulls, distinct, min/max/mean (where applicable)."""
    # Validate table existence
    exists = ENV.con.execute(
        "SELECT COUNT(*) AS c FROM information_schema.tables WHERE table_name = ?",
        [table]
    ).fetchone()[0] > 0
    if not exists:
        return (f"Table '{table}' not found.",
                {"type":"table.json","title":"Profile Error","inline":{"data":[]}})

    cols = ENV.con.execute(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = ? ORDER BY ordinal_position",
        [table]
    ).df()

    rows = []
    for _, r in cols.iterrows():
        col = r["column_name"]
        dtype = r["data_type"]
        # compute stats safely
        q = f"""
        SELECT
          COUNT(*) AS row_count,
          SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) AS nulls,
          COUNT(DISTINCT {col}) AS distinct_count
        FROM {table}
        """
        stats = ENV.con.execute(q).df().iloc[0].to_dict()
        nulls = int(stats["nulls"])
        distinct_count = int(stats["distinct_count"])
        row_count = int(stats["row_count"])

        min_v = max_v = mean_v = None
        # only for numeric columns
        if dtype.lower() in ("integer", "bigint", "smallint", "tinyint", "hugeint", "double", "float", "real", "decimal"):
            qn = f"SELECT MIN({col}) AS min_v, MAX({col}) AS max_v, AVG(CAST({col} AS DOUBLE)) AS mean_v FROM {table}"
            nstats = ENV.con.execute(qn).df().iloc[0].to_dict()
            min_v, max_v, mean_v = nstats["min_v"], nstats["max_v"], nstats["mean_v"]

        rows.append({
            "column": col,
            "dtype": dtype,
            "rows": row_count,
            "nulls": nulls,
            "null_pct": round((nulls / row_count) * 100, 2) if row_count else None,
            "distinct": distinct_count,
            "min": min_v,
            "max": max_v,
            "mean": round(mean_v, 4) if isinstance(mean_v, (float, int)) and not math.isnan(mean_v or 0) else None
        })

    df = pd.DataFrame(rows)
    content = f"Profiled {table}: {len(rows)} column(s)."
    artifact = {
        "type": "table.json",
        "title": f"Profile: {table}",
        "inline": {"data": _to_rows(df)},
    }
    return content, artifact

@tool(response_format="content_and_artifact")
def dq_check(rule: str, table: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
    """Run a simple DQ rule. Supported:
    - 'no_negative_transactions' on transactions.amount
    - 'nonnegative_balance' on accounts.balance
    - 'kyc_complete_rate' (customers.kyc_status)
    Optionally pass table for context.
    """
    rule = rule.strip().lower()
    if rule == "no_negative_transactions":
        df = ENV.con.execute("""
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) AS negative_count
            FROM transactions
        """).df()
        row = df.iloc[0]
        status = "PASS" if int(row["negative_count"]) == 0 else "WARN"
        details = [{"metric":"negative_txn_count","value":int(row["negative_count"])},
                   {"metric":"total_txn","value":int(row["total"])}]
        title = "DQ: No Negative Transactions"
        content = f"{status}: {int(row['negative_count'])} negative txns out of {int(row['total'])}."
    elif rule == "nonnegative_balance":
        df = ENV.con.execute("""
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN balance < 0 THEN 1 ELSE 0 END) AS negative_accts
            FROM accounts
        """).df()
        row = df.iloc[0]
        status = "PASS" if int(row["negative_accts"]) == 0 else "FAIL"
        details = [{"metric":"negative_accounts","value":int(row["negative_accts"])},
                   {"metric":"total_accounts","value":int(row["total"])}]
        title = "DQ: Nonnegative Account Balance"
        content = f"{status}: {int(row['negative_accts'])} accts with negative balance."
    elif rule == "kyc_complete_rate":
        df = ENV.con.execute("""
            SELECT kyc_status, COUNT(*) AS cnt
            FROM customers
            GROUP BY 1
            ORDER BY 2 DESC
        """).df()
        total = int(df["cnt"].sum())
        complete = int(df[df["kyc_status"]=="complete"]["cnt"].sum())
        rate = round(complete / total * 100, 2) if total else 0.0
        status = "PASS" if rate >= 80.0 else "WARN"
        details = [{"metric":"kyc_complete_pct","value":rate},
                   {"metric":"total_customers","value":total}]
        title = "DQ: KYC Completion Rate"
        content = f"{status}: {rate}% customers complete KYC."
        # Return the distribution table
        artifact = {
            "type": "table.json",
            "title": title,
            "inline": {"data": _to_rows(df)},
            "limits": {"truncated": False}
        }
        return content, artifact
    else:
        return ("Unknown rule. Try: no_negative_transactions | nonnegative_balance | kyc_complete_rate",
                {"type":"table.json","title":"DQ Error","inline":{"data":[]}})

    # For the first two rules, return a tiny metrics table
    metrics_df = pd.DataFrame(details)
    artifact = {
        "type": "table.json",
        "title": title,
        "inline": {"data": _to_rows(metrics_df)},
        "limits": {"truncated": False}
    }
    return content, artifact

# -------------------------------
# Agent: tools + instructions
# -------------------------------

INSTRUCTIONS = """You are a Senior Data Analyst for a retail bank.
You have tools to:
- list assets and columns in the internal (synthetic) warehouse
- run SQL SELECT queries
- profile a table
- run basic data quality checks

Guidelines:
- Prefer using the tools to gather data, then summarize your findings clearly.
- For SQL, always start with a SELECT and keep it scoped; add GROUP BY when aggregating.
- If the user asks for KPIs over time, group by month on transactions.post_date.
- Include concise, actionable insights after showing results (e.g., top categories, outliers).

You MUST end your final message with a single fenced JSON code block that is a valid artifact manifest.

Rules:
- Put the manifest in the last line(s) of your reply inside ```json … ``` fences.
- The manifest MUST be valid JSON (no comments, no trailing commas).
- Do not write anything after the JSON block.

Schema:
{
  "artifact": {
    "type": "chart.vegaLite" | "table.json" | "code",
    "title": "<short title>",
    "inline": {
      // For charts: a valid Vega-Lite v5 spec and optional small data
      "spec": { ... },            // optional for table/code
      "data": [ ... ],            // array of objects or series (keep reasonably small)
      // For code:
      "language": "python|sql|bash|... (optional)",
      "text": "code text (optional)"
    }
    // (Optional, future-friendly) If data is large or binary, prefer:
    // "ref": { "uri": "blob://...", "bytes": 123456, "checksum": "sha256:...", "spec": { ... } }
  }
}

Examples:

```json
{ "artifact": {
  "type": "table.json",
  "title": "Top Merchant Categories",
  "inline": { "data": [
    { "merchant_category": "GROCERY", "spend": 124523.77 },
    { "merchant_category": "DINING",  "spend": 89340.12 }
  ] }
} }
"""

# Build the deep agent (a LangGraph graph)
agent = create_deep_agent(
    tools=[list_assets, sql, profile, dq_check],
    instructions=INSTRUCTIONS,
    model=azure_openai_model,
    # You can add subagents later if desired; keeping MVP simple.
)
