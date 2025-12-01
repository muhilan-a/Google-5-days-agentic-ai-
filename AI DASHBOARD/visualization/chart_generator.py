"""
Chart Generation for Streamlit Dashboard
Creates interactive visualizations using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List


def create_revenue_trend(data: Dict[str, Any]) -> go.Figure:
    """Create revenue trend line chart"""
    
    # Extract monthly data
    by_month = data.get('by_month', {})
    
    if by_month:
        # Parse month data
        months = list(by_month.keys())
        revenue = list(by_month.values())
    else:
        # Fallback demo data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [50000, 62000, 58000, 71000, 69000, 78000]
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=revenue,
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#4285f4', width=3),
        marker=dict(size=10, color='#4285f4'),
        fill='tozeroy',
        fillcolor='rgba(66, 133, 244, 0.2)',
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': 'Revenue Trend Over Time',
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Period',
        yaxis_title='Revenue ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        showlegend=False,
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
    
    return fig


def create_customer_segments_pie(rfm_data: Dict[str, int]) -> go.Figure:
    """Create customer segmentation pie chart"""
    
    if not rfm_data or len(rfm_data) == 0:
        # Fallback demo data
        rfm_data = {
            'Champions': 120,
            'Regular': 180,
            'At Risk': 75,
            'New': 45
        }
    
    labels = list(rfm_data.keys())
    values = list(rfm_data.values())
    
    # Color scheme
    colors = ['#34a853', '#4285f4', '#fbbc04', '#ea4335']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors[:len(labels)]),
        textinfo='label+percent',
        textfont_size=12,
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': 'Customer Segmentation (RFM Analysis)',
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        template='plotly_white',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(family='Inter, sans-serif', size=11, color='#334155'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=12, color='#64748b'),
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    return fig


def create_department_bar(dept_data: Dict[str, int]) -> go.Figure:
    """Create department distribution bar chart"""
    
    if not dept_data or len(dept_data) == 0:
        # Fallback demo data
        dept_data = {
            'Engineering': 45,
            'Sales': 32,
            'Marketing': 18,
            'Operations': 25,
            'HR': 12,
            'Finance': 15
        }
    
    departments = list(dept_data.keys())
    employee_count = list(dept_data.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=departments,
            y=employee_count,
            marker=dict(
                color=employee_count,
                colorscale='Viridis',
                showscale=False
            ),
            text=employee_count,
            textposition='outside',
            textfont=dict(size=12),
            hovertemplate='<b>%{x}</b><br>Employees: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Employee Distribution by Department',
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Department',
        yaxis_title='Number of Employees',
        template='plotly_white',
        height=400,
        showlegend=False,
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
    
    return fig


def create_financial_gauge(health_score: float) -> go.Figure:
    """Create financial health gauge chart"""
    
    # Ensure health_score is valid
    if health_score is None or health_score < 0:
        health_score = 75.0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Financial Health Score", 'font': {'size': 20}},
        number={'suffix': "/100", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "darkblue"},
            'bar': {'color': "#4285f4", 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffcccc'},
                {'range': [40, 70], 'color': '#ffffcc'},
                {'range': [70, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        template='plotly_white',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=12, color='#64748b')
    )
    
    return fig


def create_kpi_cards(data: Dict[str, Any], domain: str) -> go.Figure:
    """Create KPI cards visualization"""
    
    summary = data.get('summary', {})
    
    if domain == 'sales':
        metrics = {
            'Total Revenue': f"${summary.get('total_revenue', 0):,.0f}",
            'Total Orders': f"{summary.get('total_orders', 0):,}",
            'Avg Order Value': f"${summary.get('average_order_value', 0):,.2f}",
            'Customer LTV': f"${summary.get('customer_lifetime_value', 0):,.2f}"
        }
    elif domain == 'hr':
        metrics = {
            'Total Employees': f"{summary.get('total_employees', 0):,}",
            'Avg Tenure': f"{summary.get('average_tenure_years', 0):.1f} yrs",
            'High Risk %': f"{summary.get('high_risk_percentage', 0):.1f}%",
            'Diversity Ratio': f"{summary.get('gender_diversity_ratio', 0):.1f}%"
        }
    else:  # finance
        metrics = {
            'Total Revenue': f"${summary.get('total_revenue', 0):,.0f}",
            'Gross Margin': f"{summary.get('gross_margin_percentage', 0):.1f}%",
            'Tax Rate': f"{summary.get('effective_tax_rate', 0):.1f}%",
            'Health Score': f"{summary.get('financial_health_score', 0):.1f}/100"
        }
    
    # Create subplot grid
    fig = make_subplots(
        rows=1, 
        cols=len(metrics),
        specs=[[{'type': 'indicator'}] * len(metrics)],
        horizontal_spacing=0.05
    )
    
    # Add indicators
    for i, (label, value) in enumerate(metrics.items(), 1):
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=1,  # Dummy value
                title={
                    'text': f"<b>{label}</b><br><span style='font-size:24px'>{value}</span>",
                    'font': {'size': 14}
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=i
        )
    
    fig.update_layout(
        template='plotly_white',
        height=150,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=11, color='#334155')
    )
    
    return fig


def create_tenure_distribution(tenure_data: Dict[str, int]) -> go.Figure:
    """Create tenure distribution bar chart"""
    
    if not tenure_data or len(tenure_data) == 0:
        tenure_data = {
            '0-2 years': 45,
            '2-5 years': 38,
            '5-10 years': 28,
            '10+ years': 20
        }
    
    categories = list(tenure_data.keys())
    counts = list(tenure_data.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=counts,
            marker_color='#34a853',
            text=counts,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Employees: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Employee Tenure Distribution',
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Tenure Range',
        yaxis_title='Number of Employees',
        template='plotly_white',
        height=400,
        showlegend=False,
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
    
    return fig


def create_quarterly_revenue(quarterly_data: Dict[str, float]) -> go.Figure:
    """Create quarterly revenue bar chart"""
    
    if not quarterly_data or len(quarterly_data) == 0:
        quarterly_data = {
            '2024-Q1': 250000,
            '2024-Q2': 280000,
            '2024-Q3': 265000,
            '2024-Q4': 310000
        }
    
    quarters = list(quarterly_data.keys())
    revenue = list(quarterly_data.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=quarters,
            y=revenue,
            marker_color='#fbbc04',
            text=[f'${v:,.0f}' for v in revenue],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Quarterly Revenue',
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Quarter',
        yaxis_title='Revenue ($)',
        template='plotly_white',
        height=400,
        showlegend=False,
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
    
    return fig


def create_top_products_bar(products_data: Dict[str, float], top_n: int = 10) -> go.Figure:
    """Create top products horizontal bar chart"""
    
    if not products_data or len(products_data) == 0:
        products_data = {
            'Product A': 125000,
            'Product B': 98000,
            'Product C': 87000,
            'Product D': 76000,
            'Product E': 65000
        }
    
    # Sort and get top N
    sorted_products = sorted(products_data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    products = [p[0] for p in sorted_products]
    revenue = [p[1] for p in sorted_products]
    
    fig = go.Figure(data=[
        go.Bar(
            y=products,
            x=revenue,
            orientation='h',
            marker=dict(
                color=revenue,
                colorscale='Blues',
                showscale=False
            ),
            text=[f'${v:,.0f}' for v in revenue],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': f'Top {len(products)} Products by Revenue',
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Revenue ($)',
        yaxis_title='Product',
        template='plotly_white',
        height=400,
        showlegend=False,
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
            categoryorder='total ascending',
            gridcolor='#e2e8f0',
            gridwidth=1,
            showline=True,
            linecolor='#cbd5e1',
            linewidth=1
        ),
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    return fig


# Export all functions
__all__ = [
    'create_revenue_trend',
    'create_customer_segments_pie',
    'create_department_bar',
    'create_financial_gauge',
    'create_kpi_cards',
    'create_tenure_distribution',
    'create_quarterly_revenue',
    'create_top_products_bar'
]
