安装：
执行b_install.cgi，然后按照提示一步步设置好就可以使用鸟。

历史:
2.0 正式版
在线更新功能。
修正回复索引。
修改默认模板。（不完全支持旧模板）
增加强制切断。
修正新建文件有时无法成功的BUG。
增加了文章隐藏功能。
修正了文章回复管理的BUG。
增加密码最大长度为 20 个字符。
增加普通用户登录注册功能。

2.0 Preview
增加了所见即所得在线编辑器。
全仿WINDOWS软件界面更容易上手。
修正Newest模板兼容性错误。
修正QLOG错误。
增强文章切断功能。
UTF8化。

1.1正式版:
修正了config.cgi中文件锁的错误。

1.0正式版:
增加了自动识别URL的功能。
更新了默认模板。
修改了日历的HTML代码。
增加了回复表格的Class属性"replytable"。
增加了站点访问统计。
修正了CONFIG中关于COOKIES的错误。

Preview 3:
增加了在日志编辑页面上传文件的功能。
更改了文件上传后的命名方式，以日期命名。
修正了安装后不能登录的BUG。
修正了未来可能与XHTML+CSS创建的标准网页相冲突的地方。
修正了模板修改中的一个标签错误。
修正了删除空记录的BUG。
修正了QLOG中回复表单过大的问题。
修正了由于删除引起的搜索问题。
Prevew 2
增加了QQ自定义模板的显示。
增加了对RSS1.0的支持。

文件：
压缩包内应该包括如下文件
文件/目录名      描述                     权限
b_img            [DIR] Blog基本图片目录 
uploaddata       [DIR] 上传文件所在目录    777
blogdata         [DIR] Blog基本文件目录    777
userdata         [DIR] 用户文件目录        777
b_install.cgi    安装程序                  755
config.cgi       Mantoz库文件              644
b_lib.cgi        Blog的库文件              644
blog_manager.cgi Blog管理程序              755
blog.cgi         Blog页面显示程序          755
upfile.cgi       文件上传程序               755
client.js        显示页面相关Javascript代码 644
jscript.js          编辑页面相关Javascript代码 644
gb-uni.tab       GB转UNICODE代码表          666
Readme.txt       自述文件                   不用传了