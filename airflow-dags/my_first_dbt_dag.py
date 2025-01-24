from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
import subprocess

# Slack Webhook URL (use the webhook you created earlier)
SLACK_API_TOKEN = "https://hooks.slack.com/services/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"
slack_channel = "#all-jignasha-dobariya"  # Replace with your Slack channel

def slack_failure_callback(context):
    """Send detailed failure message to Slack."""
    slack_msg = (
        f":red_circle: Task Failed\n"
        f"*DAG*: {context.get('dag').dag_id}\n"
        f"*Execution Date*: {context.get('execution_date')}\n"
        f"*DagRun ID*: {context.get('dag_run').run_id}"
    )
    failed_task_alert = SlackWebhookOperator(
        task_id="slack_failed_notification",
        webhook_token=SLACK_API_TOKEN,  # Webhook URL here
        text=slack_msg,
        channel=slack_channel,
    )
    failed_task_alert.execute(context=context)

def slack_success_callback(context):
    """Send detailed success message to Slack."""
    slack_msg = (
        f":white_check_mark: DAG Succeeded\n"
        f"*DAG*: {context.get('dag').dag_id}\n"
        f"*Execution Date*: {context.get('execution_date')}\n"
        f"*DagRun ID*: {context.get('dag_run').run_id}"  # Use run_id instead of log_url
    )
    success_task_alert = SlackWebhookOperator(
        task_id="slack_success_notification",
        webhook_token=SLACK_API_TOKEN,  # Webhook URL here
        text=slack_msg,
        channel=slack_channel,
    )
    success_task_alert.execute(context=context)

def run_dbt_model():
    try:
        result = subprocess.run(
            ['dbt', 'run', '--project-dir', '/opt/dbt-project', '--profiles-dir', '/opt/dbt-project', '--select', 'my_first_dbt_model'],
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
    'on_failure_callback': slack_failure_callback,  # Add the failure callback
    'on_success_callback': slack_success_callback,  # Add the success callback
}

# Create the DAG
with DAG(
    'my_first_dbt_dag',
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
