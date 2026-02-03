from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import json
from urllib.request import urlopen

# 1. 데이터를 가져와서 DB에 넣는 함수
def get_and_save_btc_price():
    # A. 비트코인 가격 수집 (Extract)
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=krw"
    response = urlopen(url)
    data = json.loads(response.read())
    price = data['bitcoin']['krw']
    
    # B. DB 연결 준비 (Hook 사용)
    # 'postgres_default'는 Airflow가 설치될 때 자동으로 만들어주는 기본 연결 설정입니다.
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # C. SQL 작성 및 실행 (Load)
    insert_sql = f"INSERT INTO bitcoin_prices (price, created_at) VALUES ({price}, NOW());"
    postgres_hook.run(insert_sql)
    
    print(f"✅ DB 저장 완료! 가격: {price}원")

# 2. DAG 정의
with DAG(
    dag_id='bitcoin_db_saver_v1',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    # 작업 1: 테이블 만들기 (없으면 생성)
    create_table_task = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE TABLE IF NOT EXISTS bitcoin_prices (
            id SERIAL PRIMARY KEY,
            price NUMERIC,
            created_at TIMESTAMP
        );
        """
    )

    # 작업 2: 데이터 수집 및 저장
    save_price_task = PythonOperator(
        task_id='save_btc_price',
        python_callable=get_and_save_btc_price
    )

    # 순서: 테이블이 먼저 있어야 데이터를 넣겠죠?
    create_table_task >> save_price_task