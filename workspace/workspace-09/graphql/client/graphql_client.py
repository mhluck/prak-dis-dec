import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

async def main():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    
    # Create a GraphQL client using the defined transport
    client = Client(transport=transport)
    
    # Provide a GraphQL query
    query = gql(
        """
        query getSdms {
            sdms {
                id
                npp
                nama
            }
        }
        """
    )
    
    # Execute the query
    async with client as session:
        result = await session.execute(query)
        print(result)

asyncio.run(main())