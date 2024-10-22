from scipy.signal import lti 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def get_system(type, T, w0, m):
    if type == "LP2":
        sys = lti([T],[1/(w0**2), 2*m/w0, 1])
    if type == "BP2":
        sys = lti([2*m*T/w0, 0],[1/(w0**2), 2*m/w0, 1])
    if type == "HP2":
        sys = lti([T/(w0**2), 0, 0],[1/(w0**2), 2*m/w0, 1])
    if type == "BR2":
        sys = lti([T/(w0**2), 0, T],[1/(w0**2), 2*m/w0, 1])
    return sys


def plot_bode_response(sys, mag_unit, freq_unit, w=None):
    w, Hjw = sys.freqresp(w=w)
    modulus = np.abs(Hjw)
    phase = np.angle(Hjw)*180/np.pi

    name = "Modulus {}".format(mag_unit)

    if mag_unit == "dB":
        modulus = 20*np.log10(modulus)
        y_type = "linear"
        y_text = "dB"
    if mag_unit == "linear":
        y_type = "linear"
        y_text = ""
    if mag_unit == "log":
        y_type = "log"
        y_text = ""

    x_text = freq_unit
    if freq_unit == "rad/s":
        name = "w"

    if freq_unit == "Hz":
        w = w/(2*np.pi) 
        name = "f"

    data_mag = {
        "x": w,
        "y": modulus,
        "name": "Modulus",
        "hovertemplate": "<b>{}</b>: %{{x:.3f}} {}<br><b>mag</b>: %{{y:.3f}} {}<br><b>phase</b>: %{{text:.3f}} deg<br>".format(name, x_text, y_text),
        "text": phase,
        "showlegend": False
        }
        
    data_phase = {
        "x": w,
        "y": phase,
        "name": "Phase",
        "hovertemplate": "<b>{}</b>: %{{x:.3f}} {}<br><b>mag</b>: %{{text:.3f}} {}<br><b>phase</b>: %{{y:.3f}} deg<br>".format(name, x_text, y_text),
        "text": modulus,
        "showlegend": False
        }
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
    fig.add_traces(data_mag, rows=1, cols=1)
    fig.add_traces(data_phase, rows=2, cols=1)
    fig.update_yaxes(title_text="Modulus", row=1, col=1, type=y_type)
    fig.update_xaxes(type="log", row=1, col=1)
    fig.update_yaxes(title_text="Argument", row=2, col=1)
    fig.update_xaxes(title_text=x_text, type="log", row=2, col=1)
    fig['layout'].update(height=600)
    return fig


def plot_zpk_map(sys):
    poles = sys.poles
    zeros = sys.zeros
    data_poles =  {
        "x": np.real(poles),
        "y": np.imag(poles),
        "name": "poles",
        "hovertemplate": "<b>Pole<b><br><b>real</b>: %{x:.3f}<br><b>imag</b>: %{y:.3f}<br>",
        "mode": "markers",
        "marker": {"symbol": "x", "size": 8},
        }
    data_zeros =  {
        "x": np.real(zeros),
        "y": np.imag(zeros),
        "name": "zeros",
        "hovertemplate": "<b>Zero<b><br><b>real</b>: %{x:.3f}<br><b>imag</b>: %{y:.3f}<br>",
        "mode": "markers",
        "marker": {"symbol": "circle", "size": 8},
        }
    fig = go.Figure([data_poles, data_zeros], { "xaxis": {"title": {"text": "real"}},"yaxis": {"title": {"text": "imag"}, "scaleanchor":"x", "scaleratio":1}})
    return fig


def plot_step_response(sys):
    t, s = sys.step(N=1024)
    fig = px.line(x=t, y=s, labels={'x': 't [s]', 'y':'s(t)'}, height=550)
    return fig
