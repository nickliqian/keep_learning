jupyter notebook my_notebook.ipynb

[NotebookApp] Kernel started: 87f7d2c0-13e3-43df-8bb8-1bd37aaf3373

jupyter qtconsole --existing 87f7d2c0

IPython魔法方法
%connect_info 显示连接信息
======================================================================
{
  "iopub_port": 58689,
  "hb_port": 36988,
  "stdin_port": 54036,
  "key": "e0f5c41f-9180ef068404b7b6934cf933",
  "shell_port": 55643,
  "kernel_name": "",
  "signature_scheme": "hmac-sha256",
  "transport": "tcp",
  "control_port": 41644,
  "ip": "127.0.0.1"
}

Paste the above JSON into a file, and connect with:
    $> jupyter <app> --existing <file>
or, if you are local, you can connect with just:
    $> jupyter <app> --existing kernel-48ac61ec-7950-47e7-a955-dfac2ac717c5.json
or even just:
    $> jupyter <app> --existing
if this is the most recent Jupyter kernel you have started.
=====================================================================

Comm
Comms允许前端和内核之间的自定义消息。
例如，ipywidgets使用comm来更新小部件状态。
一个comm由一对对象组成，在内核和前端，有一个自动分配的唯一ID。
当一方发送消息时，另一侧的回调由该消息数据触发。
任何一方，前端或内核，都可以打开或关闭通讯。