

FROM apache/airflow:latest

# Switch to the Airflow user (you already included this correctly)
USER airflow

# Install DBT core and the DBT Postgres adapter
RUN pip install --no-cache-dir dbt-core==1.6.1 dbt-postgres==1.6.1 protobuf==4.23.0

# Install the Slack provider package
RUN pip install --no-cache-dir apache-airflow-providers-slack