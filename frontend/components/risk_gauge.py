"""Plotly gauge chart components for risk and health scores."""
import plotly.graph_objects as go
import streamlit as st


def render_risk_gauge(risk_score: float, risk_level: str = ""):
    """Render a risk gauge chart (0-100, higher = riskier).

    Args:
        risk_score: Risk score from 0 to 100.
        risk_level: Text label for the risk level.
    """
    risk_score = max(0, min(100, risk_score))

    color = "#10b981"
    if risk_score >= 75:
        color = "#ef4444"
    elif risk_score >= 50:
        color = "#f59e0b"
    elif risk_score >= 25:
        color = "#f59e0b"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            number={"suffix": "%", "font": {"size": 36, "color": "#e2e8f0"}},
            title={
                "text": f"Risk Level: {risk_level}" if risk_level else "Risk Score",
                "font": {"size": 14, "color": "#94a3b8"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#334155",
                    "dtick": 25,
                    "tickfont": {"color": "#64748b", "size": 10},
                },
                "bar": {"color": color, "thickness": 0.8},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 25], "color": "rgba(16, 185, 129, 0.1)"},
                    {"range": [25, 50], "color": "rgba(245, 158, 11, 0.1)"},
                    {"range": [50, 75], "color": "rgba(249, 115, 22, 0.1)"},
                    {"range": [75, 100], "color": "rgba(239, 68, 68, 0.1)"},
                ],
                "threshold": {
                    "line": {"color": "#ef4444", "width": 3},
                    "thickness": 0.8,
                    "value": risk_score,
                },
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0"},
        height=250,
        margin=dict(l=30, r=30, t=50, b=10),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_health_gauge(health_score: float):
    """Render a health gauge chart (0-100, higher = healthier).

    Args:
        health_score: Health score from 0 to 100.
    """
    health_score = max(0, min(100, health_score))

    color = "#ef4444"
    if health_score >= 75:
        color = "#10b981"
    elif health_score >= 50:
        color = "#f59e0b"
    elif health_score >= 25:
        color = "#f59e0b"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=health_score,
            number={"suffix": "%", "font": {"size": 36, "color": "#e2e8f0"}},
            title={
                "text": "Customer Health",
                "font": {"size": 14, "color": "#94a3b8"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#334155",
                    "dtick": 25,
                    "tickfont": {"color": "#64748b", "size": 10},
                },
                "bar": {"color": color, "thickness": 0.8},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 25], "color": "rgba(239, 68, 68, 0.1)"},
                    {"range": [25, 50], "color": "rgba(249, 115, 22, 0.1)"},
                    {"range": [50, 75], "color": "rgba(245, 158, 11, 0.1)"},
                    {"range": [75, 100], "color": "rgba(16, 185, 129, 0.1)"},
                ],
                "threshold": {
                    "line": {"color": "#10b981", "width": 3},
                    "thickness": 0.8,
                    "value": health_score,
                },
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0"},
        height=250,
        margin=dict(l=30, r=30, t=50, b=10),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
