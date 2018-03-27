
### Notes
```angular2html
jupyter notebook my_notebook.ipynb

[NotebookApp] Kernel started: 87f7d2c0-13e3-43df-8bb8-1bd37aaf3373

jupyter qtconsole --existing 87f7d2c0
```


### IPython魔法方法
```
%connect_info 显示连接信息

=====================================================================
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
```
### Comm
Comms允许前端和内核之间的自定义消息。
例如，ipywidgets使用comm来更新小部件状态。
一个comm由一对对象组成，在内核和前端，有一个自动分配的唯一ID。
当一方发送消息时，另一侧的回调由该消息数据触发。
任何一方，前端或内核，都可以打开或关闭通讯。

1. 在前端注册comm，在核心打开comm
2. 在核心注册comm，在前端打开comm

Configuration
    - Jupyter’s common configuration system
    - Notebook server
    - Notebook front-end client
    - Notebook extensions

### Jupyter配置概览
1. Jupyter通用配置系统
2. Notebook服务器配置
使用`jupyter notebook --generate-config`生成`~/.jupyter/jupyter_notebook_config.py`配置文件  
查看配置选项列表：`jupyter notebook --help`
```
# 日志格式
format
    c.Application.log_datefmt = '%Y-%m-%d %H:%M:%S'
    c.Application.log_format = '[%(color)s<%(levelname)7.s %(asctime)s.%(msecs).03d %(name)s>%(end_color)s %(message)s]'
    %(levelname)7.5s -> 7是偏移位数，5是截取字符长度
```
```
# 日志类别和优先级
log_level
    critical   50
    error      40
    warning    30
    info       20
    debug      10
    notset     0
```
服务器可配置功能
- 日志格式、等级
- 配置文件路径、名称、自动生成
- 设置请求头参数和请求规则
- 设置登录身份，权限
- 设置SSL/TSL证书路径
- 设置传输速率
- 

3. 前端客户端配置
4. notebook扩展插件


### 修改notebook登录密码
使用`jupyter notebook password`修改密码，
并在`~/.jupyter/jupyter_notebook_config.json`中保存密码的hash值。  
也可以配置文件`jupyter_notebook_config.py`中也可以配置密码
`c.NotebookApp.password = u'sha1:67c9e60bb8b6:9ffede0825894254b2e042ea597d771089e11aed'`
但如果同时在json文件和py文件中设置了密码，那么会优先使用json文件的设置。

### 使用SSL(HTTPS)加密通信
首先你要有证书文件和秘钥文件，
你可以使用openssl生成自签名证书。例如，以下命令将创建有效期为365天的证书，同时将密钥和证书数据写入同一文件：
```angular2html
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mykey.key -out mycert.pem
```
然后，你就可以在命令行运行的时候指定证书和秘钥文件，启动ssl https加密通讯
```angular2html
jupyter notebook --certfile=mycert.pem --keyfile mykey.key
```
此处有可能出现问题
```angular2html
SSL Error on 12 ('127.0.0.1', 53786): [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:645)
```
是因为浏览器打开时默认打开http连接，会造成服务器短暂的连接错误，待浏览器自动跳转为https连接就可以正常访问了。


### notebook最小配置项
```python3
# Set options for certfile, ip, password, and toggle off
# browser auto-opening
c.NotebookApp.certfile = u'/absolute/path/to/your/certificate/mycert.pem'
c.NotebookApp.keyfile = u'/absolute/path/to/your/certificate/mykey.key'
# Set ip to '*' to bind on all interfaces (ips) for the public server
c.NotebookApp.ip = '*'
c.NotebookApp.password = u'sha1:bcd259ccf...<your hashed password here>'
c.NotebookApp.open_browser = False

# It is a good idea to set a known, fixed port for server access
c.NotebookApp.port = 9999
```  
- ssl整数/秘钥
- 允许访问的ip
- 访问密码
- 是否在允许server时自动打开浏览器
- 服务器端口

### 防火墙设置
要正常运行服务，服务器必须开启配置文件中jupyter_notebook_config.py配置c.NotebookApp.port指定的端口的网络连接。  
防火墙还必须允许来自127.0.0.1（本地主机）的49152至65535端口连接，因为服务器使用这些端口与笔记本内核进行通信。  
内核通信端口由ZeroMQ随机选择，并且可能需要每个内核多个连接，因此必须有大量能够访问的端口。  


### 把notebook嵌入另一个网站
在你的站点配置以下语句
```python3
c.NotebookApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors https://www.traincode.com 'self' "
    }
}
```
然后新建`~/.jupyter/custom/custom.js`
填入以下内容用于配置单标签功能
```python3
define(['base/js/namespace'], function(Jupyter){
    Jupyter._target = '_self';
});
```

### Known issues
1. 当使用代理的时候，Jupyter服务器在使用websocket连接时有可能会失败
2. 使用Docker CMD有时会异常


### Security in the Jupyter Notebook Server (安全性)
正常情况下有以下三种方式认证请求
```
1. 设置header中的Authorization
    ```angular2html
       Authorization: token abcdef...
    ```
2. 在url参数中添加令牌
    ```angular2html
    https://my-notebook/tree/?token=abcdef...
    ```
3. 使用密码登录
```

另外，令牌会在服务器启动的时候自动生成，可以复制到浏览器中，
同时系统也会生成一个打开浏览器记录cookie的一次性标记。
查看所有正在运行的服务器和标记列表 `jupyter notebook list`

使用一下配置禁用认证，即无需认证直接访问：
```
# 禁用令牌
c.NotebookApp.token = ''
# 禁用密码
c.NotebookApp.password = ''
```

### Jupyter安全模式 security model
- 转义不受信任的HTML
- 不执行不受信任的JavaScript
- 不信任Markdown单元格中的HTML和Javascript
- 用户生成的输出是可信的
- 任何其他HTML或Javascript（例如在Markdown单元格中由其他人生成的输出）永远不会被信任
- 信任的核心问题是“当前用户是否这样做过？“

### The details of trust
当`.ipynb`文件被保存时，内容和秘钥会计算一个签名存在数据库中。
文件的内容/秘钥/签名会存在本地数据库中：
```
~/.local/share/jupyter/nbsignatures.db  # Linux
~/Library/Jupyter/nbsignatures.db       # OS X
%APPDATA%/jupyter/nbsignatures.db       # Windows
```
每个签名都对应于用户代码的输出，这是可信任的。
每次打开笔记本时服务器都会计算签名并且检查他是否在数据库中，然后签名匹配那么HTML和JS输出时的加载就是可信任的。


### 更新信任
notebook的信任签名会在保存的时候更新。
如果有任何不受信任的输出在notebook中，notebook将标记为不受信任状态，也不会储存签名。
如果所有不受信任的签名被移除，通过`clear output`或者`重新执行`方式，那么botebook又将被标记为可信。
虽然每个输出都更新了信任，但这仅在单个会话期间进行。一个新加载的笔记本文件要么是可信的，要么不是完整的。


### 显示信任
有时候重新执行笔记本来生成信任的输出不是一种选择，要么是因为依赖不可用，要么需要很长时间。
用户可以通过两种方式显式信任笔记本(生成签名)：
```
# 在命令行中使用
jupyter trust /path/to/notebook.ipynb
# 加载文件后，使用 File/Trust Notebook
```
这两种方法只是加载笔记本，计算一个新的签名，并将该签名添加到用户的数据库。


### notebook主题机制
可能会提供主题机制: 使用custom.css或者CSS/HTML输出，但只对收信任的文档有效。


### 合作 Collaboration
合作使用notebook共享文件时，信任机制会导致每次共享都是从一个不受信任的状态开始的。
三种方法：
```
- 重新把notebook跑一遍
- 使用命令行或者文件信任个能来更新信任
- 共享签名数据库，修改配置如下，指定数据库路径
c.NotebookNotary.data_dir = "/path/to/signature_dir"
```


## 配置notebook前端
这个文档是关于如何为Notebook JavaScript保存一些配置选项的粗略解释。
由于大多数选项都传递到其他库，所以没有完整的配置选项列表，这意味着如果没有任何错误消息，就可以忽略非有效配置。
### 如何进行前端配置工作
- get a handle of a configurable JavaScript object.
>获取可配置JavaScript对象的句柄
- access its configuration attribute.
>访问配置属性
- update its configuration attribute with a JSON patch.
>使用JSON补丁更新配置属性
### 示例配置
为CodeMirror代码单元indentUnit的默认配置
在控制台运行如下代码，然后刷新页面，就可以修改缩进。
```
// 修改缩进
var cell = Jupyter.notebook.get_selected_cell();
var config = cell.config;
var patch = {
      CodeCell:{
        cm_config:{indentUnit:2}
      }
    };
config.update(patch)

// 恢复缩进
var cell = Jupyter.notebook.get_selected_cell();
var config = cell.config;
var patch = {
      CodeCell:{
        cm_config:{indentUnit: null} // only change here.
      }
    }
config.update(patch)
```
### 可持久的配置
通过修改`~/.jupyter/nbconfig/<section>.json`下的内容
可以然后前端配置持久修改
section可以是notebook/tree/editor等
这会应用到所有页面


## 将Jupyter扩展作为Python包分发
notebook客户端和服务端都是可深度定制的
- nbextension  
    单个js文件或者包含css/js文件的文件夹等  
    至少包含一个js模块/包，作为一个AMD模块导出为一个`load_ipython_extension`函数
- server extension  
    一个可导入的Python模块，需要实现`load_jupyter_server_extension`函数
- bundler extension
    一个可导入的Python模块，生成 File->Download as / Deploy 作为菜单项触发器
### 安装Jupyter扩展
```
pip install helpful_package
# or
conda install helpful_package
# or
apt-get install helpful_package
# where 'helpful_package' is a Python package containing one or more Jupyter Extensions
```
#### 使用服务器扩展
```
# pip user
jupyter serverextension enable --py helpful_package
# virtualenv or conda user 
# Make sure that your virtualenv or conda environment is activated
[source] activate my-environment
jupyter serverextension enable --py helpful_package --sys-prefix
```
#### 安装nbextension扩展
安装前端扩展，默认情况不启用
```
jupyter nbextension install --py helpful_package # or --sys-prefix if using virtualenv or conda
```
#### 启用nbextension扩展
如果每次在浏览器中加载Jupyter应用程序（例如实验室，笔记本，仪表板，终端）时应该加载一个包
则可以使用以下命令启用nbextension：
```
jupyter nbextension enable --py helpful_package # or --sys-prefix if using virtualenv or conda
```
### 查看扩展列表
```
jupyter nbextension list
jupyter serverextension list
jupyter bundlerextension list
```

### 在包中添加资源

### 示例-服务器扩展
```
- setup.py
- MANIFEST.in
- my_module/
  - __init__.py
```
在`my_module/__init__.py`中定义`load_jupyter_server_extension`
```
def _jupyter_server_extension_paths():
    return [{
        "module": "my_module"
    }]

def load_jupyter_server_extension(nbapp):
    nbapp.log.info("my module enabled!")
```
安装和启用
```
jupyter serverextension enable --py my_module [--sys-prefix]
```

### 示例-服务器扩展和notebook扩展
```
- setup.py
- MANIFEST.in
- my_fancy_module/
  - __init__.py
  - static/
    index.js
```
修改文件`my_fancy_module/__init__.py`
```
def _jupyter_server_extension_paths():
    return [{
        "module": "my_fancy_module"
    }]

# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `my_fancy_module` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest="my_fancy_module",
        # _also_ in the `nbextension/` namespace
        require="my_fancy_module/index")]

def load_jupyter_server_extension(nbapp):
    nbapp.log.info("my module enabled!")
```
安装和启用前端和服务端扩展
```
jupyter nbextension install --py my_fancy_module [--sys-prefix|--user]
jupyter nbextension enable --py my_fancy_module [--sys-prefix|--system]
jupyter serverextension enable --py my_fancy_module [--sys-prefix|--system]
```

### 示例-绑定扩展


...


## 扩展Notebook


