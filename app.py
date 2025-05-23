import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
from databricks import sql
import time 


server_hostname = st.secrets.databricks.server_hostname
http_path = st.secrets.databricks.http_path
access_token = st.secrets.databricks.access_token

try:
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token,
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(st.secrets.databricks.query)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

    df = pd.DataFrame(
        data, 
        columns=columns
    )

    st.image('https://peakplay-public-assets.s3.us-east-1.amazonaws.com/peakplay-logos/peakplay-logo-darkmode.svg', width=200)  # adjust path/width as needed
    st.title("TheBigJackpot Rankings")

    filter_input = st.text_input(
        "Enter your ID.. ", 
        key="input_id", 
        max_chars=7,
        help="This is the 6 digit number you received from our support team. ",
        placeholder='ABC-123'

    )

    filtered_df = df.copy()
    if filter_input:
        filtered_df = df[df['email'].astype(str).str.contains(filter_input)]

    
    st.dataframe(filtered_df)
    st_autorefresh(interval=30 * 1000, key='datarefresh')

    time.sleep(60)
    st.rerun()
except Exception as e:
    st.error(f"Error connecting to the Databricks: {e}")
