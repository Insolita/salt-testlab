FROM debian:stretch

ENV DEBIAN_FRONTEND noninteractive
ENV container docker
ARG SSH_LOGIN='root'
ARG SSH_PASS='root'
ARG SSH_PORT=22


# add contrib, non-free and backports repositories
ADD sources.list /etc/apt/sources.list
# pin stable repositories
ADD preferences /etc/apt/preferences

# clean out, update and install some base utilities
RUN apt-get -y update && \
	apt-get -y install apt-utils lsb-release curl wget git cron at logrotate rsyslog apt-transport-https\
		unattended-upgrades ssmtp lsof procps openssh-server sshpass python3 sudo gnupg  \
		initscripts libsystemd0 libudev1 systemd sysvinit-utils udev fuse  util-linux python3-psycopg2  && \
	apt-get clean && \
	wget -O - https://repo.saltstack.com/py3/debian/9/amd64/2019.2/SALTSTACK-GPG-KEY.pub | sudo apt-key add - && \
	echo 'deb http://repo.saltstack.com/py3/debian/9/amd64/2019.2 stretch main' >> /etc/apt/sources.list.d/saltstack.list && \
    apt-get -y update && \
	apt-get -y install salt-minion && \
	sed -i '/imklog/{s/^/#/}' /etc/rsyslog.conf \
	&& sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
      && sed -i s/#Port.*/Port\ ${SSH_PORT}/ /etc/ssh/sshd_config \
      && echo "ssh-serv" >> /etc/hostname

RUN if [ $SSH_LOGIN = "root" ]; then \
        echo "${SSH_LOGIN}:${SSH_PASS}" | chpasswd; \
    else \
        useradd -m "${SSH_LOGIN}" && echo "${SSH_LOGIN}:${SSH_PASS}" | chpasswd && adduser "${SSH_LOGIN}" sudo; \
    fi


RUN cd /lib/systemd/system/sysinit.target.wants/ && \
		ls | grep -v systemd-tmpfiles-setup.service | xargs rm -f && \
		rm -f /lib/systemd/system/sockets.target.wants/*udev* && \
		systemctl mask -- \
			tmp.mount \
			etc-hostname.mount \
			etc-hosts.mount \
			etc-resolv.conf.mount \
			swap.target \
			getty.target \
			getty-static.service \
			cgproxy.service \
			systemd-tmpfiles-setup-dev.service \
			systemd-ask-password-wall.path \
			systemd-logind.service && \
		systemctl set-default multi-user.target || true

RUN sed -ri /etc/systemd/journald.conf \
			-e 's!^#?Storage=.*!Storage=volatile!'
RUN systemctl enable ssh.service

RUN ssh-keygen -A

VOLUME [ "/sys/fs/cgroup", "/lib/modules", "/run", "/run/lock", "/tmp" ]
COPY minion /etc/salt/

CMD ["/lib/systemd/systemd"]
