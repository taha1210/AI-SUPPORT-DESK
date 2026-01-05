from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class RouteResponse(BaseModel):
    route: str = Field(description="One of: 'postgres', 'vector', 'external', 'llm'")

def route_query(query: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(RouteResponse)
    
    system = """You are an expert router for a support desk. Classify the query:
    - 'postgres': For customer, tickets, or account data.
    - 'vector': For FAQs, help articles, or support guides.
    - 'external': For weather or crypto prices.
    - 'llm': For greetings (e.g., 'how are you'), general talk, or unclear queries."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{query}"),
    ])
    
    chain = prompt | structured_llm
    try:
        result = chain.invoke({"query": query})
        return result.route
    except Exception as e:
        print(f"Routing Error: {e}")
        return "llm" 