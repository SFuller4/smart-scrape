from typing import Optional, Type

# from langchain.callbacks.manager import CallbackManagerForToolRun
from pydantic import BaseModel, Field

from tools.base import BaseTool
from twitter_api_wrapper import TwitterAPIClient

class TweetSchema(BaseModel):
    query: str = Field(
        ...,
        description="The text for the tweet.",
    )

class GetRecentTweetsTool(BaseTool):
    """Tool that tweets on Twitter."""

    name = "Tweet on Twitter"

    slug = "tweeterTweet"

    description = "Tweet a message using Twitter."

    args_schema: Type[TweetSchema] = TweetSchema

    tool_id = "6e57b718-8953-448b-98db-fd19c1d1469c"
    
    client = TwitterAPIClient()

    def _run(
        self, query: str, #run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Tweet message and return."""

        result = self.client.analyse_prompt_and_fetch_tweets(query)
        return result
