"""Human Review Page - human-in-the-loop governance for recommendations."""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.utils.styling import get_custom_css
from frontend.utils.api_client import APIClient
from frontend.components.confidence_bars import render_confidence_bar

st.set_page_config(page_title="Human Review - InsightForge AI", page_icon="✅", layout="wide")
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

st.markdown("<h1 class='gradient-text'>Human Review & Governance</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1rem;'>Approve, reject, or modify next best actions before they are executed. Decided recommendations train the local memory engine.</p>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# Fetch pending recommendations from database or mock them
pending_recs = []
if backend_online:
    try:
        res = api_client.get_pending_recommendations()
        pending_recs = res.get("recommendations", [])
    except Exception as e:
        st.error(f"Error fetching pending actions: {e}")
else:
    # Check if we have mock session database
    if 'mock_pending_recs' not in st.session_state:
        st.session_state['mock_pending_recs'] = [
            {"id": 101, "action": "Schedule Executive Business Review", "description": "Arrange urgent executive meeting to address concerns and align on success metrics", "priority": "critical", "impact": "high", "confidence": 0.92, "status": "pending"},
            {"id": 102, "action": "Assign Dedicated Customer Success Manager", "description": "Immediately assign senior CSM for personalized guidance and weekly check-ins", "priority": "high", "impact": "high", "confidence": 0.88, "status": "pending"},
            {"id": 103, "action": "Launch Retention Campaign", "description": "Initiate targeted retention with custom training and onboarding refresh", "priority": "high", "impact": "medium", "confidence": 0.85, "status": "pending"},
            {"id": 104, "action": "Offer Complimentary Premium Onboarding", "description": "Provide premium onboarding package to resolve adoption issues before renewal", "priority": "medium", "impact": "high", "confidence": 0.80, "status": "pending"},
            {"id": 105, "action": "Escalate Open Support Tickets", "description": "Prioritize all open tickets with dedicated engineering support", "priority": "high", "impact": "medium", "confidence": 0.90, "status": "pending"}
        ]
    pending_recs = [r for r in st.session_state['mock_pending_recs'] if r.get("status") == "pending"]

# Decisions history storage
if 'decisions_history' not in st.session_state:
    st.session_state['decisions_history'] = []

if pending_recs:
    st.markdown(f"Currently waiting for review: **{len(pending_recs)}** actions")
    
    for idx, r in enumerate(pending_recs):
        rec_id = r.get("id")
        action = r.get("action")
        description = r.get("description")
        priority = r.get("priority", "medium").lower()
        impact = r.get("impact", "medium").upper()
        confidence = r.get("confidence", 0.5)
        
        # Priority badges
        p_badge = f"<span class='badge badge-{priority}'>{priority.upper()} PRIORITY</span>"
        i_badge = f"<span class='impact-indicator impact-{impact.lower()}'>{impact} IMPACT</span>"
        
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="margin-bottom: 0.5rem;">
                    <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary);">{action}</div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem; margin: 0.5rem 0;">{description}</div>
                    <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem;">
                        {p_badge}
                        {i_badge}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Confidence bar
            conf_value = confidence * 100 if confidence <= 1 else confidence
            render_confidence_bar("Recommendation Confidence", conf_value)
            
            st.write("")
            
            # Input fields for reasons
            reason = st.text_input("Governance Note / Feedback Reason", key=f"reason_{rec_id}", placeholder="Specify rationale for approval or rejection...")
            
            c_app, c_rej, c_mod = st.columns(3)
            
            with c_app:
                if st.button("✅ Approve", key=f"approve_btn_{rec_id}", use_container_width=True):
                    if backend_online:
                        api_client.approve_recommendation(rec_id, reason)
                    else:
                        # Update mock state
                        for item in st.session_state['mock_pending_recs']:
                            if item["id"] == rec_id:
                                item["status"] = "approved"
                        st.session_state['decisions_history'].append({
                            "recommendation": action,
                            "decision": "Approved",
                            "outcome": "Accepted",
                            "confidence_delta": 0.05,
                            "reason": reason
                        })
                    st.success("Recommendation approved!")
                    st.rerun()
                    
            with c_rej:
                if st.button("❌ Reject", key=f"reject_btn_{rec_id}", use_container_width=True):
                    if backend_online:
                        api_client.reject_recommendation(rec_id, reason)
                    else:
                        for item in st.session_state['mock_pending_recs']:
                            if item["id"] == rec_id:
                                item["status"] = "rejected"
                        st.session_state['decisions_history'].append({
                            "recommendation": action,
                            "decision": "Rejected",
                            "outcome": f"Rejected: {reason}",
                            "confidence_delta": -0.03,
                            "reason": reason
                        })
                    st.warning("Recommendation rejected.")
                    st.rerun()
                    
            with c_mod:
                # Expander for modification
                with st.expander("✏️ Modify Action Details"):
                    modified_text = st.text_area("Modified Action Text", value=action, key=f"mod_text_{rec_id}")
                    if st.button("Submit Modified Action", key=f"mod_sub_{rec_id}", use_container_width=True):
                        if backend_online:
                            api_client.modify_recommendation(rec_id, modified_text, reason)
                        else:
                            for item in st.session_state['mock_pending_recs']:
                                if item["id"] == rec_id:
                                    item["action"] = modified_text
                                    item["status"] = "approved"
                            st.session_state['decisions_history'].append({
                                "recommendation": modified_text,
                                "decision": "Modified & Approved",
                                "outcome": "Modified and Accepted",
                                "confidence_delta": 0.02,
                                "reason": reason
                            })
                        st.success("Recommendation modified and approved!")
                        st.rerun()
            st.write("")
else:
    st.success("🎉 All recommendations have been processed! No pending governance queue.")
    
# Decision History list
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-title'><span class='icon'>📋</span> Recent Governance Decisions</h3>", unsafe_allow_html=True)

decisions = []
if backend_online:
    try:
        mem_res = api_client.get_memory()
        decisions = mem_res.get("entries", [])
    except Exception:
        pass
else:
    decisions = st.session_state['decisions_history']

if decisions:
    for d in decisions:
        rec_text = d.get("recommendation", d.get("recommendation", ""))
        decision = d.get("decision", "Approved" if d.get("approved") else "Rejected")
        outcome = d.get("outcome", "")
        reason_str = d.get("reason", "")
        time_str = d.get("timestamp", "Just now")
        
        status_style = "badge-approved" if "approve" in decision.lower() or d.get("approved") else "badge-rejected"
        
        st.markdown(
            f"""
            <div class="premium-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong>{rec_text}</strong>
                    <span class="badge {status_style}">{decision.upper()}</span>
                </div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">
                    <div><strong>Outcome:</strong> {outcome}</div>
                    {f"<div><strong>Reason:</strong> {reason_str}</div>" if reason_str else ""}
                    <div style="color: var(--text-muted); margin-top: 4px;">⏱ {time_str}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No governance decisions logged in this session yet.")
