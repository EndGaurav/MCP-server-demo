# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP
import os
import math 
import requests
import sys

# Create an MCP server
mcp = FastMCP("Demo")
sys.stdout.reconfigure(encoding='utf-8')
WEATHER_API_KEY=os.getenv("WEATHER_API_KEY")
print(WEATHER_API_KEY)

NOTES_FILE = os.path.join(os.path.dirname(__file__),"notes.txt")


def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as file:
            file.write("")
            
            
# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    # this """tool description""" is known as docstring.
    # it is very useful of llm to understand your tool's parameter, description, return value data.
    """Add two numbers"""
    return a + b

@mcp.tool()
def add_note(message: str) -> str: 
    """
    Append a new note to the sticky note file.
    
    Args: message (str): The note content to be added.
    
    Returns: str: Confirmation message indicating the note was saved.
    """
    ensure_file()
    
    with open(NOTES_FILE, "a") as file:
        file.write(message + "\n")
        
    return "Note saved!"

@mcp.tool()
def read_notes() -> str:
    """
    Read the notes from the given file.
    
    Returns: str: content of the file and if the content is not available then a message which will indicate there is no content available. 
    """
    ensure_file()
    with open(NOTES_FILE, 'r') as file:
        content = file.read().strip()
        return content or "No notes yet"
    
@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Read the notes from the given file.
    
    Returns: 
        str: The last note entry. If no notes exist, a default message is returned.  
    """
    ensure_file()
    with open(NOTES_FILE, 'r') as file:
        lines = file.readline()
    return lines[-1].strip() if lines else "No notes yet"
        
@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize all current notes.
    
    Returns: 
        str: A prompt string that includes all the notes and asks for a summary.
            If no notes exist, a message will be shown indicarting that.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as file:
        content = file.read().stripe()
        if not content:
            return "There is no notes yet"
        return f"Summarize the current notes: {content}"
    
@mcp.tool()
def get_weather(city_name: str) -> str:
    """
    Getting the weather data for a given city_name. 
    Args: 
        city_name (str): city name whoes weather needs to be get.
    Returns: str: tell me weather information if it is available and if not available, default message will be provided.
    
    """
    
    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={city_name}&appid={WEATHER_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        parsed_response = response.json()
        # print(parsed_response)
        return f"The weather in {city_name} is {math.floor(parsed_response['main']['temp'])}."
    return "Something went wrong"

