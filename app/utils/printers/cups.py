
from app.config import Config
from app.models.result import CommonResult

def print_file(file_path, printer_name=None, print_options=None):
    """_summary_

    Args:
        file_path (str): 文件路径
        printer_name (str, None): 打印机名称. Defaults to None.
        print_options (str, None): 打印选项. Defaults to None.

    Returns:
        CommonResult: _description_
    """
    import cups
    try:
        print(f'开始打印文件：{file_path}')
        host = Config.CUPS['host']
        port = Config.CUPS['port']

        # 连接到 CUPS 服务器
        conn = cups.Connection(host = host, port = port)

        # 获取可用的打印机列表
        printers = conn.getPrinters()
        if printer_name and printer_name in printers:
            # 如果指定了打印机名称并且该打印机存在
            print(f"正在使用指定的打印机: {printer_name}")
            selected_printer = printer_name
        else:
            # 使用默认打印机
            selected_printer = list(printers.keys())[0]
            print(f"正在使用默认打印机: {selected_printer}")
        
        if print_options is None:
            # 默认打印机设置打印选项
            print_options = {
                'media': 'A4',  # 设置纸张大小
                'color-mode': 'color'  # 设置彩色或黑白打印
            }
        
        # 发送文件到打印机
        job_id = conn.printFile(selected_printer, file_path, "printer bot", print_options)
        
        print(f"文件已发送到打印机，作业ID: {job_id}")
        return CommonResult(status=True,message=f"文件已发送到打印机，作业ID: {job_id}",data={'job_id':job_id})
    
    except cups.IPPError as e:
        print(f"CUPS 错误: {e}")
        return CommonResult(status=False,message=f"CUPS错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
        return CommonResult(status=False,message=f"未知错误: {e}")

