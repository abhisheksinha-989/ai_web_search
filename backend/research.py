import requests
import json
import http.client
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

YOUCOM_API_KEY = os.getenv("YOUCOM_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_with_openrouter(prompt, api_key=OPENROUTER_API_KEY, max_tokens=2500):
    """Generate response using Qwen 2.5 via OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "Research Assistant"
    }
    payload = {
        "model": "qwen/qwen-2.5-72b-instruct",
        "messages": [
            {"role": "system", "content": "You are an expert research assistant. Provide detailed, factual answers based on given information."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"] if "choices" in result else None
    except requests.exceptions.RequestException as e:
        print(f"OpenRouter API error: {e}")
        return None

def search_with_serper(query, api_key=SERPER_API_KEY):
    """Search with Serper API"""
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query, "num": 15})  # Increased to 15
    headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Serper API error: {e}")
        return None

def search_with_youcom(query, api_key=YOUCOM_API_KEY):
    """Search with You.com API"""
    headers = {'X-API-Key': api_key}
    params = {'q': query, 'num_web_results': 15}  # Increased to 15
    try:
        response = requests.get('https://api.you.com/api/search', headers=headers, params=params, timeout=30)
        return response.json()
    except Exception as e:
        print(f"You.com API error: {e}")
        return None

def extract_search_results(serper_data, youcom_data):
    """Extract unique search results - now up to 15 from each source"""
    results = []
    if serper_data and 'organic' in serper_data:
        for result in serper_data['organic'][:15]:  # Increased to 15
            results.append({'title': result.get('title', ''), 'snippet': result.get('snippet', ''), 'link': result.get('link', ''), 'source': 'Serper'})
    if youcom_data and 'hits' in youcom_data:
        for hit in youcom_data['hits'][:15]:  # Increased to 15
            results.append({'title': hit.get('title', ''), 'snippet': hit.get('description', ''), 'link': hit.get('url', ''), 'source': 'You.com'})
    unique_results = []
    seen_titles = set()
    for result in results:
        title_key = result['title'].lower()[:100]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_results.append(result)
    return unique_results[:30]  # Return up to 30 unique results

def create_context(results):
    """Create context from search results"""
    context_parts = [f"RESULT {i+1}:\nTITLE: {r['title']}\nCONTENT: {r['snippet']}\nSOURCE: {r['source']}\nURL: {r['link']}\n" for i, r in enumerate(results[:15])]  # Use first 15 for context
    return "\n".join(context_parts)[:4000]  # Increased context length

def create_prompt(query, context):
    """Create a detailed, universal prompt for all query types"""
    return f"""You are an expert AI research assistant tasked with providing comprehensive, accurate, and well-structured answers based solely on the provided search results. Adapt your response to the query type for optimal relevance and clarity.

QUERY: {query}

SEARCH RESULTS:
{context}

RESPONSE GUIDELINES:

1. **Query Type Adaptation**:
   - **Technical/Coding Queries**: Provide detailed code examples with explanations, best practices, and error handling.
   - **General Knowledge**: Offer a thorough overview with specific facts, historical context, and examples.
   - **Research/Academic**: Use a formal tone, structured analysis, and cite sources explicitly (e.g., "Source: [URL]").
   - **How-To/Instructional**: Provide clear, step-by-step instructions with practical tips and potential pitfalls.
   - **Comparative Queries**: Present a balanced comparison with pros, cons, and key differentiators in a table format if applicable.

2. **Response Structure**:
   - Start with a concise, direct answer to the query.
   - Organize content into logical sections with descriptive headings.
   - Use bullet points or numbered lists for clarity and readability.
   - Include specific details such as numbers, dates, names, or technical specifications when available.

3. **Content Requirements**:
   - Base the response strictly on the provided search results; do not speculate or add external information.
   - If information is missing or limited, explicitly state: "The provided search results do not contain enough information to fully answer this query."
   - Include practical examples or real-world applications where relevant.
   - For sensitive topics (e.g., medical, legal), include a disclaimer: "This information is not a substitute for professional advice."

4. **Formatting**:
   - Use markdown for clear formatting (e.g., **bold** for emphasis, `code` blocks for programming).
   - Include tables for comparisons or structured data.
   - Use consistent section headings and avoid overly verbose language.
   - For code, specify the programming language and ensure syntax accuracy.

5. **Special Cases**:
   - **Coding Queries**: Provide complete, runnable code with comments explaining key sections.
   - **Current Events**: Focus on the most recent information from the results, noting dates where available.
   - **Subjective Topics**: Present multiple perspectives neutrally, citing sources for each viewpoint.
   - **Complex Queries**: Break down the response into sub-questions or components for clarity.

6. **Accuracy and Transparency**:
   - Prioritize factual accuracy over completeness; do not fill gaps with assumptions.
   - If results are contradictory, highlight inconsistencies and explain which source is more reliable, if possible.
   - Cite sources by referencing their URLs or titles as provided in the search results.

RESPONSE:"""

def get_research_answer(query):
    """Get research answer using search APIs and OpenRouter"""
    start_time = time.time()
    
    serper_data = search_with_serper(query)
    youcom_data = search_with_youcom(query)
    results = extract_search_results(serper_data, youcom_data)
    
    if not results:
        print("No search results found.")
        return None, []
    
    context = create_context(results)
    prompt = create_prompt(query, context)
    summary = generate_with_openrouter(prompt)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    return summary, results