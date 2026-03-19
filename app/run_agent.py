import asyncio
import sys

from agents import Runner
from app.agent import agent


async def main():

    # get user request from command line
    user_request = " ".join(sys.argv[1:])

    # fallback if nothing provided
    if not user_request:
        user_request = "Generate a weekly sales report."

    result = await Runner.run(
        agent,
        user_request
    )

    print(result.final_output)


asyncio.run(main())