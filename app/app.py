import streamlit as st
import plotly.figure_factory as ff
import numpy as np
from systems import *

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("LTI Analysis")
    st.subheader("System Selection")
    type = st.selectbox( 'Type Of Filter', ('LP2', 'BP2', 'HP2','BR2'), index=0)
    T = st.number_input('T', value=1.0, step=10**-2 )
    w0 = st.number_input('w0 [rad/s]', value=10.0, step=10**-2 )
    m = st.number_input('m', value=0.5, step=10**-2 )
    st.subheader("Response")
    response = st.selectbox('Type', ('Bode', 'Step', 'Poles & Zeros'), index=0)
    st.subheader("Bode Units")
    mag_unit = st.selectbox( 'Mag', ('linear', 'dB', 'log'), index=1)
    freq_unit = st.selectbox( 'Freq Unit', ('rad/s', 'Hz'), index=0)

# process form
sys = get_system(type, T, w0, m)
if response == "Step":
    st.title('Step Reponse')
    fig = plot_step_response(sys)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

if response == "Bode":
    st.title('Bode Plot')
    w0_temp = np.log10(w0)
    w = np.logspace(w0_temp-2, w0_temp+2, 500)
    fig = plot_bode_response(sys, mag_unit, freq_unit, w=w)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

if response == "Poles & Zeros":
    st.title('Poles & Zeros Map')
    fig = plot_zpk_map(sys)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
