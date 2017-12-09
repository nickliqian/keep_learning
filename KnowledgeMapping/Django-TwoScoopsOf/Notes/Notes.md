from future import absolute_import
使用上述导入可以实现显示导入绝对路径的模块

from core.views import FoodMixin
absolute import 绝对导入
Use when importing from outside the current app
从当前应用程序外部导入时使用


from .models import WaffleCone
explicit relative 显式相对导入
Use when importing from another module in the current app
从当前应用中的另一个模块导入时使用

from models import WaffleCone
implicit relative 隐式相对导入
Often used when importing from another module in the current app, but not a good idea
在从当前应用中的另一个模块导入时经常使用，但不太好

Vagrant和VirtualBox是建立相同开发环境的最常用的方法。
or Docker

pip install -e
Usage:
  pip install [options] <requirement specifier> [package-index-options] ...
  pip install [options] -r <requirements file> [package-index-options] ...
  pip install [options] [-e] <vcs project url> ...
  pip install [options] [-e] <local project path> ...
  pip install [options] <archive url/path> ...


<repository_root>/
    <django_project_root>/
        <configuration_root>/

如果您在确定您在virtualenv中使用哪个版本的依赖关系时遇到困难，请在命令行中键入以下命令列出您的依赖关系：
$ pip freeze --local


django项目构建工具
cookiecutter-django
django-kevin
and django-twoscoops-
project

保持app的精简，便于维护。而不是一个大型复杂的app。

behaviors.py : An option for locating model mixins per subsection 6.5.1.
constants.py : A good name for placement of app-level settings. If there are enough of them involved in an app, breaking them out into their own module can add clarity to a project.
decorators.py Where we like to locate our decorators. For more information on decorators, see section 9.3.
db/ Used in many projects for any custom model elds or components.
fields.py is commonly used for form elds, but is sometimes used for model elds when there isn’t enough eld code to justify creating a db/ package.
factories.py Where we like to place our test data factories. Described in brief in subsection 22.3.5
helpers.py What we call helper functions. ese are where we put code extracted from views (subsection 16.3.3) and models (section 6.5) to make them lighter. Synonymous with utils.py managers.py When models.py grows too large, a common remedy is to move any custom model managers to this module.
signals.py While we argue against providing custom signals (see chapter 28), this can be a useful place to put them.
utils.py Synonymous with helpers.py viewmixins.py View modules and packages can be thinned by moving any view mixins to this module. See section 10.2.


对于settinfs有一些实践经验：
所有的setting改变都需要进行版本控制。特别是在生产环境中，其中的日期，时间和设置变更的注释务必可以追踪。
不要重复设置。 你应该从基本设置文件继承这些设置，而不是从一个文件夹迁移/复制到另一个文件夹。
保密钥匙的安全，应该避免版本控制，例如秘钥信息最好从环境变量获取或者不上传git。


SECRET KEY setting
https://docs.djangoproject.com/en/1.8/topics/signing/
