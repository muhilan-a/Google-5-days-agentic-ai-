"""
AI-Powered Finance Agent using Google Gemini
"""

from typing import Dict, Any
import os
import json
import google.generativeai as genai
from .base_agent import BaseAgent


class FinanceAIAgent(BaseAgent):
    """AI-powered Finance Intelligence Agent using Gemini"""
    
    def __init__(self, api_key: str = None):
        super().__init__(
            agent_id="finance_ai_agent_001",
            agent_type="finance",
            kpi_file_path="./data/processed/finance_kpis.json"
        )
        
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            self.logger.warning("No Google API key found. AI features disabled.")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process finance query using Gemini AI"""
        
        if not self.model:
            return {
                "success": False,
                "response": "AI features are disabled. Please set GOOGLE_API_KEY.",
                "data": self.kpi_data.get('summary', {})
            }
        
        try:
            system_context = self._create_system_context()
            full_prompt = f"""{system_context}

Finance Data:
{json.dumps(self.kpi_data, indent=2)}

User Question: {query}

Provide CFO-level financial analysis."""
            
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
                "response": f"Error: {str(e)}",
                "data": {}
            }
    
    def _create_system_context(self) -> str:
        """Create system context for finance agent"""
        return """You are an expert Financial Intelligence AI Agent specializing in:
- Financial performance analysis and reporting
- Profitability and margin optimization
- Cost management and efficiency
- Financial forecasting and budgeting
- Cash flow and working capital management
- Financial risk assessment

Your role:
1. Analyze financial KPIs with strategic context
2. Identify financial risks and opportunities
3. Provide actionable financial recommendations
4. Explain complex financial concepts clearly
5. Support data-driven financial decision-making

Communication style: Precise, numbers-focused, CFO-level analytical, professional."""
    
    def analyze_profitability(self) -> Dict[str, Any]:
        """Analyze profitability metrics"""
        query = """Analyze profitability metrics in the data:
1. Evaluate gross margin and profitability trends
2. Identify margin improvement opportunities
3. Compare against industry benchmarks (typical ranges)
4. Analyze cost structure efficiency
5. Recommend pricing or cost optimization strategies"""
        return self.process_query(query)
    
    def financial_health_assessment(self) -> Dict[str, Any]:
        """Assess overall financial health"""
        query = """Based on the financial health score and all metrics:
1. Provide comprehensive financial health assessment
2. Identify key strengths and weaknesses
3. Analyze sustainability and growth capacity
4. Recommend actions to improve financial position
5. Assess readiness for growth or investment"""
        return self.process_query(query)
    
    def cost_optimization_analysis(self) -> Dict[str, Any]:
        """Analyze cost optimization opportunities"""
        query = """Analyze cost structure:
1. Identify high-cost areas (tax, freight, operations)
2. Benchmark costs against revenue
3. Recommend specific cost reduction strategies
4. Assess impact on margins
5. Prioritize quick wins vs long-term initiatives"""
        return self.process_query(query)
