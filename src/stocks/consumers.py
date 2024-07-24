from channels.generic.websocket import AsyncWebsocketConsumer
import json


class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        stock_slug = self.scope["url_route"]["kwargs"]["slug"]
        self.stock_slug = stock_slug
        self.room_group_name = stock_slug
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # return await super().connect()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # return await super().disconnect(code)

    # async def receive(self, text_data=None, bytes_data=None):
    #     text_data_json = json.loads(text_data)
    #     prices = text_data_json["prices"]
    #     await self.group_send_prices(prices)
    #     return await super().receive(text_data, bytes_data)

    # async def group_send_prices(self, prices):
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             "type": "stock_prices_message",
    #             "prices": prices,
    #         },
    #     )

    async def stock_prices_message(self, event):
        prices = event["prices"]
        await self.send(text_data=json.dumps({"prices": prices}))
