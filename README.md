<h3>### Управление пакетами. Дистрибьюция софта ###</h3>

<h4>Описание домашнего задания</h4>

<ul>
<li>создать свой RPM (можно взять свое приложение, либо собрать к примеру апач с определенными опциями);</li>
<li>создать свой репо и разместить там свой RPM;</li>
<li>реализовать это все либо в вагранте, либо развернуть у себя через nginx и дать ссылку на репо.</li>
</ul>

<h4># Создадим виртуальную машину rpmbulder</h4>

<p>В домашней директории создадим директорию rpmbulder, в котором будут храниться настройки виртуальной машины:</p>

<pre>[student@pv-homeworks1-10 sergsha]$ mkdir ./rpmbulder
[student@pv-homeworks1-10 sergsha]$</pre>

<p>Перейдём в директорию rpmbulder:</p>

<pre>[student@pv-homeworks1-10 sergsha]$ cd ./rpmbulder/
[student@pv-homeworks1-10 rpmbulder]$</pre>

<p>Создадим файл Vagrantfile:</p>

<pre>[student@pv-homeworks1-10 nfs]$ vi ./Vagrantfile</pre>

<p>Заполним следующим содержимым:</p>

<pre>## -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"

  config.vm.provider "virtualbox" do |v|
    v.memory = 256
    v.cpus = 1
  end

  config.vm.define "rpmbuilder" do |rpmbuilder|
    rpmbuilder.vm.network "private_network", ip: "192.168.50.12", virtualbox__intnet: "net1"
    rpmbuilder.vm.hostname = "rpmbuilder"
  end

end
</pre>

<p>Запустим виртуальную машину:</p>

<pre>[student@pv-homeworks1-10 rpmbuilder]$ vagrant up</pre>

<p>Проверим состояние созданных и запущенных машин:</p>

<pre>[student@pv-homeworks1-10 rpmbuilder]$ vagrant status
Current machine states:

rpmbuilder                running (virtualbox)

The VM is running. To stop this VM, you can run `vagrant halt` to
shut it down forcefully, or you can run `vagrant suspend` to simply
suspend the virtual machine. In either case, to restart it again,
simply run `vagrant up`.
[student@pv-homeworks1-10 rpmbuilder]$</pre>

<p>Заходим на сервер rpmbuilder:</p>

<pre>[student@pv-homeworks1-10 rpmbuilder]$ vagrant ssh
[vagrant@rpmbuilder ~]$</pre>

<p>Установим следующие пакеты:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo yum -y install rpmdevtools rpm-build createrepo yum-utils tree
[vagrant@rpmbuilder ~]$</pre>

<p>Создадим дерево каталогов:</p>

<pre>[vagrant@rpmbuilder ~]$ rpmdev-setuptree
[vagrant@rpmbuilder ~]$</pre>

<p>Смотрим полученное дерево каталогов:</p>

<pre>[vagrant@rpmbuilder ~]$ tree -d -L 1 ./rpmbuild
./rpmbuild
├── BUILD
├── RPMS
├── SOURCES
├── SPECS
└── SRPMS

5 directories
[vagrant@rpmbuilder ~]$</pre>

<p>В директории SOURCES создадим скрипт hello.sh, который после установки расположится в /usr/local/bin/:</p>

<pre>[vagrant@rpmbuilder ~]$ vi ./rpmbuild/SOURCES/hello.sh</pre>

<pre>#!/bin/bash

echo "Hello World!"
</pre>

<p>В директории создадим cpec файл hello.spec:</p>

<pre>[vagrant@rpmbuilder ~]$ vi ./rpmbuild/SPECS/hello.spec</pre>

<pre>Name:           hello
Version:        1.0
Release:        1
Summary:        My Script
License:        -

Source0:        hello.sh

BuildArch:      noarch

Buildroot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Hello World

%install
install -D -pm 755 %{SOURCE0} %{buildroot}/usr/local/bin/hello.sh

%files
/usr/local/bin/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
echo "$(date +%a\ %b\ %d\ %Y) $USER"
- Add hello.sh

%post
/usr/local/bin/hello.sh
</pre>

<p>В раздел %post добавлена строка, которая после установки пакета сразу запускает скрипт.</p>

<p>Приступаем к сборке RPM пакета:</p>

<pre>[vagrant@rpmbuilder ~]$ rpmbuild -bb rpmbuild/SPECS/hello.spec
Executing(%install): /bin/sh -e /var/tmp/rpm-tmp.0lyNSe
+ umask 022
+ cd /home/vagrant/rpmbuild/BUILD
+ '[' /home/vagrant/rpmbuild/BUILDROOT/hello-1.0-1.x86_64 '!=' / ']'
+ rm -rf /home/vagrant/rpmbuild/BUILDROOT/hello-1.0-1.x86_64
++ dirname /home/vagrant/rpmbuild/BUILDROOT/hello-1.0-1.x86_64
+ mkdir -p /home/vagrant/rpmbuild/BUILDROOT
+ mkdir /home/vagrant/rpmbuild/BUILDROOT/hello-1.0-1.x86_64
+ install -D -pm 755 /home/vagrant/rpmbuild/SOURCES/hello.sh /home/vagrant/rpmbuild/BUILDROOT/hello-1.0-1.x86_64/usr/local/bin/hello.sh
+ '[' noarch = noarch ']'
+ case "${QA_CHECK_RPATHS:-}" in
+ /usr/lib/rpm/check-buildroot
+ /usr/lib/rpm/redhat/brp-compress
+ /usr/lib/rpm/redhat/brp-strip /usr/bin/strip
+ /usr/lib/rpm/redhat/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump
+ /usr/lib/rpm/redhat/brp-strip-static-archive /usr/bin/strip
+ /usr/lib/rpm/brp-python-bytecompile /usr/bin/python 1
+ /usr/lib/rpm/redhat/brp-python-hardlink
+ /usr/lib/rpm/redhat/brp-java-repack-jars
Processing files: hello-1.0-1.noarch
Provides: hello = 1.0-1
Requires(interp): /bin/sh
Requires(rpmlib): rpmlib(CompressedFileNames) <= 3.0.4-1 rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires(post): /bin/sh
Requires: /bin/bash
Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/vagrant/rpmbuild/BUILDROOT/hello-1.0-1.x86_64
Wrote: /home/vagrant/rpmbuild/RPMS/noarch/hello-1.0-1.noarch.rpm
Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.xIlDab
+ umask 022
+ cd /home/vagrant/rpmbuild/BUILD
+ rm -rf /home/vagrant/rpmbuild/BUILDROOT/hello-1.0-1.x86_64
+ exit 0
[vagrant@rpmbuilder ~]$</pre>

<p>Смотрим, что пакет создался:</p>

<pre>[vagrant@rpmbuilder ~]$ ls -l ./rpmbuild/RPMS/noarch/
total 4
-rw-rw-r--. 1 vagrant vagrant 2164 May 30 20:50 hello-1.0-1.noarch.rpm
[vagrant@rpmbuilder ~]$</pre>

<p>Теперь попробуем установить наш пакет:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo rpm -iv ./rpmbuild/RPMS/noarch/hello-1.0-1.noarch.rpm
Preparing packages...
hello-1.0-1.noarch
Hello World!
[vagrant@rpmbuilder ~]$</pre>

<p>Удалим наш только что установленный пакет:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo rpm -e hello
[vagrant@rpmbuilder ~]$</pre>

<h4>Создадим собственный репозиторий и разместим там ранее собранный RPM пакет.</h4>

<p>Приступаем к созданию своего репозитория. Для этого установим и настроим nginx:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo yum -y install epel-release</pre>
<pre>[vagrant@rpmbuilder ~]$ sudo yum -y install nginx</pre>

<p>Создадим каталог repo:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo mkdir /usr/share/nginx/html/repo
[vagrant@rpmbuilder ~]$</pre>

<p>Скопируем в этот каталог наш собранный RPM пакет:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo cp ./rpmbuild/RPMS/noarch/hello-1.0-1.noarch.rpm /usr/share/nginx/html/repo/
[vagrant@rpmbuilder ~]$</pre>

<p>Иницилизируем наш новый репозиторий:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo createrepo /usr/share/nginx/html/repo/
Spawning worker 0 with 1 pkgs
Workers Finished
Saving Primary metadata
Saving file lists metadata
Saving other metadata
Generating sqlite DBs
Sqlite DBs complete
[vagrant@rpmbuilder ~]$</pre>

<p>Настроим в nginx доступ к директории repo. В location / в файле /etc/nginx/nginx.conf добавим директиву autoindex on:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo vi /etc/nginx/default.d/autoindex.conf</pre>

<pre>        index index.html index.htm;
        autoindex on;</pre>

<p>Проверим синтаксис конфигурации nginx:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
[vagrant@rpmbuilder ~]$</pre>

<p>Обновим конфигурацию nginx:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo nginx -s reload
[vagrant@rpmbuilder ~]$</pre>

<p>С помощью утилиты curl проверим:</p>

<pre>[vagrant@rpmbuilder ~]$ curl -a http://localhost/repo/
&lt;html&gt;
&lt;head&gt;&lt;title&gt;Index of /repo/&lt;/title&gt;&lt;/head&gt;
&lt;body&gt;
&lt;h1&gt;Index of /repo/&lt;/h1&gt;&lt;hr&gt;&lt;pre&gt;&lt;a href="../"&gt;../&lt;/a&gt;
&lt;a href="repodata/"&gt;repodata/&lt;/a&gt;                                          30-May-2022 21:24                   -
&lt;a href="hello-1.0-1.noarch.rpm"&gt;hello-1.0-1.noarch.rpm&lt;/a&gt;                             30-May-2022 21:20                2164
&lt;/pre&gt;&lt;hr&gt;&lt;/body&gt;
&lt;/html&gt;
</pre>

<p>Теперь добавим репозиторий с именем, например, hello в /etc/yum.repos.d/:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo vi /etc/yum.repos.d/hello.repo</pre>

<pre>[hello]
name=hello-world
baseurl=http://localhost/repo
gpgcheck=0
enabled=1
</pre>

<p>Убеждаемся, что репозиторий hello подключился:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo yum repolist enabled | grep hello
hello                 hello-world                                              1
[vagrant@rpmbuilder ~]$ sudo yum list | grep hello
hello.noarch                             1.0-1                         hello
[vagrant@rpmbuilder ~]$</pre>

<p>Репозиторий готов, теперь пробуем установить пакет hello с репозитория:</p>

<pre>[vagrant@rpmbuilder ~]$ sudo yum -y install hello
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: centosmirror.netcup.net
 * epel: mirror.de.leaseweb.net
 * extras: centos.schlundtech.de
 * updates: centosmirror.netcup.net
Resolving Dependencies
--> Running transaction check
---> Package hello.noarch 0:1.0-1 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=====================================================================================
 Package            Arch                Version             Repository          Size
=====================================================================================
Installing:
 hello              noarch              1.0-1               hello              2.1 k

Transaction Summary
=====================================================================================
Install  1 Package

Total download size: 2.1 k
Installed size: 33
Downloading packages:
hello-1.0-1.noarch.rpm                                        | 2.1 kB  00:00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : hello-1.0-1.noarch                                                1/1
Hello World!
  Verifying  : hello-1.0-1.noarch                                                1/1

Installed:
  hello.noarch 0:1.0-1

Complete!
[vagrant@rpmbuilder ~]$</pre>

<p>Попробуем запустить программу</p>

<pre>[vagrant@rpmbuilder ~]$ hello.sh
Hello World!
[vagrant@rpmbuilder ~]$</pre>

<p>Программа выполнена, всё прошло успешно.</p>
