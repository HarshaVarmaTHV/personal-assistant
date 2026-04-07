import asyncio
from toolbox_core import ToolboxClient, auth_methods

# Replace with the Cloud Run service URL generated in the previous step
URL = "https://toolbox-5r65z6mfgq-uc.a.run.app"

auth_token_provider = auth_methods.aget_google_id_token(URL) # can also use sync method

async def main():
  async with ToolboxClient(
      URL,
      client_headers={"Authorization": auth_token_provider},
  ) as toolbox:
    toolset = await toolbox.load_toolset('firestore_full_access')
    for tool in toolset:
        print(tool._name)


asyncio.run(main())
