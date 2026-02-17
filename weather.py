# for type hints 
from typing import Any
from mcp.server.fastmcp import FastMCP

#initialize the weather server
mcp = FastMCP("Weather")

#constants
NWS_API_BASE = "the api to grad weather will come her "
USER_AGENT = "The version of my app will go here eg. weather-app/1.0"

#helper functions for the tool 
# async function for calling the weather api 
async def make_nws_request(url: str)-> dict[str, Any] | None:
    #this function will return string keys with any type of value or None if error occurs
    """the function make request to the NWS server with error handling """
    await


# a function to format the data for properly feeding to the LLM

def format_alert(feature: dict)-> str:
    """formats the alert in json i guess"""
    