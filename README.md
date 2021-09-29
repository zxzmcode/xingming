# xingming

个人博客，目的主要是用来记录个人日常使用的各种技术文档的。所以暂不开启登录和评论功能。

# 关于目录的说明

article --> 博客文章的主体部分。主要用来展示文章，标签，分类等等 

config --> 配置文件所在目录，生产环境建议置于环境变量中 

frontTemplate --> 前端模板所在文件夹，包含对应所有css，图片等等

templates --> django 模板文件夹 

static --> 静态文件所在文件夹 

xingming --> 项目主文件夹 

requirements.txt --> 项目依赖，由于和以前一个项目公用一个conda虚拟环境，所以有些依赖应该是不需要的，请自行排查。

# 关于开发说明

该博客前端模板使用[Blog-template](https://github.com/Kudaompq/Blog-template)，来源于githup博主Kudaompq。
采用python语言3.9.6版本和Django 3.2.6编写。

# 开源授权

由于Kudaompq未指定开源协议，同时本人暂未获取授权。所以改代码仅供学习，请勿用作商务用途。

# 关于使用
## 直接应用

* 1、运行环境 

  安装好python和pip。推荐python=3.9.6。具体安装方法请自行解决

* 2、安装依赖 

  进入项目文件夹后执行下面命令，安装指定的依赖

    ```
    pip install -r requirements.txt
    ```

* 3、配置数据库和redis 

  在修改config/database-*.conf文件，这里提供了linux和windows两个环境的，这是编写时有两个环境，一个是在Linux做测试的，一个是在Windows下进行开发的。所以读者按需修改，默认是database-windows.conf

    ```editorconfig
    [mysql_connection]
    # 下面内容不需要引号表示
    name = mysql_db_name
    user = mysql_db_user
    password = mysql_password
    host = mysql_ip
    port = mysql_port
    
    [redis_connection]
    location = redis://redis_ip:redis_port
    password = redis_password
    ```

* 4、初始化数据库 

  django可以通过一下命令进行数据库建表修改表结构等等。

    ```shell
    python manage.py makemigations
    python manage.py migrate
    ```

* 5、创建用户

  进行操作之后，数据库中还没有任何数据。所以需要创建用户。这里给出命令。之后按要求填写即可。

  ```shell
  python manage.py createsuperuser
  ```

* 6、启动项目

  使用以下命令启动项目，启动时可以不接0.0.0.0:80。但是个人喜欢用80端口。这里就这样写了

  ```shell
  python manage.py runserver 0.0.0.0:80
  ```

## Docker环境

* 1、配置数据库和redis 

  在修改config/database-*.conf文件，这里提供了linux和windows两个环境的，这是编写时有两个环境，一个是在Linux做测试的，一个是在Windows下进行开发的。所以读者按需修改，默认是database-windows.conf

    ```editorconfig
    [mysql_connection]
    # 下面内容不需要引号表示
    name = mysql_db_name
    user = mysql_db_user
    password = mysql_password
    host = mysql_ip
    port = mysql_port
    
    [redis_connection]
    location = redis://redis_ip:redis_port
    password = redis_password
    ```

* 2、执行docker build 进行打包镜像

```shell
docker build -t xingming:1.0.1 .

```

* 3、启动镜像,并绑定到对应的8080端口

```shell
docker run -d -it -p 8080:8080 --name xingming xingming:1.0.1 
```
