# for type hints 
from typing import Any
from mcp.server.fastmcp import FastMCP
import httpx
#initialize the weather server
mcp = FastMCP("Weather")

#constants
NWS_API_BASE = "weather.indianapi.in"
USER_AGENT = "The version of my app will go here eg. weather-app/1.0"

#helper functions for the tool 
# async function for calling the weather api 
async def make_nws_request(url: str)-> dict[str, Any] | None:
    #this function will return string keys with any type of value or None if error occurs
    """the function make request to the NWS server with error handling  
        the header tell the website that its a user agent to prevent geting blocked
        """
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try: # here the url is give into tthe url variable no explicit entry needed
            response = await client.get(url, headers= headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            #exception handling with None and Exception of all type will be handled here 
            return None



# a function to format the data for properly feeding to the LLM
#EASY helper function to gather weather data 
def format_alert(feature: dict)-> str:
    """formats the alert in json i guess"""
    props = feature["properties"]
    return f"""
Event:{props.get("event",)}
Area:{props.get("area")}
Severity:{props.get("severity")}
Description:{props.get("description")}
Instruction:{props.get("instruction")}"""