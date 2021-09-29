# python:3.9.7-alpine 会出现很多问题，所以这里选择python:3.9.7
# FROM python:3.9.7-alpine
FROM python:3.9.7
WORKDIR /data/xingming
ADD . /data/xingming
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone
RUN python manage.py makemigations
RUN python manage.py migrate
EXPOSE 8080
ENV TZ Asia/Shanghai
ENTRYPOINT ["uwsgi","--ini","/data/xingming/uwsgi.ini"]
