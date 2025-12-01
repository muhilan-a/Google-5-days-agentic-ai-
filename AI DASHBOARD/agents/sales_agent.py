"""
AI-Powered Sales Agent using Google Gemini
"""

from typing import Dict, Any
import os
import json
import google.generativeai as genai
from .base_agent import BaseAgent


class SalesAIAgent(BaseAgent):
    """AI-powered Sales Intelligence Agent using Gemini"""
    
    def __init__(self, api_key: str = None):
        super().__init__(
            agent_id="sales_ai_agent_001",
            agent_type="sales",
            kpi_file_path="./data/processed/sales_kpis.json"
        )
        
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use Gemini 1.5 Flash for faster responses, or gemini-1.5-pro for better quality
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.chat = None  # Will be initialized when needed
        else:
            self.model = None
            self.logger.warning("No Google API key found. AI features disabled.")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process sales query using Gemini AI"""
        
        if not self.model:
            return {
                "success": False,
                "response": "AI features are disabled. Please set GOOGLE_API_KEY.",
                "data": self.kpi_data.get('summary', {})
            }
        
        try:
            # Create context-aware prompt
            system_context = self._create_system_context()
            full_prompt = f"""{system_context}

Sales Data:
{json.dumps(self.kpi_data, indent=2)}

User Question: {query}

Provide a comprehensive, data-driven analysis."""
            
            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)
            
            return {
                "success": True,
                "response": response.text,
                "agent": self.agent_id,
                "data": self.kpi_data.get('summary', {})
            }
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {str(e)}")
            return {
                "success": False,
                "response": f"Error processing query: {str(e)}",
                "data": {}
            }
    
    def _create_system_context(self) -> str:
        """Create system context for sales agent"""
        return """You are an expert Sales Intelligence AI Agent with deep expertise in:
- Revenue analysis and forecasting
- Customer segmentation and behavior analysis (RFM methodology)
- Sales performance optimization
- Market trends and competitive insights
- Customer lifetime value strategies

Your role:
1. Analyze sales data with business context
2. Identify growth opportunities and risks
3. Provide actionable, specific recommendations
4. Explain complex metrics in business-friendly language
5. Use actual numbers from the data provided

Communication style: Professional, data-driven, concise, actionable."""
    
    def get_revenue_forecast(self) -> Dict[str, Any]:
        """Generate revenue forecast"""
        query = """Analyze the revenue trends in the data. Based on historical patterns:
1. Forecast revenue for the next quarter
2. Provide confidence level for your forecast
3. Identify key factors influencing the forecast
4. Recommend actions to achieve or exceed projections"""
        return self.process_query(query)
    
    def analyze_customer_segments(self) -> Dict[str, Any]:
        """Analyze customer segmentation"""
        query = """Analyze the RFM customer segments in the data:
1. Characterize each segment (Champions, Regular, At Risk)
2. Identify which segments need immediate attention
3. Recommend specific strategies for each segment
4. Suggest how to move customers to higher-value segments"""
        return self.process_query(query)
    
    def analyze_top_products(self) -> Dict[str, Any]:
        """Analyze top products"""
        query = """Analyze the top products data:
1. Identify best and worst performers
2. Explain why certain products succeed
3. Recommend product strategy adjustments
4. Identify cross-sell and upsell opportunities"""
        return self.process_query(query)
