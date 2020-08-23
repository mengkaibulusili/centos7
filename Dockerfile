FROM scratch
ADD centos-7-x86_64-docker.tar.xz /

RUN   sed -i "s/#baseurl/baseurl/g" /etc/yum.repos.d/CentOS-Base.repo \
  && sed -i "s/mirrorlist=http/#mirrorlist=http/g" /etc/yum.repos.d/CentOS-Base.repo \
  && sed -i "s@http://mirror.centos.org@https://mirrors.huaweicloud.com@g" /etc/yum.repos.d/CentOS-Base.repo \
  && yum clean all \
  && yum makecache \
  && yum -y install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel  \
  && yum -y install gcc automake autoconf libtool make wget \
  && yum -y install kde-l10n-Chinese telnet  \
  && yum -y install glibc-common \
  && yum clean all \
  && localedef -c -f UTF-8 -i zh_CN zh_CN.utf8   \
  && echo -e 'export LANG="zh_CN.UTF-8"\nexport LC_ALL="zh_CN.UTF-8"' > /etc/locale.conf \
  && source /etc/locale.conf 

LABEL \
  org.label-schema.schema-version="1.0" \
  org.label-schema.name="CentOS Base Image" \
  org.label-schema.vendor="CentOS" \
  org.label-schema.license="GPLv2" \
  org.label-schema.build-date="20200809" \
  org.opencontainers.image.title="CentOS Base Image" \
  org.opencontainers.image.vendor="CentOS" \
  org.opencontainers.image.licenses="GPL-2.0-only" \
  org.opencontainers.image.created="2020-08-09 00:00:00+01:00"

ENV LC_ALL  zh_CN.UTF-8
ENV LANG    zh_CN.UTF-8


CMD ["/bin/bash"]