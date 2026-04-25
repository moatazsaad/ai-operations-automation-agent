import asyncio
import sys
from agents import Runner
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from app.agent import create_operations_agent

# Define main async function
async def main():
    user_request = " ".join(sys.argv[1:])
    if not user_request:
        user_request = "Generate a weekly sales report."
        
    # Create MCP server parameters to launch it locally
    params = MCPServerStdioParams(command="python", args=["-m", "app.mcp_server"])

    # Create MCP stdio client that will connect to the MCP server process
    server = MCPServerStdio(params=params, cache_tools_list=True, name="operations-mcp")

    # Open MCP server connection
    async with server:
        
        # Build  agent and attach the connected MCP server
        agent = create_operations_agent(server)

        # Run agent 
        result = await Runner.run(agent, user_request)
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())