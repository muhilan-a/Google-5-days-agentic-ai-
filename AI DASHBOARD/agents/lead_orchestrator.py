"""
Lead Orchestrator Agent using Google Gemini
Coordinates multiple specialist agents
"""

from typing import Dict, Any, List
import os
import json
import re
import google.generativeai as genai
from .sales_agent import SalesAIAgent
from .hr_agent import HRAIAgent
from .finance_agent import FinanceAIAgent


class LeadOrchestratorAgent:
    """Coordinates multiple specialist agents using Gemini"""
    
    def __init__(self, api_key: str = None):
        self.agent_id = "lead_orchestrator_001"
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        # Initialize sub-agents
        self.sales_agent = SalesAIAgent(api_key=self.api_key)
        self.hr_agent = HRAIAgent(api_key=self.api_key)
        self.finance_agent = FinanceAIAgent(api_key=self.api_key)
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process query by routing to appropriate agents"""
        
        if not self.model:
            return self._fallback_routing(query)
        
        try:
            # Intelligent routing using Gemini
            required_agents = self._route_query(query)
            
            # Collect responses from each agent
            agent_responses = {}
            
            if "sales" in required_agents:
                agent_responses["sales"] = self.sales_agent.process_query(query)
            
            if "hr" in required_agents:
                agent_responses["hr"] = self.hr_agent.process_query(query)
            
            if "finance" in required_agents:
                agent_responses["finance"] = self.finance_agent.process_query(query)
            
            # Synthesize responses if multiple agents
            if len(agent_responses) > 1:
                synthesized = self._synthesize_responses(query, agent_responses)
            else:
                synthesized = list(agent_responses.values())[0]['response']
            
            return {
                "success": True,
                "response": synthesized,
                "routed_to": required_agents,
                "agent_responses": agent_responses
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Error: {str(e)}",
                "routed_to": [],
                "agent_responses": {}
            }
    
    def _route_query(self, query: str) -> List[str]:
        """Use Gemini to intelligently route query"""
        
        routing_prompt = f"""Analyze this business intelligence query and determine which specialist agents should handle it.

User Query: "{query}"

Available Specialist Agents:
- sales: Handles revenue, customers, orders, products, sales trends, customer segmentation
- hr: Handles employees, attrition, workforce, diversity, talent, organizational health
- finance: Handles profitability, costs, financial health, margins, budgets, cash flow

Instructions:
- Return ONLY a comma-separated list of agent names needed
- If query mentions multiple domains, include all relevant agents
- Examples: "sales" or "sales,finance" or "sales,hr,finance"

Your response (agent names only):"""
        
        try:
            response = self.model.generate_content(routing_prompt)
            agents_text = response.text.strip().lower()
            
            # Parse agent names
            agents = []
            if 'sales' in agents_text:
                agents.append('sales')
            if 'hr' in agents_text:
                agents.append('hr')
            if 'finance' in agents_text:
                agents.append('finance')
            
            # Default to all agents if none detected
            if not agents:
                agents = ['sales', 'hr', 'finance']
            
            return agents
            
        except Exception as e:
            print(f"Routing error: {e}")
            return ['sales', 'hr', 'finance']  # Fallback
    
    def _synthesize_responses(self, query: str, agent_responses: Dict[str, Any]) -> str:
        """Use Gemini to synthesize multiple agent responses"""
        
        # Build responses text
        responses_text = []
        for agent, resp in agent_responses.items():
            if resp.get('success'):
                responses_text.append(f"**{agent.upper()} SPECIALIST:**\n{resp['response']}")
        
        combined_responses = "\n\n---\n\n".join(responses_text)
        
        synthesis_prompt = f"""You are a Lead Business Intelligence Coordinator synthesizing insights from multiple specialists.

User Question: "{query}"

Specialist Responses:
{combined_responses}

Your Task:
1. Create a unified, coherent response that directly answers the user's question
2. Integrate insights from all specialists
3. Identify cross-domain connections and patterns
4. Provide clear, executive-level recommendations
5. Keep the response concise and actionable

Synthesized Response:"""
        
        try:
            response = self.model.generate_content(synthesis_prompt)
            return response.text
            
        except Exception as e:
            print(f"Synthesis error: {e}")
            return combined_responses  # Fallback
    
    def _fallback_routing(self, query: str) -> Dict[str, Any]:
        """Simple keyword-based routing when AI unavailable"""
        query_lower = query.lower()
        
        responses = {}
        
        # Keyword-based routing
        if any(word in query_lower for word in ['revenue', 'sales', 'customer', 'product', 'order']):
            responses['sales'] = self.sales_agent.process_query(query)
        
        if any(word in query_lower for word in ['employee', 'hr', 'attrition', 'workforce', 'talent', 'diversity']):
            responses['hr'] = self.hr_agent.process_query(query)
        
        if any(word in query_lower for word in ['profit', 'finance', 'cost', 'margin', 'budget', 'financial']):
            responses['finance'] = self.finance_agent.process_query(query)
        
        # If no keywords matched, query all agents
        if not responses:
            responses = {
                'sales': self.sales_agent.process_query(query),
                'hr': self.hr_agent.process_query(query),
                'finance': self.finance_agent.process_query(query)
            }
        
        # Combine responses
        combined = "\n\n".join([
            f"**{k.upper()} ANALYSIS:**\n{v['response']}" 
            for k, v in responses.items() if v.get('success')
        ])
        
        return {
            "success": True,
            "response": combined,
            "routed_to": list(responses.keys()),
            "agent_responses": responses
        }
    
    def generate_executive_summary(self) -> str:
        """Generate comprehensive executive summary using Gemini"""
        
        # Get insights from all agents
        sales_insights = self.sales_agent.get_insights()
        hr_insights = self.hr_agent.get_insights()
        finance_insights = self.finance_agent.get_insights()
        
        if not self.model:
            # Fallback formatting
            return f"""**EXECUTIVE SUMMARY**

**SALES INSIGHTS:**
{chr(10).join(['• ' + i for i in sales_insights])}

**HR INSIGHTS:**
{chr(10).join(['• ' + i for i in hr_insights])}

**FINANCE INSIGHTS:**
{chr(10).join(['• ' + i for i in finance_insights])}"""
        
        summary_prompt = f"""Create a comprehensive executive dashboard summary for business leadership.

SALES INSIGHTS:
{chr(10).join(['- ' + i for i in sales_insights])}

HR/PEOPLE INSIGHTS:
{chr(10).join(['- ' + i for i in hr_insights])}

FINANCE INSIGHTS:
{chr(10).join(['- ' + i for i in finance_insights])}

Create an executive summary with:
1. **Overall Business Health Status** (2-3 sentences)
2. **Top 3 Strengths** (bullet points)
3. **Top 3 Concerns/Risks** (bullet points)
4. **Strategic Recommendations** (3-5 actionable items)

Format: Professional, concise, executive-level language."""
        
        try:
            response = self.model.generate_content(summary_prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def cross_domain_analysis(self, question: str) -> str:
        """Perform cross-domain analysis using Gemini"""
        
        # Gather all data
        sales_data = self.sales_agent.kpi_data
        hr_data = self.hr_agent.kpi_data
        finance_data = self.finance_agent.kpi_data
        
        if not self.model:
            return "Cross-domain analysis requires AI features. Please set GOOGLE_API_KEY."
        
        analysis_prompt = f"""Perform cross-domain business intelligence analysis.

Question: {question}

SALES DATA:
{json.dumps(sales_data.get('summary', {}), indent=2)}

HR DATA:
{json.dumps(hr_data.get('summary', {}), indent=2)}

FINANCE DATA:
{json.dumps(finance_data.get('summary', {}), indent=2)}

Task:
1. Analyze relationships and correlations across Sales, HR, and Finance
2. Identify causal connections (e.g., how HR metrics affect finance)
3. Provide integrated insights that span multiple domains
4. Recommend cross-functional initiatives

Analysis:"""
        
        try:
            response = self.model.generate_content(analysis_prompt)
            return response.text
        except Exception as e:
            return f"Analysis error: {str(e)}"
