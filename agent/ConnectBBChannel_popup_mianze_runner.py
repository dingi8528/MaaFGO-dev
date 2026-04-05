from maa.toolkit import Toolkit
from maa.tasker import Tasker
from maa.resource import Resource
from maa.controller import (
    Win32Controller,
    MaaWin32ScreencapMethodEnum,
    MaaWin32InputMethodEnum,
)



def run_temp_task():
    # 1. 初始化 MAA 环境 (纯净进程中必须先执行此步骤)
    Toolkit.init_option("./")

    print("正在使用 Toolkit 扫描系统窗口...")
    all_windows = Toolkit.find_desktop_windows()

    target_hwnd = None
    target_title = ""

    # 2. 模糊匹配寻找包含 "BBchannel" 的窗口
    for win in all_windows:
        # 兼容不同 MaaFramework 版本的属性名
        title = getattr(win, "window_name", getattr(win, "title", ""))

        if "免责声明" in title:
            target_hwnd = win.hwnd
            target_title = title
            print(f"--> 发现目标临时窗口: [{target_title}], 句柄: {target_hwnd}")
            break

    if not target_hwnd:
        print("--> 错误: 未找到标题包含 'BBchannel' 的窗口，临时任务退出。")
        return False

    # 3. 初始化并连接 Win32 控制器 (使用你查确定的 hWnd 关键字)
    print("--> 正在建立临时窗口的底层连接...")
    controller = Win32Controller(
        hWnd=target_hwnd,
        screencap_method=MaaWin32ScreencapMethodEnum.ScreenDC,
        mouse_method=MaaWin32InputMethodEnum.Seize,
        keyboard_method=MaaWin32InputMethodEnum.Seize,
    )
    controller.post_connection().wait()
    print("--> 临时窗口连接成功！")

    # 4. 绑定资源与任务器
    resource = Resource()
    tasker = Tasker()
    tasker.bind(resource, controller)

    # 5. 加载专属于临时窗口的流水线资源
    # 注意：你需要在这里指定临时任务专属的 resource 文件夹路径
    # 这里路径是以运行的MFA文件为基准的
    resource_path = "../resource"
    resource.post_bundle(resource_path).wait()

    if not tasker.inited:
        print("--> 错误: Tasker 初始化失败，请检查资源路径。")
        return False

    # 6. 下发临时流水线任务
    print("--> 开始执行临时窗口的流水线任务...")
    # 把 "YourTempTaskEntry" 换成你准备好的 JSON 文件里的入口任务名
    task_job = tasker.post_task("BBC-操作开始")
    task_job.wait()

    print("--> 临时窗口任务全部执行完毕，进程准备退出。")
    return True


if __name__ == "__main__":
    run_temp_task()