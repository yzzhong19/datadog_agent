# agent.py (modify get_tools_async and other parts as needed)

import asyncio
import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters

load_dotenv('../../.env')

async def get_tools_async():
  """Gets tools from the MCP server."""
  print("Attempting to connect to MCP server...")

  tools, exit_stack = await MCPToolset.from_server(
      # Use StdioServerParameters for local process communication
      connection_params=StdioServerParameters(
          command='node',
          args=[
            "/Users/sherwoodcallaway/code/agihouse-hackathon/datadog-mcp/dist/index.js",
          ],
          env={
              "DATADOG_APP_KEY": os.getenv("DATADOG_APP_KEY"),
              "DATADOG_API_KEY": os.getenv("DATADOG_API_KEY"),
              "DATADOG_SITE": os.getenv("DATADOG_SITE")
          }
      )
      # For remote servers, you would use SseServerParams instead:
      # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
  )

  print("MCP toolset created successfully")

  # MCP requires maintaining a connection to the local MCP Server.
  # exit_stack manages the cleanup of this connection.
  return tools, exit_stack

async def create_agent():
  """Creates an agent with tools from MCP server."""

  # Get tools from MCP server
  tools, exit_stack = await get_tools_async()

  agent = LlmAgent(
      model='gemini-2.0-flash',
      name='datadog_agent',
      instruction='Datadog agent',
      tools=tools,
  )
  return agent, exit_stack


root_agent = create_agent()

