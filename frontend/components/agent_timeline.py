"""Agent execution timeline visualization."""
import streamlit as st


def render_agent_timeline(timeline: list):
    """Render a vertical timeline of agent execution steps.

    Args:
        timeline: List of dicts with keys:
            - agent_name: Name of the agent
            - status: 'completed', 'error', or 'running'
            - execution_time_ms: Execution time in milliseconds
            - output: Agent output summary (optional)
    """
    if not timeline:
        st.info("No timeline data available.")
        return

    st.markdown('<div class="timeline-container">', unsafe_allow_html=True)

    for i, step in enumerate(timeline):
        agent_name = step.get("agent_name", step.get("agent", f"Agent {i + 1}"))
        status = step.get("status", "completed").lower()
        exec_time = step.get("execution_time_ms", step.get("duration_ms", 0))
        output = step.get("output", step.get("result", ""))

        # Status icon and class
        if status == "completed":
            status_icon = "✅"
            status_class = "completed"
        elif status == "error":
            status_icon = "❌"
            status_class = "error"
        else:
            status_icon = "⏳"
            status_class = "running"

        # Format execution time
        if exec_time >= 1000:
            time_str = f"{exec_time / 1000:.1f}s"
        else:
            time_str = f"{exec_time}ms"

        item_html = f"""
        <div class="timeline-item {status_class}">
            <div>
                <span class="timeline-agent-name">{status_icon} {agent_name}</span>
                <div class="timeline-meta">⏱ {time_str} • Status: {status.title()}</div>
            </div>
        </div>
        """
        st.markdown(item_html, unsafe_allow_html=True)

        # Expandable output
        if output:
            output_text = output if isinstance(output, str) else str(output)
            if len(output_text) > 50:
                with st.expander(f"📋 {agent_name} Output", expanded=False):
                    st.markdown(
                        f'<div class="evidence-panel"><div class="premium-card-body">{output_text}</div></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    f'<div style="padding-left: 1.5rem; margin-top: -0.5rem; margin-bottom: 0.5rem;">'
                    f'<span style="color: var(--text-secondary); font-size: 0.8rem;">{output_text}</span></div>',
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)
