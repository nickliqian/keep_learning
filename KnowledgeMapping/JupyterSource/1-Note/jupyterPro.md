# 安装
pip3 install --upgrade pip
pip3 install jupyter
# 启动
jupyter notebook
# 访问
http://localhost:8888
# 自定义端口启动
jupyter notebook --port 9999
# 不打开浏览器启动
jupyter notebook --no-browser
# 帮助
jupyter notebook --help

# 迁移iPython配置
jupyter migrate
# notebook配置文件目录
~/.jupyter/custom
~/.jupyter/jupyter_notebook_config.py
~/.jupyter/jupyter_nbconvert_config.py
~/.jupyter/jupyter_qtconsole_config.py
~/.jupyter/jupyter_console_config.py
# 更改notebook配置，可以设置 JUPYTER_CONFIG_DIR：
JUPYTER_CONFIG_DIR=./jupyter_config
jupyter notebook

# 修改使用配置文件的路径
jupyter notebook --config=/path/to/myconfig.py

# jupyter software
> Jupyter
> JupyterHub
> nbconvert
> Other language kernel
    - R
    - Java
> Customize
    - Widgets
    - Extensions
    - Dashboards
    - Help


-h, --help
显示帮助信息，包括可用的子命令。

--config-dir
显示配置目录的位置。

--data-dir
显示数据目录的位置。

--runtime-dir
显示数据目录的位置。

--paths
显示所有Jupyter目录和搜索路径。

--json
以机器可读的JSON格式打印目录和搜索路径。

jupyter-foo -> jupyter foo


JUPYTER_CONFIG_DIR for config file location

JUPYTER_PATH for datafile directory locations

JUPYTER_RUNTIME_DIR for runtime file location


创建默认配置文件
jupyter {application} --generate-config
生成文件 -> jupyter_application_config.py
编辑文件，配置属性 -> c.NotebookApp.port = 8754
命令行设置
# 长选项
jupyter notebook --NotebookApp.port=8754
# 短选项
jupyter notebook --port 8754
jupyter notebook no-browser


jupyter {application} --help       # 短选项
jupyter {application} --help-all   # 长选项


=================
jupyter用户界面
    - Jupyter Notebook      基于Web应用程序
    - Jupyter Console       交互式计算终端控制台
    - Jupyter QtConsole     Qt应用程序用于丰富输出的交互式计算
Kernels
    - Ipython               Python中的交互式计算
    - ipywidgets            Jupyter Notebook中的Python交互式小部件
    - ipyparallel           Python提供无缝笔记本集成的轻量级并行计算
格式及转换
    - nbconvert             将动态笔记本转换为静态格式，如HTML，Markdown，LaTeX / PDF和reStrucuredText
    - nbformat              以编程方式处理笔记本文档
Education
    - nbgrader              用于管理，分级和报告基于笔记本的作业的工具
Deployment
    - jupyterhub            多用户notebook应用
    - jupyter-drive         google云驱动
    - nbviewer              notebook静态HTML
    - tmpnb                 在云上使用临时notenook
    - tmpnb-deploy          部署tmpnb
    - dockerspawner         docker内部署jupyterhub
    - docker-stacks         将Jupyter应用程序和内核堆叠为Docker容器
Architecture(体系结构)
    - jupyter_client        Jupyter消息协议的规范和Python中的客户端库
    - jupyter_core          核心功能和其他实用程序




IPython可嵌入解释器到自己的项目中


jupyter孵化项目
- content management extensions - Jupyter Content Management Extensions
- dashboards - Jupyter Dynamic Dashboards from Notebooks
- declarative widgets - Jupyter Declarative Widgets Extension
- kernel gateway bundlers - Converts a notebook to a kernel gateway microservice bundle for download
- showcase - A spot to try demos of one or more incubating Jupyter projects in Binder
- sparkmagic - Jupyter magics and kernels for working with remote Spark clusters
- traittypes - Traitlets types for NumPy, SciPy and friends


# 显示系统信息
python -c "import IPython; print(IPython.sys_info())"
