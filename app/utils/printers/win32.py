
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
    try:
        print(f'开始打印文件：{file_path}')
        import win32print
        import win32api
        
        # 获取默认打印机
        printer_name = win32print.GetDefaultPrinter()
        # 打印文件
        print_code = win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)
        print(f"文件已发送到打印机，print_code: {print_code}")
        if print_code > 32:
            return CommonResult(status=True,message=f"文件已发送到打印机，print_code: {print_code}",data={'print_code':print_code})
        else:
            return CommonResult(status=False,message=f"文件打印失败，print_code: {print_code}")

    except Exception as e:
        print(f"未知错误: {e}")
        return CommonResult(status=False,message=f"未知错误: {e}")



def print_text_file(file_path, printer_name=None, color=True, paper_size='A4'):
    return CommonResult(status=False,message="开发中……")
    # import win32print
    # import win32ui
    # import win32con
    # # 获取默认打印机的名字
    # if printer_name is None:
    #     printer_name = win32print.GetDefaultPrinter()
    # print(f"Printing to: {printer_name}")

    # # 打开设备上下文
    # hDC = win32ui.CreateDC()
    # hDC.CreatePrinterDC(printer_name)

    # # 设置打印属性
    # devmode = win32print.GetPrinter(hDC.GetHandle(), 2)["pDevMode"]
    
    # # 设置纸张大小
    # if paper_size == 'A4':
    #     devmode.PaperSize = 9  # A4 (9)
    # elif paper_size == 'Letter':
    #     devmode.PaperSize = 1  # Letter (1)
    # else:
    #     raise ValueError("Unsupported paper size. Use 'A4' or 'Letter'.")

    # # 设置颜色模式
    # if not color:
    #     devmode.Color = 2  # 2 for monochrome
    # else:
    #     devmode.Color = 1  # 1 for color

    # # 应用设置
    # hDC.SetDeviceMode(devmode)

    # # 创建一个兼容的内存设备上下文
    # hMemDC = hDC.CreateCompatibleDC()

    # # 创建一个位图
    # bitmap = win32ui.CreateBitmap()
    # bitmap.CreateCompatibleBitmap(hDC, 612, 792)  # A4 纸张尺寸 (595x842) 或者 Letter (612x792)
    # hMemDC.SelectObject(bitmap)

    # # 设置字体
    # font = win32ui.CreateFont({
    #     "name": "Arial",
    #     "height": 12,
    #     "weight": 400,
    #     "italic": 0,
    #     "underline": 0,
    # })
    # hMemDC.SelectObject(font)

    # # 读取文本文件
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     text = file.read()

    # # 绘制文本
    # y = 10  # 起始位置
    # for line in text.splitlines():
    #     hMemDC.TextOut(10, y, line)
    #     y += 14  # 每行的高度

    # # 开始文档
    # hDC.StartDoc(file_path)
    # hDC.StartPage()

    # # 将位图复制到打印机设备上下文
    # hDC.BitBlt((0, 0), (bitmap.GetWidth(), bitmap.GetHeight()), hMemDC, (0, 0), win32con.SRCCOPY)

    # # 结束页面和文档
    # hDC.EndPage()
    # hDC.EndDoc()

    # # 清理
    # hDC.DeleteDC()
    # hMemDC.DeleteDC()
    # win32gui.DeleteObject(bitmap.GetHandle())

