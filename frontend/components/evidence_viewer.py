"""Evidence and explanation viewer component."""
import streamlit as st
from frontend.components.confidence_bars import render_confidence_bar


def render_evidence_viewer(explanations: list):
    """Render evidence and reasoning panels for recommendations.

    Args:
        explanations: List of dicts with keys:
            - title: Recommendation title
            - reason / reasoning: Why this was recommended
            - evidence: List of evidence strings
            - sources / source_documents: List of source document references
            - confidence: Confidence score (0-100)
    """
    if not explanations:
        st.info("No explanations available.")
        return

    for i, explanation in enumerate(explanations):
        title = explanation.get("title", explanation.get("action", f"Recommendation {i + 1}"))
        reason = explanation.get("reason", explanation.get("reasoning", "No reasoning provided."))
        evidence = explanation.get("evidence", [])
        sources = explanation.get("sources", explanation.get("source_documents", []))
        confidence = explanation.get("confidence", 0)

        with st.expander(f"🔍 {title}", expanded=(i == 0)):
            # Why section
            st.markdown(
                f"""
                <div class="evidence-panel">
                    <h4>💡 Why This Recommendation</h4>
                    <div style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.7;">
                        {reason}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Evidence section
            if evidence:
                evidence_items = ""
                for ev in evidence:
                    ev_text = ev if isinstance(ev, str) else str(ev)
                    evidence_items += f'<div class="evidence-item">{ev_text}</div>'

                st.markdown(
                    f"""
                    <div class="evidence-panel">
                        <h4>📊 Supporting Evidence</h4>
                        {evidence_items}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Source documents
            if sources:
                source_html = ""
                for src in sources:
                    src_text = src if isinstance(src, str) else src.get("filename", str(src))
                    source_html += f'<span class="evidence-source">📄 {src_text}</span>'

                st.markdown(
                    f"""
                    <div class="evidence-panel">
                        <h4>📁 Source Documents</h4>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                            {source_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Confidence
            if confidence:
                conf_value = confidence * 100 if confidence <= 1 else confidence
                render_confidence_bar("Confidence", conf_value)
