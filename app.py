import streamlit as st
import pandas as pd
from databricks import sql
import time 

# Set up connection parameters (use secrets or env vars in production!)
server_hostname = ''
http_path = ''
access_token = ''

st.title("scott raja rankings hehe")

try:
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token,
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM peak_play.silver.scott_raja_rankings_tmp")
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df)

except Exception as e:
    st.error(f"Failed to load data: {e}")

time.sleep(60)
st.experimental_rerun()