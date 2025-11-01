
# TP03 Mini Project: Python + Power BI

## Files
- `TP03_sales_data.csv`: Raw synthetic dataset with a few duplicates/missing values (realistic).
- `TP03_sales_data_clean.csv`: Cleaned dataset for analysis / Power BI.
- `TP03_analysis.py`: Turnkey Python analysis (EDA + customer segmentation).
- `PowerBI_PowerQuery_M.txt`: Power Query (M) code to import / transform the cleaned CSV.
- `PowerBI_DAX_Measures.txt`: Common DAX measures and a Calendar table template.

## How to Run (Python)
1. Place all files in the same folder.
2. Run:
   ```bash
   python TP03_analysis.py
   ```
3. Outputs:
   - Folder `figures/` with:
     - `sales_over_time.png`
     - `top_products.png`
     - `revenue_by_region.png`
     - `customer_segments.png`
   - `customer_segments.csv` with cluster assignments.
   - `TP03_sales_data_clean.csv` (re-generated if needed).

## How to Use in Power BI
1. Open **Power BI Desktop**.
2. Get Data ➜ **Text/CSV** ➜ select `TP03_sales_data_clean.csv`.
3. Click **Transform Data** and open **Advanced Editor**.
4. Replace the query with the contents of `PowerBI_PowerQuery_M.txt` (update file path if needed).
5. Load data.
6. In **Modeling**, create a new table and paste the `Calendar` definition from `PowerBI_DAX_Measures.txt`.
7. Add measures in the same file:
   - `Total Sales`, `Total Quantity`, `Average Order Value`, `Sales YTD`, `Sales MoM %`.
8. Build visuals:
   - Line chart: Axis = `Calendar[Month]`, Values = `[Total Sales]`.
   - Bar chart (Top 10 products): Axis = `Sales[product]`, Values = `[Total Sales]` + Top N filter = 10.
   - Map or bar by `Sales[region]`.
   - KPIs: `[Total Sales]`, `[Average Order Value]`, `[Total Quantity]`.

## Notes
- You can schedule refresh in Power BI Service when the CSV is hosted in SharePoint/OneDrive.
- Feel free to extend clustering features or add forecasting in Python (e.g., Prophet).
