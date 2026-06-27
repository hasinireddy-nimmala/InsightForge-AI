"""AI Analysis Page - triggers and visualizes multi-agent decision intelligence pipeline."""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.utils.styling import get_custom_css
from frontend.utils.api_client import APIClient
from frontend.components.agent_timeline import render_agent_timeline
from frontend.components.risk_gauge import render_risk_gauge, render_health_gauge

st.set_page_config(page_title="AI Analysis - InsightForge AI", page_icon="🔍", layout="wide")
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

st.markdown("<h1 class='gradient-text'>AI Decision Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1rem;'>Orchestrate Planner and specialized agents to map relationship risks, assess health status, and identify expansion opportunities.</p>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# Input Panel
col_input, col_run = st.columns([2, 1])

# Pre-seeded demo scenarios
demo_interaction = ""
demo_file_path = "data/demo/sample_meeting_notes.txt"
if os.path.exists(demo_file_path):
    try:
        with open(demo_file_path, "r", encoding="utf-8") as f:
            demo_interaction = f.read()
    except Exception:
        pass

with col_input:
    st.markdown("<h3 class='section-title'><span class='icon'>📝</span> Interaction Context</h3>", unsafe_allow_html=True)
    
    # Customer Selection
    customer_id = st.text_input("Customer ID", value="Acme Corporation")
    
    # Custom Interaction Text
    interaction_text = st.text_area(
        "Enter customer email thread, call transcript, or meeting notes for analysis:",
        value=demo_interaction,
        height=300
    )

with col_run:
    st.markdown("<h3 class='section-title'><span class='icon'>⚙️</span> Pipeline Control</h3>", unsafe_allow_html=True)
    st.markdown("Orchestrate analysis via LangGraph. The Planner dynamically delegates tasks to 6 specialized agents.")
    
    # List uploaded docs to select for context
    indexed_docs = []
    if backend_online:
        docs_res = api_client.list_documents()
        indexed_docs = docs_res.get("documents", [])
    else:
        indexed_docs = [
            {"id": 1, "filename": "sample_meeting_notes.txt"},
            {"id": 2, "filename": "sample_crm_export.csv"},
            {"id": 3, "filename": "sample_support_tickets.txt"}
        ]
        
    doc_options = {d["filename"]: d["id"] for d in indexed_docs}
    selected_doc_names = st.multiselect(
        "Attach indexed documents for RAG context:",
        options=list(doc_options.keys()),
        default=list(doc_options.keys())[:1] if doc_options else None
    )
    selected_doc_ids = [doc_options[name] for name in selected_doc_names]
    
    st.write("")
    if st.button("🚀 Run AI Analysis Pipeline", type="primary", use_container_width=True):
        if backend_online:
            with st.spinner("Invoking Planner Agent and initializing agent threads..."):
                analysis_res = api_client.run_analysis(
                    input_text=interaction_text,
                    customer_id=customer_id,
                    document_ids=selected_doc_ids
                )
                if analysis_res:
                    st.session_state['analysis_results'] = analysis_res
                    st.success("Analysis pipeline completed successfully!")
                else:
                    st.error("Pipeline execution encountered an error.")
        else:
            # Generate local demo results
            st.info("Demo Mode: Simulating pipeline run. Triggering mock Gemini responses.")
            
            # Map mock outputs matching requirements
            import uuid
            st.session_state['analysis_results'] = {
                "analysis_id": str(uuid.uuid4())[:8],
                "status": "completed",
                "customer_id": customer_id,
                "plan": ["retrieve_context", "analyze_business", "detect_risks", "find_opportunities", "recommend_actions", "explain_reasoning"],
                "business_analysis": {
                    "summary": "Customer Acme Corporation is experiencing significant onboarding challenges leading to declining platform adoption. With renewal approaching in 45 days, there is an urgent need for executive intervention and dedicated success management. Support ticket volume has increased 60% while usage metrics show a 35% decline, indicating growing dissatisfaction. The VP of Operations has expressed frustration about lack of executive engagement and is reportedly considering alternatives.",
                    "sentiment": "negative",
                    "business_goal": "Reduce churn risk and drive platform adoption before renewal deadline",
                    "customer_health_score": 32.0,
                    "stakeholders": ["Sarah Chen - VP of Operations", "Michael Rodriguez - IT Director", "End Users (Engineering Team)"],
                    "pain_points": ["Poor onboarding experience", "Increasing support ticket volume", "Declining platform usage", "Lack of dedicated support contact", "Integration delays", "Insufficient training"]
                },
                "risks": {
                    "risk_level": "high",
                    "risk_score": 78.0,
                    "risks": [
                        {"name": "Churn Risk", "description": "Customer showing dissatisfaction with declining usage and increasing support tickets", "confidence": 0.87, "evidence": ["Usage declined 35% over last quarter", "3 escalated support tickets in 2 weeks"]},
                        {"name": "Renewal Risk", "description": "Contract renewal approaching with unresolved issues", "confidence": 0.82, "evidence": ["Renewal due in 45 days", "Customer expressed frustration in last meeting"]},
                        {"name": "Escalation Risk", "description": "Support ticket volume increasing with higher severity", "confidence": 0.75, "evidence": ["Support tickets increased 60%", "Average resolution time growing"]},
                        {"name": "Product Adoption Risk", "description": "Low feature adoption indicating poor onboarding", "confidence": 0.80, "evidence": ["Only 30% feature adoption rate", "Training completion below 50%"]}
                    ]
                },
                "opportunities": {
                    "opportunities": [
                        {"title": "Premium Onboarding Package", "description": "Dedicated onboarding support could resolve adoption issues and demonstrate commitment", "impact": "high", "confidence": 0.85},
                        {"title": "Executive Business Review", "description": "Strategic alignment session to address concerns and showcase platform value", "impact": "high", "confidence": 0.80},
                        {"title": "Customer Success Manager Assignment", "description": "Dedicated CSM to drive adoption and provide proactive support", "impact": "medium", "confidence": 0.78},
                        {"title": "Custom Integration Support", "description": "Tailored integration assistance to resolve technical pain points", "impact": "medium", "confidence": 0.72}
                    ]
                },
                "actions": [
                    {"action": "Schedule Executive Business Review", "description": "Arrange urgent executive meeting to address concerns and align on success metrics", "priority": "critical", "impact": "high", "confidence": 0.92, "reasoning": "Customer VP expressed dissatisfaction; executive engagement shows commitment", "evidence": ["VP mentioned dissatisfaction in last 3 meetings", "Usage dropped 35%"], "source_documents": ["meeting_notes.txt"]},
                    {"action": "Assign Dedicated Customer Success Manager", "description": "Immediately assign senior CSM for personalized guidance and weekly check-ins", "priority": "high", "impact": "high", "confidence": 0.88, "reasoning": "Reactive support model failing; proactive CSM needed", "evidence": ["Support tickets up 60%", "No proactive outreach in 45 days"], "source_documents": ["support_tickets.txt"]},
                    {"action": "Launch Retention Campaign", "description": "Initiate targeted retention with custom training and onboarding refresh", "priority": "high", "impact": "medium", "confidence": 0.85, "reasoning": "Renewal in 45 days requires immediate value demonstration", "evidence": ["Feature adoption at only 30%", "Training completion below 50%"], "source_documents": ["crm_export.csv"]},
                    {"action": "Offer Complimentary Premium Onboarding", "description": "Provide premium onboarding package to resolve adoption issues before renewal", "priority": "medium", "impact": "high", "confidence": 0.80, "reasoning": "Root cause of dissatisfaction is poor initial onboarding experience", "evidence": ["Customer cited onboarding as primary frustration"], "source_documents": ["meeting_notes.txt"]},
                    {"action": "Escalate Open Support Tickets", "description": "Prioritize all open tickets with dedicated engineering support", "priority": "high", "impact": "medium", "confidence": 0.90, "reasoning": "Unresolved tickets eroding trust and satisfaction", "evidence": ["4 open tickets older than 7 days", "2 critical severity tickets"], "source_documents": ["support_tickets.txt"]}
                ],
                "explanations": [
                    {"recommendation": "Schedule Executive Business Review", "reason": "Customer VP expressed dissatisfaction in last 3 meetings with declining engagement. An executive review demonstrates organizational commitment and provides opportunity to realign on success metrics.", "evidence": ["VP mentioned considering alternatives", "Usage declined 35% QoQ", "No executive engagement in 60 days"], "source_documents": ["meeting_notes.txt - Section 3", "crm_export.csv"], "confidence": 0.92},
                    {"recommendation": "Assign Dedicated Customer Success Manager", "reason": "Current reactive support model is failing to address growing customer needs. A dedicated CSM can anticipate issues and drive proactive adoption.", "evidence": ["Support tickets increased 60%", "No proactive outreach in 45 days", "Customer requested single point of contact"], "source_documents": ["support_tickets.txt", "meeting_notes.txt"], "confidence": 0.88},
                    {"recommendation": "Launch Retention Campaign", "reason": "With renewal approaching in 45 days and declining usage, targeted intervention needed to demonstrate ongoing platform value.", "evidence": ["Renewal in 45 days", "Feature adoption at 30%", "Negative sentiment trend"], "source_documents": ["crm_export.csv", "meeting_notes.txt"], "confidence": 0.85},
                    {"recommendation": "Offer Complimentary Premium Onboarding", "reason": "Root cause analysis shows poor onboarding as the primary driver of dissatisfaction. Addressing this directly shows responsiveness.", "evidence": ["Customer cited onboarding as #1 frustration", "Training completion below 50%"], "source_documents": ["meeting_notes.txt"], "confidence": 0.80},
                    {"recommendation": "Escalate Open Support Tickets", "reason": "Unresolved technical issues are compounding customer frustration and blocking adoption. Rapid resolution will build trust.", "evidence": ["4 tickets open >7 days", "2 critical severity unresolved", "Customer threatened escalation"], "source_documents": ["support_tickets.txt"], "confidence": 0.90}
                ],
                "agent_timeline": [
                    {"agent_name": "Planner Agent", "status": "completed", "execution_time_ms": 420.0, "output_summary": "Created plan with 6 steps"},
                    {"agent_name": "Context Retrieval Agent", "status": "completed", "execution_time_ms": 150.0, "output_summary": "Retrieved 8 relevant chunks from 3 source files"},
                    {"agent_name": "Business Analysis Agent", "status": "completed", "execution_time_ms": 980.0, "output_summary": "Determined sentiment: negative, health score: 32.0"},
                    {"agent_name": "Risk Detection Agent", "status": "completed", "execution_time_ms": 1150.0, "output_summary": "Detected 4 risk items. Level: high, Score: 78.0"},
                    {"agent_name": "Opportunity Discovery Agent", "status": "completed", "execution_time_ms": 860.0, "output_summary": "Identified 4 expansion/growth opportunities"},
                    {"agent_name": "Next Best Action Agent", "status": "completed", "execution_time_ms": 1050.0, "output_summary": "Generated 5 next best actions"},
                    {"agent_name": "Explanation Agent", "status": "completed", "execution_time_ms": 940.0, "output_summary": "Generated explanations for 5 recommendations"}
                ]
            }
            st.success("Analysis pipeline completed successfully!")

# Display Results if cached
if 'analysis_results' in st.session_state:
    res = st.session_state['analysis_results']
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='gradient-text'>Analysis Dashboard — ID: {res.get('analysis_id')}</h2>", unsafe_allow_html=True)
    
    # Segment 1: Execution Timeline
    st.markdown("<h3 class='section-title'><span class='icon'>⚡</span> Agent Execution Timeline</h3>", unsafe_allow_html=True)
    
    # Map output_summary to output to support render_agent_timeline signature
    mapped_timeline = []
    for item in res.get("agent_timeline", []):
        mapped_timeline.append({
            "agent_name": item.get("agent_name"),
            "status": item.get("status"),
            "execution_time_ms": item.get("execution_time_ms"),
            "output": item.get("output_summary")
        })
    render_agent_timeline(mapped_timeline)
    
    # Segment 2: Health and Risk Gauges
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    col_g1, col_g2 = st.columns(2)
    
    ba = res.get("business_analysis", {})
    risks_data = res.get("risks", {})
    
    with col_g1:
        render_health_gauge(ba.get("customer_health_score", 50.0))
        
    with col_g2:
        render_risk_gauge(risks_data.get("risk_score", 50.0), risks_data.get("risk_level", "medium"))
        
    # Segment 3: Business Summary
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'><span class='icon'>📊</span> Executive Business Profile</h3>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"**Executive Summary:**\n{ba.get('summary')}")
        st.write("")
        c_det1, c_det2 = st.columns(2)
        
        with c_det1:
            st.markdown(f"**Sentiment Profile:** `{ba.get('sentiment', '').upper()}`")
            st.markdown(f"**Primary Business Goal:** {ba.get('business_goal')}")
            st.markdown(f"**Stakeholders Engaged:**")
            for sh in ba.get("stakeholders", []):
                st.markdown(f"- {sh}")
                
        with c_det2:
            st.markdown("**Key Customer Pain Points:**")
            for pp in ba.get("pain_points", []):
                st.markdown(f"- {pp}")
                
    # Segment 4: Risks and Opportunities
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    col_r, col_o = st.columns(2)
    
    with col_r:
        st.markdown("<h3 class='section-title'><span class='icon'>⚠️</span> Detected Risks</h3>", unsafe_allow_html=True)
        for r in risks_data.get("risks", []):
            with st.container(border=True):
                st.markdown(f"🚨 **{r.get('name')}** (Confidence: {int(r.get('confidence', 0)*100)}%)")
                st.markdown(f"<span style='color: #94a3b8; font-size: 0.85rem;'>{r.get('description')}</span>", unsafe_allow_html=True)
                st.markdown("**Evidence Details:**")
                for ev in r.get("evidence", []):
                    st.markdown(f"- *\"{ev}\"*")
                    
    with col_o:
        st.markdown("<h3 class='section-title'><span class='icon'>💡</span> Discovered Opportunities</h3>", unsafe_allow_html=True)
        opps = res.get("opportunities", {}).get("opportunities", [])
        for o in opps:
            with st.container(border=True):
                impact_badge = f"<span class='badge badge-{o.get('impact').lower()}'>{o.get('impact')} IMPACT</span>"
                st.markdown(f"🌱 **{o.get('title')}**  {impact_badge}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: #94a3b8; font-size: 0.85rem;'>{o.get('description')}</span>", unsafe_allow_html=True)
                st.markdown(f"Confidence: **{int(o.get('confidence', 0)*100)}%**")
else:
    st.warning("Please enter/attach context above and trigger the analysis.")
