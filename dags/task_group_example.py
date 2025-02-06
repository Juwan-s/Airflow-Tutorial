from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.decorators import task_group
from airflow.utils.edgemodifier import Label

from datetime import datetime

with DAG(
    dag_id = 'task_group',
    start_date = datetime(2025, 1, 1),
    schedule='@daily',
    default_args={"retries": 1},

):
    
    @task_group(default_args={"retries": 3})
    def group1():
        """This docstring will become the tooltip for the TaskGroup"""

        task1 = EmptyOperator(task_id='task1')
        task2 = BashOperator(task_id='task2',
                             bash_command="echo Hello!",
                             retries=2)
        
        print(task1.retries)
        print(task2.retries)


    task3 = EmptyOperator(task_id='task3')


    group1() >> Label("When completed") >> task3
    