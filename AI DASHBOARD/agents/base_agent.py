"""
Base Agent for MCP Multi-Agent System
Uses Google Gemini AI
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
import json

logging.basicConfig(level=logging.INFO)


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, agent_id: str, agent_type: str, kpi_file_path: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.kpi_file_path = kpi_file_path
        self.kpi_data = self.load_kpis()
        self.logger = logging.getLogger(f"{agent_type}.{agent_id}")
        self.conversation_history = []
    
    def load_kpis(self) -> Dict[str, Any]:
        """Load KPI data from JSON file"""
        try:
            with open(self.kpi_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"KPI file not found: {self.kpi_file_path}")
            return {"summary": {}, "insights": []}
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in: {self.kpi_file_path}")
            return {"summary": {}, "insights": []}
    
    @abstractmethod
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process user query - must be implemented by child classes"""
        pass
    
    def get_summary(self) -> Dict[str, Any]:
        """Get KPI summary"""
        return self.kpi_data.get('summary', {})
    
    def get_insights(self) -> List[str]:
        """Get insights list"""
        return self.kpi_data.get('insights', [])
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "active",
            "data_loaded": bool(self.kpi_data)
        }
