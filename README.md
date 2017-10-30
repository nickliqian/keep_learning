# Ralph Project Doc Translate To Chinese
翻译AMS项目[Ralph NG](http://ralph-ng.readthedocs.io/en/latest/)开发文档。


# Ralph NG
Ralph NG是一个简单而强大的资产管理系统，DCIM和CMDB数据中心和后台系统。

|缩写| 英文全称| 中文名称|
|-|-|-|
|DCIM|Data Center Infrastructure Management|数据中心基础设施管理|
|CMDB|Configuration Management Database|配置管理数据库|

特征：
- 跟踪资产购买及其生命周期
- 自动发现现有的硬件
- 生成灵活而准确的成本报告

免责声明：Ralph NG是Ralph 2.x的精简和简化版本。 本文档不包括可在此处访问的旧版本。

## 安装指南

对于生产，我们提供deb程序和docker（组合）镜像。我们只支持AMD64平台上的Ubuntu 14.04 Trusty发行版。

另一方面，如果您是开发人员，我们强烈建议使用我们的`Vagrant`，`vagrant`目录包含了许多我们开发的附属项目。

### Debian / Ubuntu包 - 推荐
确保您的安装是纯净版的Ubuntu 14.04，没有安装任何其他软件包，并`apt-transport-https`安装。

    sudo apt-get update && sudo apt-get install apt-transport-https
现在，添加我们的官方ralph存储库：

    sudo apt-key adv --keyserver  hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61
    sudo sh -c "echo 'deb https://dl.bintray.com/vi4m/ralph wheezy main' >  /etc/apt/sources.list.d/vi4m_ralph.list"
然后，只需安装ralph的传统方式：

    sudo apt-get update
    sudo apt-get install ralph-core redis-server mysql-server
注意：主要的Ralph实例需要安装redis和mysql服务器。如果您只想在某个地方安装ralph代理，只需安装`ralph-core`并将其指向网络上某处的特定mysql和redis实例即可。

#### 配置
创建数据库。

    > mysql -u root
    > CREATE database ralph default character set 'utf8';

#### 设置
我们正在制定一些全面的配置管理文件。目前，我们只是读取一些环境变量，所以只需要粘贴到`〜/ .profile`中的某个地方，就可以根据需要自定义它们。

    cat〜/ .profile

    export DATABASE_NAME=ralph
    export DATABASE_USER=someuser
    export DATABASE_PASSWORD=somepassword
    export DATABASE_HOST=127.0.0.1
    export PATH=/opt/ralph/ralph-core/bin/:$PATH
    export RALPH_DEBUG=1
#### 初始化
1. 键入`ralph migrate`以在数据库中创建表。
2. 键入`ralph sitetree_resync_apps`重新加载菜单。
3. 键入`ralph createsuperuser`以添加新用户。

运行你的ralph实例 `ralph runserver 0.0.0.0:8000`

现在，将您的浏览器指向`http:// localhost:8000`并登录。Happy Ralphing!

### Docker安装（试验版）
您可以在[https://github.com/allegro/ralph/tree/ng/contrib](https://github.com/allegro/ralph/tree/ng/contrib)目录中找到试验版的docker-compose配置。请注意，它仍然是测试版。

#### 安装
首先安装`docker`和`docker-compose`。

#### 创建撰写配置
将`docker-compose.yml.tmpl`外部ralph源复制到docker-compose.yml并进行调整。

#### 构建
然后构建ralph：

    docker-compose build
初始化数据库运行：

    docker-compose run --rm web /root/init.sh
请注意，这个命令最初只能执行一次。

如果您需要使用一些演示数据来填充Ralph：

    docker-compose run --rm web ralph demodata
#### 运行
最后运行拉尔夫：

    docker-compose up -d
Ralph应该可以通过`http://127.0.0.1`进行访问（或者如果您正在使用`boot2docker`的`$(boot2docker ip)`）。可用的文档在`http://127.0.0.1/docs`。

如果你升级ralph镜像（源代码）运行：

    docker-compose run --rm web /root/upgrade.sh
### 从Ralph 2迁移
如果您以前使用过Ralph 2，并希望保存所有数据，请参阅Ralph 2指南的迁移


### LDAP认证

可以通过各种LDAP / AD系统启用认证。

您将需要安装`pip install -r requirements/prod_ldap.txt`。然后在本地设置中添加LDAP作为身份验证后端：

      AUTHENTICATION_BACKENDS = (
      'django_auth_ldap.backend.LDAPBackend',
      'django.contrib.auth.backends.ModelBackend',
      )
      LOGGING['loggers']['django_auth_ldap'] = {
      'handlers': ['file'],
      'propagate': True,
      'level': 'DEBUG',
      }
您将需要配置LDAP连接以及将远程用户和组映射到本地连接。有关详细信息，请参阅官方django-auth-ldap文档[http://packages.python.org/django-auth-ldap](http://packages.python.org/django-auth-ldap)。例如，连接到Active Directory服务可能如下所示：

    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
    AUTH_LDAP_SERVER_URI = "ldap://activedirectory.domain:389"
    AUTH_LDAP_BIND_DN = "secret"
    AUTH_LDAP_BIND_PASSWORD = "secret"
    AUTH_LDAP_PROTOCOL_VERSION = 3
    AUTH_LDAP_USER_USERNAME_ATTR = "sAMAccountName"
    AUTH_LDAP_USER_SEARCH_BASE = "DC=allegrogroup,DC=internal"
    AUTH_LDAP_USER_SEARCH_FILTER = '(&(objectClass=*)({0}=%(user)s))'.format(AUTH_LDAP_USER_USERNAME_ATTR)
    AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_USER_SEARCH_BASE,ldap.SCOPE_SUBTREE, AUTH_LDAP_USER_SEARCH_FILTER)
    AUTH_LDAP_USER_ATTR_MAP = {
      "first_name": "givenName",
      "last_name": "sn",
      "email": "mail",
      "company": "company",
      "manager": "manager",
      "department": "department",
      "employee_id": "employeeID",
      "location": "officeName",
      "country": "ISO-country-code",
    }
但是，当使用OpenDJ作为LDAP服务器时，`AUTH_LDAP_USER_USERNAME_ATTR`应等于`uid`：

    AUTH_LDAP_USER_USERNAME_ATTR = "uid"
对于其他实现，`objectClass`可能具有以下值：

- Active Directory：objectClass = user，
- Novell eDirectory：objectClass = inetOrgPerson，
- 打开LDAP：objectClass = posixAccount


`Manager`是特殊字段，被视为另一个用户的参考，例如“CN = John Smith，OU = TOR，OU = Corp-Users，DC = mydomain，DC = internal”映射到“John Smith”文本。

`Country`是特殊字段，该字段的值必须是ISO 3166-1 alfa-2格式的地区代码 。

Ralph提供ldap组到django组映射。所有你需要做的是：

- import custom 导入自定义的 `MappedGroupOfNamesType`
- 设置组镜像
- 声明映射


    from ralph.account.ldap import MappedGroupOfNamesType
    AUTH_LDAP_GROUP_MAPPING = {
      'CN=_gr_ralph,OU=Other,DC=mygroups,DC=domain': "staff",
      'CN=_gr_ralph_assets_buyer,OU=Other,DC=mygroups,DC=domain': "assets-buyer",
      'CN=_gr_ralph_assets_helper,OU=Other,DC=mygroups,DC=domain': "assets-helper",
      'CN=_gr_ralph_assets_staff,OU=Other,DC=mygroups,DC=domain': "assets-staff",
      'CN=_gr_ralph_admin,OU=Other,DC=mygroups,DC=domain': "superuser",
    }
    AUTH_LDAP_MIRROR_GROUPS = True
    AUTH_LDAP_GROUP_TYPE = MappedGroupOfNamesType(name_attr="cn")
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch("DC=organization,DC=internal",
    ldap.SCOPE_SUBTREE, '(objectClass=group)')


如果您将一个LDAP组嵌套在另一个LDAP组中，并希望在Ralph中使用这样的（父组）组，则必须在以下位置定义此映射`AUTH_LDAP_NESTED_GROUPS`：

    AUTH_LDAP_NESTED_GROUPS = {
      'CN=_gr_ralph_users,OU=Other,DC=mygroups,DC=domain': "staff",  # _gr_ralph_users contains other LDAP groups inside
    }


注意：对于OpenDJ实现`AUTH_LDAP_GROUP_MAPPING`不是强制性的。`AUTH_LDAP_GROUP_TYPE`并`AUTH_LDAP_GROUP_SEARCH`应设置如下：

    from django_auth_ldap.config import GroupOfUniqueNamesType
    AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType()
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch("DC=organization,DC=internal",
      ldap.SCOPE_SUBTREE, '(structuralObjectClass=groupOfUniqueNames)')


如果您想要定义具有与ralph角色相同的名称的ldap组，则不应声明映射`AUTH_LDAP_GROUP_MAPPING`。如果有任何一个映射定义，另一个组将被过滤。一些群体有特殊的含义。例如，用户需要在`active`状态登录， ` superuser`给予超级用户权限。你可以参考`groups` 阅读更多的信息。

如果您不想将所有用户导入到ralph，您可以定义用户筛选：

    AUTH_LDAP_USER_FILTER = '(|(memberOf=CN=_gr_ralph_group1,OU=something,'\
    'DC=mygroup,DC=domain)(memberOf=CN=_gr_ralph_group2,OU=something else,'\
    'DC=mygroups,DC=domain))'


如果OpenDJ用的是`isMemberOf`而不是`memberOf`。

要同步用户列表，您必须运行命令：

    $ ralph ldap_sync

在此过程中，脚本将报告每加载的第100个项目的进度。

### 与OpenStack同步
Ralph 3支持与OpenStack的单向同步。可以从OpenStack下载数据，包括项目和实例。所有同步数据将以只读模式在Ralph中可用。只能更改服务环境，标签和备注字段。

注意：一个CloudHost 的服务环境是从一个Cloud Project继承而来的 。

#### 安装
要启用openstack_sync插件，您必须通过执行以下来命令安装python依赖：  `pip install -r requirements/openstack.txt`

还有必要将OpenStack实例配置添加到本地设置中。示例配置应如下所示：

    OPENSTACK_INSTANCES = [
    {
    'username': 'someuser',
    'password': 'somepassword',
    'tenant_name':  'admin',
    'version':  '2.0',
    'auth_url': 'http://1.2.3.4:35357/v2.0/',
    'tag':  'someinfo'
    },
    {
    ... another instance ...
    }
    ]
`someuser`: 是一个具有列出所有项目/租户和实例的权限的OpenStack用户

`tenant_name`: 用户将会认证的项目/租户

`version`:OpenStack API的版本，目前只支持API 2.x

`auth_url`: OpenStack API可用的地址

`tag`:这是一个标签，将添加到从OpenStack迁移的每个云项目和云主机

您可以通过在OPENSTACK_INSTANCES列表中添加另一个python dict来 添加多个OpenStack实例。

#### 如何执行
您可以通过执行：手动运行脚本，`ralph openstack_sync` 也可以将其添加到`corntab`中。

首先执行将所有的Cloud Project，Cloud Hosts和Cloud Flavors从OpenStack添加到Ralph。执行后，将添加和修改数据以及删除配置的OpenStack实例中不再存在的所有对象。


### 数据导入

可以通过各种格式导入数据（例如：csv，xml等）。它可以通过图形界面（GUI）和命令行（CLI）来实现。

#### CLI导入
导入数据的示例命令可能如下所示::

    $ ralph importer --skipid --type file ./path/to/DataCenterAsset.csv --model_name DataCenterAsset
或者是

    $ ralph importer --skipid --type zip ./path/to/exported-files.zip
要查看所有可用的导入选项，请使用：

    $ ralph importer --help
#### GUI导入
(TODO)

### 从Ralph 2迁移
我们的通用导入器/导出器允许您轻松地从Ralph 2导出和导入所有数据。

首先从Ralph 2导出所有的数据：

    $ (ralph) ralph export_model ralph2.zip
这将导出所有可用的模型到csv文件，并将它们存储在当前目录中的ralph2.zip文件中。

然后将此zip文件导入Ralph NG：

    $ (ralph-ng) ralph importer --skipid --type zip ralph2.zip
请注意，该`--skipid`选项非常重要 - 它将跳过现有的Ralph 2 ID并在Ralph NG中分配新的ID。

如果导入错误，请修复Ralph端的数据问题（例如，Ralph NG中需要的缺少字段值），清除NG数据库并重新导入。要清除数据库，可以运行以下命令：

    $ (ralph-ng) ralph flush && ralph migrate


## 快速开始
### Ralph快速启动

Ralph帮助您存储有关的信息：

数据中心资产：
- 仓库
- 数据中心机房
- 服务器
- 机架，包括图形布局
- 配线架

后勤资产：
- 打印机，笔记本电脑，台式机
- 手机
- 配件

非物质资产：
- 软件和硬件许可证
- 供应商合同和支持
- 包括成本和合同在内的域名


#### 介绍
在本教程中，我们将介绍：

- 向Ralph系统添加 new blade server
- taking a dc visualization tour （进行直流可视化巡视？）
- 为Microsoft Office 2015添加购买的许可证，并为其分配硬件。


##### 添加数据中心资产
我们添加一个新的Blade System，它将作为“负载平衡器”系统。我们希望在垂直视图下可视化，并为其分配一些支持和许可证。要做到这一点，去`Data Center -> Hardware -> Add data center asset`菜单。

![添加资产](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-add-asset.png)

添加新服务器只需要3个字段：

- `model`
- `barcode`（或`serial number` - 如果设备上没有barcode）
- `service environment`
但是首先我们需要设置它们。


##### 添加模型
`Model`字段可帮助您组织许多相同型号的设备。您可以输入`Model`字段，并从现有数据库模型开始输入以搜索模型。如果列表为空也无需担心。在没有表单的情况下添加模型也很容易。只需点击模型字段中的‘+按钮’即可。在新窗口中，只需命名此modle，例如：“PowerEdge R620”。从“three-like”菜单中选择category。不要忘记将type设置为“数据中心” -并 在数据中心模块中使用。您也可以添加office模型 - 只需切换`type`字段。

![Model视图](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-model.png)

##### 添加服务
`Service`字段组织了许多相同用途的设备在一起。可以举这样一个例子 - “内部负载平衡系统”，“客户端Joe的硬件”等。此字段是向系统添加新资产所必需的。

`Service Environment`是关于服务的下一级细节 - 我们称之为“environments”。示例：生产，测试，开发或简单的“prod，test，dev”。这是决定如何修补系统，部署系统，处理系统升级的非常重要的信息，因此我们在Ralph系统周围使用这些信息。

让我们添加“Load balancing - production（负载均衡 - 生产）”服务。为此，请单击`Service`字段旁边的小loop按钮，然后在下一个窗口中单击“Add Service Env”按钮。

- Remarks 是您对此服务的评论的generic placeholder（通用占位符）
- Service 添加到系统的服务列表
- Environment 给定服务的环境清单
- Tags(optional) 如果要更好地组织数据，您可以分配“标签”。有关更多信息，请参见“标签”一章。

跟你看到的一样，没有任何一个信息。我们必须添加一些信息。首先点击`+`按钮，添加Service（服务）。

输入数据如下：


- Name：“负载平衡”
- Active：当服务在整个系统中可见时检查

可选字段：

- UID：您可以为服务（例如公司的项目）分配外部ID或标签
- Profit Center -  如果所有服务均由一个组织（公司）提供，则可以为该项目从会计系统中添加profit center
- Business and Technical Owners  -  这是意味着负责特定服务，业务（功能，开发）和技术（sla，uptime）人员列表。例如，对于我们的 Load Balancing负载平衡项目来说，业务人员负赞助，技术人员负责服务的稳定性，往往是技术 team leader。
- Support team - 负责维护和运行的管理员团队


添加新服务后，请添加以下一些环境： `prod, test, dev`


![快速启动，附加服务](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-add-service.png)

就是这样。这是一次性的设置，所以你可以在整个系统中使用用户服务。

##### 特定位置
若要查看DC视图资产，我们需要指定位置，并添加一些物件如`Racks`和`Server Rooms`。然后，您可以在整个应用程序中自由使用它。


- rack - 点击`+`添加一个。命名为“Rack1”，然后在下一个窗口中添加名为“Room1”的服务器机房 - 这不是必需的，但很方便。
- orientation，`column number`，`row number` 用于垂直可视化，所以请保留它，我们稍后再回过来看。
- rack accesories - 您可以在给定的Rack上指定例如brushes, patch panels的位置，但现在不需要关注这个。

现在，让我们把注意力放在`Asset view`的`Position`字段。它是rack内的U-level position。

- `position`是rack内的U-level position。如果要安装电源，例如安装在背面的rack上，请选择0作为position。然后您可以选择“Orientation”作为详细信息。
- `slot` - DC中的某些类型的设备可以占据单个位置（U）。一个可能的例子是blade systems，可以将blade servers存储在同一个U位置。在这种情况下，我们使用`solts`字段在DC可视化中正确查看它们。您可以使用以前的“Model”添加表单设置slots数，使用“前/后的布局尺寸”字段的布局。


我们的情况是，leave slot未设置 ，而且 - 因为我们想把我们的blade systems放在`6-position-type 6`的`position`领域。

##### 把它包起来
最后一件事是填写条形码（例如：123456）并保存。

这样就好了。恭喜！

你的动作： 添加新的服务，使用它在任何位置设置新的DataCenter，并添加了Rack *安装的新的资产。

简单吧！现在去DataCenter - > Hardware to assets listing。然后到DC Vizualization看map上的Rack。

#### 数据中心可视化 Data Center visualization
##### 找到你的rack
在本教程中，您将学习如何管理DataCenter的graphical representation图形表示。

我们来到“Data Center visualization”菜单项，找到你的数据中心。你应该可以在map上看到一个新的rack。

![快速入门，dcview](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-dcview.png)

单击“Edit”功能并尝试

- 将rack拖到新位置
- 通过点击“rotate”按钮旋转
- 通过点击 pencil按钮重命名


提示：

您可以通过更改“Data center”网格列和行数来扩展数据中心布局。

##### 直接从dc视图添加新的rack
您可以从 dc visualization快速添加多个新rack。

要做到这一点，输入“Edit mode”，并使用“plus cursor加号光标”点击视图添加多个rack。您可以分别编辑它们，但要记住完成后点击“Save”按钮。

![快速启动-多机架](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-multiple-racks.png)

##### Accesing the DC inspector 访问DC Inspector
我们在教程开始时先搜索“Rack1”。单击直流机架视图进入机架详细信息视图。

（此处无法加载ytb视频）

显示Rack的后侧和前侧。

##### 访问编辑资产表单
如果您在Rack搭建了一些资产，请点击“Rack Inspector”中的“Edit asset”，返回资产视图。

在这里我们可以解释Asset'的其他不清晰的字段。

- `inventory number` - 在许多情况下，可能是您自己的内部ID，例如：从旧系统导入一些数据时。
- `task url` - 可以在您现有的工作流系统（例如jira）中使用，如果需要。
- `force deprecation` - 在某些例外情况下，您希望强制给某些资产作为弃用状态，即使它仍处于弃用期。
- `required support` - 检查您是否知道此资产将来需要供应商的支持。
- `parent` - 层次结构中的父对象，通常不需要。几个例子：

> - blade server的父代是blade system
- virtual machine的父代是hypervisor
- openstack vm的父代是openstack tenant


###### 技巧和窍门

如果不使用其中的某些功能，您可以在settings->permissions中设置并减少可见的字段数。 有关权限的信息，请参阅我们的高级指南。

#### 分配许可证 Assigning licenses
有两种使用许可证模块的方法。

- 转到许可证模块（Licenses - >Licenses）添加您购买的新许可证。
- 转到特定资产视图 - >Licenses。在这里，您可以访问分配给给定资产的许可证。


我们走第一条路线。假设我们已经购买了10位微软Office 2015用户许可证。

##### 创建新的许可证
点击添加许可证添加一个。你必须选择：


![快速启动，附加许可证](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-add-license.png)

- 许可证类型`license type`（每个用户，每个核心core等）
- 软件`software`（例如“Microsoft Office 2015”） - 点击`+`添加新的。在下一个窗口中，当你想使用这个许可证（`dc + back office`）时，所以选择`All`
- 库存编号`inventory number` - 是您的内部公司编号
- 区域`region`（例如：pl，en，de）允许您在不同的位置使用不同的数据。将其视为不同的国家/地区使用的单一软件。当您在不同位置使用Ralph时，只需创建一些“默认default”作为解决方法。
- `S / N`是您存储软件许可证密钥/序列号的字段。
- 购买的商品数量`Number of purchased items` - 设置许可证license数量很重要。当您有单个许可证密钥时，您不应该为批量购买的每个许可证添加另一个记录。你只需要在这里设置项目数量。


**如您所见，免费许可证的数量将自动显示在整个应用程序中。**

##### 分配许可证
您可以在硬件许可证`hardware license`的情况下使用“分配`Assignments`”选项卡进行分配，或在每个用户许可证案例中分配“分配给用户`Assigned to users`”。

如果您将软件标记为启用了后台`back office`和数据中心`data center`，则可以在此快速入门教程开始时添加资产 - 只需输入`123456`条形码 `barcode`，或使用“循环`Loop`”图标进行搜索。

如果您输入“10”许可证 `licenses`，您将使用所有可用的许可证（“0 free”）。

![快速入门指派许可](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-assign-license.png)

##### 许可证报告 Licenses reports
您可以通过使用我们的一个报告来分析许可证的详细信息使用情况。


![快速入门的许可证的报告](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-licences-reports.png)

#### 供应商支持 Vendor supports
支持模块`Supports module`类似于许可证（它由资产的标签“Supports”和主菜单（“Supports”）)中的单独模块组成，但该模块存储不同类型的数据。支持Supports是从供应商处购买的产品的一种服务，用作SLA，维护或升级服务。

许可证模块的显着差异：

- `Supports`只能添加到资产，而不是用户（很明显，对吗？;-)）
- `Supports`有额外的`Status`字段来区分过期的supports 与active。

![快速启动，支持](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-supports.png)

像往常一样，您可以随意添加附件（例如支持合同的pdf扫描）。

#### 盘点 Stock-taking
在业务领域，必须对公司拥有的资产的数量和条件进行验证。Ralph简化了这个繁琐的过程，为员工提供了工具，允许员工毫不费力地几乎没有时间地报告分配的项目的状态。

开始 stock-taking过程：

- 仓库管理面板 warehouse admin panel中的复选框（启用与给定仓库相关的所有资产的库存）
- 区域管理面板region admin panel 中的复选框（启用归属于分配给给定区域的用户的所有资产）

现在用户可以在`My equipment`中选择查看分配的项目信息： 

![快速入门 - 盘点](http://ralph-ng.readthedocs.io/en/latest/img/stock-taking.png)

一旦用户确认他们有特定的资产清单标签被添加到数据库中的资产记录，并记录在硬件历史记录中。标签可以使用设置文件和仓库管理员配置。Self-stock-taking过程与regular stock-taking没有冲突。完成后，您可以简单地取消勾选管理面板中的框。

----

就是这些了！恭喜，您已经完成了我们的快速入门！

您可能想要学习工作流（转换）教程和自己定制，PDF模板，权限定制等等 - 只需参考高级用户指南。

## 高级指南 Advanced guide
本指南处理更高级的主题，如定制和工作流系统。

### 工作流系统 Workflow system
[待记录]

### PDF输出 PDF outprints
[待记录]

### 权限 Permissions
[待记录]

### 用户资产视图 User assets view
[待记录]


## DCIM
### 介绍
TODO
Data Center Infrastructure Management
数据中心基础设施管理

### 配置路径 Configuration path
您可以选择指定配置路径`configuration path`为您的数据中心对象` Data Center objects`，如  `Data Center Asset`，`Virtual Server`或`Cloud Host`。此路径可以稍后用作配置管理工具的输入，如Puppet或Ansible。

首先，您应该定义（层次结构）配置模块（`http://<YOU_RALPH_URL>/assets/configurationmodule/`）。您可以将配置模块存储在树形（使用`parent`关系）中以对多个配置进行分组。树结构可用于反映存储配置文件的目录结构。

- 如果您使用Puppet，配置模块可以直接映射到[Puppet模块](https://docs.puppet.com/puppet/latest/reference/modules_fundamentals.html)。

- 如果您使用Ansible，请使用配置模块对多个配置进行分组。

然后可以添加配置类（`http://<YOUR_RALPH_URL>/assets/configurationclass/`）。此类将被用于标记host所持有的此配置。

- 在Puppet的情况下，它直接映射到Puppet class.。

- 对于Ansible，这可以映射到Playbook。

最后，您可以附加配置到你的主机 your host（`Data Center Asset`，`Virtual Server` 等）`configuration path`字段。这可以仅用于管理员信息，但您也可以使用它自动化您的配置管理工具！只需简单根据Ralph的API 从主机获取`configuration_path`，并将其应用于您的工具。

您可以使用自定义字段来设置传递给配置管理工具的一些变量。要在`REST API`中显示`configuration_variables`字段下的自定义字段，请选择`use as configuration variable`设置。有关更多信息，请参阅自定义字段部分。


## 部署 Deployment
### 介绍
TODO

### 预启动配置 Preboot configuration
`Preboot configuration`允许您在定义正在`Deployment`中执行的自定义文件 。如`kickstart`，`iPXE`或`preseed`。

要定义`preboot configuration` ，您需要：
- 访问`Preboot configuration`（`/ deployment / prebootconfiguration /`）页面
- 单击“添加预启动配置`Add preboot configuration`”
- 在新页面上有一个表单与几个字段，如：

```
- Name (This is the name, by which you could reference this `preboot
  configuration` in future)
- Type (one of these options: 'kickstart`, `iPXE`)
- Configuration
- Description
```

`Configuration`字段：此字段允许你写`kickstart`，`preseed`，`iPXE`或一些常规`script`配置。可以包含来自Ralph的变量。这些是：

```
- configuration_class_name (eg. 'www')
- configuration_module (eg. 'ralph')
- configuration_path (eg. 'ralph/www')
- dc (eg. 'data-center1')
- deployment_id (eg. 'ea9ea3a0-1c4d-42b7-a19b-922000abe9f7')
- domain (eg. 'dc1.mydc.net')
- done_url (eg. 'http://127.0.0.1:8000/deployment/ea9ea3a0-1c4d-42b7-a19b-922000abe9f7/mark_as_done')
- hostname (eg. 'ralph123.dc1.mydc.net')
- initrd (eg. 'http://127.0.0.1:8000/deployment/ea9ea3a0-1c4d-42b7-a19b-922000abe9f7/initrd')
- kernel (eg. 'http://127.0.0.1:8000/deployment/ea9ea3a0-1c4d-42b7-a19b-922000abe9f7/kernel')
- kickstart (eg. 'http://127.0.0.1:8000/deployment/ea9ea3a0-1c4d-42b7-a19b-922000abe9f7/kickstart')
- preseed (eg. 'http://127.0.0.1:8000/deployment/ea9ea3a0-1c4d-42b7-a19b-922000abe9f7/preseed')
- script (eg. 'http://127.0.0.1:8000/deployment/ea9ea3a0-1c4d-42b7-a19b-922000abe9f7/script')
- ralph_instance (eg. 'http://127.0.0.1:8000')
- service_env (eg. 'Backup systems - prod')
- service_uid (eg. 'sc-123')`
```

要使用特定变量，请将其包装在`{{ }}`大括号中，例如{{ domain }}。

以上所有链接（如：链接 `http://127.0.0.1:8000/deployment/ea9ea3a0-1c4d-42b7-a19b-922000abe9f7/mark_as_done` ）以
`http://127.0.0.1:8000`开头。因为默认设置`default settings`是

    RALPH_INSTANCE = 'http://127.0.0.1:8000'

您应该自定义`RALPH_INSTANCE`变量以适应您的设置。

#### 例：
这是`kickstart`使用上述变量（`hostname`）之一的文件示例

```
lang en_US
langsupport en_US
keyboard us

echo {{ hostname }}
```


## 域名联系 Domain Contracts
### 介绍
TLDR;   
这是一个域名`domain `所有权模块，而不是DNS管理工具。对于DNS记录集成查看[django-powerdns-dnssec](https://github.com/allegro/django-powerdns-dnssec)模块和PowerDNS服务器

`Domain Contracts `模块处理与域相关的优惠，目的和付款信息。它也可以用于Domain交易公司。这个模块与前面提到的`django-powerdns-dnssec`很相似。


### 快速开始 - 添加域 Quickstart - adding the domain
1. 单击  Domain -> Domains -> Add domain
2. 输入域名“allegrogroup.com”。
3. 不设置上级域名，因为它是顶级域名。
4. Service/env 描述了为此域创建的特定原因。创建名为“`Auction service`”的新服务，例如，环境称为“生产production”。对于内部域，我们可以使用“测试testing”环境。
5. 从列表中选择所需的域状态 domain Status - 例如，如果域被主动使用，则为“"Active”。
6. 当您想要将domains组合在一起时，业务部门 Business segment 就会帮助您，创建一个示例“Marketplaces市场”。
7. 选择负责域名和子域名管理的业主人员。
8. 选择负责域名技术维护的技术负责人。
9. Domain Holder是一家接收域名的公司，例如“Allegro Group”。
10. 现在您必须在给定期间填写域名价格。输入域名到期日，注册人姓名（例如：“CNC”，“售后”），最后是域名价格。
11. 您可以重复此过程以添加 适当的子域appropriate subdomains，例如添加名称为“test.allegrogroup.com”的新域new domain， parent设置为“allegrogroup.com”。


## 自定义字段 Custom fields
Ralph的定制字段有这些特征：

- 它可以附加到任何模型model
- 字段可能对值类型有限制（例如，必须是int，string，url，bool）
- 字段可能会限制可能的选择（如html的选择字段）


### 定义您自己的自定义字段
要定义自己的自定义字段 `custom fields`，请转到`http://<YOUR-RALPH-URL>/custom_fields/customfield/`或在菜单中选择它`Settings > Custom fields`。

可选项：

- `name` - 您的自定义字段的名称
- `attribute name` - 这是自定义字段的名称。它是使用API时其中的关键。
- `type` - 自定义字段类型。可能的选择是：
> - `string`
> - `integer`
> - `date`
> - `url`
> - `choice list`
- `choices` - 如果您选择了`choices`类型，请填写它。这是自定义字段的可能选择的列表。使用 `|`分开选项，例如 `abc|def|ghi`。
- `default value` - 如果您填写它，该值将被用作您的自定义字段的默认值，
- `use as configuration variable` - 设置时，此变量将在“`configuration_variables`”字段中的API中公开。您稍后可以在配置管理工具（如Puppet或Ansible）中使用。


**例：**

![自定义字段定义](http://ralph-ng.readthedocs.io/en/latest/img/custom-field-add.png)

### 将自定义字段附加到对象 Attaching custom fields to objects
您可以将自定义字段附加到任何对象类型（如果由开发人员为特定类型启用）。

Ralph的自定义字段与这里的任何其他字段几乎相同。第一个类型（部分）自定义字段的名称到该`Key`字段中。

![自定义字段，自动完成](http://ralph-ng.readthedocs.io/en/latest/img/custom-field-autocomplete.png)

然后在自动填充列表中选择您选择的自定义字段。请注意（对于某些类型）字段的值可能会更改其类型，例如选择列表。键入或选择所需的值并保存更改！


![自定义字段，选择价值](http://ralph-ng.readthedocs.io/en/latest/img/custom-field-select-value.png)

对于任何对象，每个自定义字段最多可以包含一个值（换句话说，您不能将相同的自定义字段多次附加到单个对象）。

### API
您可以通过Ralph API更改自定义字段，就像使用它的GUI一样简单！

### 阅读自定义字段
自定义字段以只读形式附加到任何API（适用）资源作为键值字典。

此字典中的关键字`attribute_name`定义在自定义字段中。如上所述，它是自定义字段的名称。

例：
```
{
    ...
    "custom_fields": {
        "monitoring": "zabbix",
        "docker_version": "1.11"  # this field doesn't have `use_as_configuration_variable` checked, so it won't be visible in `configuration_variables` field
    },
    "configuration_variables": {
        "monitoring": "zabbix"
    },
    ...
}
```
### 过滤 Filtering
您可以通过您选择的自定义字段的值轻松地过滤对象。预先计划`attribute_name`通过`customfield__`在对象名单，URL只选择匹配您所选择的自定义字段，例如：`http://<YOUR-RALPH-URL>/api/data-center-assets/?customfield__docker_version=1.10`。

### 更改自定义字段
要预览 REST-friendly way 中的 自定义字段，访问 `http://<YOUR-RALPH-URL>/api/<YOUR-RESOURCE-URL>/customfields/`，例如` http://<YOUR-RALPH-URL>/api/assetmodels/1234/customfields/`。在这里，您有自定义字段附加到此特定对象（在本例中为model id 1234）。

例：
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "custom_field": {
                "name": "docker version",
                "attribute_name": "docker_version",
                "type": "string",
                "default_value": "1.10"
            },
            "value": "1.11",
            "url": "http://<YOUR-RALPH-URL>/api/assetmodels/1234/customfields/1/"
        },
        {
            "id": 29,
            "custom_field": {
                "name": "monitoring",
                "attribute_name": "monitoring",
                "type": "choice list",
                "default_value": "zabbix"
            },
            "value": "zabbix",
            "url": "http://<YOUR-RALPH-URL>/api/assetmodels/1234/customfields/29/"
        }
    ]
}
```
您可以在此添加此对象的新自定义字段值（在自定义字段列表中设置POST请求）或更新任何现有自定义字段值（对所选自定义字段值进行PUT或PATCH请求，例如`http://<YOUR-RALPH-URL>/api/assetmodels/1234/customfields/29/）`。例如，您可以使POST以`http://<YOUR-RALPH-URL>/api/assetmodels/1234/customfields/`请求以下数据将新的自定义字段附加到 Asset Model with ID `1234`：

```
{
    "value": "http://ralph.allegrogroup.com/manual.pdf",
    "custom_field": "manual_url"
}
```
您可以使用自定义字段ID或属性名称将其指向API。

请注意，这里的每个动作都将发生在特定对象的上下文中 - 每个自定义字段都将附加到当前url（ex ` /assetmodels/1234`）指向的资源中。


## 仪表板 Dashboards
Dashboard 提供了通过条形图或饼图显示数据的基本机制。

## 与statsd集成 Integration with statsd
statsd - 单机搭建
每个图形都可以将数据推送到statsd。您必须添加`STATSD_GRAPHS_PREFIX`到您的 settings，并设置`ALLOW_PUSH_GRAPHS_DATA_TO_STATSD`和`COLLECT_METRICS`为True。接下来，检查`Push to statsd`具体图表，并使用Ralph的管理命令`push_graphs_to_statsd`将您的数据推送到statsd。

### 入门
本教程中的所有示例数据均由Ralph的命令生成`ralph make_demo_data`。

## 目标
在每个数据中心显示带有数量资产的图表。

## 第一个仪表板
首先，我们必须在Ralph中创建新的dasboard对象，方法是在菜单中`Dashboards > Dashboards`单击`Add new dashboard`以添加新的对象。

![添加仪表板](http://ralph-ng.readthedocs.io/en/latest/img/dashboard-create-dasboard.png)

下一步是创建图形并对其进行配置。 


![添加图表](http://ralph-ng.readthedocs.io/en/latest/img/dashboard-create-dasboard.png)

以上形式的重要字段是`Params`- 此字段接受JSON格式的图形配置。键`labels`，`series`，`filters`是必需的。以下这些字段的简短描述：

- `labels` - 模型中的哪个字段是字符串表示，
- `series` - 这个字段的聚合，合计
- `filters`- 根据条件过滤查询，类似于Django ORM的查询（有关更多信息，请访问Django文档），
- `excludes`- 排除结果中的项目 - 与`filters`相反，
- `aggregate_expression`- 默认情况下与`series`一致，您可以通过正确的聚合表达式（例如*或 path to field）覆盖此值，
- `target`-包含键：`model`，`filter`，`value`，此选项可更改可点击图的默认视图。

OK，保存我们的新的 dashboard object。现在我们可以在`Graphs`字段中看到`item`- `DC Capacity` 并选择它们。保存后，选择`Dashboards > Dashboards`在列表视图中单击`Link`。 

![链接到仪表板](http://ralph-ng.readthedocs.io/en/latest/img/dashboard-link.png)

最后结果：

![链接仪表板结果](http://ralph-ng.readthedocs.io/en/latest/img/dashboard-final-dc.png)

### 聚合选项 Aggregating options
#### 不同的值 distinct
`series`允许通过不同的值聚合。要使用它， 可以使用管道`|distinct`修饰器 扩展`series`查询
```
{
    "labels": "name",
    "series": "serverroom__rack|distinct",
    "filters": {
        "series__lt": 5
    },
}
```
#### 比例 Ratio
`series`允许计算两个聚合字段的比例。设置图表的`Aggregate type`图为`Ratio`，并为`series`使用两个值的列表：
```
{
    "labels": "service_env__service__name",
    "series": [
        "securityscan__is_patched",
        "id"
    ]
}
```
#### 按日期分组 Grouping by date
`series`允许基于部分日期的聚合，如year或  month：
```
{
    "labels": "service_env__service__name",
    "series": "created|year",
}
```

### 特殊的过滤器和字段 Special filters and fields
特殊过滤器是有时候会有帮助。

#### series
`series` 是包含所有注释值的特殊字段，可以像其他文件一样进行过滤：
```
{
    "labels": "name",
    "series": "serverroom__rack",
    "filters": {
        "series__lt": 5
    },
}
```
#### or, and
`or`，`and`扩展查询有关的额外条件，如：
```
{
    "labels": "name",
    "series": "serverroom__rack",
    "excludes": {
        "name__exact|or": [null, ''],
    },
}
```
过滤器接受元素的参数列表。

#### from_now
对于`filters`，`from_now`仅在日期和日期时间字段中使用，例如：
```
{
    "labels": "name",
    "series": "serverroom__rack__datacenterasset",
    "filters": {
        "created__gt|from_now": "-1y",
    },
}
```
上面的过滤器将限制查询一年内创建的对象。周期可能变化：

- `y` - 年，
- `m` - 月，
- `d` - 天，


## Ralph API consumption（消耗）
Ralph通过REST-wide WEB API公开了许多资源和操作，可用于查询数据库和使用数据填充数据。Ralph API使用 Django Rest框架，所以每个与之相关的主题都应该在Ralph API中工作。

### 认证 Authentication
每个用户都有自动生成的用于API认证的个人令牌。您可以通过访问您的个人资料页面或发送请求来获取您的令牌api-token-auth：

    curl -H "Content-Type: application/json" -X POST https://<YOUR-RALPH-URL>/api-token-auth/ -d '{"username": "<YOUR-USERNAME>", "password": "<YOUR-PASSWORD>"}'
    {"token":"79ee13720dbf474399dde532daad558aaeb131c3"}

如果您没有分配API令牌，请发送上面的请求 - 它会自动生成API令牌。

在API的每个请求中，您必须在请求标头中使用您的API令牌密钥：

    curl -X GET https://<YOUR-RALPH-URL>/api/ -H 'Authorization: Token <YOUR-TOKEN>'

### API版本控制 API Versioning
Api要求客户端在Accept标头中指定版本。

    Example:
    GET /bookings/ HTTP/1.1
    Host: example.com
    Accept: application/json; version=v1

### 输出格式 Output format
Ralph API支持JSON输出格式（默认情况下）和浏览器中的HTML预览（转到 `https：/// api /` 预览）。

### 可用资源 Available resources
`work in progress`

### HTTP methods
可以在API中使用以下方法。请参考具体模块的API参考，以获得更准确的解释。

方法	在集合	在单一资源上
得到	获取完整的资源列表	获取资源详情
POST	添加新资源	-
放	-	编辑资源（您需要提供所有数据）
补丁	-	编辑资源（您只需要提供更改的数据）
删除	-	删除资源

| Method        | On a collection           | On a single resource  |
| ------------- |:-------------:| -----:|
| GET     | 获取完整的资源列表 | 获取资源详情 |
|POST     | 添加新资源     |  - |
| PUT | --      |    编辑资源（您需要提供所有数据） |
| PATCH | --     |    编辑资源（您只需要提供更改的数据） |
| DELETE | --     |   删除资源 |


### 获取样本资源 Get sample resource
使用HTTP GET方法获取资源的详细信息。例：


    curl https://<YOUR-RALPH-URL>/api/data-center-assets/1/ | python -m json.tool

结果是：
```
{
    "id": 11105,
    "url": "http://127.0.0.1:8000/api/data-center-assets/1/",
    "hostname": "aws-proxy-1.my-dc",
    "status": "used",
    "sn": "12345",
    "barcode": "54321",
    "price": "55500.00",
    "remarks": "Used as proxy to AWS",
    "position": 12,
    "orientation": "front",
    "configuration_path": "/aws_proxy/prod",
    "service_env": {
        "id": 11,
        "url": "http://127.0.0.1:8000/api/service-environments/11/",
        "service": {
            "id": 1,
            "url": "http://127.0.0.1:8000/api/services/1/",
            "name": "AWS Proxy",
            ...
        },
        "environment": {
            "id": 2,
            "url": "http://127.0.0.1:8000/api/environments/2/",
            "name": "prod",
        }
    }
    },
    "model": {
        "id": 168,
        "url": "http://127.0.0.1:8000/api/asset-models/168/",
        "name": "R630",
        "type": "data_center",
        "power_consumption": 1234,
        "height_of_device": 1.0,
        "cores_count": 8,
        "has_parent": false,
        "manufacturer": {
            "id": 33,
            "url": "http://127.0.0.1:8000/api/manufacturers/33/",
            "name": "Dell",
            ...
        },
        ...
    },
    "rack": {
        "id": 15,
        "url": "http://127.0.0.1:8000/api/racks/15/",
        "name": "Rack 123",
        "server_room": {
            "id": 1,
            "url": "http://127.0.0.1:8000/api/server-rooms/1/",
            "name": "Room 1",
            "data_center": {
                "id": 99,
                "url": "http://127.0.0.1:8000/api/data-centers/99/",
                "name": "New York",
            }
        },
        ...
    },
    ...
}
```
为了可读性，响应的一部分被跳过。

### 您可以通过标签搜索记录：
    curl https://<YOUR-RALPH-URL>/api/data-center-assets/?tag=tag1&tag=tag2 | python -m json.tool

您将找到包含所有指定标签的所有记录。

### 保存样本资源
PATCH data center asset with data:
PATCH数据中心的资产与数据：
```
{
    "hostname": "aws-proxy-2.my-dc",
    "status": "damaged",
    "service_env": 12,
    "licences": [1, 2, 3]
}
```
请注意：在此示例中： 设置相关对象（not-simple，如字符串或数字）只传递其ID（请参阅service_env） 设置许多相关对象，将其传递到列表中（请参阅licences）*可以传递文本选择字段的值（状态），即使它存储为数字。

### 过滤 Filtering
Ralph API支持多个查询文件管理器：

您可以通过向发送`OPTIONS`请求特定资源（查看`filtering`项目）来检查可能的字段用以过滤。

- 过滤（精确）字段值（例如`<URL>?hostname=s1234.local`）
- 使用Django `__`用法查询过滤器（有关详细信息，请参阅Django Field文档），例如。`<URL>?hostname__startswith=s123`或者`<URL>?invoice_date__lte=2015-01-01`
- 扩展过滤器 - 允许使用单个查询参数对多个字段进行过滤 - 它对于多态模型（如`BaseObject`）来说是有用的- 例如通过`name`参数过滤，您将按`DataCenterAsset`主机名过滤`BackOfficeAssetHostname`等。示例：`<URL>/base-objects/?name=s1234.local`
- 使用`tag`查询参数过滤标签。可以在url查询中指定多个标签。例：`<URL>?tag=abc&tag=def&tag=123`


字段查找也使用扩展过滤器`BaseObject`，例如。<URL>/base-objects/?name__startswith=s123

### 转换API
所选模型的可用转换列表

    GET /api/data_center/datacenterasset/46/transitions/

结果是：
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "url": "<URL>/api/transitions/5/",
            "source": [
                "new",
                "in use",
                "free",
                "damaged",
                "liquidated",
                "to deploy"
            ],
            "target": "Keep orginal status",
            "name": "Change rack",
            "run_asynchronously": true,
            "async_service_name": "ASYNC_TRANSITIONS",
            "model": "<URL>/api/transitions-model/2/",
            "actions": [
                "<URL>/api/transitions-action/22/"
            ]
        },
...
```
运行转换的POST参数列表：
List of POST parameters to run transition for transition:

    OPTIONS <URL>/api/virtual/virtualserver/767/transitions/Initialization/

结果是：
```
{
  "name": "Transition",
  "description": "Transition API endpoint for selected model.\n\nExample:\n    OPTIONS: /api/<app_label>/<model>/<pk>/transitions/<transition_name>\n    or <transiton_id>",
  "renders": [
    "application/json",
    "text/html",
    "application/xml"
  ],
  "parses": [
    "application/json",
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "application/xml"
  ],
  "actions": {
    "POST": {
      "network_environment": {
        "type": "choice",
        "required": true,
        "read_only": false,
        "label": "Network environment",
        "choices": [
          {
            "display_name": "aa0003bb (testowa)",
            "value": "1"
          },
          {
            "display_name": "Other",
            "value": "__other__"
          }
        ]
      },
    ...
```

## ralph-cli

`ralph-cli`是一个开源工具（参见它的GitHub repo），意味着Ralph可以作为一种命令行接口。其目标是为所有Ralph的功能提供“Swiss Army knife瑞士军刀”，这种功能足以将其从网页GUI引入终端。

此时，您可以使用它来发现硬件的组件（使用  `scan` 命令），但我们将来会扩展功能（请参阅  Ideas for Future Development）。值得一提的是，  `ralph-cli`也有能力发现MAC地址，这是必要的，如果你想从Ralph部署你的主机（当然，你可以手动输入所有这些数据到Ralph，但ralph-cli大大方便这个过程）。

如果您想开始使用它，请参阅其文档 - 特别是快速入门部分，也可能是关键概念部分。

如果您发现任何问题`ralph-cli`（或者您有任何建议/想法），请在此处创建一个问题。如果你想贡献一些代码（在我们鼓励你做的事情中），你可能也想阅读 开发部分（BTW，`ralph-cli`写在Go中，但是使用Python作为scan scripts）。


## We are open :-)

Ralph是一个开源系统，它允许以简单直接的方式管理数据中心。我们不只是提供来源，我们所有的开发过程，包括规划，蓝图，甚至项目迭代都在公开环境完成！该项目背后的灵活和适应性强的架构鼓励开发人员尝试其需求和期望。如何成为开发过程的一部分？

### 简而言之
这是您如何修复错误或添加功能在几个快速步骤：

1. fork us on GitHub,
2. checkout your fork,
3. write a code (with PEP8 rules), test, commit,
4. push changes to your fork,
5. open a pull request.


## 成为贡献者
### Hello!
在我们的Gitter聊天https://gitter.im/allegro/ralph上介绍自己，当前与Ralph相关的问题和疑虑被提出，分享和解决。

### 开发环境
使您的软件兼容Ralph开发要求。

1. 装git和Vagrant应用。
2. `git clone https://github.com/allegro/ralph`.  "ng" 的github 分支是用的 Ralph 3.0, 这是目前正在开发最新版本. 对于2.x版本我们不会做更多的开发了。
3. 在“vagrant”目录中，您将找到设置开发环境的Vagrantfile。只需键入`vagrant up`即可启动完整的开发环境。
4. 现在登录虚拟框环境`vagrant ssh`。
5. 虚拟环境自动激活 - shell脚本位于`〜/ bin / activate`中。
6. 运行`make menu`。
7. 运行ralph实例`make run`，使用账号`ralph：ralph` 登录到`localhost：8000`。

然后，你们都设置好了。对于设置中有可能出现的所有问题，请参考`https://github.com/allegro/ralph/tree/ng/vagrant`

如果您想通过自己的Django应用程序扩展Ralph，请将您的配置放在  `vagrant/Vagrantfile.local`（例如同步的文件夹）中。您还可以在其中附加自定义供应脚本`vagrant/provision.local.s`h。

### 错误跟踪器和冲刺 Bug tracker & sprints
Github issues tracker 把握我们的开发。我们使用`milestones`用于我们的迭代（每一周或者两周），并有一些预计的发布日期。使用浏览器访问：用于 Scrum board的`https://waffle.io/allegro/ralph?label=ng`（使用milestone 字段进行过滤）以获取更多详细信息。

### Blueprints 蓝图
我们使用所谓的“蓝图”来讨论Github上的每个设计决策。这只是一些Github问题，有一些设计草案，图表和一般性讨论。您可以通过在问题列表上使用“蓝图”标签来识别蓝图。

### 技术文档
准备编码？请参考 我们的技术/架构文档

## Do's and don't's
### Do's
如果您想得到快速回复，请通知@ vi4m Gitter在“issue”部分中，在Github上开始您的item。我们的主页是讨论性质。随意探索Python编程的魅力。贡献/分享代码很重要。

### Don't's
"When is it ready?"的答案应该是"When it is ready"。
“什么时候准备好？”这个问题的答案应该是已经准备好了！

### Django's template standard
有几个简单的规则：

1. 在`load`和模板的其他部分之间 有一个空行。
2. 每一块/段代码之间应该 有一个空行。
3. 如果您打开一些HTML tag 或 Django template tag，那么您必须缩进行，不包括简单代码，自我关闭标签（查找 `inline block`和`{% url ... %}`示例）。
4. 而最后一个（最重要的）：当你写模板，有一些常用知识。

所有的这些规定都是为了可读性而不是为了浏览器的解析。

例：
```
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans 'Users' %}{% endblock %}

{% block sidebar %}
  {% if users %}
    <ul>
      {% for user in users %}
        <li>
            <a href="{% url admin:users user.pk %}">{{ user }}</a>
        </li>
      {% endif %}
    </ul>
  {% endif %}
{% endblock %}
```

## Finding your way around the sources ？
### 概念 Concept
整个应用程序是基于高度可操作的django模型。Django框架自己生成用户界面表单。由于简单性是我们的主要关注点，我们更倾向于保持models更加丰富和用户接口更加细致。这就是为什么我们依靠Django管理面板来管理用户界面。

### 主要模块
Ralph分为不同的模型，如：
- 资产 存储有关固定资产的大量信息
- 扫描 发现数据中心的设备
- 许可证 管理软件和硬件的许可证
- CMDB 配置管理数据库

注意：请帮助我们改进此文档！:-)


## Ralph Admin
Ralph Admin class（`ralph.admin.mixins.RalphAdmin`）建立在常规Django Admin之上，并具有一系列扩展功能。其中一些列在下面。

### 导入和导出 Import-Export
Ralph Admin内置了支持导入和导出对象的模块（使用django-import-export）。可能的配置如下：

#### 资源类 Resource class
在您的Admin中定义`resouce_class`，以指定`django-import-export`的资源类，用于处理该模型的导入和导出。

例：

    class SupportAdmin(RalphAdmin):
    ...
   	 resource_class = resources.SupportResource
    ...
#### 导出查询 Export queryset
在您的Admin中定义`_export_queryset_manager`属性，以指定将用于处理导出查询的管理器。这应该是字符串与模型的属性名称的适当管理器。

例：

    class SupportAdmin(RalphAdmin):
    ...
    	_export_queryset_manager = 'objects_with_related'
    ...
从Admin导出默认情况下，使用`get_queryset`从Django's admin正确处理所有过滤等。从Admin导出时，您的资源中定义的`get_queryset`不被使用，但将它们指向相同的对象管理器是一个很好的做法。

### 获取相关对象 Fetching related objects
默认情况下，Ralph Admin 选择并预取Resource's Meta中定义的所有相关对象。


## 自定义字段 Custom fields
### 如何将自定义字段附加到模型？
将`WithCustomFieldsMixin`类混合到你的model definition（从`ralph.lib.custom_fields.models`导入）

### 管理员集成 Admin integration
要在Django Admin中为您的模型使用自定义字段，请将`CustomFieldValueAdminMaxin`类混合到您的model admin（从ralph.lib.custom_fields.admin导入）

### Django Rest框架集成 
要在`Django Rest Framework`中使用自定义字段，`WithCustomFieldsSerializerMixin`请将类混合到您的API序列化程序（从`ralph.lib.custom_fields.api`导入）



## 转换 Transitions
对象从一个到另一个的转换（例如状态） - 这有助于产品生命周期管理。对于每个对象（asset, support, licence），您可以定义一些工作流（set of transitions），并为每个转换提供特殊的操作。

### 定义动作
您可以通过添加方法将新的操作添加到您的类中并进行装饰`@transition_action`。例如：
```
class Order(models.Model, metaclass=TransitionWorkflowBase):
    status = TransitionField(
        default=OrderStatus.new.id,
        choices=OrderStatus(),
    )

    @classmethod
    @transition_action
    def pack(cls, instances, request, **kwargs):
        notify_buyer('We pack your order for you.')

    @classmethod
    @transition_action
    def go_to_post_office(cls, instances, request, **kwargs):
        notify_buyer('We send your order to you.')
```
当您可以指定工作流程时，现在可以在管理面板中执行操作。
添加转换

#### 额外的参数 Extra parameters
如果您的操作需要额外的参数来执行，您可以添加字段：
```
from django import forms

ALLOW_COMMENT = True

    ...
    @classmethod
    @transition_action(
        form_fields = {
            'comment': {
                'field': forms.CharField(),
                'condition': lambda obj: (obj.status > 2) and ALLOW_COMMENT
            }
        }
    )
    def pack(cls, instances, request, **kwargs):
        notify_buyer(
            'We pack your order for you.',
            pickers_comment=kwargs['comment'],
        )

```
额外的参数

允许参数字段:: `field`-标准表单字段，例如从`django.forms`，  `condition`-功能至极接受一个参数，并返回boolean值，当条件都满足的字段将被显示。

如果转换只是一个动作要求，设置`only_one_action`为`True`。

如果操作返回附件（例如：PDF文档），设置`return_attachment`为`True`。

#### 在转换历史记录中存储其他数据
如果您想向转换历史记录添加其他信息，则需要在操作中添加到字典`history_kwargs`：
```
    def unassign_user(cls, instances, request, **kwargs):
        for instance in instances:
            kwargs['history_kwargs'][instance.pk][
                'affected_user'
            ] = str(instance.user)
            instance.user = None
```
#### 在操作之间共享数据
您还可以使用`shared_params`在连续操作之间共享额外的数据，就像`history_kwargs`一样

#### 重新操作 Rescheduling actions
异步转换（操作）能够稍后重新安排（例如，当等待某些条件满足时，而不是主动等待）。为此，只需在你的操作中抛出`ralph.lib.transitions.exceptions.RescheduleAsyncTransitionActionLater`异常。

当操作过会重置时， `history_kwargs`和`shared_params`都可以妥善进行处理（和恢复）。





## 扩展 Extending Ralph
Ralph NG很容易扩展，例如在Asset Review上下文中提供自定义选项卡。

注意：我们鼓励开发人员提供新功能和集成功能！请阅读本文档了解更多信息。

### 扩展细节视图 Extending the Detail View
为asset detail view提供自定义子页面是将另一个Django应用程序的内容集成到Ralph admin页面中的最方便的方法。所有注册视图将由ralph 网站上的标签表示。请注意，单视图类不能在多个管理站点中重复使用。

您必须编写自己的类视图和模板。添加额外的视图有两种可能：装饰器和类'属性。

### Your view
它必须是从`RalphListView`或`RalphDetailView`继承的正常视图（CBV ）（与视图的意图有关）。

#### RalphListView
这个类专门用于列表视图。

#### RalphDetailView
这个类专门用于细节视图。类的实例提供了其他属性：

- `model` - 实际模型类，
- `object`- 具体对象，来自`model`和`id`。
您可以从template 访问object。

#### RalphDetailViewAdmin
如果要显示标准 admin model 为标签，请使用此类。类接受来自`django.contrib.admin.ModelAdmin`的两个基本属性：

- `inlines`，
- `fieldsets`。


例：
```
class NetworkInline(TabularInline):
    model = IPAddress


class NetworkView(RalphDetailViewAdmin):
    icon = 'chain'
    name = 'network'
    label = 'Network'
    url_name = 'network'

    inlines = [NetworkInline]
```

#### 模板 Template
每个模板必须继承自`BASE_TEMPLATE`。

基本模板：
```
{% extends BASE_TEMPLATE %}

{% block content %}
    {{ var }}
{% endblock %}
```
您的模板必须放在预定义的路径之一中：

- `model/name.html`
- `app_label/model/name.html`

Where：

`app_label`- `app_label`提取自`model`，
`model`- 小写名称`model`，
`name` - 视图的名称来自视图的实例。


#### 通过类属性注册视图
注意：如果您直接在Ralph进行开发，请使用此方法。

在`admin.py`中：
```
from ralph.admin import RalphAdmin, register
from ralph.admin.views import RalphDetailView
from ralph.back_office.models import Warehouse


class ExtraView(RalphDetailView):
    name = 'extra_list'
    label = 'Extra Detail View'


@register(Warehouse)
class WarehouseAdmin(RalphAdmin):
    change_views = [ExtraView]
```

#### 通过装饰器注册视图
注意：此方法推荐用于外部应用。

你的应用程序的某个地方：
```
from ralph.admin.decorators import register_extra_view
from ralph.admin.views import RalphDetailView
from ralph.back_office.models import Warehouse


@register_extra_view(Warehouse, register_extra_view.CHANGE)
class ExtraView(RalphDetailView):
    name = 'extra_details'
    label = 'Extra Detail View'
```

### 使用高级搜索过滤器 Using advanced search filters
您可以轻松地定义自己的高级搜索过滤器（通过文本，日期等进行搜索）。可用的过滤器有：

- BooleanFilter（`ralph.admin.filters.BooleanFilter`）
- ChoicesFilter（`ralph.admin.filters.ChoicesFilter`）
- DateFilter（`ralph.admin.filters.DateFilter`）
- TextFilter（`ralph.admin.filters.TextFilter`）


要使用过滤器定义你的class，您可以在其中指定字段的标题和参数，以对结果进行过滤:
```
class BarcodeFilter(TextFilter):
    title = _('Barcode')
    parameter_name = 'barcode'
```
然后在你的admin class定义中简单地将此类添加到`list_filter`属性中：
```
class MyAdmin(RalphAdmin):
    list_filter = [BarcodeFilter]
```
要使用`ChoicesFilter`，您需要指定一个附加的参数：`choices_list`。`choices_list`是可供选择的列表（此处推荐使用`dj.choices.Choices`实例）。

#### 附加过滤器选项： Additional filters options:
##### 过滤标题 Filter title
```
class ServerRoom(models.Model):
    data_center = models.ForeignKey(DataCenter, verbose_name=_("data center"))
    data_center._filter_title = _('data center')
```
如果`_filter_title`被附加到字段，过滤器将在列表中显示被输入的名称，而不是从模型的字段获取。

##### 自动完成 Autocomplete
```
class ServerRoom(models.Model):
    data_center = models.ForeignKey(DataCenter, verbose_name=_("data center"))
    data_center._autocomplete = False
```
对于每个字段ForeignKey，默认情况下使用 autocomplete widget（组件）。如果你希望这是可选字段，可以将`_autocomplete`设置为False。




## Deb packaging HOWTO 怎样安装Deb包
我们使用`dh_virtualenv`可以方便的从虚拟环境安装所有的依赖包。然后，我们将deb二进制文件上传到bintray.com，以方便管理。

#### 发布新的deb快照 Issuing the new deb snapshot
Vagrant内：

1. 确保您有`export BINTRAY_APIKEY=APIKEYHERE` - 二进制上传的 bintray api key set （密钥集）。
2. `make package`构建包`./packaging/build` ，然后将其`./packaging/upload`上传到bintray。
3. 内部名称将会是“ralph-3.0.0-＃BUILDNUMBER”


注1：在内部我们运行dch debian工具来帮助我们生成代码，并生成`debian/changelog. file`。发布新的“major”版本后，需要在`debian/changelog`文件中使用dch实用程序来手动预设新版本。记得在发布新的文件后提交这个文件！

注2：未来我们可能会以某种方式将其完全自动化;-)

#### 来源
- `/packaging` 包含构建和上传到bintray.com服务器的构建脚本
- `/debian` 需要为一些源代码指定位置。
- `debian/rules`和`debian/control`具有一些构建配置
- `debian/changelog` - 跟踪构建代号




## 常问问题 FAQ
### 附加额外的视图到admin class后， 报错`ImproperlyConfigured`
单个额外的视图类不能重复使用在多个管理站点。要在多个管理站点中使用它，请创建分开的类别的额外视图：
```
class MyView(RalphDetailViewAdmin):
    icon = 'chain'
    ...

class MyView2(MyView):
    pass
```
然后在你的admin中使用它：
```
@register(MyModel)
class MyAdmin(RalphAdmin):
    change_views = [MyView]

@register(MyModel2)
class MyAdmin2(RalphAdmin):
    change_views = [MyView2]
```
Attachments app是此机制的示例用法 - 对于每个使用`AttachmentsMixin`的admin site，都创建了不同的AttachmentsView类。