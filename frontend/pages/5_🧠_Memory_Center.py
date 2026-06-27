"""Memory Center Page - displays learning trends, memory tables, and confidence logs."""
import streamlit as st
import sys
import os
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.utils.styling import get_custom_css
from frontend.utils.api_client import APIClient

st.set_page_config(page_title="Memory Center - InsightForge AI", page_icon="🧠", layout="wide")
st.markdown(f"<style>{get_custom_css()}</style>", unsafe_allow_html=True)

# Sidebar
api_client = APIClient()
health = api_client.health_check()
backend_online = health.get("status") != "offline"

with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><h2 style='margin: 0; color: #06b6d4; font-weight: 800; font-size: 1.6rem;'>🔮 InsightForge AI</h2></div>", unsafe_allow_html=True)
    if backend_online:
        st.markdown('<div class="status-indicator status-online" style="width: 100%; justify-content: center; margin-bottom: 1.5rem;"><span class="status-dot online"></span><span>SYSTEM ONLINE</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-offline" style="width: 100%; justify-content: center; margin-bottom: 1.5rem;"><span class="status-dot offline"></span><span>SYSTEM OFFLINE (DEMO)</span></div>', unsafe_allow_html=True)

st.markdown("<h1 class='gradient-text'>Recommendation Memory Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1rem;'>Analyze historical governance outcomes. Recommendations calibrate their confidence dynamically based on the patterns below.</p>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# Fetch memory metrics
total_decisions = 0
approval_rate = 0.0
trends = []
memories = []

if backend_online:
    try:
        trends_res = api_client.get_memory_trends()
        total_decisions = trends_res.get("total_decisions", 0)
        approval_rate = trends_res.get("overall_approval_rate", 0.0)
        trends = trends_res.get("trends", [])
        
        mem_res = api_client.get_memory()
        memories = mem_res.get("entries", [])
    except Exception as e:
        st.error(f"Error loading memory statistics: {e}")
else:
    # Demo defaults
    total_decisions = 18
    approval_rate = 88.9
    trends = [
        {"period": "2026-06", "total_recommendations": 10, "approved": 9, "rejected": 1, "approval_rate": 90.0},
        {"period": "2026-05", "total_recommendations": 8, "approved": 7, "rejected": 1, "approval_rate": 87.5}
    ]
    
    # Check if we have mock decisions in session state
    mock_history = st.session_state.get('decisions_history', [])
    for d in mock_history:
        total_decisions += 1
        
    memories = [
        {"id": 1, "customer_id": "Acme Corporation", "recommendation": "Schedule Executive Business Review", "approved": True, "outcome": "Accepted", "confidence_delta": 0.05, "timestamp": "2026-06-27 12:00:00"},
        {"id": 2, "customer_id": "Acme Corporation", "recommendation": "Assign Dedicated Customer Success Manager", "approved": True, "outcome": "Accepted", "confidence_delta": 0.05, "timestamp": "2026-06-27 12:05:00"},
        {"id": 3, "customer_id": "Acme Corporation", "recommendation": "Launch Retention Campaign", "approved": True, "outcome": "Accepted", "confidence_delta": 0.05, "timestamp": "2026-06-27 12:10:00"},
        {"id": 4, "customer_id": "Globex Corp", "recommendation": "Offer 20% Churn Prevention Discount", "approved": False, "outcome": "Rejected: Too high discount allowed", "confidence_delta": -0.03, "timestamp": "2026-06-26 15:30:00"}
    ]
    
    for mh in mock_history:
        memories.insert(0, {
            "id": len(memories) + 1,
            "customer_id": "Acme Corporation",
            "recommendation": mh["recommendation"],
            "approved": "approve" in mh["decision"].lower(),
            "outcome": mh["outcome"],
            "confidence_delta": mh["confidence_delta"],
            "timestamp": "Just now"
        })

# Render memory metrics
st.markdown(
    f"""
    <div style="display: flex; gap: 2rem; margin-bottom: 2rem; flex-wrap: wrap;">
        <div class="kpi-card" style="flex: 1; min-width: 250px;">
            <span class="kpi-value">{total_decisions}</span>
            <span class="kpi-title">Total Decisions Logged</span>
        </div>
        <div class="kpi-card" style="flex: 1; min-width: 250px;">
            <span class="kpi-value" style="color: var(--accent-emerald);">{approval_rate}%</span>
            <span class="kpi-title">Overall Approval Rate</span>
        </div>
        <div class="kpi-card" style="flex: 1; min-width: 250px;">
            <span class="kpi-value" style="color: var(--accent-cyan);">{len(memories)}</span>
            <span class="kpi-title">Active Learning Embeddings</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

col_chart, col_cal = st.columns([3, 2])

with col_chart:
    st.markdown("<h3 class='section-title'><span class='icon'>📈</span> Approval Trends Over Time</h3>", unsafe_allow_html=True)
    
    if trends:
        periods = [t["period"] for t in reversed(trends)]
        approved = [t["approved"] for t in reversed(trends)]
        rejected = [t["rejected"] for t in reversed(trends)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Approved", 
            x=periods, 
            y=approved, 
            marker_color="#10b981",
            opacity=0.85
        ))
        fig.add_trace(go.Bar(
            name="Rejected", 
            x=periods, 
            y=rejected, 
            marker_color="#ef4444",
            opacity=0.85
        ))
        
        fig.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#e2e8f0"},
            height=300,
            margin=dict(l=20, r=20, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Insufficient timeline trend data.")

with col_cal:
    st.markdown("<h3 class='section-title'><span class='icon'>⚙️</span> Confidence Calibration Matrix</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="premium-card">
            <div style="font-size: 0.9rem; line-height: 1.6; color: var(--text-secondary);">
                InsightForge AI employs a <strong>Memory-Driven Calibration Engine</strong> to adjust agent confidence:
                <ul style="margin-top: 0.5rem; padding-left: 1.25rem;">
                    <li><strong>Approved Recommendations:</strong> Boosts future similarity matches by <span style="color: var(--accent-emerald); font-weight: 600;">+5% confidence</span>.</li>
                    <li><strong>Modified & Approved Recommendations:</strong> Boosts future matches by <span style="color: var(--accent-cyan); font-weight: 600;">+2% confidence</span>.</li>
                    <li><strong>Rejected Recommendations:</strong> Reduces future matches by <span style="color: var(--danger-red); font-weight: 600;">-3% confidence</span>.</li>
                </ul>
                This forces the Next Best Action Agent to auto-calibrate recommendations dynamically to mirror human decision-making and preferences.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Memories Table
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-title'><span class='icon'>💾</span> Recommendation Learning Memory</h3>", unsafe_allow_html=True)

if memories:
    for m in memories:
        rec = m.get("recommendation")
        cust = m.get("customer_id")
        app = m.get("approved")
        outcome = m.get("outcome")
        delta = m.get("confidence_delta")
        t_stamp = m.get("timestamp")
        
        status_badge = "<span class='badge badge-approved'>APPROVED</span>" if app else "<span class='badge badge-rejected'>REJECTED</span>"
        delta_color = "var(--accent-emerald)" if delta > 0 else "var(--danger-red)"
        delta_sign = "+" if delta > 0 else ""
        
        st.markdown(
            f"""
            <div class="premium-card" style="padding: 1rem 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                    <div>
                        <span style="font-weight: 700; font-size: 1.05rem; color: var(--text-primary);">{rec}</span>
                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 2px;">
                            Customer: <strong>{cust}</strong> • {t_stamp}
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        {status_badge}
                        <span style="font-weight: 700; color: {delta_color}; font-size: 0.9rem;">
                            Calibration: {delta_sign}{delta*100:.0f}%
                        </span>
                    </div>
                </div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.5rem; border-top: 1px solid var(--border-color); padding-top: 0.5rem;">
                    <strong>Decision Outcome:</strong> {outcome}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No learning memories recorded yet.")
