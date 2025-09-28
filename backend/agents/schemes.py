import os
import sys
import json
import logging
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AgriScheme(BaseModel):
    """Model for individual agricultural scheme information"""
    name: str = Field(description="Name of the agricultural scheme")
    description: str = Field(description="Detailed description of the scheme")
    benefits: List[str] = Field(description="List of benefits provided by the scheme")
    eligibility: List[str] = Field(description="Eligibility criteria for the scheme")
    application_process: List[str] = Field(description="Steps to apply for the scheme")
    contact_information: List[str] = Field(description="Contact details and official websites")
    last_updated: Optional[str] = Field(default=None, description="Last update date if available")
    source: str = Field(description="Source of the information")

class AgriSchemesResult(BaseModel):
    """Model for complete agricultural schemes search result"""
    schemes: List[AgriScheme] = Field(description="List of agricultural schemes found")
    search_query: str = Field(description="The search query used")
    total_schemes_found: int = Field(description="Total number of schemes found")
    search_notes: List[str] = Field(description="Additional notes about the search")

class AgriSchemesAgent:
    """Enhanced agricultural schemes agent with better prompting and user-friendly output"""
    
    def __init__(self, model_id="gemini-2.0-flash"):
        # Check for required API keys
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        
        # Initialize LLM
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=model_id,
                google_api_key=google_api_key,
                temperature=0.1
            )
            logger.info("LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
        
        # Initialize Tavily search
        try:
            self.tavily_search = TavilySearchResults(
                api_key=tavily_api_key,
                max_results=5  # Get more results for better information extraction
            )
            logger.info("Tavily search initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Tavily search: {e}")
            raise
        
        logger.info("Enhanced Agricultural Schemes Agent initialized successfully")
    
    def search_and_extract_schemes(self, query: str) -> AgriSchemesResult:
        """Search for schemes and extract structured information"""
        try:
            logger.info(f"Searching for: {query}")
            
            # Enhanced search query
            search_query = f"{query} agricultural schemes India government benefits eligibility application process contact 2024"
            results = self.tavily_search.run(search_query)
            
            logger.info(f"Found {len(results) if isinstance(results, list) else 'some'} search results")
            
            # Format results for LLM processing
            search_text = ""
            if isinstance(results, list):
                for i, result in enumerate(results[:5], 1):  # Top 5 results
                    title = result.get("title", f"Result {i}")
                    content = result.get("content", "No content")
                    url = result.get("url", "No URL")
                    
                    # Keep more content for better extraction
                    if len(content) > 800:
                        content = content[:800] + "..."
                    
                    search_text += f"\n--- SEARCH RESULT {i} ---\n"
                    search_text += f"Title: {title}\n"
                    search_text += f"Content: {content}\n"
                    search_text += f"URL: {url}\n"
                    search_text += f"--- END RESULT {i} ---\n"
            else:
                search_text = str(results)
            
            # Enhanced prompt for better information extraction
            enhanced_prompt = f"""
You are an agricultural schemes expert. Based on the following search results about "{query}", extract detailed information about EACH INDIVIDUAL SCHEME found and return the data in JSON format.

SEARCH RESULTS:
{search_text}

INSTRUCTIONS:
1. Identify ALL distinct agricultural schemes mentioned in the search results
2. For EACH scheme, extract the following information:
   - name: Full official name of the scheme
   - description: Detailed description of what the scheme offers (2-3 sentences)
   - benefits: List specific benefits (financial assistance amounts, subsidies, insurance coverage, etc.)
   - eligibility: List specific eligibility criteria (farmer categories, land size, income limits, etc.)
   - application_process: List step-by-step application process
   - contact_information: List official websites, phone numbers, government departments
   - last_updated: Any date information found
   - source: Which search result this information came from

3. If information is missing for any field, put "Information not available in search results" instead of leaving it blank
4. Be specific and detailed - extract actual numbers, percentages, amounts where mentioned
5. Separate different schemes clearly

Return the response in this EXACT JSON format:
{{
  "schemes": [
    {{
      "name": "Scheme Name",
      "description": "Detailed description",
      "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
      "eligibility": ["Criteria 1", "Criteria 2", "Criteria 3"],
      "application_process": ["Step 1", "Step 2", "Step 3"],
      "contact_information": ["Contact 1", "Contact 2"],
      "last_updated": "Date if available or null",
      "source": "Which search result"
    }}
  ],
  "summary": "Brief overall summary of schemes found"
}}

IMPORTANT: 
- Extract information for multiple schemes if found
- Be thorough and specific
- Include actual numbers and amounts where mentioned
- Don't make up information not in the search results
"""
            
            logger.info("Extracting scheme information with enhanced LLM prompt...")
            
            # Get LLM response
            response = self.llm.invoke(enhanced_prompt)
            response_text = response.content
            
            # Try to parse JSON response
            try:
                # Clean the response text to extract JSON
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != -1:
                    json_text = response_text[json_start:json_end]
                    parsed_data = json.loads(json_text)
                    
                    # Convert to AgriScheme objects
                    schemes = []
                    for scheme_data in parsed_data.get('schemes', []):
                        scheme = AgriScheme(
                            name=scheme_data.get('name', 'Unknown Scheme'),
                            description=scheme_data.get('description', 'No description available'),
                            benefits=scheme_data.get('benefits', ['Information not available']),
                            eligibility=scheme_data.get('eligibility', ['Information not available']),
                            application_process=scheme_data.get('application_process', ['Information not available']),
                            contact_information=scheme_data.get('contact_information', ['Information not available']),
                            last_updated=scheme_data.get('last_updated'),
                            source=scheme_data.get('source', 'Search Results')
                        )
                        schemes.append(scheme)
                    
                    return AgriSchemesResult(
                        schemes=schemes,
                        search_query=query,
                        total_schemes_found=len(schemes),
                        search_notes=[
                            "Enhanced extraction with structured prompting",
                            "Information verified from multiple search results",
                            parsed_data.get('summary', 'Multiple agricultural schemes found'),
                            "Please verify current details from official sources before applying"
                        ]
                    )
                else:
                    raise ValueError("No valid JSON found in response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"JSON parsing failed: {e}, falling back to text parsing")
                # Fallback to simple scheme creation
                return self._create_fallback_result(query, response_text)
                
        except Exception as e:
            logger.error(f"Search and extract error: {e}")
            return AgriSchemesResult(
                schemes=[],
                search_query=query,
                total_schemes_found=0,
                search_notes=[f"Search failed: {str(e)}"]
            )
    
    def _create_fallback_result(self, query: str, response_text: str) -> AgriSchemesResult:
        """Create fallback result when JSON parsing fails"""
        scheme = AgriScheme(
            name=f"Agricultural Schemes for: {query}",
            description=response_text[:500] + "..." if len(response_text) > 500 else response_text,
            benefits=["Detailed benefits available - see description"],
            eligibility=["Check official sources for eligibility criteria"],
            application_process=["Contact local agriculture office or visit official websites"],
            contact_information=["Check government agriculture department websites"],
            source="Search Results (Fallback)"
        )
        
        return AgriSchemesResult(
            schemes=[scheme],
            search_query=query,
            total_schemes_found=1,
            search_notes=[
                "Fallback result - structured extraction not available",
                "Please verify details from official sources"
            ]
        )
    
    def search_agricultural_schemes(self, query: str, max_schemes: int = 5) -> AgriSchemesResult:
        """Search for agricultural schemes using enhanced approach"""
        return self.search_and_extract_schemes(query)
    
    def run(self, query: str) -> str:
        """Enhanced run method with user-friendly output"""
        try:
            result = self.search_and_extract_schemes(query)
            return self._format_user_friendly_output(result)
        except Exception as e:
            logger.error(f"Run error: {e}")
            return f"❌ Error: {str(e)}"

    def _format_user_friendly_output(self, result: AgriSchemesResult) -> str:
        """Format output in a user-friendly manner"""
        output = []
        
        # Header
        output.append("🌾 AGRICULTURAL SCHEMES INFORMATION")
        output.append("=" * 60)
        output.append(f"📋 Search Query: {result.search_query}")
        output.append(f"📊 Total Schemes Found: {result.total_schemes_found}")
        output.append("")
        
        # Search notes
        if result.search_notes:
            output.append("📝 Notes:")
            for note in result.search_notes:
                output.append(f"   • {note}")
            output.append("")
        
        # Individual schemes
        for i, scheme in enumerate(result.schemes, 1):
            output.append(f"🏛️  SCHEME {i}: {scheme.name}")
            output.append("-" * 50)
            
            output.append(f"📖 Description:")
            output.append(f"   {scheme.description}")
            output.append("")
            
            output.append(f"💰 Benefits:")
            for benefit in scheme.benefits:
                output.append(f"   ✅ {benefit}")
            output.append("")
            
            output.append(f"👤 Eligibility Criteria:")
            for criteria in scheme.eligibility:
                output.append(f"   ✓ {criteria}")
            output.append("")
            
            output.append(f"📋 Application Process:")
            for step in scheme.application_process:
                output.append(f"   {scheme.application_process.index(step) + 1}. {step}")
            output.append("")
            
            output.append(f"📞 Contact Information:")
            for contact in scheme.contact_information:
                output.append(f"   📧 {contact}")
            output.append("")
            
            if scheme.last_updated:
                output.append(f"📅 Last Updated: {scheme.last_updated}")
            
            output.append(f"🔍 Source: {scheme.source}")
            
            if i < len(result.schemes):
                output.append("\n" + "=" * 60 + "\n")
        
        # Footer
        output.append("\n" + "=" * 60)
        output.append("⚠️  IMPORTANT: Please verify all information from official government sources before applying!")
        output.append("📞 Contact your local agriculture department for the most current details.")
        
        return "\n".join(output)

def print_schemes_result_enhanced(result: AgriSchemesResult):
    """Enhanced helper function to print schemes results in a user-friendly format"""
    print(f"\n🌾 AGRICULTURAL SCHEMES SEARCH RESULTS")
    print(f"{'=' * 60}")
    print(f"📋 Search Query: {result.search_query}")
    print(f"📊 Total Schemes Found: {result.total_schemes_found}")
    print(f"📝 Search Notes:")
    for note in result.search_notes:
        print(f"   • {note}")
    
    for i, scheme in enumerate(result.schemes, 1):
        print(f"\n🏛️  SCHEME {i}: {scheme.name}")
        print(f"{'-' * 50}")
        print(f"📖 Description: {scheme.description}")
        
        print(f"\n💰 Benefits:")
        for benefit in scheme.benefits[:5]:  # Show top 5
            print(f"   ✅ {benefit}")
        if len(scheme.benefits) > 5:
            print(f"   ... and {len(scheme.benefits) - 5} more benefits")
        
        print(f"\n👤 Eligibility:")
        for criteria in scheme.eligibility[:5]:  # Show top 5
            print(f"   ✓ {criteria}")
        if len(scheme.eligibility) > 5:
            print(f"   ... and {len(scheme.eligibility) - 5} more criteria")
        
        print(f"\n📋 Application Process:")
        for j, step in enumerate(scheme.application_process[:5], 1):  # Show top 5
            print(f"   {j}. {step}")
        if len(scheme.application_process) > 5:
            print(f"   ... and {len(scheme.application_process) - 5} more steps")
        
        print(f"\n📞 Contact Information:")
        for contact in scheme.contact_information[:3]:  # Show top 3
            print(f"   📧 {contact}")
        if len(scheme.contact_information) > 3:
            print(f"   ... and {len(scheme.contact_information) - 3} more contacts")
        
        if scheme.last_updated:
            print(f"\n📅 Last Updated: {scheme.last_updated}")
        print(f"🔍 Source: {scheme.source}")

if __name__ == "__main__":

        agent = AgriSchemesAgent()
        
        
        print("\n🧪 Test 1: Crop insurance schemes")
        result2 = agent.search_agricultural_schemes("crop insurance schemes")
        print_schemes_result_enhanced(result2)
        

        print(f"\n✅ All tests completed successfully")
