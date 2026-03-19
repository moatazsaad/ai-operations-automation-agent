# import the revenue tool from the tools file
from app.tools.database_tools import get_total_revenue


# call the function and store the returned value
revenue = get_total_revenue()

# print the result
print("Total revenue:", revenue)