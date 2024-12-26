
from pathlib import Path
from app.config import Config
from dingtalk_stream import AckMessage
import dingtalk_stream
from app import g_cache,g_cache_lock
from app.utils.cache import Cache
from app.utils.dingtalk.message import DingTalkMessage




class MyEventHandler(dingtalk_stream.EventHandler):
    async def process(self, event: dingtalk_stream.EventMessage):
        print("MyEventHandler process")
        print(event.headers.event_type,
              event.headers.event_id,
              event.headers.event_born_time,
              event.data)
        return AckMessage.STATUS_OK, 'OK'


class MyCallbackHandler(dingtalk_stream.CallbackHandler):
    async def process(self, message: dingtalk_stream.CallbackMessage):
        print("MyCallbackHandler process")
        print(message.headers.topic,
              message.data)
        # 缓存
        c =Cache(g_cache,g_cache_lock)
        root_path  = Path(__file__).resolve().parent.parent.parent
        m = DingTalkMessage(data=message.data,root_path=root_path,cache=c)
        # 受理信息
        result = m.handle_dingtalk_message()
        print(result)
        return AckMessage.STATUS_OK, 'OK'

    

def initialize_dingtalk_stream():
    credential = dingtalk_stream.Credential(Config.DING_TALK['AppKey'], Config.DING_TALK['AppSecret'])
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_all_event_handler(MyEventHandler())
    client.register_callback_handler(dingtalk_stream.ChatbotMessage.TOPIC, MyCallbackHandler())
    client.start_forever()
