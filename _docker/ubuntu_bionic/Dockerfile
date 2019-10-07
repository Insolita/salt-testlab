FROM ubuntu:bionic

ENV DEBIAN_FRONTEND noninteractive
ENV container docker
ARG SSH_LOGIN='root'
ARG SSH_PASS='root'
ARG SSH_PORT=22


# clean out, update and install some base utilities
RUN apt-get -y update  && \
	apt-get -y install apt-utils lsb-release curl wget git cron at logrotate rsyslog \
		unattended-upgrades msmtp lsof procps openssh-server sshpass python3 sudo gnupg\
		 libsystemd0 libudev1 systemd sysvinit-utils udev fuse squashfuse util-linux python3-psycopg2 &&\
	apt-get clean && \
	wget -O - https://repo.saltstack.com/py3/ubuntu/18.04/amd64/2019.2/SALTSTACK-GPG-KEY.pub | sudo apt-key add - && \
	echo 'deb http://repo.saltstack.com/py3/ubuntu/18.04/amd64/2019.2 bionic main' >> /etc/apt/sources.list.d/saltstack.list && \
	apt-get -y update && \
	apt-get -y install salt-minion && \
	# set up udev for snap as in https://github.com/ogra1/snapd-docker/blob/5e8fff3d93d5374121ca96ee4f2c207a2e30e461/build.sh
	dpkg-divert --local --rename --add /sbin/udevadm && \
	ln -s /bin/true /sbin/udevadm && \
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
