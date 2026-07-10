from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VENV_PYTHON = os.path.join(PROJECT_ROOT, ".venv", "bin", "python")

default_args = {
    "owner": "data_engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="walmart_retail_medallion_pipeline",
    default_args=default_args,
    description="Orchestrated execution of local retail Medallion architecture using Polars and DuckDB",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["retail", "polars", "lakehouse"],
) as dag:

    run_silver_transform = BashOperator(
        task_id="bronze_to_silver_transform",
        bash_command=f"cd {PROJECT_ROOT} && {VENV_PYTHON} src/transform.py",
    )

    run_gold_aggregation = BashOperator(
        task_id="silver_to_gold_aggregation",
        bash_command=f"cd {PROJECT_ROOT} && {VENV_PYTHON} src/aggregate.py",
    )

    run_analytics_serving = BashOperator(
        task_id="gold_to_analytics_serving",
        bash_command=f"cd {PROJECT_ROOT} && {VENV_PYTHON} src/analytics.py",
    )

    run_quality_validation = BashOperator(
        task_id="data_quality_validation",
        bash_command=f"cd {PROJECT_ROOT} && {VENV_PYTHON} src/validate.py",
    )

    run_silver_transform >> run_gold_aggregation >> run_quality_validation >> run_analytics_serving