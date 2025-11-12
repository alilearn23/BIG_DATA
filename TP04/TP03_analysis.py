
"""
TP03 Analysis Script
- Loads sales data
- Cleans & preprocesses
- EDA (descriptives, correlations, trends)
- Advanced analysis: simple customer segmentation via KMeans
- Saves figures and a cleaned dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path

RAW_CSV = "TP03_sales_data.csv"
CLEAN_CSV = "TP03_sales_data_clean.csv"

def load_and_clean(raw_csv=RAW_CSV, clean_csv=CLEAN_CSV):
    df = pd.read_csv(raw_csv)
    # basic cleaning
    df = df.drop_duplicates().copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["region"] = df["region"].fillna("Unknown")
    df["category"] = df["category"].fillna("Unknown")
    # derived fields
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df.to_csv(clean_csv, index=False)
    return df

def eda(df: pd.DataFrame, out_dir="figures"):
    Path(out_dir).mkdir(exist_ok=True)
    # 1) Sales over time
    s = df.groupby("month")["revenue"].sum()
    ax = s.plot(kind="line", title="Sales Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/sales_over_time.png")
    plt.clf()

    # 2) Top products
    top = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(10)
    ax = top.plot(kind="bar", title="Top 10 Products by Revenue")
    ax.set_xlabel("Product")
    ax.set_ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/top_products.png")
    plt.clf()

    # 3) Regional sales
    reg = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    ax = reg.plot(kind="bar", title="Revenue by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/revenue_by_region.png")
    plt.clf()

def customer_segmentation(df: pd.DataFrame, out_dir="figures"):
    Path(out_dir).mkdir(exist_ok=True)
    # Build simple RFM-like features per customer
    r = df.groupby("customer_id").agg(
        total_revenue=("revenue", "sum"),
        avg_basket=("revenue", "mean"),
        orders=("order_id", "nunique"),
        avg_qty=("quantity", "mean"),
    ).fillna(0.0)

    scaler = StandardScaler()
    X = scaler.fit_transform(r)

    # KMeans with 4 clusters
    km = KMeans(n_clusters=4, random_state=42, n_init="auto")
    r["cluster"] = km.fit_predict(X)

    # Persist clusters
    r.to_csv("customer_segments.csv")

    # Plot cluster sizes
    sizes = r["cluster"].value_counts().sort_index()
    ax = sizes.plot(kind="bar", title="Customer Segments (counts)")
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/customer_segments.png")
    plt.clf()

def main():
    df = load_and_clean()
    eda(df)
    customer_segmentation(df)
    print("Done. Outputs saved to 'figures/' and cleaned CSV created.")

if __name__ == "__main__":
    main()
