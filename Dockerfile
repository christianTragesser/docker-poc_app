FROM centos:centos7
RUN yum makecache && yum install -y php && yum clean all
ADD ./html/ /var/www/html 
RUN ln -sf /dev/stdout /var/log/httpd/access_log && \
    ln -sf /dev/stderr /var/log/httpd/error_log
EXPOSE 80
ENTRYPOINT /usr/sbin/apachectl -D FOREGROUND
