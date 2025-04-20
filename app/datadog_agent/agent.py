# agent.py (modify get_tools_async and other parts as needed)
import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters

load_dotenv('../.env')
async def get_tools_async():
  """Gets tools from the File System MCP Server."""
  print("Attempting to connect to MCP Filesystem server...")
  tools, exit_stack = await MCPToolset.from_server(
      # Use StdioServerParameters for local process communication
      connection_params=StdioServerParameters(
          command='node',
          args=[ "/Users/yizhenzhong/Documents/AI/agi_hackathon/mcp-server-datadog/build/index.js",
          ],
          env={
              "DATADOG_APP_KEY": "44ff78f74586be29f41b592810fc7444e2968044",
              "DATADOG_API_KEY": "869a92f90e5275d16854809c568f6c43",
              "DATADOG_SITE": "datadoghq.eu"
          }
      )
      # For remote servers, you would use SseServerParams instead:
      # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
  )
  print("MCP Toolset created successfully.")
  # MCP requires maintaining a connection to the local MCP Server.
  # exit_stack manages the cleanup of this connection.
  return tools, exit_stack

async def create_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_tools_async()

  agent = LlmAgent(
      model='gemini-2.0-flash', # Adjust model name if needed based on availability
      name='filesystem_assistant',
      instruction='Datadog agent to help with monitoring and alerting.',
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return agent, exit_stack


root_agent = create_agent()

