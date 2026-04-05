# 你的 AgentServer Custom Action 文件
import subprocess
from maa.context import Context
from maa.custom_action import CustomAction
from maa.agent.agent_server import AgentServer


@AgentServer.custom_action("ConnectBBChannel_popup_mianze")
class ConnectBBChannel_popup_mianzeAction(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        print("主程序：即将挂起当前流程，呼叫子进程处理 BBchannel...")

        # 阻塞式运行 ConnectBBChannel_runner.py。capture_output 会捕获子进程的 print 方便你调试
        result = subprocess.run(
            # 这里路径是以运行的MFA文件为基准的
            ["python", "agent/ConnectBBChannel_runner.py"],
            capture_output=True,
            text=True
        )

        # 打印子进程的运行日志
        print("====== 子进程输出日志开始 ======")
        print(result.stdout)
        if result.stderr:
            print("错误信息:", result.stderr)
        print("====== 子进程输出日志结束 ======")

        if result.returncode == 0:
            print("主程序：临时任务已顺利完成，主流水线继续往下走！")
            return True
        else:
            print("主程序：子进程执行中出现异常。")
            return False