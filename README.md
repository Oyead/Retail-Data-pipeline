# Walmart Retail Data Pipeline

A medallion architecture data pipeline that processes Walmart retail sales data through Bronze, Silver, and Gold lakehouse layers, with an analytics serving layer powered by DuckDB.

## Architecture

```
data/bronze/walmart Retail Data.xlsx
         |
         v  [extract.py]    -- Bronze: Ingest raw Excel via Polars
         |
         v  [transform.py]  -- Silver: Clean, filter, derive columns
         |
data/silver/cleaned_sales.parquet
         |
         v  [aggregate.py]  -- Gold: Aggregate KPIs by Region + Category
         |
data/gold/regional_performance/Region=*/
         |
         v  [analytics.py]  -- Analytics: Query with DuckDB, generate report
         |
    stdout (Executive Summary)
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Data Processing | [Polars](https://pola.rs/) |
| Analytical Queries | [DuckDB](https://duckdb.org/) |
| Orchestration | [Apache Airflow](https://airflow.apache.org/) |
| Storage Format | Parquet (Hive-partitioned) |
| Source Format | Excel (.xlsx) |

## Project Structure

```
retail_pipeline/
├── airflow/
│   ├── dags/
│   │   └── walmart_pipeline_dag.py   # DAG definition
│   └── airflow.cfg                    # Airflow configuration
├── data/
│   ├── bronze/                        # Raw source data
│   ├── silver/                        # Cleaned & transformed data
│   └── gold/                          # Aggregated business KPIs
├── src/
│   ├── extract.py                     # Bronze layer ingestion
│   ├── transform.py                   # Silver layer cleaning & derivation
│   ├── aggregate.py                   # Gold layer KPI aggregation
│   └── analytics.py                   # DuckDB analytics & reporting
├── tests/
│   └── test_transform.py              # Unit tests for transform layer
├── .gitignore
└── requirments.txt
```

## Pipeline Stages

### Bronze — `src/extract.py`
Reads the raw Walmart retail Excel dataset from `data/bronze/` into a Polars LazyFrame using the `calamine` engine.

### Silver — `src/transform.py`
Applies cleaning and business logic to the Bronze data:
- Strips non-numeric characters from customer fields and casts to `Int64`
- Back-fills null values in `Product Base Margin`
- Filters out rows with `Order Quantity <= 0` or negative `Sales`
- Derives `Gross_Revenue` (Order Quantity × Unit Price) and `Total_Cost` (Sales − Profit − Shipping Cost)

Outputs a materialized Parquet file to `data/silver/`.

### Gold — `src/aggregate.py`
Aggregates Silver data by `Region` and `Product Category` to compute:
- **Total_Sales** — sum of Sales
- **Total_Profit** — sum of Profit
- **Total_Shipping_Cost** — sum of Shipping Cost
- **Total_Units_Sold** — sum of Order Quantity
- **Profit_Margin_Pct** — (Profit / Sales) × 100

Writes Hive-partitioned Parquet to `data/gold/regional_performance/`.

### Analytics — `src/analytics.py`
Queries Gold-layer Parquet files via DuckDB SQL and generates an executive regional summary report to stdout.

## Getting Started

### Prerequisites

- Python 3.10+
- An Airflow-compatible environment (for orchestration)

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install polars duckdb openpyxl pytest apache-airflow
```

### Running the Pipeline

Each stage can be run independently:

```bash
# Bronze -> Silver
python src/transform.py

# Silver -> Gold
python src/aggregate.py

# Gold -> Analytics report
python src/analytics.py
```

### Running with Airflow

```bash
airflow db migrate
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
airflow scheduler &
airflow webserver &
```

The DAG `walmart_retail_medallion_pipeline` runs daily and chains all four stages:

```
transform >> aggregate >> validate >> analytics
```

> **Note:** The DAG references `src/validate.py` for data quality checks, which is not yet implemented.

## Testing

```bash
pytest tests/
```

Tests validate the Silver transformation logic against mock data, verifying:
- Customer field parsing and type casting
- Null back-fill behavior for `Product Base Margin`
- Derived column calculations (`Gross_Revenue`, `Total_Cost`)

## License

This project is for educational and internal use.
