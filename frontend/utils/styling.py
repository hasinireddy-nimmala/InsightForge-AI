"""Premium CSS styling for InsightForge AI dashboard."""


def get_custom_css() -> str:
    """Return comprehensive premium CSS for the InsightForge AI dashboard.

    This CSS creates a premium SaaS look with glassmorphism, gradient borders,
    smooth animations, and carefully crafted visual hierarchy.
    """
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ========== ROOT VARIABLES ========== */
    :root {
        --deep-navy: #0a0f1c;
        --dark-blue: #111827;
        --card-bg: rgba(17, 24, 39, 0.8);
        --card-bg-solid: #111827;
        --accent-cyan: #06b6d4;
        --accent-purple: #8b5cf6;
        --accent-emerald: #10b981;
        --warning-amber: #f59e0b;
        --danger-red: #ef4444;
        --text-primary: #e2e8f0;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-color: rgba(255, 255, 255, 0.1);
        --border-hover: rgba(255, 255, 255, 0.2);
        --glow-cyan: rgba(6, 182, 212, 0.3);
        --glow-purple: rgba(139, 92, 246, 0.3);
        --glow-emerald: rgba(16, 185, 129, 0.3);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
        --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.6);
        --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ========== GLOBAL OVERRIDES ========== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: linear-gradient(180deg, rgba(10, 15, 28, 0.95) 0%, rgba(10, 15, 28, 0) 100%);
        backdrop-filter: blur(10px);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--deep-navy);
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--accent-cyan), var(--accent-purple));
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-cyan);
    }

    /* Main background */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0f1c 0%, #0f172a 25%, #0a0f1c 50%, #111827 75%, #0a0f1c 100%);
        background-attachment: fixed;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1321 0%, #111827 100%);
        border-right: 1px solid var(--border-color);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* ========== GRADIENT TEXT ========== */
    .gradient-text {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-purple) 50%, var(--accent-cyan) 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 4s ease-in-out infinite;
        font-weight: 800;
    }
    @keyframes gradientShift {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }

    /* ========== KPI CARDS ========== */
    .kpi-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        text-align: center;
        transition: all var(--transition-normal);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.6s ease-out;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
        opacity: 0;
        transition: opacity var(--transition-normal);
    }
    .kpi-card:hover {
        transform: scale(1.02);
        border-color: var(--border-hover);
        box-shadow: 0 8px 32px rgba(6, 182, 212, 0.15), 0 0 60px rgba(6, 182, 212, 0.05);
    }
    .kpi-card:hover::before {
        opacity: 1;
    }
    .kpi-icon {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.2;
        margin-bottom: 0.25rem;
    }
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }
    .kpi-delta {
        font-size: 0.85rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 20px;
        display: inline-block;
    }
    .kpi-delta.positive {
        color: var(--accent-emerald);
        background: rgba(16, 185, 129, 0.1);
    }
    .kpi-delta.negative {
        color: var(--danger-red);
        background: rgba(239, 68, 68, 0.1);
    }

    /* ========== ACTION CARDS ========== */
    .action-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all var(--transition-normal);
        position: relative;
        overflow: hidden;
        animation: slideUp 0.5s ease-out;
    }
    .action-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    .action-card.priority-critical {
        border-left: 4px solid var(--danger-red);
    }
    .action-card.priority-high {
        border-left: 4px solid var(--warning-amber);
    }
    .action-card.priority-medium {
        border-left: 4px solid var(--accent-cyan);
    }
    .action-card.priority-low {
        border-left: 4px solid var(--accent-emerald);
    }
    .action-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .action-description {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .action-meta {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        align-items: center;
    }

    /* ========== RISK CARDS ========== */
    .risk-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin-bottom: 0.75rem;
        transition: all var(--transition-normal);
    }
    .risk-card:hover {
        border-color: rgba(239, 68, 68, 0.3);
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.1);
    }
    .risk-card .risk-title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.35rem;
    }
    .risk-card .risk-description {
        color: var(--text-secondary);
        font-size: 0.85rem;
        line-height: 1.5;
    }
    .risk-level-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ========== STATUS BADGES ========== */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-approved {
        background: rgba(16, 185, 129, 0.15);
        color: var(--accent-emerald);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-rejected {
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger-red);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-pending {
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning-amber);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-critical {
        background: rgba(239, 68, 68, 0.2);
        color: var(--danger-red);
        border: 1px solid rgba(239, 68, 68, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    .badge-high {
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning-amber);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-medium {
        background: rgba(6, 182, 212, 0.15);
        color: var(--accent-cyan);
        border: 1px solid rgba(6, 182, 212, 0.3);
    }
    .badge-low {
        background: rgba(16, 185, 129, 0.15);
        color: var(--accent-emerald);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-positive {
        background: rgba(16, 185, 129, 0.15);
        color: var(--accent-emerald);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-negative {
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger-red);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-neutral {
        background: rgba(148, 163, 184, 0.15);
        color: var(--text-secondary);
        border: 1px solid rgba(148, 163, 184, 0.3);
    }

    /* ========== CONFIDENCE BAR ========== */
    .confidence-bar-container {
        margin: 0.5rem 0;
    }
    .confidence-bar-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    .confidence-bar-track {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    .confidence-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        animation: barGrow 1.2s ease-out;
        position: relative;
        overflow: hidden;
    }
    .confidence-bar-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 2s ease-in-out infinite;
    }
    .confidence-bar-fill.fill-red {
        background: linear-gradient(90deg, #dc2626, #ef4444);
    }
    .confidence-bar-fill.fill-amber {
        background: linear-gradient(90deg, #d97706, #f59e0b);
    }
    .confidence-bar-fill.fill-cyan {
        background: linear-gradient(90deg, #0891b2, #06b6d4);
    }
    .confidence-bar-fill.fill-emerald {
        background: linear-gradient(90deg, #059669, #10b981);
    }

    /* ========== TIMELINE ========== */
    .timeline-container {
        position: relative;
        padding-left: 2.5rem;
        margin: 1rem 0;
    }
    .timeline-container::before {
        content: '';
        position: absolute;
        left: 14px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: linear-gradient(180deg, var(--accent-cyan), var(--accent-purple), var(--accent-emerald));
        border-radius: 2px;
    }
    .timeline-item {
        position: relative;
        padding: 0.75rem 0;
        padding-left: 1.5rem;
        animation: fadeIn 0.5s ease-out;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -1.55rem;
        top: 1.1rem;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 2px solid var(--accent-cyan);
        background: var(--deep-navy);
        z-index: 1;
    }
    .timeline-item.completed::before {
        background: var(--accent-emerald);
        border-color: var(--accent-emerald);
        box-shadow: 0 0 8px var(--glow-emerald);
    }
    .timeline-item.error::before {
        background: var(--danger-red);
        border-color: var(--danger-red);
        box-shadow: 0 0 8px rgba(239, 68, 68, 0.3);
    }
    .timeline-item.running::before {
        background: var(--accent-cyan);
        border-color: var(--accent-cyan);
        box-shadow: 0 0 8px var(--glow-cyan);
        animation: pulse 1.5s ease-in-out infinite;
    }
    .timeline-agent-name {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.95rem;
    }
    .timeline-meta {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 2px;
    }

    /* ========== EVIDENCE PANEL ========== */
    .evidence-panel {
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin: 0.75rem 0;
    }
    .evidence-panel h4 {
        color: var(--accent-cyan);
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }
    .evidence-item {
        color: var(--text-secondary);
        font-size: 0.85rem;
        padding: 0.4rem 0;
        padding-left: 1rem;
        border-left: 2px solid rgba(6, 182, 212, 0.3);
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    .evidence-source {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 8px;
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 4px;
        font-size: 0.75rem;
        color: var(--accent-purple);
        margin-right: 0.5rem;
        margin-top: 0.25rem;
    }

    /* ========== CUSTOM BUTTONS ========== */
    .btn-approve {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all var(--transition-fast) !important;
    }
    .btn-approve:hover {
        box-shadow: 0 4px 20px var(--glow-emerald) !important;
        transform: translateY(-1px) !important;
    }
    .btn-reject {
        background: linear-gradient(135deg, #dc2626, #ef4444) !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all var(--transition-fast) !important;
    }
    .btn-reject:hover {
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    .btn-modify {
        background: linear-gradient(135deg, #0891b2, #06b6d4) !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all var(--transition-fast) !important;
    }
    .btn-modify:hover {
        box-shadow: 0 4px 20px var(--glow-cyan) !important;
        transform: translateY(-1px) !important;
    }

    /* ========== HERO SECTION ========== */
    .hero-section {
        text-align: center;
        padding: 3rem 1rem 2rem;
        animation: fadeIn 0.8s ease-out;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }

    /* ========== FEATURE GRID ========== */
    .feature-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        text-align: center;
        transition: all var(--transition-normal);
        height: 100%;
        animation: slideUp 0.6s ease-out;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: var(--accent-cyan);
        box-shadow: 0 12px 40px rgba(6, 182, 212, 0.1);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .feature-description {
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* ========== METRIC NUMBERS ========== */
    .metric-large {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1;
    }
    .metric-unit {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin-left: 4px;
    }

    /* ========== DIVIDERS ========== */
    .section-divider {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 2rem 0;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-title .icon {
        font-size: 1.3rem;
    }

    /* ========== TAB CONTAINER ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: rgba(17, 24, 39, 0.5);
        border-radius: var(--radius-md);
        padding: 4px;
        border: 1px solid var(--border-color);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        color: var(--text-secondary);
        font-weight: 500;
        padding: 8px 16px;
        transition: all var(--transition-fast);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2)) !important;
        color: var(--text-primary) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ========== EXPANDER STYLING ========== */
    .streamlit-expanderHeader {
        background: rgba(17, 24, 39, 0.5) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    .streamlit-expanderContent {
        background: rgba(17, 24, 39, 0.3) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
    }

    /* ========== CARD GENERAL ========== */
    .premium-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all var(--transition-normal);
        animation: fadeIn 0.6s ease-out;
    }
    .premium-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow-md);
    }
    .premium-card-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .premium-card-body {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.7;
    }

    /* ========== STATUS INDICATOR ========== */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-online {
        background: rgba(16, 185, 129, 0.15);
        color: var(--accent-emerald);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .status-offline {
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger-red);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    .status-dot.online {
        background: var(--accent-emerald);
        box-shadow: 0 0 8px var(--glow-emerald);
        animation: pulse 2s ease-in-out infinite;
    }
    .status-dot.offline {
        background: var(--danger-red);
    }

    /* ========== QUICK START ========== */
    .quickstart-step {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color);
    }
    .quickstart-step:last-child {
        border-bottom: none;
    }
    .quickstart-number {
        width: 32px;
        height: 32px;
        min-width: 32px;
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        color: white;
    }
    .quickstart-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .quickstart-text strong {
        color: var(--text-primary);
    }

    /* ========== IMPACT INDICATOR ========== */
    .impact-indicator {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 6px;
    }
    .impact-high {
        background: rgba(6, 182, 212, 0.15);
        color: var(--accent-cyan);
    }
    .impact-medium {
        background: rgba(139, 92, 246, 0.15);
        color: var(--accent-purple);
    }
    .impact-low {
        background: rgba(148, 163, 184, 0.15);
        color: var(--text-secondary);
    }

    /* ========== KEYFRAME ANIMATIONS ========== */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes barGrow {
        from { width: 0; }
    }

    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* ========== UPLOAD AREA ========== */
    .upload-zone {
        border: 2px dashed rgba(6, 182, 212, 0.3);
        border-radius: var(--radius-lg);
        padding: 2.5rem;
        text-align: center;
        transition: all var(--transition-normal);
        background: rgba(6, 182, 212, 0.03);
    }
    .upload-zone:hover {
        border-color: var(--accent-cyan);
        background: rgba(6, 182, 212, 0.06);
    }

    /* ========== TABLE STYLING ========== */
    .doc-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: var(--radius-md);
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    .doc-table th {
        background: rgba(6, 182, 212, 0.1);
        color: var(--accent-cyan);
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }
    .doc-table td {
        padding: 10px 16px;
        color: var(--text-secondary);
        font-size: 0.85rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .doc-table tr:last-child td {
        border-bottom: none;
    }
    .doc-table tr:hover td {
        background: rgba(6, 182, 212, 0.03);
    }

    /* ========== INPUT STYLING ========== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        transition: border-color var(--transition-fast) !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 0 1px var(--accent-cyan) !important;
    }

    /* ========== REVIEW CARD ========== */
    .review-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        transition: all var(--transition-normal);
        animation: slideUp 0.5s ease-out;
    }
    .review-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow-lg);
    }
    .review-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    .review-action-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .review-section {
        margin: 1rem 0;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: var(--radius-sm);
        border-left: 3px solid var(--accent-cyan);
    }
    .review-section-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--accent-cyan);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .review-section-content {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .decision-history-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1rem;
        background: rgba(17, 24, 39, 0.5);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-sm);
        margin-bottom: 0.5rem;
    }

    /* ========== MEMORY CARD ========== */
    .memory-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin-bottom: 0.75rem;
        transition: all var(--transition-normal);
    }
    .memory-card:hover {
        border-color: rgba(139, 92, 246, 0.3);
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.08);
    }

    /* ========== LOADING ANIMATION ========== */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
    }
    .loading-spinner {
        width: 48px;
        height: 48px;
        border: 3px solid rgba(6, 182, 212, 0.1);
        border-top-color: var(--accent-cyan);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-bottom: 1rem;
    }
    .loading-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    """
