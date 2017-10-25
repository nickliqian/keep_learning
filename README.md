# ralph_doc_to_chinese
ralph_doc_to_chinese

#Ralph NG
Ralph NG是一个简单而强大的 资产管理，DCIM和CMDB数据中心和后台系统。

特征：
- 跟踪资产购买及其生命周期
- 自动发现现有硬件
- 生成灵活而准确的成本报告

免责声明：Ralph NG是Ralph 2.x的精简和简化版本。 本文档不包括可在此处访问的旧版本。

##安装指南

对于生产，我们提供deb程序和docker（组合）镜像。我们只支持AMD64平台上的Ubuntu 14.04 Trusty发行版。

另一方面，如果您是开发人员，我们强烈建议使用我们的`Vagrant`，`vagrant`目录包含了许多我们开发的附属项目。

###Debian / Ubuntu包 - 推荐
确保您的安装是纯净版的Ubuntu 14.04，没有安装任何其他软件包，并`apt-transport-https`安装。

    sudo apt-get update && sudo apt-get install apt-transport-https
现在，添加我们的官方ralph存储库：

    sudo apt-key adv --keyserver  hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61
    sudo sh -c "echo 'deb https://dl.bintray.com/vi4m/ralph wheezy main' >  /etc/apt/sources.list.d/vi4m_ralph.list"
然后，只需安装ralph的传统方式：

    sudo apt-get update
    sudo apt-get install ralph-core redis-server mysql-server
注意：主要的Ralph实例需要安装redis和mysql服务器。如果您只想在某个地方安装ralph代理，只需安装`ralph-core`并将其指向网络上某处的特定mysql和redis实例即可。

####配置
创建数据库。

    > mysql -u root
    > CREATE database ralph default character set 'utf8';

####设置
我们正在制定一些全面的配置管理文件。目前，我们只是读取一些环境变量，所以只需要粘贴到`〜/ .profile`中的某个地方，就可以根据需要自定义它们。

    cat〜/ .profile

    export DATABASE_NAME=ralph
    export DATABASE_USER=someuser
    export DATABASE_PASSWORD=somepassword
    export DATABASE_HOST=127.0.0.1
    export PATH=/opt/ralph/ralph-core/bin/:$PATH
    export RALPH_DEBUG=1
####初始化
1. 键入`ralph migrate`以在数据库中创建表。
2. 键入`ralph sitetree_resync_apps`重新加载菜单。
3. 键入`ralph createsuperuser`以添加新用户。

运行你的ralph实例 `ralph runserver 0.0.0.0:8000`

现在，将您的浏览器指向`http:// localhost:8000`并登录。Happy Ralphing!

###Docker安装（试验版）
您可以在https://github.com/allegro/ralph/tree/ng/contrib目录中找到试验版的docker-compose配置。请注意，它仍然是测试版。

####安装
首先安装`docker`和`docker-compose`。

####创建撰写配置
将`docker-compose.yml.tmpl`外部ralph源复制到docker-compose.yml并进行调整。

####构建
然后构建ralph：

    docker-compose build
初始化数据库运行：

    docker-compose run --rm web /root/init.sh
请注意，这个命令最初只能执行一次。

如果您需要使用一些演示数据来填充Ralph：

    docker-compose run --rm web ralph demodata
####运行
最后运行拉尔夫：

    docker-compose up -d
Ralph应该可以通过`http://127.0.0.1`进行访问（或者如果您正在使用`boot2docker`的`$(boot2docker ip)`）。可用的文档在`http://127.0.0.1/docs`。

如果你升级ralph镜像（源代码）运行：

    docker-compose run --rm web /root/upgrade.sh
###从Ralph 2迁移
如果您以前使用过Ralph 2，并希望保存所有数据，请参阅Ralph 2指南的迁移


###LDAP认证

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
您将需要配置LDAP连接以及将远程用户和组映射到本地连接。有关详细信息，请参阅官方django-auth-ldap文档http://packages.python.org/django-auth-ldap。例如，连接到Active Directory服务可能如下所示：

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

###与OpenStack同步
Ralph 3支持与OpenStack的单向同步。可以从OpenStack下载数据，包括项目和实例。所有同步数据将以只读模式在Ralph中可用。只能更改服务环境，标签和备注字段。

注意：一个CloudHost 的服务环境是从一个Cloud Project继承而来的 。

####安装
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

####如何执行
您可以通过执行：手动运行脚本，`ralph openstack_sync` 也可以将其添加到`corntab`中。

首先执行将所有的Cloud Project，Cloud Hosts和Cloud Flavors从OpenStack添加到Ralph。执行后，将添加和修改数据以及删除配置的OpenStack实例中不再存在的所有对象。


###数据导入

可以通过各种格式导入数据（例如：csv，xml等）。它可以通过图形界面（GUI）和命令行（CLI）来实现。

####CLI导入
导入数据的示例命令可能如下所示::

    $ ralph importer --skipid --type file ./path/to/DataCenterAsset.csv --model_name DataCenterAsset
或者是

    $ ralph importer --skipid --type zip ./path/to/exported-files.zip
要查看所有可用的导入选项，请使用：

    $ ralph importer --help
####GUI导入
(TODO)

###从Ralph 2迁移
我们的通用导入器/导出器允许您轻松地从Ralph 2导出和导入所有数据。

首先从Ralph 2导出所有的数据：

    $ (ralph) ralph export_model ralph2.zip
这将导出所有可用的模型到csv文件，并将它们存储在当前目录中的ralph2.zip文件中。

然后将此zip文件导入Ralph NG：

    $ (ralph-ng) ralph importer --skipid --type zip ralph2.zip
请注意，该`--skipid`选项非常重要 - 它将跳过现有的Ralph 2 ID并在Ralph NG中分配新的ID。

如果导入错误，请修复Ralph端的数据问题（例如，Ralph NG中需要的缺少字段值），清除NG数据库并重新导入。要清除数据库，可以运行以下命令：

    $ (ralph-ng) ralph flush && ralph migrate


##快速开始
###Ralph快速启动

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


####介绍
在本教程中，我们将介绍：

- 向Ralph系统添加 new blade server
- taking a dc visualization tour （进行直流可视化巡视？）
- 为Microsoft Office 2015添加购买的许可证，并为其分配硬件。


#####添加数据中心资产
我们添加一个新的Blade System，它将作为“负载平衡器”系统。我们希望在垂直视图下可视化，并为其分配一些支持和许可证。要做到这一点，去`Data Center -> Hardware -> Add data center asset`菜单。

![](http://ralph-ng.readthedocs.io/en/latest/img/quickstart-add-asset.png)

添加新服务器只需要3个字段：

- `model`
- `barcode`（或`serial number` - 如果设备上没有barcode）
- `service environment`
但是首先我们需要设置它们。

#------矫正位置记录------

#####添加模型
`Model`字段可帮助您组织许多相同型号的设备。您可以输入“Model”字段，并从现有数据库模型开始输入以搜索模型。但不要担心，如果列表为空。添加模型很容易，不用离开表单。只需点击+模型字段中的按钮即可。在新窗口中，只需命名此模型，例如：“PowerEdge R620”。从“三喜”菜单中选择类别。不要忘记将型号设置为“数据中心” - 在数据中心模块中使用。您也可以添加办公室模型 - 只需切换type字段。

快速启动模型

#####添加服务
Service现场组合了许多相同目的的设备。一个例子可能是 - “内部负载平衡系统”，“客户端Joe的硬件”等。此字段是向系统添加新资产所必需的。

Service Environment是关于服务的下一级细节 - 我们称之为“环境”。示例：生产，测试，开发或简单的“prod，test，dev”。这是决定如何修补系统，部署它，处理升级的非常重要的信息，因此我们在Ralph系统周围使用这些信息。

我们添加“负载均衡 - 生产”服务。为此，请单击Service字段旁边的小循环按钮，然后在下一个窗口中单击“添加服务环境”按钮。

备注是您对此服务的评论的通用占位符
服务 - 添加到系统的服务列表
环境 - 给定服务的环境清单
标签（可选） - 如果要更好地组织数据，您可以分配“标签”。有关更多信息，请参见“标签”一章。
你可以看到，没有一个。我们必须添加一些信息。首先点击+按钮，添加服务。

输入数据如下：

名称：“负载平衡”
活动：当服务在整个系统中可见时检查
可选字段：

UID：您可以为服务（例如公司的项目）分配外部ID或标签
利润中心 - 如果所有服务均由一个组织（公司）提供服务，则可以为该项目从会计系统添加利润中心
业务和技术所有者 - 这是负责服务，业务（功能，开发）和技术（sla，正常运行时间）意义的人员列表。例如，对于我们的负载平衡（业务负责人）来说，它是赞助商，技术负责人负责服务的稳定性，往往是技术团队负责人。
支持团队 - 负责维护和运行的管理员团队
添加新服务后，请添加以下一些环境： prod, test, dev

快速启动，附加服务

就是这样 这是一次性设置，因此您可以在系统周围使用用户服务。

#####指定位置
若要查看DC视图资产，我们需要指定位置，并添加一些物件如Racks和Server Rooms。然后，您可以在整个应用程序中自由使用它。

机架 - 点击+添加一个。命名为“Rack1”，然后在下一个窗口中添加名为“Room1”的服务器机房 - 这不是必需的，但方便。
方向，column number并row number 用于直流可视化，所以请留下它，我们稍后会回来。
机架配件 - 您可以指定位置，例如刷子，配线架，在给定的机架上，现在，只要离开它。
现在，让我们把你的注意力放在Position现场Asset view。它是机架内的U级位置。

position是机架内的U级位置。如果要安装电源，例如安装在背面的机架上，请选择0作为位置。然后，您可以选择“方向”了解更多详细信息。
slot - DC中的某些类型的设备可以占据单个位置（U）。一个例子可能是刀片系统，可以将刀片服务器存储在同一U位置。在这种情况下，我们使用“插槽”字段在DC可视化中正确查看它们。您可以使用以前使用的“模型”添加表单设置插槽数，使用“前/后大小”字段的布局。
在我们的情况下，离开slot，而且 - 因为我们想把我们的刀片系统放在6型6型的position领域。

#####把它包起来
最后一件事是填写条形码（例如：123456）并保存。

而已。恭喜！

你有： 添加新的服务，使用它到处 设置新的数据中心，并添加了Rack *安装的新资产

那很简单！现在去DataCenter - >硬件到资产列表。之后，请去DC Vizualization在地图上看到机架。

####数据中心可视化
#####找到你的机架
在本教程中，您将学习如何管理数据中心的图形表示。

我们来到“数据中心可视化”菜单项，找到你的数据中心。你应该看到一个新的架子在地图上可见。

快速入门，dcview

单击“编辑”功能并尝试

将机架拖到新位置
通过点击“旋转”按钮旋转它
通过点击铅笔按钮重命名它
提示：

您可以通过更改“数据中心”网格列和行数来扩展数据中心布局。

#####直接从直流视图添加新机架
您可以从直流可视化快速添加多个新机架。

要做到这一点，输入“编辑模式”，并使用“加号光标”点击视图添加多个机架。您可以分开编辑它们，但请记住，完成后点击“保存”按钮。

#####快速启动-多机架

加入DC检查员
我们在教程开始时搜索“Rack1”。单击直流机架视图进入机架详细信息视图。


显示机架的后侧和前侧。

#####访问编辑资产表单
如果您在美丽的机架上播放了一些，请点击“机架检查器”中的“编辑资源”，返回资产视图。

在这里我们可以解释资产的其他不明显的领域。

inventory number - 在许多情况下，可能是您自己的内部ID，例如：从旧系统导入一些数据时。
task url - 可以在您现有的工作流系统（如jira）中使用，如果您使用它。
force deprecation - 在某些例外情况下，您希望强制给定的资产被弃用，即使它仍处于弃用期。
required support - 检查您是否知道此资产将来需要供应商的支持。
parent - 层次结构中的父对象，通常不需要。几个例子：
刀片服务器的父代是刀片系统
虚拟机的父代是管理程序
openstack vm的父母是openstack的租户
######技巧和窍门

如果不使用其中的一些，您可以减少settings->权限中可见的字段数。 有关权限的信息，请参阅我们的高级指南

####分配许可证
有两种使用许可证模块的方法。

转到许可证模块（许可证 - >许可证）添加您购买的新许可证。
转到特定资产视图 - >许可证。在这里，您可以访问分配给给定资产的许可证。
我们走第一条路线。假设我们已经为微软Office 2015购买了10位用户许可证。

#####创建新的许可证
点击添加许可证添加一个。你必须选择：

快速启动，附加许可证

许可证类型（每个用户，每个核心等）
软件（例如“Microsoft Office 2015”） - 点击+添加新的。在下一个窗口中，当你想使用这个许可证（dc + back office）时，所以选择“全部”
库存编号是您的内部公司编号
区域（例如：pl，en，de）允许在单独的位置使用单独的数据。将其视为单独的国家/地区使用的单一软件。当您在单个位置使用Ralph时，只需创建一些“默认”作为解决方法。
S / N是您存储软件许可证密钥/序列号的字段。
购买的商品数量 - 设置许可证数量很重要。当您有单个许可证密钥时，您不应该为批量购买的每个许可证添加另一个记录。你只需要在这里设置项目数量。
如您所见，免费许可证的数量将自动显示在整个应用程序中。

#####分配许可证
您可以在硬件许可证的情况下使用“分配”选项卡进行分配，或在每个用户许可证案例中分配“分配给用户”。

如果您将软件标记为启用了后台和数据中心，则可以在此快速入门教程开始时添加资产 - 只需输入123456条形码，或使用“循环”图标进行搜索。

如果您输入“10”许可证，您将使用所有可用的许可证（“0免费”）。

快速入门指派许可

#####许可证报告
您可以通过使用我们的一个报告来分析许可证的详细信息使用情况。

快速入门的许可证的报告

####供应商支持
支持模块类似于许可证（它由资产的标签“支持”和主菜单（“支持”）中的单独模块组成，但该模块存储不同类型的数据。支持是从供应商处购买的产品的一种服务，用作SLA，维护或升级服务。

许可证模块的显着差异：

支持只能添加到资产，而不是用户（很明显，对吗？;-)）
支持有额外的“状态”字段来区分过期的支持与活动。
快速启动，支持

像往常一样，您可以随意添加附件（例如支持合同的pdf扫描）。

####盘点
在业务领域，必须对公司拥有的资产的数量和条件进行验证。拉尔夫简化了这个繁琐的过程，为员工提供了工具，允许员工毫不费力地几乎没有时间地报告分配的项目的状态。

开始拍卖过程：

仓库管理面板中的复选框（启用与给定仓库相关的所有资产的库存）
区域管理面板中的复选框（启用归属于分配给给定区域的用户的所有资产）
现在用户可以选择查看分配的项目信息My equipment： 快速入门 - 盘点

一旦用户确认他们有特定的资产清单标签被添加到数据库中的资产记录，并记录在硬件历史记录中。标签可以使用设置文件和仓库管理员配置。自我拍卖过程与常规采购没有冲突。完成后，您可以简单地取消勾选管理面板中的框。

----

所以，这是它！恭喜，您已经完成了我们的快速入门！

您可能想要学习工作流（转换）教程和自定义，PDF模板，权限定制等等 - 只需按照高级用户指南

