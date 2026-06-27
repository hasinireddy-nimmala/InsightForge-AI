"""Next Best Actions Page - displays prioritized actionable recommendations."""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.utils.styling import get_custom_css
from frontend.utils.api_client import APIClient
from frontend.components.confidence_bars import render_confidence_bar
from frontend.components.evidence_viewer import render_evidence_viewer

st.set_page_config(page_title="Next Best Actions - InsightForge AI", page_icon="🎯", layout="wide")
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

st.markdown("<h1 class='gradient-text'>Next Best Actions</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1rem;'>Review AI recommendations. Each action has been adjusted by past decision memory and includes explainable evidence.</p>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# Get actions
actions = []
explanations = []

if 'analysis_results' in st.session_state:
    res = st.session_state['analysis_results']
    actions = res.get("actions", [])
    explanations = res.get("explanations", [])
else:
    # Use demo default if session state is empty
    actions = [
        {"action": "Schedule Executive Business Review", "description": "Arrange urgent executive meeting to address concerns and align on success metrics", "priority": "critical", "impact": "high", "confidence": 0.92, "reasoning": "Customer VP expressed dissatisfaction; executive engagement shows commitment", "evidence": ["VP mentioned dissatisfaction in last 3 meetings", "Usage dropped 35%"], "source_documents": ["meeting_notes.txt"]},
        {"action": "Assign Dedicated Customer Success Manager", "description": "Immediately assign senior CSM for personalized guidance and weekly check-ins", "priority": "high", "impact": "high", "confidence": 0.88, "reasoning": "Reactive support model failing; proactive CSM needed", "evidence": ["Support tickets up 60%", "No proactive outreach in 45 days"], "source_documents": ["support_tickets.txt"]},
        {"action": "Launch Retention Campaign", "description": "Initiate targeted retention with custom training and onboarding refresh", "priority": "high", "impact": "medium", "confidence": 0.85, "reasoning": "Renewal in 45 days requires immediate value demonstration", "evidence": ["Feature adoption at only 30%", "Training completion below 50%"], "source_documents": ["crm_export.csv"]},
        {"action": "Offer Complimentary Premium Onboarding", "description": "Provide premium onboarding package to resolve adoption issues before renewal", "priority": "medium", "impact": "high", "confidence": 0.80, "reasoning": "Root cause of dissatisfaction is poor initial onboarding experience", "evidence": ["Customer cited onboarding as primary frustration"], "source_documents": ["meeting_notes.txt"]},
        {"action": "Escalate Open Support Tickets", "description": "Prioritize all open tickets with dedicated engineering support", "priority": "high", "impact": "medium", "confidence": 0.90, "reasoning": "Unresolved tickets eroding trust and satisfaction", "evidence": ["4 open tickets older than 7 days", "2 critical severity tickets"], "source_documents": ["support_tickets.txt"]}
    ]
    explanations = [
        {"recommendation": "Schedule Executive Business Review", "reason": "Customer VP expressed dissatisfaction in last 3 meetings with declining engagement. An executive review demonstrates organizational commitment and provides opportunity to realign on success metrics.", "evidence": ["VP mentioned considering alternatives", "Usage declined 35% QoQ", "No executive engagement in 60 days"], "source_documents": ["meeting_notes.txt - Section 3", "crm_export.csv"], "confidence": 0.92},
        {"recommendation": "Assign Dedicated Customer Success Manager", "reason": "Current reactive support model is failing to address growing customer needs. A dedicated CSM can anticipate issues and drive proactive adoption.", "evidence": ["Support tickets increased 60%", "No proactive outreach in 45 days", "Customer requested single point of contact"], "source_documents": ["support_tickets.txt", "meeting_notes.txt"], "confidence": 0.88},
        {"recommendation": "Launch Retention Campaign", "reason": "With renewal approaching in 45 days and declining usage, targeted intervention needed to demonstrate ongoing platform value.", "evidence": ["Renewal in 45 days", "Feature adoption at 30%", "Negative sentiment trend"], "source_documents": ["crm_export.csv", "meeting_notes.txt"], "confidence": 0.85},
        {"recommendation": "Offer Complimentary Premium Onboarding", "reason": "Root cause analysis shows poor onboarding as the primary driver of dissatisfaction. Addressing this directly shows responsiveness.", "evidence": ["Customer cited onboarding as #1 frustration", "Training completion below 50%"], "source_documents": ["meeting_notes.txt"], "confidence": 0.80},
        {"recommendation": "Escalate Open Support Tickets", "reason": "Unresolved technical issues are compounding customer frustration and blocking adoption. Rapid resolution will build trust.", "evidence": ["4 tickets open >7 days", "2 critical severity unresolved", "Customer threatened escalation"], "source_documents": ["support_tickets.txt"], "confidence": 0.90}
    ]

if actions:
    # Summary KPIs
    total_actions = len(actions)
    critical_count = sum(1 for a in actions if a.get("priority", "").lower() == "critical")
    avg_confidence = sum(a.get("confidence", 0.5) for a in actions) / total_actions
    
    st.markdown(
        f"""
        <div style="display: flex; gap: 2rem; margin-bottom: 2rem; flex-wrap: wrap;">
            <div class="kpi-card" style="flex: 1; min-width: 200px;">
                <span class="kpi-value">{total_actions}</span>
                <span class="kpi-title">Total Actions Recommended</span>
            </div>
            <div class="kpi-card" style="flex: 1; min-width: 200px;">
                <span class="kpi-value" style="color: var(--danger-red);">{critical_count}</span>
                <span class="kpi-title">Critical Actions</span>
            </div>
            <div class="kpi-card" style="flex: 1; min-width: 200px;">
                <span class="kpi-value" style="color: var(--accent-cyan);">{avg_confidence*100:.1f}%</span>
                <span class="kpi-title">Average Confidence</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Render layout with actions list and explanations side-by-side
    col_list, col_exp = st.columns([1, 1])
    
    with col_list:
        st.markdown("<h3 class='section-title'><span class='icon'>🎯</span> Prioritized NBA Cards</h3>", unsafe_allow_html=True)
        
        # Sort actions by priority (critical, high, medium, low)
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_actions = sorted(actions, key=lambda a: priority_order.get(a.get("priority", "medium").lower(), 2))
        
        for idx, a in enumerate(sorted_actions):
            action_title = a.get("action", a.get("title", ""))
            priority = a.get("priority", "medium").lower()
            impact = a.get("impact", "medium").upper()
            confidence = a.get("confidence", 0.5)
            
            p_badge = f"<span class='badge badge-{priority}'>{priority.upper()} PRIORITY</span>"
            i_badge = f"<span class='impact-indicator impact-{impact.lower()}'>{impact} IMPACT</span>"
            
            st.markdown(
                f"""
                <div class="action-card priority-{priority}">
                    <div class="action-title">{action_title}</div>
                    <div class="action-description">{a.get('description', '')}</div>
                    <div class="action-meta">
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
            
    with col_exp:
        st.markdown("<h3 class='section-title'><span class='icon'>🔍</span> Explainability & Evidence Trace</h3>", unsafe_allow_html=True)
        # Match explanations with actions
        render_evidence_viewer(explanations)
else:
    st.warning("No Next Best Actions available. Run the AI Analysis pipeline first.")
