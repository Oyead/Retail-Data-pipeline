import polars as pl
import os
from extract import extract_excel_bronze_data
def transform_bronze_to_silver(lf:pl.LazyFrame):
    silver_lf = (
        lf.with_columns(
            pl.col("Customer Name").str.replace_all(r"/D","").cast(pl.Int64,strict=False)
        )
        .with_columns(
            pl.col("Product Base Margin").fill_null(strategy="backward")
        )
        .filter(
            (pl.col("Order Quantity") > 0) & (pl.col("Sales") >= 0)
        )
        .with_columns([
            (pl.col("Order Quantity") * pl.col("Unit Price")).alias("Gross_Revenue"),
            (pl.col("Sales") - pl.col("Profit") - pl.col("Shipping Cost")).alias("Total_Cost")
        ])
    )
    return silver_lf

def save_to_silver(lf:pl.LazyFrame,output_name:str="cleaned_sales.parquet"):
    silver_path = os.path.join("data","silver",output_name)

    print(f"Saving cleaned data to silver path: {silver_path}")
    df=lf.collect(streaming=True)
    df.write_parquet(silver_path)
    print("Silver Layer materialization complete!")
if __name__ == "__main__":
    try:
        raw_lf=extract_excel_bronze_data("walmart Retail Data.xlsx")
        cleaned_lf=transform_bronze_to_silver(raw_lf)
        save_to_silver(cleaned_lf)
        print("Transformation and saving to silver layer successful!")
    except Exception as e:
        print(f"Transformation failed: {e}")