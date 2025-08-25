import os
# from openai import OpenAI
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

MOCK_SEARCH_DATABASE = {
    "ai developments 2024": [
        {
            "title": "ChatGPT-4 Turbo Released with Enhanced Capabilities",
            "url": "https://techcrunch.com/2024/chatgpt-4-turbo-release",
            "snippet": "OpenAI released ChatGPT-4 Turbo in early 2024, featuring improved reasoning capabilities, longer context windows up to 128K tokens, and better code generation. The model shows 40% improvement in mathematical problem-solving compared to GPT-4.",
            "date": "2024-02-15"
        },
        {
            "title": "Google's Gemini Ultra Achieves Human-Level Performance",
            "url": "https://ai.googleblog.com/2024/gemini-ultra-benchmark",
            "snippet": "Google's Gemini Ultra model achieved 90.04% on the MMLU benchmark, the first AI system to exceed human expert performance. The model demonstrates strong multimodal capabilities across text, image, and code understanding.",
            "date": "2024-03-10"
        },
        {
            "title": "Meta Releases Llama 3 with 400B Parameters",
            "url": "https://ai.meta.com/blog/llama-3-release",
            "snippet": "Meta's Llama 3 model family includes variants up to 400B parameters, offering competitive performance with commercial models while maintaining open-source availability. Training incorporated 15 trillion tokens of diverse data.",
            "date": "2024-04-18"
        }
    ],
    "artificial intelligence job market impact": [
        {
            "title": "AI Automation Could Replace 300 Million Jobs by 2030",
            "url": "https://www.mckinsey.com/ai-job-displacement-2024",
            "snippet": "McKinsey report suggests AI could automate tasks affecting 300 million full-time jobs globally by 2030. However, new job categories in AI development, data analysis, and human-AI collaboration are expected to emerge, potentially creating 97 million new roles.",
            "date": "2024-01-22"
        },
        {
            "title": "Tech Companies Increase AI Hiring by 76%",
            "url": "https://www.linkedin.com/business/talent/ai-hiring-trends-2024",
            "snippet": "LinkedIn data shows a 76% increase in AI-related job postings in 2024. Machine learning engineers, AI researchers, and prompt engineers are among the fastest-growing job categories. Average salaries have increased by 25% year-over-year.",
            "date": "2024-05-08"
        },
        {
            "title": "Financial Services Lead AI Adoption in Workplace",
            "url": "https://www.pwc.com/ai-workplace-adoption-2024",
            "snippet": "PwC survey reveals 68% of financial services companies have integrated AI tools into daily operations, leading all industries. Employee productivity increased by average of 23%, while job satisfaction scores improved due to reduced routine tasks.",
            "date": "2024-06-12"
        }
    ],
    "ai ethics concerns 2024": [
        {
            "title": "EU AI Act Takes Effect: Major Regulatory Changes",
            "url": "https://ec.europa.eu/ai-act-implementation-2024",
            "snippet": "The European Union's AI Act officially took effect in August 2024, establishing the world's first comprehensive AI regulation framework. High-risk AI systems must undergo conformity assessments, while prohibited AI practices include social scoring and emotion recognition in schools.",
            "date": "2024-08-01"
        },
        {
            "title": "AI Bias in Hiring Tools Under Scrutiny",
            "url": "https://www.nature.com/ai-bias-hiring-2024",
            "snippet": "Research published in Nature reveals persistent bias in AI hiring tools, with 43% showing discrimination against minority candidates. Companies like IBM and Microsoft are developing new fairness metrics and bias detection algorithms to address these issues.",
            "date": "2024-07-15"
        }
    ],
    "generative ai market growth": [
        {
            "title": "Generative AI Market Reaches $67 Billion in 2024",
            "url": "https://www.gartner.com/generative-ai-market-2024",
            "snippet": "Gartner reports the generative AI market reached $67 billion in 2024, growing 126% year-over-year. Enterprise adoption is driving growth, with 45% of large organizations implementing at least one generative AI solution for content creation, code generation, or customer service.",
            "date": "2024-09-20"
        }
    ],
    "ai workplace productivity": [
        {
            "title": "GitHub Copilot Users 55% More Productive: Study",
            "url": "https://github.blog/copilot-productivity-study-2024",
            "snippet": "GitHub study of 2,000 developers found those using Copilot completed coding tasks 55% faster on average. The tool helped reduce time spent on boilerplate code by 67%, allowing developers to focus on complex problem-solving and architecture decisions.",
            "date": "2024-03-28"
        }
    ]
}

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    date: str

@dataclass
class ResearchStep:
    query: str
    results: List[SearchResult]
    reasoning: str
    timestamp: datetime

class LogCapture:
    def __init__(self):
        self.logs = []
        
    def log(self, message):
        """Capture log message with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(message)  # Still print to console during research
        
    def get_logs(self):
        """Get all captured logs as string"""
        return "\n".join(self.logs)

class MockWebSearchTool:
    """Mock web search tool that returns predefined results"""
    
    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """Perform a mock web search"""
        # Simulate search delay
        time.sleep(0.5)
        
        # Find matching results based on keywords
        results = []
        query_lower = query.lower()
        
        for key, search_results in MOCK_SEARCH_DATABASE.items():
            # Check if query matches any keywords in the database key
            if any(word in key for word in query_lower.split()) or any(word in query_lower for word in key.split()):
                for result in search_results:
                    if len(results) < max_results:
                        results.append(SearchResult(**result))
        
        return results

class ResearchAssistant:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        # self.client = OpenAI(
        #     base_url="https://openrouter.ai/api/v1",
        #     api_key=api_key
        # )
        genai.configure(api_key=api_key)
        self.model = model
        self.search_tool = MockWebSearchTool()
        self.research_log: List[ResearchStep] = []
        self.logger = LogCapture()

    # def _call_llm(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> Any:
    #     """Call the LLM with optional tool calling"""
    #     try:
    #         params = {
    #             "model": self.model,
    #             "messages": messages,
    #             "temperature": 0.2,
    #             "max_tokens": 2000
    #         }
            
    #         if tools:
    #             params["tools"] = tools
    #             params["tool_choice"] = "auto"
            
    #         response = self.client.chat.completions.create(**params)
    #         return response
    #     except Exception as e:
    #         self.logger.log(f"Error calling LLM: {e}")
    #         return None

    def _call_llm(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> Any:
        """Call the Gemini LLM"""
        try:
            prompt = "\n".join([m["content"] for m in messages])
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            class DummyChoice:
                def __init__(self, text): self.message = type('msg', (), {'content': text})
            # Mimic OpenAI response structure
            return type('Resp', (), {'choices': [DummyChoice(response.text)]})
        except Exception as e:
            self.logger.log(f"Error calling Gemini LLM: {e}")
            return None
    
    def _get_search_queries(self, question: str) -> List[str]:
        """Generate focused search queries for a complex question"""
        prompt = f"""
        Break down this complex research question into 3-5 focused search queries that will help gather comprehensive information:
        
        Question: {question}
        
        Generate search queries that cover different aspects of the question. Each query should be specific and targeted.
        Return only the search queries, one per line, without numbering or additional text.
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self._call_llm(messages)
        
        if response and hasattr(response, 'choices') and response.choices:
            queries = response.choices[0].message.content.strip().split('\n')
            return [q.strip() for q in queries if q.strip()]
        
        # Fallback: basic keyword extraction
        self.logger.log("Using fallback query generation")
        return [question]

    def _perform_research(self, queries: List[str]) -> List[ResearchStep]:
        """Perform iterative research using multiple search queries"""
        research_steps = []
        
        for query in queries:
            self.logger.log(f"Searching for: '{query}'")
            
            reasoning = f"Searching for information about: {query}"
            results = self.search_tool.search(query, max_results=3)
            
            self.logger.log(f"   Found {len(results)} results")
            
            step = ResearchStep(
                query=query,
                results=results,
                reasoning=reasoning,
                timestamp=datetime.now()
            )
            research_steps.append(step)
            self.research_log.append(step)
        
        return research_steps

    def _has_relevant_results(self, question: str, research_steps: List[ResearchStep]) -> bool:
        """Check if we have relevant results for the question"""
        # 1. If most searches returned zero results, we likely have no relevant data
        total_results = sum(len(step.results) for step in research_steps)
        if total_results < 2:  # Require at least 2 results total
            return False

        # 2. Extract keywords from question
        question_keywords = set(question.lower().split())
        common_words = {'what', 'how', 'why', 'when', 'where', 'is', 'are', 'the', 'to', 'and', 
                        'of', 'in', 'on', 'a', 'an', 'for', 'with', 'about', 'that'}
        question_keywords = question_keywords - common_words

        if not question_keywords:  # If no meaningful keywords remain
            return True  # Default to attempting an answer

        # 3. Check if sources contain relevant keywords
        relevant_sources = 0
        for step in research_steps:
            for result in step.results:
                source_text = f"{result.title} {result.snippet}".lower()
                if any(keyword in source_text for keyword in question_keywords):
                    relevant_sources += 1

        # Return true if we have enough relevant sources (proportional to total)
        return relevant_sources >= min(2, total_results // 2)

    def _synthesize_answer(self, question: str, research_steps: List[ResearchStep]) -> str:
        """Synthesize research findings into a comprehensive answer"""
        # Check if we have relevant results before attempting synthesis
        if not self._has_relevant_results(question, research_steps):
            return f"I'm sorry, but I don't have enough relevant information to answer the question: \"{question}\"\n\nThe research didn't yield sufficient data on this topic. Please try a different question or topic."
    
        # Prepare context from research
        context = ""
        for i, step in enumerate(research_steps, 1):
            context += f"\nSearch {i}: {step.query}\n"
            for j, result in enumerate(step.results, 1):
                context += f"[{i}.{j}] {result.title}\n"
                context += f"URL: {result.url}\n"
                context += f"Content: {result.snippet}\n"
                context += f"Date: {result.date}\n\n"
        
        prompt = f"""
        Based on the research findings below, provide a comprehensive answer to the question: "{question}"

        Research Context:
        {context}

        Instructions:
        1. Synthesize information from multiple sources to provide a complete answer
        2. Include specific data points, statistics, and facts from the sources
        3. Cite sources using the format [Source X.Y] where X is the search number and Y is the result number
        4. Structure your response with clear sections/paragraphs
        5. Highlight key trends, developments, and implications
        6. Be objective and balanced in your analysis

        Provide a well-structured, informative response that demonstrates deep analysis of the research findings.
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self._call_llm(messages)
        
        if response and hasattr(response, 'choices') and response.choices:
            return response.choices[0].message.content
        
        return "Unable to synthesize research findings due to API error."

    def _generate_key_findings(self, question: str, research_steps: List[ResearchStep]) -> list:
        """Ask Gemini to generate concise, one-line key findings as bullet points."""
        # Prepare context from research
        context = ""
        for i, step in enumerate(research_steps, 1):
            context += f"\nSearch {i}: {step.query}\n"
            for j, result in enumerate(step.results, 1):
                context += f"[{i}.{j}] {result.title}\n"
                context += f"URL: {result.url}\n"
                context += f"Content: {result.snippet}\n"
                context += f"Date: {result.date}\n\n"

        prompt = (
            f"Based on the research findings below, list 5 concise, one-line key findings as bullet points using (•) and not (*). "
            f"Each point should be brief and focused.\n\n"
            f"Research Context:\n{context}"
        )
        messages = [{"role": "user", "content": prompt}]
        response = self._call_llm(messages)
        if response and hasattr(response, 'choices') and response.choices:
            findings = response.choices[0].message.content.strip().split('\n')
            # Clean up bullet points
            findings = [f.lstrip('-• ').strip() for f in findings if f.strip()]
            return findings
        return []

    def _generate_summary(self, question: str, research_steps: List[ResearchStep], answer: str) -> str:
        """Generate a concise summary of the research process and findings"""
        total_sources = sum(len(step.results) for step in research_steps)
        
        # key_stats = []
        # lines = answer.split('\n')
        # for line in lines:
        #     line = line.strip()
        #     if line and (('%' in line and any(char.isdigit() for char in line)) or 
        #                 any(word in line.lower() for word in ['million', 'billion', 'increase', 'decrease', 'growth']) and 
        #                 any(char.isdigit() for char in line)):
        #         clean_line = line.replace('**', '').replace('*', '').strip('- •')
        #         if len(clean_line) > 20 and len(key_stats) < 5:
        #             key_stats.append(clean_line)
        
        key_stats = self._generate_key_findings(question, research_steps)

        domains = set()
        for step in research_steps:
            for result in step.results:
                domain = result.url.split('/')[2] if '/' in result.url else result.url
                domains.add(domain)
        
        all_dates = []
        for step in research_steps:
            for result in step.results:
                all_dates.append(result.date)
        
        date_range = f"{min(all_dates)} to {max(all_dates)}" if all_dates else "N/A"
        
        summary = f"""
RESEARCH SUMMARY
================
Question: {question}

Research Process:
• Conducted {len(research_steps)} targeted searches
• Analyzed {total_sources} sources from {len(domains)} different domains
• Sources date range: {date_range}

Key Findings:
{chr(10).join(f"• {stat}" for stat in key_stats)}

Search Queries Used:
{chr(10).join(f"• {step.query}" for step in research_steps)}

Conclusion: The research successfully gathered comprehensive information from multiple authoritative sources, 
providing a balanced view of the topic with current data and expert insights.
"""
        return summary

    def research_question(self, question: str) -> Dict[str, Any]:
        """Main method to research a complex question"""
        self.logger.log("Research Assistant starting analysis...")
        self.logger.log(f"Question: {question}")
        self.logger.log("=" * 80)
        
        self.logger.log("Step 1: Generating search queries...")
        queries = self._get_search_queries(question)
        self.logger.log(f"Generated {len(queries)} search queries:")
        for i, query in enumerate(queries, 1):
            self.logger.log(f"  {i}. {query}")
        
        self.logger.log("Step 2: Performing research...")
        research_steps = self._perform_research(queries)
        
        self.logger.log("Step 3: Synthesizing findings...")
        answer = self._synthesize_answer(question, research_steps)
        self.logger.log("Analysis complete!")
        
        summary = self._generate_summary(question, research_steps, answer)
        
        research_log_summary = []
        for step in research_steps:
            log_entry = {
                "query": step.query,
                "results_found": len(step.results),
                "key_sources": [{"title": r.title, "url": r.url} for r in step.results[:2]],
                "timestamp": step.timestamp.isoformat()
            }
            research_log_summary.append(log_entry)
        
        return {
            "question": question,
            "answer": answer,
            "summary": summary,
            "research_log": research_log_summary,
            "detailed_logs": self.logger.get_logs(),
            "total_sources": sum(len(step.results) for step in research_steps),
            "search_queries_used": len(queries)
        }

    def print_research_log(self):
        """Print detailed research log"""
        print("\n" + "="*80)
        print("DETAILED RESEARCH LOG")
        print("="*80)
        
        for i, step in enumerate(self.research_log, 1):
            print(f"\nSearch {i}: {step.query}")
            print(f"Timestamp: {step.timestamp}")
            print(f"Results found: {len(step.results)}")
            
            for j, result in enumerate(step.results, 1):
                print(f"\n  [{i}.{j}] {result.title}")
                print(f"      URL: {result.url}")
                print(f"      Date: {result.date}")
                print(f"      Snippet: {result.snippet[:150]}...")

def main():
    print("Research Assistant")
    print("=" * 50)
    load_dotenv()
    try:
        api_key = os.getenv("API_KEY")
        if not api_key:
            print("Error: API_KEY environment variable not set.")
            return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    try:
        question = input("\nEnter your research question: ").strip()
        if not question:
            question = "What are the latest developments in AI and their impact on the job market?"
            print(f"Using default question: {question}")
    except KeyboardInterrupt:
        print("\nExiting...")
        return
    
    assistant = ResearchAssistant(api_key)

    print(f"\nStarting research...") 
    results = assistant.research_question(question)
        
    print("\n" * 2)
    print("="*80)
    print("RESEARCH COMPLETED")
    print("="*80)
        
    print(results['summary'])
        
    print(f"\nDETAILED ANALYSIS:")
    print("-" * 40)
    print(results['answer'])
        
    try:
        print(f"\n{'='*50}")
        print(f"\nDETAILED RESEARCH LOGS:")
        print("-" * 40)
        print(results['detailed_logs'])
                
        print(f"\nSOURCE BREAKDOWN:")
        print("-" * 40)
        assistant.print_research_log()
    except Exception as e:
        print(f"Error displaying research logs: {e}")

    try:
        print(f"\n{'='*50}")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"research_results_{timestamp}.txt"
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Research Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            f.write(results['summary'])
            f.write(f"\n\nDETAILED ANALYSIS:\n{'-'*40}\n")
            f.write(results['answer'])
            f.write(f"\n\nRESEARCH LOGS:\n{'-'*40}\n")
            f.write(results['detailed_logs'])
                
            print(f"saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")
    
    print(f"\nResearch session completed successfully!")

if __name__ == "__main__":
    main()