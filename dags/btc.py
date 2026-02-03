from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
from urllib.request import urlopen  # 설치 없이 인터넷 쓰는 도구

# 1. 비트코인 가격 가져오는 함수
def get_btc_price():
    # 코인게코(CoinGecko)라는 무료 공개 사이트 주소입니다
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=krw"
    
    # 인터넷 접속해서 데이터 가져오기
    response = urlopen(url)
    data = json.loads(response.read())
    
    # 가격만 쏙 뽑아내기
    price = data['bitcoin']['krw']
    
    print("--------------------------------------------------")
    print(f"💰 현재 비트코인 가격: {price:,.0f} 원")
    print("--------------------------------------------------")
    
    return price

# 2. DAG 정의 (로봇 설계도)
with DAG(
    dag_id='bitcoin_tracker_v1',  # Airflow 화면에 뜰 이름
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,       # 일단은 수동 실행
    catchup=False
) as dag:

    # 3. 작업 만들기
    fetch_price_task = PythonOperator(
        task_id='get_bitcoin_price',
        python_callable=get_btc_price
    )

    # 작업 실행!
    fetch_price_task