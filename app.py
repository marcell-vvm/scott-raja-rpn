import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
from databricks import sql
import time 

# Set up connection parameters (use secrets or env vars in production!)
server_hostname = st.secrets.databricks.server_hostname
http_path = st.secrets.databricks.http_path
access_token = st.secrets.databricks.access_token

st.title("Peak Play - Scott Raja Rankings")
st_autorefresh(interval=60 * 1000, key='datarefresh')

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
st.rerun()