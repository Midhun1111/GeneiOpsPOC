# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import requests
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        print("Message Activity encountered")
        user_message = turn_context.activity.text
        team_id = turn_context.activity.conversation.id  
        channel_id = turn_context.activity.channel_data['teamsChannelId']
        message_id = turn_context.activity.id 

        data = {
            "query_text": user_message,
            "team_id": team_id,
            "channel_id": channel_id,
            "message_id":message_id
        }
        try:
            api_response = await asyncio.wait_for(self.call_external_api(data), timeout=600)
            result=api_response['response']
            await turn_context.send_activity(f"'{result}'")
        except asyncio.TimeoutError:
            await turn_context.send_activity("Sorry, the API call timed out. Please try again later.")
        except Exception as e:
            print(e,e.__traceback__.tb_lineno)
            await turn_context.send_activity(f"An error occurred: {str(e)}")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Welcome to Geneiops!")

    async def call_external_api(self, data):
        api_url = "https://8h7d959s-5000.inc1.devtunnels.ms/process"
        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()