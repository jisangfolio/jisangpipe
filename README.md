# 💰 Bitcoin Data Pipeline & Dashboard

**Airflow + Docker + PostgreSQL + Streamlit**을 활용한 비트코인 가격 수집 및 시각화 프로젝트입니다.
매일 아침 9시(KST)에 자동으로 비트코인 가격을 수집하여 DB에 적재하고, 대시보드를 통해 시각화합니다.

## 🏗 Architecture
1. **Extract:** Python Operator를 사용하여 CoinGecko API에서 실시간 비트코인 가격 수집
2. **Load:** PostgreSQL DB에 데이터 적재 (중복 방지 및 스키마 관리)
3. **Orchestrate:** Apache Airflow를 사용하여 데이터 파이프라인 스케줄링 (매일 09:00 KST)
4. **Visualize:** Streamlit을 활용하여 DB 데이터를 실시간 차트로 시각화

## 🛠 Tech Stack
| Category | Tech |
|---|---|
| **Orchestration** | Apache Airflow 2.8.1 |
| **Container** | Docker, Docker Compose |
| **Database** | PostgreSQL 13 |
| **Dashboard** | Streamlit |
| **Language** | Python 3.9 |

## 🚀 How to Run
```bash
# 1. 실행 (Docker 환경)
docker-compose up -d

# 2. 대시보드 실행
streamlit run dashboard.py
