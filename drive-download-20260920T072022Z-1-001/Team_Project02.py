import pymysql
import pandas as pd
import streamlit as st

st.set_page_config(page_title="MySQL 데이터 조회", layout="wide")
#st.title("📊 MySQL 데이터 조회")

# DB 연결 (앱 실행 중 한 번만 생성)
@st.cache_resource
def get_connection():
    cfg = st.secrets["mysql"]
    return pymysql.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,  # 결과를 딕셔너리로 받기
    )

# 쿼리 실행 (결과를 10분 캐싱)
@st.cache_data(ttl=600)
def run_query(sql, params=None):
    conn = get_connection()
    conn.ping(reconnect=True)  # 연결 끊겼으면 재연결
    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return pd.DataFrame(rows)

df = run_query("SELECT* FROM loan_items")

st.title("📊 MySQL 데이터 조회")
st.write(f"총 {len(df)}건")
st.dataframe(df, use_container_width=True)
