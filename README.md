# DBViewer

#### 介绍
使用python实现的字符界面数据表查看工具，基于npyscreen框架实现。

#### 软件架构
```shell
kitbox

├── config
│   └── db.ini			# 数据库连接参数配置
├── log
│   └── kitbox.log		# 日志文件
└── src
    ├── db.py			# 数据库连接模块
    ├── kit.py			# 主程序
    ├── log.py		    # 日志模块
    ├── menu.py	  		# 菜单模块	
    └── pager.py	    # 翻页支持模块
```


#### 安装教程

配置数据库连接参数文件db.ini

```properties
[DEFAULT] # 默认配置
db = CIP				// 指定打开软件后，默认使用的数据库连接参数

[CIP]
type = oracle			// 连接的数据库类型，支持oracle/mysql
prename = cip			// 配置表所属的用户或者库
username = readonly		// 登录的用户名
password = readonly		// 登录的密码
host = 49.4.22.113		// 数据库服务器ip
port = 1521				// 数据库服务器端口
sid = xe				// oracle数据库的sid，当使用sid连接oracle时配置

[CAP]
type = oracle			
prename = cap
username = readonly
password = readonly
host = 49.4.22.113
port = 1521
servicename = xserv		// oracle数据库的servicename，当使用servicename连接oracle时配置

[TPP]
type = mysql			
prename = tpp
username = readonly
password = readonly
host = 49.4.22.113
port = 1521
db = tpp				// mysql数据库的库名
```



#### 使用说明

1. 启动软件

```shell
./kit.py
```

2. 主页面

![image-20220404083443155](https://s2.loli.net/2022/04/04/co9Xe5xbuJMBmWs.png)

3. 切换数据库，CTRL+X弹出菜单

![image-20220404083624523](https://s2.loli.net/2022/04/04/aXzwhDxk9KHUEqA.png)

4. 通过上下键选中数据行

![image-20220404083923927](https://s2.loli.net/2022/04/04/tdgeiHRjkE3aXV2.png)

5. 以列表方式查看选中的数据行

![image-20220404084025329](https://s2.loli.net/2022/04/04/wrSuU93BNdbK4kI.png)

6. 快速查找，数据表比较多时，可以按l键，输入全部或部分表名，快速查找表

![image-20220404085117022](https://s2.loli.net/2022/04/04/Op9bnuMo7J8gZRD.png)

6. 快捷键

```python
'^S': lambda input: self.sqlTxt.edit(),  # 编辑SQL
'^A': lambda input: self.inType.edit(),  # 编辑SQL输入类型
'^E': lambda input: self.maxRows.edit(),  # 编辑SQL输入类型
'^T': lambda input: self.tbList.edit(),  # 编辑表名
'^V': lambda input: self.tbData.edit(),  # 编辑表数据
'^P': lambda input: npyscreen.blank_terminal(),  # 刷新屏幕
'^Q': lambda input: self.exit_application()  # 退出应用
```



#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
