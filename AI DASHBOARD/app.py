"""
Streamlit Frontend for AI-Powered Multi-Agent BI Dashboard
Using Google Gemini AI
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv
import json
import plotly.graph_objects as go

# Check if running with streamlit
if not hasattr(st, 'session_state'):
    print("ERROR: This application must be run with Streamlit.")
    print("Please use the following command:")
    print("  streamlit run app.py")
    print("\nOr from the project root:")
    print("  streamlit run \"AI DASHBOARD/app.py\"")
    sys.exit(1)

from agents.lead_orchestrator import LeadOrchestratorAgent
from agents.sales_agent import SalesAIAgent
from agents.hr_agent import HRAIAgent
from agents.finance_agent import FinanceAIAgent
from visualization.chart_generator import (
    create_revenue_trend,
    create_customer_segments_pie,
    create_department_bar,
    create_financial_gauge,
    create_kpi_cards
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Business Intelligence Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 2.75rem;
        font-weight: 800;
        color: #2563eb;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
        text-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 2rem;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    /* Professional Badge */
    .gemini-badge {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        display: inline-block;
        letter-spacing: 0.025em;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    /* Agent Response Cards */
    .agent-response {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-top: 1rem;
        line-height: 1.7;
        color: #1e293b;
    }
    
    /* Section Headers */
    h1, h2, h3 {
        color: #1e40af;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h2 {
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
        color: #1e40af;
    }
    
    h3 {
        font-size: 1.35rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        color: #2563eb;
    }
    
    /* Sidebar Styling - Light Theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-right: 2px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #1e40af;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #334155;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        color: #1e40af;
    }
    
    [data-testid="stSidebar"] .stMetric {
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-1px);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Info/Alert Boxes */
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        border-radius: 8px;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
    }
    
    /* Divider Styling */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
    
    /* Metric Display */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e40af;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Chat Interface */
    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
    }
    
    .chat-user {
        background: #dbeafe;
        border-left: 4px solid #2563eb;
        color: #1e293b;
    }
    
    .chat-ai {
        background: #dcfce7;
        border-left: 4px solid #10b981;
        color: #1e293b;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Professional Spacing */
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Ensure text is visible */
    .stMarkdown {
        color: #1e293b;
    }
    
    .stMarkdown p {
        color: #334155;
    }
    
    /* Main content background */
    .main {
        background-color: #ffffff;
    }
    
    /* Ensure all text is readable */
    body {
        color: #1e293b;
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'orchestrator' not in st.session_state:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        st.session_state.orchestrator = LeadOrchestratorAgent(api_key=api_key)
        st.session_state.sales_agent = SalesAIAgent(api_key=api_key)
        st.session_state.hr_agent = HRAIAgent(api_key=api_key)
        st.session_state.finance_agent = FinanceAIAgent(api_key=api_key)
        st.session_state.api_configured = True
    else:
        st.session_state.orchestrator = None
        st.session_state.api_configured = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def main():
    """Main application"""
    
    # Professional Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<div class="main-header">AI-Powered Business Intelligence Dashboard</div>', 
                    unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Multi-Agent System with MCP Architecture • Real-time Analytics • Intelligent Insights</div>', 
                    unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align: right; padding-top: 1rem;"><div class="gemini-badge">⚡ Powered by Gemini</div></div>', 
                    unsafe_allow_html=True)
    
    # Check API key - use .get() for safe access
    if not st.session_state.get('api_configured', False):
        st.error("⚠️ Google API key not found!")
        st.info("""
        **Setup Instructions:**
        1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create a `.env` file in the `AI DASHBOARD` directory
        3. Add: `GOOGLE_API_KEY=your-api-key-here`
        4. Restart the application using: `streamlit run app.py`
        """)
        st.stop()
    
    # Professional Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0 2rem 0;">
            <h1 style="color: #1e40af; font-size: 1.75rem; margin-bottom: 0.5rem; font-weight: 700;">Navigation</h1>
            <p style="color: #475569; font-size: 0.875rem; margin: 0; font-weight: 500;">Select a page to explore</p>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "Select Page:",
            ["🏠 Dashboard", "💬 AI Chat", "📊 Sales Analytics", 
             "👥 HR Analytics", "💰 Finance Analytics", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("""
        <div style="padding: 0.5rem 0;">
            <h3 style="color: #1e40af; font-size: 1.1rem; margin-bottom: 1rem; font-weight: 600;">Key Metrics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Load quick stats
        try:
            with open('./data/processed/sales_kpis.json', 'r') as f:
                sales_data = json.load(f)
            with open('./data/processed/hr_kpis.json', 'r') as f:
                hr_data = json.load(f)
            with open('./data/processed/finance_kpis.json', 'r') as f:
                finance_data = json.load(f)
            
            st.metric("Total Revenue", 
                     f"${sales_data['summary'].get('total_revenue', 0):,.0f}")
            st.metric("Employees", 
                     f"{hr_data['summary'].get('total_employees', 0):,}")
            st.metric("Health Score", 
                     f"{finance_data['summary'].get('financial_health_score', 0):.1f}/100")
        except Exception as e:
            st.warning("⚠️ Data files not found. Please run ETL pipeline first.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #475569; font-size: 0.75rem; font-weight: 500;">
            <p style="margin: 0.25rem 0;">🔐 Secure</p>
            <p style="margin: 0.25rem 0;">🚀 Fast</p>
            <p style="margin: 0.25rem 0;">🎯 Accurate</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "💬 AI Chat":
        show_ai_chat()
    elif page == "📊 Sales Analytics":
        show_sales_analytics()
    elif page == "👥 HR Analytics":
        show_hr_analytics()
    elif page == "💰 Finance Analytics":
        show_finance_analytics()
    elif page == "⚙️ Settings":
        show_settings()


def show_dashboard():
    """Executive Dashboard"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1e40af; font-size: 2.25rem; font-weight: 800; margin-bottom: 0.5rem;">Executive Dashboard</h1>
        <p style="color: #475569; font-size: 1rem; font-weight: 500;">Comprehensive overview of your business performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate executive summary
    orchestrator = st.session_state.get('orchestrator')
    if not orchestrator:
        st.error("⚠️ Orchestrator not initialized. Please check your API key configuration.")
        st.stop()
    
    with st.spinner("🤖 Generating executive summary with Google Gemini..."):
        summary = orchestrator.generate_executive_summary()
    
    st.markdown("""
    <div style="margin: 1.5rem 0;">
        <h3 style="color: #2563eb; font-size: 1.25rem; margin-bottom: 1rem; font-weight: 600;">📋 Executive Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="agent-response">{summary}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Load data
    try:
        with open('./data/processed/sales_kpis.json', 'r') as f:
            sales_data = json.load(f)
        with open('./data/processed/hr_kpis.json', 'r') as f:
            hr_data = json.load(f)
        with open('./data/processed/finance_kpis.json', 'r') as f:
            finance_data = json.load(f)
        
        # Three columns for overview
        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="color: #1e40af; font-size: 1.75rem; font-weight: 700; margin-bottom: 1rem;">Performance Overview</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #3b82f6;">
                <h3 style="color: #1e40af; font-size: 1.1rem; font-weight: 600; margin: 0;">📈 Sales Overview</h3>
            </div>
            """, unsafe_allow_html=True)
            fig = create_revenue_trend(sales_data)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #10b981;">
                <h3 style="color: #047857; font-size: 1.1rem; font-weight: 600; margin: 0;">👥 HR Overview</h3>
            </div>
            """, unsafe_allow_html=True)
            fig = create_department_bar(hr_data.get('by_department', {}))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #f59e0b;">
                <h3 style="color: #92400e; font-size: 1.1rem; font-weight: 600; margin: 0;">💰 Finance Overview</h3>
            </div>
            """, unsafe_allow_html=True)
            fig = create_financial_gauge(
                finance_data['summary'].get('financial_health_score', 75)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")


def show_ai_chat():
    """AI Chat Interface"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1e40af; font-size: 2.25rem; font-weight: 800; margin-bottom: 0.5rem;">AI Business Analyst</h1>
        <p style="color: #475569; font-size: 1rem; font-weight: 500;">Ask questions and get intelligent insights powered by Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Ask questions about sales, HR, finance, or get cross-domain insights. The AI will route your query to the appropriate specialist agent.")
    
    # Chat input with better styling
    st.markdown("""
    <div style="margin: 1.5rem 0;">
        <h3 style="color: #2563eb; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">Ask a Question</h3>
    </div>
    """, unsafe_allow_html=True)
    
    user_query = st.text_input(
        "Your question:", 
        placeholder="e.g., What are our biggest business challenges?",
        key="chat_input",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([1, 8], gap="small")
    with col1:
        ask_button = st.button("🚀 Ask AI", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear History", use_container_width=True)
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if ask_button and user_query:
        orchestrator = st.session_state.get('orchestrator')
        if not orchestrator:
            st.error("⚠️ Orchestrator not initialized. Please check your API key configuration.")
            st.stop()
        
        with st.spinner("🤖 Google Gemini is analyzing..."):
            result = orchestrator.process_query(user_query)
        
        # Add to history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append({
            "query": user_query,
            "response": result['response'],
            "agents": result.get('routed_to', [])
        })
    
    # Display chat history with professional styling
    chat_history = st.session_state.get('chat_history', [])
    if chat_history:
        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h3 style="color: #1e40af; font-size: 1.25rem; font-weight: 600;">Conversation History</h3>
        </div>
        """, unsafe_allow_html=True)
    
    for i, chat in enumerate(reversed(chat_history)):
        with st.container():
            # User message
            st.markdown(f"""
            <div class="chat-message chat-user">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <strong style="color: #1e40af; font-size: 0.9rem;">You</strong>
                </div>
                <p style="color: #1e40af; margin: 0; line-height: 1.6; font-weight: 500;">{chat['query']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # AI response
            agents_str = ', '.join([a.title() for a in chat['agents']])
            st.markdown(f"""
            <div class="chat-message chat-ai" style="margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                    <strong style="color: #047857; font-size: 0.9rem;">🤖 AI Analyst ({agents_str})</strong>
                </div>
                <div style="color: #1e293b; line-height: 1.7; font-weight: 400;">{chat["response"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if i < len(chat_history) - 1:
                st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)


def show_sales_analytics():
    """Sales Analytics Page"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1e40af; font-size: 2.25rem; font-weight: 800; margin-bottom: 0.5rem;">Sales Analytics</h1>
        <p style="color: #475569; font-size: 1rem; font-weight: 500;">Comprehensive sales performance metrics and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with open('./data/processed/sales_kpis.json', 'r') as f:
            sales_data = json.load(f)
        
        # KPI Cards
        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <h2 style="color: #1e40af; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">Key Performance Indicators</h2>
        </div>
        """, unsafe_allow_html=True)
        fig = create_kpi_cards(sales_data, 'sales')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visualizations
        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="color: #1e40af; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">Visual Analytics</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #3b82f6;">
                <h3 style="color: #1e40af; font-size: 1.1rem; font-weight: 600; margin: 0;">Revenue Trend</h3>
            </div>
            """, unsafe_allow_html=True)
            fig = create_revenue_trend(sales_data)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #10b981;">
                <h3 style="color: #047857; font-size: 1.1rem; font-weight: 600; margin: 0;">Customer Segments</h3>
            </div>
            """, unsafe_allow_html=True)
            fig = create_customer_segments_pie(sales_data.get('rfm_segments', {}))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # AI Insights
        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="color: #1e40af; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">🤖 AI-Generated Insights</h2>
            <p style="color: #475569; font-size: 0.95rem; font-weight: 500;">Click on any analysis button to get intelligent insights powered by Google Gemini</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        sales_agent = st.session_state.get('sales_agent')
        if not sales_agent:
            st.warning("⚠️ Sales agent not initialized. Please check your API key configuration.")
        else:
            with col1:
                if st.button("📈 Revenue Forecast", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = sales_agent.get_revenue_forecast()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
            
            with col2:
                if st.button("👥 Customer Segments", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = sales_agent.analyze_customer_segments()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
            
            with col3:
                if st.button("🏆 Top Products", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = sales_agent.analyze_top_products()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
        
        # Insights list
        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="color: #1e40af; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">Key Insights</h2>
        </div>
        """, unsafe_allow_html=True)
        
        for insight in sales_data.get('insights', []):
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1rem 1.5rem; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 0.75rem;">
                <p style="color: #1e293b; margin: 0; line-height: 1.6; font-weight: 400;">{insight}</p>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading sales data: {str(e)}")


def show_hr_analytics():
    """HR Analytics Page"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1e40af; font-size: 2.25rem; font-weight: 800; margin-bottom: 0.5rem;">HR Analytics</h1>
        <p style="color: #475569; font-size: 1rem; font-weight: 500;">Workforce insights, diversity metrics, and talent analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with open('./data/processed/hr_kpis.json', 'r') as f:
            hr_data = json.load(f)
        
        # KPI Cards
        st.subheader("Key Metrics")
        fig = create_kpi_cards(hr_data, 'hr')
        st.plotly_chart(fig, use_container_width=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Department Distribution")
            fig = create_department_bar(hr_data.get('by_department', {}))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Tenure Distribution")
            tenure_data = hr_data.get('tenure_distribution', {})
            fig = go.Figure(data=[go.Bar(
                x=list(tenure_data.keys()),
                y=list(tenure_data.values()),
                marker_color='#34a853',
                text=list(tenure_data.values()),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Employees: %{y}<extra></extra>'
            )])
            fig.update_layout(
                title={
                    'text': 'Employee Tenure',
                    'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                template='plotly_white',
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter, sans-serif', size=12, color='#64748b'),
                xaxis=dict(
                    gridcolor='#e2e8f0',
                    gridwidth=1,
                    showline=True,
                    linecolor='#cbd5e1',
                    linewidth=1
                ),
                yaxis=dict(
                    gridcolor='#e2e8f0',
                    gridwidth=1,
                    showline=True,
                    linecolor='#cbd5e1',
                    linewidth=1
                ),
                margin=dict(l=50, r=30, t=60, b=50)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Insights
        st.subheader("🤖 Gemini AI-Generated Insights")
        
        col1, col2, col3 = st.columns(3)
        
        hr_agent = st.session_state.get('hr_agent')
        if not hr_agent:
            st.warning("⚠️ HR agent not initialized. Please check your API key configuration.")
        else:
            with col1:
                if st.button("⚠️ Attrition Risk", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = hr_agent.analyze_attrition_risk()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
            
            with col2:
                if st.button("🌈 Diversity Analysis", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = hr_agent.diversity_analysis()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
            
            with col3:
                if st.button("⚙️ Workforce Optimization", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = hr_agent.workforce_optimization()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
        
        # Insights and recommendations
        st.subheader("Key Insights")
        for insight in hr_data.get('insights', []):
            st.markdown(f"• {insight}")
        
        st.subheader("Recommendations")
        for rec in hr_data.get('recommendations', []):
            st.info(rec)
        
    except Exception as e:
        st.error(f"Error loading HR data: {str(e)}")


def show_finance_analytics():
    """Finance Analytics Page"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1e40af; font-size: 2.25rem; font-weight: 800; margin-bottom: 0.5rem;">Finance Analytics</h1>
        <p style="color: #475569; font-size: 1rem; font-weight: 500;">Financial health, profitability, and cost optimization insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with open('./data/processed/finance_kpis.json', 'r') as f:
            finance_data = json.load(f)
        
        # KPI Cards
        st.subheader("Key Metrics")
        fig = create_kpi_cards(finance_data, 'finance')
        st.plotly_chart(fig, use_container_width=True)
        
        # Visualizations
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Revenue by Quarter")
            quarterly = finance_data.get('by_quarter', {})
            if quarterly:
                fig = go.Figure(data=[go.Bar(
                    x=list(quarterly.keys()),
                    y=list(quarterly.values()),
                    marker_color='#fbbc04',
                    text=[f'${v:,.0f}' for v in quarterly.values()],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
                )])
                fig.update_layout(
                    title={
                        'text': 'Quarterly Revenue',
                        'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'},
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    template='plotly_white',
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter, sans-serif', size=12, color='#64748b'),
                    xaxis=dict(
                        gridcolor='#e2e8f0',
                        gridwidth=1,
                        showline=True,
                        linecolor='#cbd5e1',
                        linewidth=1
                    ),
                    yaxis=dict(
                        gridcolor='#e2e8f0',
                        gridwidth=1,
                        showline=True,
                        linecolor='#cbd5e1',
                        linewidth=1
                    ),
                    margin=dict(l=50, r=30, t=60, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Financial Health")
            fig = create_financial_gauge(
                finance_data['summary'].get('financial_health_score', 75)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Insights
        st.subheader("🤖 Gemini AI-Generated Insights")
        
        col1, col2, col3 = st.columns(3)
        
        finance_agent = st.session_state.get('finance_agent')
        if not finance_agent:
            st.warning("⚠️ Finance agent not initialized. Please check your API key configuration.")
        else:
            with col1:
                if st.button("📊 Profitability Analysis", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = finance_agent.analyze_profitability()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
            
            with col2:
                if st.button("🏥 Health Assessment", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = finance_agent.financial_health_assessment()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
            
            with col3:
                if st.button("💡 Cost Optimization", use_container_width=True):
                    with st.spinner("Analyzing with Gemini..."):
                        result = finance_agent.cost_optimization_analysis()
                    st.markdown(f'<div class="agent-response">{result["response"]}</div>', 
                               unsafe_allow_html=True)
        
        # Insights and recommendations
        st.subheader("Key Insights")
        for insight in finance_data.get('insights', []):
            st.markdown(f"• {insight}")
        
        st.subheader("Recommendations")
        for rec in finance_data.get('recommendations', []):
            st.info(rec)
        
    except Exception as e:
        st.error(f"Error loading finance data: {str(e)}")


def show_settings():
    """Settings Page"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1e40af; font-size: 2.25rem; font-weight: 800; margin-bottom: 0.5rem;">Settings</h1>
        <p style="color: #475569; font-size: 1rem; font-weight: 500;">Configure API keys and view system information</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔑 Google AI API Configuration")
    
    current_key = os.getenv("GOOGLE_API_KEY", "")
    masked_key = current_key[:8] + "..." + current_key[-4:] if current_key else "Not set"
    
    st.info(f"Current API Key: {masked_key}")
    
    st.markdown("""
    **Get your free API key:**
    1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Click "Get API Key"
    3. Copy your key
    4. Add it below or to `.env` file
    """)
    
    new_key = st.text_input("Update Google API Key:", type="password")
    
    if st.button("💾 Save API Key"):
        if new_key:
            with open('.env', 'w') as f:
                f.write(f"GOOGLE_API_KEY={new_key}\n")
            st.success("✅ API key updated! Please restart the app.")
        else:
            st.warning("Please enter a valid API key")
    
    st.divider()
    
    st.subheader("🤖 Agent Status")
    
    agents = [
        ("Sales Agent", st.session_state.get('sales_agent')),
        ("HR Agent", st.session_state.get('hr_agent')),
        ("Finance Agent", st.session_state.get('finance_agent'))
    ]
    
    for name, agent in agents:
        if agent:
            status = agent.get_status()
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{name}**")
            with col2:
                st.write(f"ID: `{status['agent_id']}`")
            with col3:
                if status['data_loaded']:
                    st.success("✅ Active")
                else:
                    st.error("❌ Error")
        else:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{name}**")
            with col2:
                st.write("ID: N/A")
            with col3:
                st.error("❌ Not Initialized")
    
    st.divider()
    
    st.subheader("📊 System Information")
    
    st.markdown("""
    **AI Model:** Google Gemini 1.5 Flash  
    **Data Source:** AdventureWorks Dataset  
    **Architecture:** MCP Multi-Agent System  
    **Agents:** Sales, HR, Finance + Lead Orchestrator  
    **Frontend:** Streamlit  
    **Visualizations:** Plotly  
    """)
    
    if st.button("🔄 Reload Data"):
        st.cache_data.clear()
        st.success("✅ Cache cleared! Refresh the page.")


if __name__ == "__main__":
    main()
