JupyterHub
# 安装依赖
# 如果需要使用多用户，请在root用户下安装依赖，不要在python虚拟环境中
sudo apt-get install npm nodejs-legacy
python3 -m pip install jupyterhub
npm install -g configurable-http-proxy
python3 -m pip install notebook
# 测试安装
jupyterhub -h
configurable-http-proxy -h
# 启动命令
jupyterhub
在浏览器中访问https://localhost:8000，然后使用您的unix账户登录。
要允许多个用户登录到Hub服务器，您必须jupyterhub以root用户身份启动：
sudo jupyterhub