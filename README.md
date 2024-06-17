# 欢迎来到我的王国
![img.png](img.png)
这里集合了我常用的几个信息管理系统。目前主要有
- 密码管理
- 账本管理
- 个人信息管理
- 菜谱管理

框架后端采用django5，前端使用bootstrap，数据库使用sqlite3.

代码存在一个bug：有可能访问另外账户的数据。
另外有很多js文件都是冗余的，没有用

运行方法：
```shell
python manage.py runserver localhost:8000
```