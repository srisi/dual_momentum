# Airflow Setup


Set home to local airflow directory (assuming each application only has one)

`export AIRFLOW_HOME=~/???/dual_momentum/backend/airflow`

Install airflow (if not yet done through reqs)

`pip install apache-airflow`

Init db

`airflow initdb`


airflow.cfg config


Set `load_examples = False`

Set email, see https://stackoverflow.com/questions/51829200/how-to-set-up-airflow-send-email



Start webserver

`airflow webserver -p 8080`

Start scheduler

`airflow scheduler`

