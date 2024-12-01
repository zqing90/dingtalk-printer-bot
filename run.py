from app import create_app
# import threading

# from app.dingtalk.dingtalk import initialize_dingtalk_stream

app = create_app()
# # 启动钉钉 Stream 客户端
# client = initialize_dingtalk_stream()



if __name__ == '__main__':
    # # 启动钉钉 Stream 客户端
    # stream_thread = threading.Thread(target=client.start_forever)
    # stream_thread.daemon = True
    # stream_thread.start()

    # 启动 Flask 应用
    app.run(debug=True)