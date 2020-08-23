<!-- TOC -->

- [1. 注意](#1-注意)
- [2. 构建 centos7](#2-构建-centos7)
- [3. 构建 py3612](#3-构建-py3612)
- [4. 构建 py3612NginxUwsgi](#4-构建-py3612nginxuwsgi)
- [5. 在 py3612NginxUwsgi 基础上封装脚本，包装自启动容器](#5-在-py3612nginxuwsgi-基础上封装脚本包装自启动容器)
  - [5.1. 先创建一个数据卷 镜像](#51-先创建一个数据卷-镜像)
  - [5.2. 创建应用容器 基于 nginx django 容器](#52-创建应用容器-基于-nginx-django-容器)
    - [5.2.1. 阻塞 容器推出的小细节](#521-阻塞-容器推出的小细节)
  - [5.3. 使用数据容器](#53-使用数据容器)
  - [5.4. 配置 nginx   uwsgi](#54-配置-nginx-uwsgi)
- [6. 详解前后端 分离部署 nginx 配置](#6-详解前后端-分离部署-nginx-配置)

<!-- /TOC -->
# 1. 注意
构建过程中对网路有一定要求。。

# 2. 构建 centos7

```bash
docker build -f Dockerfile -t  registry.cn-hangzhou.aliyuncs.com/mkmk/centos:base7 .
```

# 3. 构建 py3612
内容脚本内容在 DockerfilePy3612
```bash
docker build -f DockerfilePy3612 -t  registry.cn-hangzhou.aliyuncs.com/mkmk/centos:Py36 .
```

# 4. 构建 py3612NginxUwsgi
内容脚本内容在 DockerfilePy3612Nginx
```bash
docker build -f DockerfilePy3612Nginx -t  registry.cn-hangzhou.aliyuncs.com/mkmk/centos:Py36Nginx .
```

不方便构建的也可以直接使用
```bash
registry.cn-hangzhou.aliyuncs.com/mkmk/centos:Py36Nginx
```

# 5. 在 py3612NginxUwsgi 基础上封装脚本，包装自启动容器

## 5.1. 先创建一个数据卷 镜像

```bash
cat << EOF > DockerfileDataVolum 
FROM alpine
COPY shopServer /root/shopServer

VOLUME /root/shopServer

CMD ["/bin/bash"]
```

```bash
docker build -f DockerfileDataVolum  -t registry.cn-hangzhou.aliyuncs.com/mkmk/centos:VolumeData .
```

## 5.2. 创建应用容器 基于 nginx django 容器

### 5.2.1. 阻塞 容器推出的小细节
/root/shopServer/startServer.sh 内容
```bash
cd /root/shopServer && \
source /root/.bashrc && \
pip3 install -r requirements.txt && \
uwsgi -x /root/shopServer/shopServer.xml && \
nginx -t  -c /root/shopServer/nginx/myNginx.conf && \
nginx  -c /root/shopServer/nginx/myNginx.conf 
# tail -f 可以阻塞 容器执行网命令退出
tail -f /dev/null
```


```bash
cat << EOF > shopServerDF
FROM registry.cn-hangzhou.aliyuncs.com/mkmk/centos:Py36Nginx

CMD ["/bin/bash","/root/shopServer/startServer.sh"]
```

```bash
docker build -f shopServerDF -t registry.cn-hangzhou.aliyuncs.com/mkmk/centos:shopServer .
```

## 5.3. 使用数据容器

```bash
//新建数据容器但是不用运行
docker create --name djangoVolume  registry.cn-hangzhou.aliyuncs.com/mkmk/centos:VolumeData

docker stop centos7base  | docker rm centos7base 

//运行并 挂载数据容器
docker run -d --name centos7base -p 13000:3000 -p 15000:5000  --volumes-from djangoVolume    --privileged=true  registry.cn-hangzhou.aliyuncs.com/mkmk/centos:shopServer
```

## 5.4. 配置 nginx   uwsgi

```bash
nginx -t -c  /root/shopServer/myNginx.conf
nginx -c  /root/shopServer/myNginx.conf
```

```bash
查看服务是否正常启动
ps -ef|grep uwsgi 
```


暂停服务器脚本
```bash
nginx -s stop
pkill -9 uwsgi
pkill -9 python3
```



# 6. 详解前后端 分离部署 nginx 配置

```bash
user root;
 # 容器内设置root 权限启动 应用， 否则部分文件夹无法访问
events { 
#最大连接数
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    # 扩大请求头 的体积上限， 默认 4k
    client_header_buffer_size 16k;
    large_client_header_buffers 10 1m;
    server {
        listen 5000;
        server_name  _; #改为自己的域名，没域名修改为127.0.0.1:80
        charset utf-8;
		
		# django 后端 api 服务
        location /api/ {
           include uwsgi_params;
           uwsgi_pass 127.0.0.1:8999;  #端口要和uwsgi里配置的一样
           uwsgi_param UWSGI_SCRIPT shopServer.wsgi;  #wsgi.py所在的目录名+.wsgi
           uwsgi_param UWSGI_CHDIR /root/shopServer/; #项目路径
        }

        # 静态资源路径 也可以不配置， 
        #因为我们使用的是 webpack 打包的应用程序
        # 只要部署了 build 文件即可
        location /static/ {
        alias /root/shopServer/templates/static/; #静态资源路径
        }

		# 部署前台 资源 的 打包路径
        location / {
           index index.html;
           alias /root/shopServer/build/;
        }
        access_log  /root/shopServer/server.log;
        error_log  /root/shopServer/server.error.log;
    }
}
```
