"""
Visualization module for AI BI Dashboard
"""

from .chart_generator import (
    create_revenue_trend,
    create_customer_segments_pie,
    create_department_bar,
    create_financial_gauge,
    create_kpi_cards,
    create_tenure_distribution,
    create_quarterly_revenue,
    create_top_products_bar
)

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
