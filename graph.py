import re 
from typing import Dict, Any, Annotated, List, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages 
from langgraph.checkpoint.memory import MemorySaver

from app.agent.router import route_query
from app.tools.vector_tool import search_knowledge_base
from app.tools.postgres_tool import run_postgres_query

class AgentState(TypedDict):
    messages: Annotated[List[Any], add_messages]
    query: str
    route: str
    response: str

def generate_sql(user_query: str) -> str:
    """
    User ki query ko SQL mein convert karta hai (Requirement #5)
    """
    q = user_query.lower()
    
    if "ticket" in q:
        customer_id = re.findall(r'\d+', q)
        if "customer" in q and customer_id:
            return f"SELECT * FROM tickets WHERE customer_id = {customer_id[0]};"
        return "SELECT * FROM tickets LIMIT 5;"
    
    elif "customer" in q:
        return "SELECT * FROM customers LIMIT 5;"
    
    return "SELECT * FROM customers;" 


def router_node(state: AgentState) -> Dict[str, Any]:
    route = route_query(state["query"])
    return {"route": route}

def postgres_node(state: AgentState) -> Dict[str, Any]:
    sql_query = generate_sql(state["query"])
    result = run_postgres_query(sql_query)
    
    response_text = f"Database Results: {result}"
    return {"response": response_text, "messages": [("ai", response_text)]}

def vector_node(state: AgentState) -> Dict[str, Any]:
    result = search_knowledge_base(state["query"])
    response_text = f"Knowledge Base says: {result}"
    return {"response": response_text, "messages": [("ai", response_text)]}

def external_node(state: AgentState) -> Dict[str, Any]:
    query = state["query"].lower()
    if "weather" in query:
        res = "🌤️ Weather today is sunny, around 32°C (mock data)."
    elif "price" in query:
        res = "💰 Bitcoin is at $95,000 (mock data)."
    else:
        res = "External API response (mock)"
    return {"response": res, "messages": [("ai", res)]}

def llm_node(state: AgentState) -> Dict[str, Any]:
    res = "I am your AI assistant. How can I help with your account or support questions?"
    return {"response": res, "messages": [("ai", res)]}


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("router", router_node)
    workflow.add_node("postgres", postgres_node)
    workflow.add_node("vector", vector_node)
    workflow.add_node("external", external_node)
    workflow.add_node("llm", llm_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "postgres": "postgres",
            "vector": "vector",
            "external": "external",
            "llm": "llm",
        },
    )

    workflow.add_edge("postgres", END)
    workflow.add_edge("vector", END)
    workflow.add_edge("external", END)
    workflow.add_edge("llm", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

def run_agent(query: str, thread_id: str = "user_123"):
    agent = build_graph()
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"query": query, "messages": [("user", query)]}
    result = agent.invoke(inputs, config)
    return result["response"]