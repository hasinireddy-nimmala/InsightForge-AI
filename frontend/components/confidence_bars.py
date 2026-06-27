"""Animated confidence bar components."""
import streamlit as st


def _get_fill_class(confidence: float) -> str:
    """Return CSS class based on confidence level."""
    if confidence < 40:
        return "fill-red"
    elif confidence < 60:
        return "fill-amber"
    elif confidence < 80:
        return "fill-cyan"
    else:
        return "fill-emerald"


def render_confidence_bar(label: str, confidence: float, color: str = None):
    """Render a single animated confidence bar.

    Args:
        label: Label for the bar.
        confidence: Confidence value from 0 to 100.
        color: Optional override color for the bar fill.
    """
    confidence = max(0, min(100, confidence))
    fill_class = _get_fill_class(confidence)

    if color:
        fill_style = f'style="background: {color};"'
        fill_class_attr = ""
    else:
        fill_style = ""
        fill_class_attr = fill_class

    bar_html = f"""
    <div class="confidence-bar-container">
        <div class="confidence-bar-label">
            <span>{label}</span>
            <span style="font-weight: 600; color: #e2e8f0;">{confidence:.0f}%</span>
        </div>
        <div class="confidence-bar-track">
            <div class="confidence-bar-fill {fill_class_attr}" {fill_style}
                 style="width: {confidence}%;"></div>
        </div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)


def render_confidence_bars(items: list):
    """Render multiple confidence bars.

    Args:
        items: List of dicts with keys: label, confidence, color (optional).
    """
    for item in items:
        render_confidence_bar(
            label=item.get("label", ""),
            confidence=item.get("confidence", 0),
            color=item.get("color"),
        )
