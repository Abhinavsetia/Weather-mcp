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
Event:{props.get("event","Unknown")}
Area:{props.get("areaDesc", "Unknown")}
Severity:{props.get("severity", "Unknown")}
Description:{props.get("description", "No description is available atm")}
Instruction:{props.get("instruction","sorry the instruction were'nt provided")}"""



#the mcp tool module 
#the tool will be responsible for the etire execution of the script 
@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    mcp tool to get_alerts for a US state
    
    Args:
        state: two-letter US state code (eg CA,NY)

    """
    #here the helper function is called, also this mcp give the weather alert active ones
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    #error handling with if data doesnt exist or if features is not in the data
    if not data or "features" not in data:
        return "Unable to fetch the alerts or there are'nt any."
    #this if statement handles if is empty return that no alerts as of now
    if not data["features"]:
        return "No active alerts for this state.."
    #but if there are alerts then the second helper function will format them for readability
    #here alerts are formated for each featuer out of the features 
    alerts = [format_alert(feature) for feature in data["features"]]
    #this is a shortcut to appead all the formatted features to alerts list and finally join them below 
    return "\n---\n".join(alerts)


def main():
    mcp.run(transport='stdio')

if "__name__" == "__main__":
        main()