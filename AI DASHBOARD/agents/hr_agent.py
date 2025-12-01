"""
AI-Powered HR Agent using Google Gemini
"""

from typing import Dict, Any
import os
import json
import google.generativeai as genai
from .base_agent import BaseAgent


class HRAIAgent(BaseAgent):
    """AI-powered HR Intelligence Agent using Gemini"""
    
    def __init__(self, api_key: str = None):
        super().__init__(
            agent_id="hr_ai_agent_001",
            agent_type="hr",
            kpi_file_path="./data/processed/hr_kpis.json"
        )
        
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            self.logger.warning("No Google API key found. AI features disabled.")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process HR query using Gemini AI"""
        
        if not self.model:
            return {
                "success": False,
                "response": "AI features are disabled. Please set GOOGLE_API_KEY.",
                "data": self.kpi_data.get('summary', {})
            }
        
        try:
            system_context = self._create_system_context()
            full_prompt = f"""{system_context}

HR Data:
{json.dumps(self.kpi_data, indent=2)}

User Question: {query}

Provide empathetic, data-driven HR analysis."""
            
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
        """Create system context for HR agent"""
        return """You are an expert People Analytics AI Agent specializing in:
- Workforce planning and optimization
- Employee retention and attrition analysis
- Diversity, equity, and inclusion metrics
- Talent acquisition and development
- Organizational health assessment

Your role:
1. Analyze HR metrics with people-centric insights
2. Identify talent risks and opportunities
3. Recommend evidence-based HR interventions
4. Predict workforce trends and needs
5. Balance business needs with employee wellbeing

Communication style: Empathetic, data-driven, actionable, focused on both organizational and employee success."""
    
    def analyze_attrition_risk(self) -> Dict[str, Any]:
        """Analyze attrition risks"""
        query = """Based on the HR data, especially risk scores and attrition metrics:
1. Identify high-risk employee segments
2. Analyze root causes of attrition risk
3. Recommend targeted retention interventions
4. Estimate potential cost impact of attrition
5. Suggest preventive measures"""
        return self.process_query(query)
    
    def diversity_analysis(self) -> Dict[str, Any]:
        """Analyze diversity metrics"""
        query = """Analyze the diversity metrics (gender, department distribution):
1. Assess current diversity levels
2. Identify gaps and underrepresented groups
3. Compare to industry benchmarks (if applicable)
4. Recommend inclusive hiring practices
5. Suggest concrete diversity improvement strategies"""
        return self.process_query(query)
    
    def workforce_optimization(self) -> Dict[str, Any]:
        """Recommend workforce optimization"""
        query = """Based on workforce metrics:
1. Analyze current workforce composition and efficiency
2. Identify potential over/under-staffed departments
3. Recommend optimal workforce allocation
4. Suggest succession planning strategies
5. Propose talent development initiatives"""
        return self.process_query(query)
