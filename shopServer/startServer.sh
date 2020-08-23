cd /root/shopServer && \
source /root/.bashrc && \
pip3 install -r requirements.txt && \
uwsgi -x /root/shopServer/shopServer.xml && \
nginx -t  -c /root/shopServer/nginx/myNginx.conf && \
nginx  -c /root/shopServer/nginx/myNginx.conf 
tail -f /dev/null