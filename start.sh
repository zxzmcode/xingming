# !/bin/bash
######################################################################
# 功能: 用来启动docker容器中的uwsgi进程
# 作者: zxzmcode
# 日期: 2021-09-28
# 版本: v1
# 描述: 由于在Docker容器通过CMD ["/usr/local/bin/uwsgi",
#       "--ini","uwsgi.ini"] 无法启动uwsgi进程，使用该脚本完成
######################################################################
/usr/local/bin/uwsgi --ini /data/xingming/uwsgi.ini