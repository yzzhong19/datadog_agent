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
from google.adk.models.lite_llm import LiteLlm

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
              "DD_API_KEY": "869a92f90e5275d16854809c568f6c43",
              "DD_APP_KEY": "44ff78f74586be29f41b592810fc7444e2968044",
              "DD_SITE": "datadoghq.eu",
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

  # Instantiate the agent
  agent = LlmAgent(
      model=LiteLlm(model="anthropic/claude-3-5-sonnet-20240620"),
      name='datadog_agent',
      instruction='Datadog agent',
      tools=tools,
  )

  return agent, exit_stack


root_agent = create_agent()

