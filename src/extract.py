import polars as pl
import os
def extract_excel_bronze_data(file_name:str,sheet_name:str = None) -> pl.LazyFrame:
    bronze_path = os.path.join("data","bronze",file_name)
    if not os.path.exists(bronze_path):
        raise FileNotFoundError(f"File {bronze_path} does not exist.")
    df = pl.read_excel(source=bronze_path,sheet_name=sheet_name,engine="calamine")
    return df.lazy()
if __name__ == "__main__":
    try:
        lf=extract_excel_bronze_data("walmart Retail Data.xlsx")
        print("Test Successful!")
        print(lf.schema)

    except Exception as e:
        print(f"Extraction failed: {e}")
