# import asyncio
# from app.tools.report_tools import generate_sales_report

# async def main():
#     result = await generate_sales_report.on_invoke_tool(None, "{}")
#     print(result)

# asyncio.run(main())
from app.tools.report_tools import build_sales_report

path = build_sales_report()
print(path)