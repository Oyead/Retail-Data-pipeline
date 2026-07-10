import duckdb
import polars as pl
import os
def query_regional_performance() -> pl.DataFrame:
    gold_path = os.path.join("data","gold","regional_performance","*","*.parquet")
    print("Executing DuckDB query over gold path...")
    conn = duckdb.connect(database=':memory')
    query = f"""
        SELECT
            Region,
            "Product Category",
            ROUND(CAST(TOTAL_Sales AS NUMERIC), 2) AS Sales,
            ROUND(CAST(TOTAL_Profit AS NUMERIC), 2) AS Profit,
            ROUND(CAST(Profit_Margin_Pct AS NUMERIC), 2) AS Margin_Percentage,
        FROM read_parquet('{gold_path}',hive_partitioning=true)
        ORDER BY Region, Sales DESC
    """
    return conn.execute(query).pl()
def generate_excutive_summary(df:pl.DataFrame):
    print("\n========================================================")
    print("            WALMART EXECUTIVE REGIONAL REPORT           ")
    print("========================================================\n")
    print(df)
    print("\n========================================================")
if __name__ == "__main__":
    try:
        report_df=query_regional_performance()
        generate_excutive_summary(report_df)
    except Exception as e:
        print(f"Error occurred while generating the report: {e}")    
