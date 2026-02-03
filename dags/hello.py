from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# 1. 함수 정의 (실제로 일을 하는 녀석들)
def start_work():
    print("🚀 작업을 시작합니다!")

def end_work():
    print("✅ 모든 작업이 정상적으로 끝났습니다. 수고하셨어요!")

# 2. DAG 정의 (작업의 판을 짜는 곳)
with DAG(
    dag_id='jisang_first_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    # 3. 오퍼레이터 정의 (함수를 Airflow 작업으로 감싸기)
    task1 = PythonOperator(
        task_id='start_task',
        python_callable=start_work
    )

    task2 = PythonOperator(
        task_id='end_task',
        python_callable=end_work
    )

    # 4. 순서 정의 (화살표로 순서 정하기)
    # task1이 끝나야 task2가 실행된다는 뜻
    task1 >> task2