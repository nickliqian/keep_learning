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