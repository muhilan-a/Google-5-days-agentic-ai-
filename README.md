# 🤖 AI-Powered Business Intelligence Dashboard

A comprehensive multi-agent Business Intelligence dashboard powered by Google Gemini AI, featuring intelligent analytics for Sales, HR, and Finance domains using the AdventureWorks dataset.

## ✨ Features

- **Multi-Agent Architecture**: Specialized AI agents for Sales, HR, and Finance analytics
- **Google Gemini AI Integration**: Powered by Google Gemini 2.5 Flash for intelligent insights
- **Interactive Dashboard**: Beautiful Streamlit-based web interface
- **Real-time Analytics**: Dynamic visualizations using Plotly
- **ETL Pipeline**: Automated data processing from AdventureWorks dataset
- **Secure API Key Management**: Environment-based configuration

## 🏗️ Architecture

The system uses a **Multi-Agent MCP (Model Context Protocol) Architecture**:

- **Lead Orchestrator Agent**: Routes queries to appropriate specialist agents
- **Sales AI Agent**: Analyzes sales data, revenue trends, customer segments
- **HR AI Agent**: Provides workforce insights, attrition analysis, diversity metrics
- **Finance AI Agent**: Financial health assessment, profitability analysis, cost optimization

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- AdventureWorks dataset (Excel files in `data/raw/` directory)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "AI Projects/Ai Dashboard"
   ```

2. **Navigate to the AI DASHBOARD directory**
   ```bash
   cd "AI DASHBOARD"
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `env.template` to `.env` in the `AI DASHBOARD` directory
   ```bash
   cd "AI DASHBOARD"
   cp env.template .env
   ```
   - Open `.env` and add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```

5. **Run the ETL pipeline** (if data processing is needed)
   ```bash
   python etl/adventureworks_etl.py
   ```

6. **Launch the dashboard**
   ```bash
   streamlit run app.py
   ```

## 🔐 Environment Variables

Create a `.env` file in the `AI DASHBOARD` directory with the following:

```env
GOOGLE_API_KEY=your-google-gemini-api-key-here
```

**Quick Setup:**
1. Copy the template file: `cp env.template .env`
2. Edit `.env` and replace `your-google-gemini-api-key-here` with your actual API key
3. Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

**Important Security Notes:**
- Never commit your `.env` file to version control
- The `.env` file is already included in `.gitignore`
- Use `env.template` as a reference for the required format

## 📁 Project Structure

```
AI DASHBOARD/
├── agents/              # AI agent implementations
│   ├── base_agent.py
│   ├── sales_agent.py
│   ├── hr_agent.py
│   ├── finance_agent.py
│   └── lead_orchestrator.py
├── data/
│   ├── raw/            # Raw AdventureWorks Excel files
│   └── processed/      # Processed KPI JSON files
├── etl/                # ETL pipeline scripts
├── visualization/      # Chart generation modules
├── app.py             # Main Streamlit application
└── requirements.txt   # Python dependencies
```

## 🎯 Usage

### Starting the Dashboard

1. Ensure your `.env` file is configured with your Google API key
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to the URL shown (typically `http://localhost:8501`)

### Dashboard Pages

- **🏠 Dashboard**: Executive overview with AI-generated summaries
- **💬 AI Chat**: Interactive chat with AI business analysts
- **📊 Sales Analytics**: Sales metrics, revenue trends, customer analysis
- **👥 HR Analytics**: Workforce insights, attrition risk, diversity metrics
- **💰 Finance Analytics**: Financial health, profitability, cost optimization
- **⚙️ Settings**: API configuration and system information

### Using the AI Chat

Ask natural language questions such as:
- "What are our biggest business challenges?"
- "Show me revenue trends for the last quarter"
- "Analyze employee attrition risk"
- "What's our financial health score?"

## 🛠️ Development

### Running the ETL Pipeline

Process raw AdventureWorks data into KPI JSON files:

```bash
python etl/adventureworks_etl.py
```

This generates:
- `data/processed/sales_kpis.json`
- `data/processed/hr_kpis.json`
- `data/processed/finance_kpis.json`

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `process_query()` method
3. Register the agent in `LeadOrchestratorAgent`
4. Add UI components in `app.py`

## 📦 Dependencies

- `streamlit==1.31.0` - Web framework
- `google-generativeai==0.3.2` - Google Gemini AI
- `pandas==2.1.4` - Data manipulation
- `plotly==5.18.0` - Interactive visualizations
- `python-dotenv==1.0.0` - Environment variable management
- `Pillow==10.2.0` - Image processing
- `protobuf==4.25.1` - Protocol buffers

## 🔒 Security Best Practices

1. **Never commit `.env` files** - They contain sensitive API keys
2. **Use environment variables** - All API keys are loaded from `.env`
3. **Rotate API keys regularly** - Update your keys if compromised
4. **Set API key restrictions** - Use Google Cloud Console to limit key usage

## 🐛 Troubleshooting

### API Key Not Found
- Ensure `.env` file exists in the `AI DASHBOARD` directory
- Verify `GOOGLE_API_KEY` is set correctly
- Restart the Streamlit app after creating/updating `.env`

### Data Files Not Found
- Run the ETL pipeline: `python etl/adventureworks_etl.py`
- Ensure Excel files are in `data/raw/` directory

### Import Errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows existing style conventions
- Environment variables are never committed
- New features include appropriate documentation

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using Google Gemini AI and Streamlit**

