# for type hints 
from typing import Any
from mcp.server.fastmcp import FastMCP

#initialize the weather server
mcp = FastMCP("Weather")

#constants
NWS_API_BASE = "the api to grad weather will come her "
USER_AGENT = "The version of my app will go here eg. weather-app/1.0"

#helper functions for the tool 
