import pandas as pd
import streamlit as st
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="📅 Local Events Calendar", layout="centered")
st.title("📅 Team Event Calendar")

# Refreshing value in ms
st_autorefresh(interval=6000, key="datarefresh")

EXCEL_Path = Path("calendar_test.xlsx")

@st.cache_data(ttl=300)
def load_calendar_data(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_excel(path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date')

try: 
    df = load_calendar_data(EXCEL_Path)

    grouped = df.groupby(df['Date'].dt.to_period("M"))
    for period, group in grouped:
        st.subheader(period.strftime('%B %Y'))
        for _, row in group.iterrows():
            st.markdown(f"- **{row['Date'].strftime('%a, %b, %d')}** - {row['EventName']}")
except Exception as e:
        st.error(f"Error loading calendar: {e}")