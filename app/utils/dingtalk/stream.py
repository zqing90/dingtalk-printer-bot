# from app.config import Config
# from dingtalk_stream import AckMessage
# import dingtalk_stream



# class MyEventHandler(dingtalk_stream.EventHandler):
#     async def process(self, event: dingtalk_stream.EventMessage):
#         print("process1")
#         print(event.headers.event_type,
#               event.headers.event_id,
#               event.headers.event_born_time,
#               event.data)
#         return AckMessage.STATUS_OK, 'OK'


# class MyCallbackHandler(dingtalk_stream.CallbackHandler):
#     async def process(self, message: dingtalk_stream.CallbackMessage):
#         print("process2")
#         print(message.headers.topic,
#               message.data)
#         return AckMessage.STATUS_OK, 'OK'

    

# def initialize_dingtalk_stream():
#     credential = dingtalk_stream.Credential(Config.DING_TALK['AppKey'], Config.DING_TALK['AppSecret'])
#     client = dingtalk_stream.DingTalkStreamClient(credential)
#     client.register_all_event_handler(MyEventHandler())
#     # client.register_callback_handler(dingtalk_stream.ChatbotMessage.TOPIC, MyCallbackHandler())
#     client.register_callback_handler(dingtalk_stream.ChatbotMessage.TOPIC, MyCallbackHandler())
#     client.start_forever()
