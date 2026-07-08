import polars as pl
import pytest
from src.transform import transform_bronze_to_silver

def test_transform_bronze_to_silver_calculates_correctly():
    mock_data = pl.DataFrame({
        "City": ["Cairo", "Alexandria"],
        "Customer Age": ["25", "34 yrs"], 
        "Customer Name": ["Alice", "Bob"],
        "Customer Segment": ["Corporate", "Home Office"],
        "Discount": [0.05, 0.1],
        "Number of Records": [1, 1],
        "Order Date": [pl.Date(2026, 7, 1), pl.Date(2026, 7, 2)],
        "Order ID": [1001, 1002],
        "Order Priority": ["High", "Low"],
        "Order Quantity": [2, 5],        
        "Product Base Margin": [0.4, None], 
        "Product Category": ["Electronics", "Furniture"],
        "Product Container": ["Large Box", "Small Pack"],
        "Product Name": ["Laptop", "Desk"],
        "Product Sub-Category": ["Computers", "Chairs"],
        "Profit": [150.0, 50.0],
        "Region": ["North", "South"],
        "Row ID": [1, 2],
        "Sales": [1000.0, 500.0],   
        "Ship Date": [pl.Date(2026, 7, 2), pl.Date(2026, 7, 3)],
        "Ship Mode": ["Express", "Regular"],
        "Shipping Cost": [25.0, 15.0],
        "State": ["Giza", "Alex"],
        "Unit Price": [500.0, 100.0],
        "Zip Code": [12345, 54321]
    }).lazy()

    result_df = transform_bronze_to_silver(mock_data).collect()

    assert result_df.get_column("Customer Age").to_list() == [25, 34]
    assert result_df.get_column("Customer Age").dtype == pl.Int64

    assert result_df.get_column("Product Base Margin").to_list() == [0.4, 0.4]

    assert result_df.get_column("Gross_Revenue").to_list()[0] == 1000.0

    assert result_df.get_column("Total_Cost").to_list()[0] == 825.0