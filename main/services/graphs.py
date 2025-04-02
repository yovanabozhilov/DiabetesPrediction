# graph_service.py
import plotly.graph_objects as go
from plotly.io import to_html

def generate_insulin_graph(values):
    insulin = values[4]
    insulin_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=insulin,
        title={'text': "Insulin Level (μU/mL)"},
        gauge={
            'axis': {'range': [0, 846]},  
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 5], 'color': "yellow"},  
                {'range': [5, 25], 'color': "green"},  
                {'range': [25, 846], 'color': "red"},  
            ],
        }
    ))
    return to_html(insulin_fig, full_html=False)

def generate_bp_graph(values):
    bp = values[2]
    bp_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bp,
        title={'text': "Blood Pressure (mmHg)"},
        gauge={
            'axis': {'range': [0, 200]},  
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 60], 'color': "yellow"}, 
                {'range': [60, 100], 'color': "green"}, 
                {'range': [100, 120], 'color': "orange"}, 
                {'range': [120, 200], 'color': "red"},  
            ],
        }
    ))
    return to_html(bp_fig, full_html=False)

def generate_bmi_graph(values):
    bmi = values[5]
    bmi_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={'text': "BMI (kg/m²)"},
        gauge={
            'axis': {'range': [0, 50]},  
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 18.5], 'color': "yellow"}, 
                {'range': [18.5, 25], 'color': "green"},  
                {'range': [25, 30], 'color': "orange"},  
                {'range': [30, 50], 'color': "red"},  
            ],
        }
    ))
    return to_html(bmi_fig, full_html=False)
