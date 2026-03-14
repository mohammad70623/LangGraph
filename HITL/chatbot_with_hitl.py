from langgraph.graph import StateGraph, START
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langgraph.types import interrupt, Command
from dotenv import load_dotenv
import requests
import os

load_dotenv() 
model = ChatGroq(model="openai/gpt-oss-safeguard-20b", temperature=0, max_tokens=1024)

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch the latest stock price for a given symbol (e.g., 'AAPL', 'TSLA') 
    using Alpha Vantage API. API key is loaded from environment variables.
    """
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    )
    response = requests.get(url)
    return response.json()

