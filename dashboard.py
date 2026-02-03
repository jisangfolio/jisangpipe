import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time

# 1. 페이지 설정
st.set_page_config(page_title="비트코인 실시간 대시보드", page_icon="📈")
st.title("💰 BTC")

# 2. DB 연결 설정 (Docker에 떠 있는 Postgres에 접속)
# 접속 정보: postgresql://아이디:비번@주소:포트/DB이름
db_connection_str = 'postgresql://airflow:airflow@localhost:5432/airflow'
db_connection = create_engine(db_connection_str)

# 3. 데이터 가져오기 함수
def load_data():
    try:
        # SQL을 날려서 데이터프레임으로 가져옴
        df = pd.read_sql("SELECT * FROM bitcoin_prices ORDER BY created_at DESC", db_connection)
        return df
    except Exception as e:
        st.error(f"DB 연결 실패! Docker가 켜져 있는지 확인하세요.\n에러: {e}")
        return pd.DataFrame()

# 4. 화면 그리기
if st.button('🔄 새로고침'):
    st.rerun()

# 데이터 로드
df = load_data()

if not df.empty:
    # 가장 최근 가격
    current_price = df.iloc[0]['price']
    st.metric(label="현재 비트코인 가격", value=f"{current_price:,.0f} 원")

    # 차트 그리기 (최신 50개만)
    st.subheader("📊 가격 변동 추이")
    st.line_chart(df.set_index('created_at')['price'].head(50))

    # 표 보여주기
    with st.expander("상세 데이터 보기"):
        st.dataframe(df)
else:
    st.warning("아직 데이터가 없습니다. Airflow를 실행해주세요!")