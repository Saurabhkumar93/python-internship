import streamlit as st
import pandas as pd
import numpy as np
#title-
st.title("Kvon Tech")
st.text("Welcome to Kvon tech")

df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20))
)

st.dataframe(df) 

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)