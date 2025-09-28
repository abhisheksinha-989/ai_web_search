# 🔍 AI Search Assistant

A sophisticated web application that leverages multiple AI APIs to provide comprehensive research reports. The application searches across different sources, analyzes the content using advanced AI models, and presents detailed, well-structured research reports with a modern dark theme interface.

## 🌐 Live Website

**Access the live application here:** [https://ai-web-search.onrender.com/](https://ai-web-search.onrender.com/)

## 🌟 Features

### 🔬 Advanced Research Capabilities
- **Multi-Source Analysis**: Searches different sources simultaneously using Serper and You.com APIs
- **AI-Powered Synthesis**: Uses Qwen 2.5 72B model via OpenRouter for intelligent content analysis
- **Comprehensive Reports**: Generates detailed, well-structured research reports with proper citations
- **Smart Context Processing**: Analyzes up to 4000 characters of context from search results

### 🎨 Modern User Interface
- **Dark Theme**: Eye-friendly dark interface with purple/blue gradient accents
- **Responsive Design**: Fully responsive layout that works on desktop, tablet, and mobile
- **Real-time Updates**: Live progress indicators and smooth animations
- **Professional Typography**: Enhanced code blocks and markdown rendering

### ⚡ Technical Excellence
- **FastAPI Backend**: High-performance asynchronous API server
- **Docker Containerization**: Easy deployment with Docker
- **Environment Security**: Secure API key management with .env files
- **CORS Enabled**: Cross-origin resource sharing for flexible deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerized deployment)
- API keys for:
  - [OpenRouter](https://openrouter.ai/)
  - [Serper](https://serper.dev/)
  - [You.com](https://you.com/)

### Installation

#### Method 1: Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd research-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Run the application**
```bash
python run.py
# or
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Method 2: Docker Deployment

1. **Build the Docker image**
```bash
docker build -t research-assistant .
```

2. **Run the container**
```bash
docker run -p 8000:8000 --env-file .env research-assistant
```

### Access the Application

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 📁 Project Structure

```
research-assistant/
├── .env                     # Environment variables
├── .env.example            # Environment template
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── run.py                 # Application runner
├── app/                   # Backend application
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   └── research.py        # Research logic and API calls
└── frontend/              # Frontend assets
    ├── index.html         # Main HTML file
    ├── style.css          # Dark theme styles
    └── script.js          # Frontend logic
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Serper API Configuration  
SERPER_API_KEY=your_serper_api_key_here

# You.com API Configuration
YOUCOM_API_KEY=your_youcom_api_key_here
```

### API Services Overview

| Service | Purpose | Rate Limits | Cost |
|---------|---------|-------------|------|
| **OpenRouter** | AI model inference (Qwen 2.5 72B) | Varies by model | ~$0.008/1K tokens |
| **Serper** | Google search results | 2,500 queries/month free | $50/10K queries |
| **You.com** | Alternative search results | 1,000 queries/month free | $49/10K queries |

## 🎯 Usage Guide

### Basic Research Query

1. **Enter your research question** in the search box
2. **Click "Research"** to start the analysis
3. **Wait for processing** (typically 30-60 seconds)
4. **Review the comprehensive report** with sources and statistics

### Example Queries

- "What are the latest developments in quantum computing?"
- "Compare machine learning frameworks for natural language processing"
- "Explain the implications of blockchain technology in healthcare"
- "What are the best practices for React performance optimization?"

### Response Structure

Each research report includes:

1. **Executive Summary**: Concise overview of findings
2. **Detailed Analysis**: Section-by-section breakdown
3. **Source Citations**: Proper attribution with links
4. **Statistics**: Word count, processing time, sources analyzed

## 🔌 API Reference

### POST /api/research

Submit a research query and receive a comprehensive report.

**Request:**
```json
{
  "query": "What are the best LLMs developed to date?"
}
```

**Response:**
```json
{
  "summary": "Comprehensive research report in markdown format...",
  "sources": [
    {
      "title": "Source Title",
      "snippet": "Content snippet",
      "link": "https://example.com",
      "source": "Serper"
    }
  ],
  "word_count": 1250,
  "processing_time": 45.2
}
```

### GET /api/health

Health check endpoint to verify service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Research Assistant API"
}
```

## 🛠️ Development

### Adding New Search APIs

1. **Create a new search function** in `app/research.py`:
```python
def search_with_new_api(query, api_key):
    # Implementation
    return results
```

2. **Update the extraction logic** in `extract_search_results()`
3. **Modify the main research function** in `get_research_answer()`

### Customizing the AI Prompt

Edit the `create_prompt()` function in `app/research.py` to modify the research guidelines and response format.

### Styling Customization

The dark theme can be customized by modifying CSS variables in `frontend/style.css`:

```css
:root {
    --primary: #8b5cf6;        /* Main brand color */
    --background: #0f0f23;     /* Background color */
    --surface: #1a1a2e;        /* Card backgrounds */
    --text: #e2e8f0;           /* Primary text color */
}
```

## 📊 Performance Optimization

### Caching Strategies

```python
# Example caching implementation
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_cached_research(query: str):
    query_hash = hashlib.md5(query.encode()).hexdigest()
    # Cache implementation
```

### Rate Limiting

```python
# Example rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

## 🔒 Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables for all sensitive data
- Regularly rotate API keys
- Monitor API usage for anomalies

### Input Validation
```python
from pydantic import BaseModel, constr

class ResearchRequest(BaseModel):
    query: constr(min_length=5, max_length=500)
```

## 🐛 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'research'**
- Ensure you're running from the project root directory
- Check that the `app` directory contains `__init__.py`

**API Key Errors**
- Verify all API keys are set in the `.env` file
- Check API key validity and quotas

**Slow Response Times**
- Research typically takes 30-60 seconds
- Consider implementing caching for repeated queries

**CORS Errors**
- Ensure the frontend is served from the correct origin
- Check CORS configuration in `app/main.py`

### Debug Mode

Enable detailed logging by setting environment variables:

```bash
export UVICORN_LOG_LEVEL=debug
export PYTHONPATH=.
```

## 📈 Monitoring and Analytics

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Performance Metrics

- Query processing time
- Source analysis count
- Token usage statistics
- Error rates and types

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a pull request

### Code Standards

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Include docstrings for all functions
- Write tests for new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter** for providing access to advanced AI models
- **Serper** and **You.com** for search API services
- **FastAPI** team for the excellent web framework
- **Qwen** team for the powerful language model

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs`
- Review the troubleshooting section above

---

**⭐ If you find this project useful, please give it a star on GitHub!**

---
