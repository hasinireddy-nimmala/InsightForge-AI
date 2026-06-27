"""KPI metric cards with glassmorphism styling."""
import streamlit as st


def render_kpi_cards(metrics: list):
    """Render a row of KPI metric cards with glassmorphism effect.

    Args:
        metrics: List of dicts with keys: title, value, delta, icon, color
    """
    cols = st.columns(len(metrics))
    for i, (col, metric) in enumerate(zip(cols, metrics)):
        with col:
            delta_val = metric.get("delta", "")
            delta_class = ""
            delta_html = ""
            if delta_val:
                if isinstance(delta_val, str):
                    is_positive = delta_val.startswith("+") or delta_val.startswith("↑")
                else:
                    is_positive = delta_val > 0
                delta_class = "positive" if is_positive else "negative"
                delta_display = delta_val if isinstance(delta_val, str) else f"{delta_val:+}"
                delta_html = f'<span class="kpi-delta {delta_class}">{delta_display}</span>'

            color = metric.get("color", "#06b6d4")
            icon = metric.get("icon", "📊")
            value = metric.get("value", "0")
            title = metric.get("title", "Metric")

            card_html = f"""
            <div class="kpi-card" style="animation-delay: {i * 0.1}s;">
                <span class="kpi-icon">{icon}</span>
                <div class="kpi-value" style="color: {color};">{value}</div>
                <div class="kpi-title">{title}</div>
                {delta_html}
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
