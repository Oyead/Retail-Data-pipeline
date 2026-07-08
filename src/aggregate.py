import polars as pl
import os

def load_silver_data(file_name:str = "cleaned_sales.parquet"):
    silver_path = os.path.join("data","silver",file_name)
    if not os.path.exists(silver_path):
        raise FileNotFoundError(f"Silver data not found at {silver_path}. Please ensure the transformation step has been completed.")
    return pl.scan_parquet(silver_path)
def generate_gold_regional_kpis(lf:pl.LazyFrame)-> pl.LazyFrame:
    print("Generating gold layer KPIs...")
    return(
        lf.group_by(["Region","Product Category"])
        .agg([
            pl.col("Sales").sum().alias("Total_Sales"),
            pl.col("Profit").sum().alias("Total_Profit"),
            pl.col("Shipping Cost").sum().alias("Total_Shipping_Cost"),
            pl.col("Order Quantity").sum().alias("Total_Units_Sold"),
            (pl.col("Profit").sum() / pl.col("Sales").sum()*100).alias("Profit_Margin_Pct")
        ])
        .sort("Total_Sales",descending=True)
    )
def write_gold_lakehouse(lf:pl.LazyFrame,folder_name:str,partition_cols:list[str]):
    gold_dir = os.path.join("data","gold",folder_name)
    print(f"Materializing gold lakehouse table partitioned by {partition_cols} -> {gold_dir}...")

    df=lf.collect(engine="streaming")
    df.write_parquet(gold_dir,use_pyarrow=True,pyarrow_options={"partition_cols":partition_cols})
    print(f"Gold table [{folder_name}] written successfully to {gold_dir}!")
if __name__ == "__main__":
    try:
        silver_lf = load_silver_data()
        
        regional_kpis = generate_gold_regional_kpis(silver_lf)
        
        write_gold_lakehouse(regional_kpis, "regional_performance", partition_cols=["Region"])
        
    except Exception as e:
        print(f"Gold aggregation failed: {e}")
