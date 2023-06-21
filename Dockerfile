FROM python:3.7

WORKDIR /app

# 添加cache
COPY requirements.txt /app/

#RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY . /app

#ENV C_FORCE_ROOT true
#
#ENV DISPLAY ":0"
#
#EXPOSE 8080
#CMD ["/bin/bash","docker_entry.sh"]
