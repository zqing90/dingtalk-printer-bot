class Config:
    # 打印机设置
    PRINTER ={
        "name":"Canon_G3000_series_cups",
        "options":{
            'media': 'A4',
            'color-mode': 'color',
            }
    }
    CUPS = {
        "host": "localhost",# 使用远程打印有BUG 找不到对应的文件
        "port": 631,
    }
    DING_TALK = {
        'AgentId':'<your agentId>',
        'AppKey':'<your appKey>',
        'AppSecret':'<your appSecret>',
        'AccessTokenURL':'https://api.dingtalk.com/v1.0/oauth2/accessToken',
        'DownloaFiledURL':'https://api.dingtalk.com/v1.0/robot/messageFiles/download',
        "SendMessageURL":'https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend'
    }
    FONT = {
        "font_name":"SimSun", # 默认字体：宋体
        "font_path":"SIMSUN.TTC", # 路径：app/fonts，可自行添加对应的字体
        "font_size":16 # 默认字体14
    }
