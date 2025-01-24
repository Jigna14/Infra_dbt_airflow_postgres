from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess

def run_dbt_model():
    try:
        result = subprocess.run(
            ['dbt', 'run', '--project-dir', '/opt/dbt-project', '--profiles-dir', '/opt/dbt-project'],
            check=True,  # Will raise an error for non-zero exit status
            capture_output=True,  # Capture both stdout and stderr
            text=True
        )
        print(result.stdout)  # Print the stdout
    except subprocess.CalledProcessError as e:
        print("Error during DBT run:", e.stderr)  # Print the stderr in case of failure
        raise e  # Raise again to make sure the task fails correctly

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
with DAG(
    'my_second_dbt_dag',
    default_args=default_args,
    description='A simple DAG to run a DBT model',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['dbt'],
) as dag:

    # Task to run DBT model
    run_dbt_task = PythonOperator(
        task_id='run_dbt_model',
        python_callable=run_dbt_model
    )

# Add tasks to the DAG (if more are needed, they can be chained here)
run_dbt_task
