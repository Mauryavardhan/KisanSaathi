import json
import os
import sys
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the price tool
from get_price_tool import fetch_market_price

# LangChain imports
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage

load_dotenv()

class MarketPriceDetectionAgent:
    def __init__(self, model_name="gemini-2.0-flash"):
        """
        Initialize the Market Price Detection Agent with LangChain using Gemini.
        
        Args:
            model_name (str): Gemini model to use
        """
        self.model_name = model_name
        
        # Initialize the LLM with Gemini
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.1,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Create custom market price tool
        self.market_price_tool = Tool(
            name="fetch_market_price",
            description="""Fetch agricultural market prices from Indian government API. 
            Use this tool to get current market prices for agricultural commodities.
            
            Input formats supported:
            1. "Karnataka Rice" - Get rice prices in Karnataka
            2. "Maharashtra Cotton Pune" - Get cotton prices in Pune district, Maharashtra
            3. "Punjab" - Get all commodity prices in Punjab
            4. "West Bengal Wheat" - Get wheat prices in West Bengal
            
            Supported states: Karnataka, Maharashtra, Punjab, Gujarat, Rajasthan, Tamil Nadu, 
            West Bengal, Uttar Pradesh, Madhya Pradesh, Andhra Pradesh, and others.
            
            Supported commodities: Any commodity available in Indian mandis including
            Rice, Wheat, Cotton, Soybean, Maize, Sugarcane, Pulses, Tomato, Onion, Potato,
            Coconut, Arecanut, Ginger, Turmeric, Cardamom, Pepper, Coffee, Tea, Jute,
            and any other agricultural commodity traded in Indian markets.
            
            Returns market price data including min, max, and modal prices in ₹/quintal.""",
            func=self._fetch_market_price_wrapper
        )
        
        # Initialize Tavily search tool
        self.tavily_tool = TavilySearchResults(
            max_results=5,
            api_key=os.getenv("TAVILY_API_KEY")
        )
        
        # Combine all tools
        self.tools = [self.market_price_tool, self.tavily_tool]
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an elite Indian agricultural market intelligence analyst with deep expertise in Indian commodity trading, APMC markets, and agricultural dynamics. Your mission is to provide comprehensive, data-driven insights that empower Indian farmers, traders, mandis, and agribusinesses to make profitable decisions in the Indian context.

**CORE RESPONSIBILITIES:**

1. **Indian Market Intelligence**: 
   - Fetch live commodity prices from Indian exchanges (MCX, NCDEX) and APMC mandis
   - Monitor prices across different states and agricultural regions in India
   - Track mandi rates for wheat, rice, cotton, soybean, maize, sugarcane, pulses
   - Compare prices between different mandis and identify arbitrage opportunities

2. **Indian Agricultural Analysis**:
   - Analyze monsoon impact on crop production and prices
   - Monitor Indian government policies (MSP, subsidies, export-import policies)
   - Track seasonal patterns specific to Indian cropping seasons (Kharif, Rabi)
   - Analyze regional variations across Indian agricultural zones

3. **Indian Market Predictions**:
   - Forecast prices based on Indian monsoon patterns and seasonal cycles
   - Assess impact of government announcements on agricultural markets
   - Monitor festival season demand patterns (Diwali, harvest festivals)
   - Track storage and procurement by FCI and state agencies

4. **Indian Agricultural Research**:
   - Search for Indian agricultural ministry updates and policy changes
   - Monitor Indian weather department forecasts and their crop impact
   - Track export-import policies affecting Indian agricultural commodities
   - Analyze Indian crop sowing and harvest reports

**ENHANCED SEARCH STRATEGIES FOR INDIAN MARKETS:**

When using search tools, focus on Indian sources:
- Search "wheat mandi prices today India" for current rates across mandis
- Look for "Indian agriculture news today ministry" for government updates
- Search "monsoon forecast India agriculture 2024" for weather impacts
- Query "MSP wheat rice 2024 government India" for minimum support prices
- Find "NCDEX MCX commodity prices today" for exchange rates
- Search "Indian crop production estimate 2024" for supply forecasts
- Look for "APMC mandi rates [state name] today" for regional prices

**INDIAN MARKET RESPONSE FRAMEWORK:**

**Indian Market Summary**: Key price movements across major Indian mandis
**Price Analysis**: Current rates in ₹/quintal, daily/weekly changes, mandi-wise comparison
**Monsoon Impact**: Weather effects on crop production and market sentiment
**Government Policies**: MSP announcements, export bans, import duties, subsidies
**Technical Analysis**: Support/resistance levels for Indian commodity futures
**News Impact**: Agricultural ministry updates, state government decisions
**Trading Opportunities**: Best mandis for buying/selling, timing recommendations
**Risk Factors**: Weather risks, policy changes, storage concerns
**Regional Analysis**: State-wise price variations and transportation costs
**Seasonal Outlook**: Kharif/Rabi season forecasts and price predictions

**INDIAN AGRICULTURAL CONTEXT:**
- Focus on crops relevant to Indian farmers: wheat, rice, cotton, sugarcane, soybean, maize, pulses
- Consider Indian units: quintals, acres, ₹/quintal pricing
- Include regional languages context when relevant
- Factor in Indian festival seasons and their demand impact
- Consider Indian storage infrastructure and post-harvest losses
- Account for Indian transportation and logistics challenges

**AUTHORITATIVE INDIAN SOURCES TO REFERENCE:**
- Ministry of Agriculture & Farmers Welfare (GoI)
- Indian Meteorological Department (IMD)
- Food Corporation of India (FCI)
- NCDEX, MCX commodity exchanges
- State APMC websites and mandi committees
- ICAR research institutes
- National Sample Survey Office (NSSO)
- Directorate of Economics & Statistics (Agriculture)

**QUALITY STANDARDS FOR INDIAN MARKETS:**
- Always provide prices in Indian Rupees (₹/quintal)
- Include specific mandi names and locations
- Reference Indian government sources and policies
- Consider regional variations across Indian states
- Factor in monsoon and seasonal patterns unique to India
- Provide actionable insights for Indian farmers and traders
- Include confidence levels based on data reliability from Indian sources

**CRITICAL SUCCESS FACTORS:**
- Prioritize Indian agricultural market data and news
- Use search tools to gather data from Indian government and commodity websites
- Synthesize information from multiple Indian regional sources
- Provide context relevant to Indian farming practices and market dynamics
- Focus on actionable insights for the Indian agricultural ecosystem
- Stay current with Indian agricultural policies and seasonal developments

Always use the fetch_market_price tool to get real-time data from the Indian government API before providing analysis."""),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        # Create the agent
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def _fetch_market_price_wrapper(self, input_str: str) -> str:
        """
        Wrapper function for the market price tool to work with LangChain.
        Can parse natural language inputs like "Karnataka Rice" or "Maharashtra Cotton Pune"
        
        Args:
            input_str (str): Input string containing parameters
            
        Returns:
            str: Formatted market price data
        """
        try:
            # Parse input string to extract parameters
            # Support multiple formats:
            # 1. "state_name=Karnataka, commodity=Rice, district=Bangalore"
            # 2. "Karnataka Rice" 
            # 3. "Maharashtra Cotton Pune"
            # 4. "Punjab"
            
            state_name = None
            commodity = None
            district = None
            
            if input_str:
                input_str = input_str.strip()
                
                # Check if it's key-value format
                if '=' in input_str:
                    params = {}
                    parts = input_str.split(',')
                    for part in parts:
                        if '=' in part:
                            key, value = part.strip().split('=', 1)
                            params[key.strip()] = value.strip()
                    
                    state_name = params.get('state_name', 'Karnataka')
                    commodity = params.get('commodity', None)
                    district = params.get('district', None)
                else:
                    # Parse natural language format
                    words = input_str.split()
                    
                    # Common Indian states
                    indian_states = [
                        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
                        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
                        'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
                        'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
                    ]
                    
                    # Find state in the input
                    state_found = False
                    for i, word in enumerate(words):
                        # Check for multi-word states
                        if i < len(words) - 1:
                            two_word_state = f"{word} {words[i+1]}"
                            if two_word_state in indian_states:
                                state_name = two_word_state
                                # Remove the state words from the list
                                words = words[:i] + words[i+2:]
                                state_found = True
                                break
                        # Check for single word states
                        if word in indian_states:
                            state_name = word
                            words = words[:i] + words[i+1:]
                            state_found = True
                            break
                    
                    # After finding state, remaining words could be commodity and/or district
                    # We need to be smarter about parsing multi-word commodities vs districts
                    if words:
                        # Common district keywords that help identify where commodity ends and district begins
                        district_keywords = ['district', 'city', 'mandi', 'market', 'taluka', 'tehsil']
                        
                        # Try to find district keywords to separate commodity from district
                        district_start_idx = -1
                        for i, word in enumerate(words):
                            if word.lower() in district_keywords:
                                district_start_idx = i
                                break
                        
                        if district_start_idx >= 0:
                            # Found district keyword - everything before is commodity, after is district
                            commodity = ' '.join(words[:district_start_idx])
                            district = ' '.join(words[district_start_idx:])
                        else:
                            # No district keywords found - need to guess based on common patterns
                            if len(words) == 1:
                                commodity = words[0]
                            elif len(words) == 2:
                                # For two words, assume it's a two-word commodity
                                commodity = ' '.join(words)
                            else:
                                # For more than 2 words, check if last word(s) look like district names
                                # (contain parentheses, start with capital, etc.)
                                last_word = words[-1]
                                if ('(' in last_word and ')' in last_word) or last_word.isupper() or len(last_word) < 3:
                                    # Last word looks like part of commodity name (parentheses, short, etc.)
                                    commodity = ' '.join(words)
                                else:
                                    # Assume last word is district, rest is commodity
                                    commodity = ' '.join(words[:-1])
                                    district = words[-1]
                    
                    # Default state if not found
                    if not state_name:
                        state_name = 'Karnataka'
            
            # Call the actual function
            result = fetch_market_price(state_name, commodity, district)
            
            # Format the result for display
            if result.get('success'):
                output = f"✅ Found {result['count']} records for {state_name}"
                if commodity:
                    output += f" (Commodity: {commodity})"
                if district:
                    output += f" (District: {district})"
                output += "\n\n"
                
                for i, record in enumerate(result['data'][:5], 1):  # Show first 5 records
                    output += f"Record {i}:\n"
                    output += f"  Market: {record['market']}\n"
                    output += f"  Commodity: {record['commodity']}\n"
                    output += f"  Variety: {record['variety']}\n"
                    output += f"  Price Range: ₹{record['min_price']} - ₹{record['max_price']}\n"
                    output += f"  Modal Price: ₹{record['modal_price']}\n"
                    output += f"  Arrival Date: {record['arrival_date']}\n\n"
                
                if result['count'] > 5:
                    output += f"... and {result['count'] - 5} more records\n"
                    
                return output
            else:
                return f"❌ No records found: {result.get('message', 'Unknown error')}"
                
        except Exception as e:
            return f"❌ Error fetching market prices: {str(e)}"
    
    def get_market_analysis(self, query: str) -> str:
        """
        Get comprehensive market analysis for a given query.
        
        Args:
            query (str): User query about market prices
            
        Returns:
            str: Market analysis response
        """
        try:
            result = self.agent_executor.invoke({
                "input": query,
                "chat_history": []
            })
            return result["output"]
        except Exception as e:
            return f"Error in market analysis: {str(e)}"
    
    def chat(self, message: str) -> str:
        """
        Chat interface for the market price agent.
        
        Args:
            message (str): User message
            
        Returns:
            str: Agent response
        """
        return self.get_market_analysis(message)

def main():
    """Main function to test the agent."""
    print("=== Agricultural Market Price Detection Agent Demo ===\n")
    
    # Initialize the agent
    agent = MarketPriceDetectionAgent()
    
    # Test queries
    test_queries = [
        "What are the current rice prices in Karnataka and Maharashtra?",
        "Compare cotton prices between Gujarat and Maharashtra mandis for arbitrage opportunities",
        "Get current soybean prices in Madhya Pradesh markets"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 50)
        try:
            response = agent.chat(query)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
