# Import the client
from xdk import Client

# Replace with your actual Bearer Token
client = Client(bearer_token="YOUR_BEARER_TOKEN_HERE")

# Fetch recent Posts mentioning "api"
response = client.posts.search_recent(query="api", max_results=10)

# Print the first Post's text
if response.data:
    print(f"Latest Post: {response.data[0]['text']}")
else:
    print("No Posts found.")