class AuthorAdmin(admin.ModelAdmin) 可选如下字段
	

#### 控制actions bar 出现在页面的位置。默认在页面顶部.  

    actions_on_top = True;actions_on_bottom=False


#### date_hierarchy 设置为在你的model 中的DateField或DateTimeField的字段名，然后更改列表将包含一个依据这个字段基于日期的下拉导航。

    date_hierarchy = 'pub_date'



#### 填充表单只包含在内的字段，顺序显示，不同行

    fields = ('name', 'title')

#### ('url', 'title') 元组内的会在一行

    fields = (('url', 'title'), 'content')

#### 填充表单不包含在内的字段，其余的全部有

    exclude = ('birth_date',)

*如果fields和fieldsets 选项都不存在, Django将会默认显示每一个不是 AutoField 并且 editable=True的字段, 在单一的字段集，和在模块中定义的字段有相同的顺序

#### 分组显示
```
fieldsets = (
    ('Hello', {
        'fields': ('location', 'base',)
    }),

    ('World', {
	'classes': ('collapse',),
        'fields': ('disk',)
    }),
)
```

field_options 字典有以下关键字:
fields 字段名元组将显示在该fieldset. 此键必选.
fields 能够包含定义在readonly_fields 中显示的值作为只读.
classes 显示或者隐藏这一个表单组
```
{
'classes': ('wide', 'extrapretty'),
}
```
Fieldsets 使用 wide 样式将会有额外的水平空格.
description 在每一个fieldset的顶部显示额外文本。可以富文本。

#### filter_horizontal
filter_horizontal = ' ManyToManyField'
选和不选选项框并排出现


#### filter_vertical
filter_vertical = 'ManyToManyField'
使用过滤器界面的垂直显示，其中出现在所选选项框上方的未选定选项框。


#### form = MyArticleAdminForm
```
class MyArticleAdminForm(forms.ModelForm):
    def clean_name(self):
        # do something that validates your data
        return self.cleaned_data["name"]
class ArticleAdmin(admin.ModelAdmin):
    form = MyArticleAdminForm
```
在管理员中添加数据的自定义验证

```
from django import forms
from django.contrib import admin
from myapp.models import Person

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ['name']

class PersonAdmin(admin.ModelAdmin):
    exclude = ['age']
    form = PersonForm
# 在上例中， “age” 字段将被排除而 “name” 字段将被包含在最终产生的表单中。
```

#### formfield_overrides
这个属性通过一种临时的方案来覆盖现有的模型中Field （字段）类型在admin site中的显示类型。
```
from django.db import models
from django.contrib import admin

# Import our custom widget and our model from where they're defined
from myapp.widgets import RichTextEditorWidget
from myapp.models import MyModel

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RichTextEditorWidget},
    }
```


#### list_display
使用list_display 去控制哪些字段会显示在Admin 的修改列表页面中。
list_display = ('first_name', 'last_name')
在list_display中，你有4种赋值方式可以使用：
```
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
```
```
def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = 'Name'

class PersonAdmin(admin.ModelAdmin):
    list_display = (upper_case_name,)
```
```
class PersonAdmin(admin.ModelAdmin):
    list_display = ('upper_case_name',)

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()
    upper_case_name.short_description = 'Name'
```

```
from django.db import models
from django.contrib import admin

class Person(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()

    def decade_born_in(self):
        return self.birthday.strftime('%Y')[:3] + "0's"
    decade_born_in.short_description = 'Birth decade'

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'decade_born_in')
```
如果你不希望转义方法的输出，可以给方法一个allow_tags 属性，其值为True。
    colored_name.allow_tags = True

排序
    colored_first_name.admin_order_field = 'first_name'

#### list_display_links
使用list_display_links可以控制list_display中的字段是否应该链接到对象的“更改”页面。
list_display_links = ('first_name', 'last_name')
将其设置为None，根本不会获得任何链接。


#### list_editable
list_editable = ('first_name', 'last_name')
将list_editable设置为模型上的字段名称列表，这将允许在更改列表页面上进行编辑。
允许用户一次编辑和保存多行。
同一字段不能在list_editable和list_display_links中列出。


#### list_filter
list_filter = ('is_staff', 'company')

字段名称，其指定的字段应该是BooleanField、CharField、DateField、DateTimeField、IntegerField、ForeignKey 或ManyToManyField，例如︰
```
class PersonAdmin(admin.ModelAdmin):
    list_filter = ('is_staff', 'company')
```
list_filter 中的字段名称也可以使用__ 查找跨关联关系，例如︰
```
class PersonAdmin(admin.UserAdmin):
    list_filter = ('company__name',)
```


#### list_max_show_all
list_max_show_all = 200
list_max_show_all以控制在“显示所有”管理更改列表页面上可以显示的项目数。只有当总结果计数小于或等于此设置时，管理员才会在更改列表上显示“显示全部”链接。


#### list_per_page
list_per_page = 100
list_per_page 设置控制Admin 修改列表页面每页中显示多少项。默认设置为100。



#### list_select_related
list_select_related = 布尔值，列表或元组。默认值为False
设置list_select_related以告诉Django在检索管理更改列表页面上的对象列表时使用select_related()。这可以节省大量的数据库查询。
    class ArticleAdmin(admin.ModelAdmin):
    	list_select_related = ('author', 'category')


#### ordering
ordering = 'name'
设置ordering以指定如何在Django管理视图中对对象列表进行排序。



#### prepopulated_fields
将prepopulated_fields设置为将字段名称映射到其应预先填充的字段的字典
    class ArticleAdmin(admin.ModelAdmin):
    	prepopulated_fields = {"slug": ("title",)}

#### preserve_filters
preserve_filters = True
管理员现在在创建，编辑或删除对象后保留列表视图中的过滤器。

#### radio_fields
如果radio_fields中存在字段，Django将使用单选按钮接口
    class PersonAdmin(admin.ModelAdmin):
    	radio_fields = {"group": admin.VERTICAL}
    


#### raw_id_fields
raw_id_fields 是一个字段列表，你希望将ForeignKey 或ManyToManyField 转换成Input Widget
    class ArticleAdmin(admin.ModelAdmin):
    	raw_id_fields = ("newspaper",)


#### readonly_fields
readonly_fields = ('address_report',)
此选项中的任何字段（应为list或tuple）将按原样显示其数据，且不可编辑；它们也会从用于创建和编辑的ModelForm中排除。


#### save_as 
save_as = False
如果save_as 为True，"保存并添加另一个"将由"另存为"按钮取代。


#### save_on_top
save_on_top = False 
如果您设置save_on_top，则按钮将同时显示在顶部和底部。


#### search_fields
这些字段应该是某种文本字段，如CharField 或TextField。
search_fields = ['foreign_key__related_fieldname']
search_fields = ['first_name', 'last_name']
search_fields = ['^first_name', '^last_name'] 此查询比正常'%john%' 查询效率高，
search_fields = ['=first_name', '=last_name'] 精确匹配，不区分大小写。


#### show_full_result_count
show_full_result_count = True
设置show_full_result_count以控制是否应在过滤的管理页面上显示对象的完整计数（例如99 结果 103 total））。如果此选项设置为False，则像99 结果 （显示 ）。

#### view_on_site
设置view_on_site以控制是否显示“在网站上查看”链接。此链接将带您到一个URL，您可以在其中显示已保存的对象。
view_on_site = True



ModelAdmin methods
save_model
delete_model
save_formset
get_ordering
get_search_results
save_related
get_readonly_fields
get_prepopulated_fields
get_list_display
get_list_display_links
get_fields
get_fieldsets
get_list_filter
get_search_fields
get_inline_instances
get_urls


InlineModelAdmin objects

```
from django.db import models

class Author(models.Model):
   name = models.CharField(max_length=100)

class Book(models.Model):
   author = models.ForeignKey(Author)
   title = models.CharField(max_length=100)
```
```
from django.contrib import admin

class BookInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]
```



