# System requirements

### 1. Hardware Requirements
- CentOS 7 64-bit
- 2+ computing CPUs
- 8GB+ memory
- 100GB+ disk space

*Please ensure that your system has the essential software packages installed properly before running the installing script. The following should be installed by a system administrator (requires sudo).*

### 2. Install Prerequisites

*We strongly recommend you update and upgrade your operating system software. These upgrades can provide security and software fixes that might prevent future problems.*

1. Update software:
```
sudo yum -y upgrade
```

2. Add required repositories:
```
sudo yum -y install epel-release
sudo rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
```

Run `sudo vi /etc/yum.repos.d/MariaDB.repo` and paste this:
```
# MariaDB 10.4 CentOS repository list
# http://downloads.mariadb.org/mariadb/repositories/
[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/10.4/centos7-amd64
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
```

3. Install required packages:
```
sudo yum -y groupinstall 'development tools'
sudo yum -y install python-devel python3-devel wget argtable argtable-devel xz-devel ncurses-devel zlib-devel libdb-devel expat-devel perl-ExtUtils-MakeMaker R
sudo yum install -y libX11-devel readline-devel libXt-devel ncurses-devel inkscape \
    expat expat-devel freetype freetype-devel zlib zlib-devel perl-App-cpanminus \
    perl-Test-Most blas-devel atlas-devel lapack-devel libpng12 libpng12-devel \
    perl-XML-Simple perl-JSON csh gcc gcc-c++ make binutils gd gsl-devel git graphviz \
    java-1.7.0-openjdk perl-Archive-Zip perl-CGI curl perl-CGI-Session \
    perl-CPAN-Meta-YAML perl-DBI perl-Data-Dumper perl-GD perl-IO-Compress \
    perl-Module-Build perl-XML-LibXML perl-XML-Parser perl-XML-SAX perl-XML-SAX-Writer \
    perl-XML-Twig perl-XML-Writer perl-YAML perl-PerlIO-gzip libstdc++-static \
    cairo-devel openssl-devel openssl-static libssh2-devel libcurl-devel \
    wget rsync bzip2 bzip2-devel xz-devel time zip unzip which perl-CPAN \
    perl-LWP-Protocol-https cronie gnuplot perl-JSON-XS perl-IO-Socket-IP
sudo yum --enablerepo=remi,remi-php74 -y install httpd httpd-devel php php-common php-mysql php-devel php-gd php-pecl-memcache php-pspell php-snmp php-xmlrpc php-xml php-mbstring
sudo yum -y install mariadb-server
```

Install required libs for mysqlclient (thanks to [this](https://stackoverflow.com/questions/46495448/unable-to-install-mysqlclient-on-centos)):
```
sudo rpm -Uvh https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
sudo yum -y install mysql-community-devel.x86_64
```

Install `mod_xsendfile` for Apache:
```
wget https://raw.githubusercontent.com/nmaier/mod_xsendfile/master/mod_xsendfile.c
sudo apxs -cia mod_xsendfile.c
```

Install R packages:
```
sudo su - -c "R -q -e \"install.packages('ggplot2', repos='http://cran.rstudio.com/')\""
```

4. Configure firewall for http, https, and smtp:
```
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=smtp
sudo firewall-cmd --reload
```

If you got error `firewall-cmd: command not found`, install `firewalld` then run the above commands again:
```
sudo yum -y install firewalld
systemctl restart firewalld
```

5. Start Apache and MariaDB:
```
sudo systemctl enable httpd && sudo systemctl start httpd
sudo systemctl enable mariadb.service && sudo systemctl start mariadb.service
```

6. Create dedicated user for Apache:
```
sudo adduser hpdb
sudo passwd hpdb
```

We need to give `hpdb` sudo permission.

If you're using Google Cloud:
```
sudo usermod -g google-sudoers hpdb
```

If you're using Digital Ocean or Linode:
```
sudo usermod -g wheel hpdb
```

If you're using other platforms, refer to their documentation.

7. Disable SELinux:
```
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
```

8. Enable swap memory (optional, recommended):

Create swap file:
```
sudo dd if=/dev/zero of=/swapfile count=16 bs=1GiB
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Make the swap file permanent:
```
echo '/swapfile swap swap sw 0 0' | sudo tee -a /etc/fstab
```

Tweak swap settings (optional):
```
echo 'vm.swappiness = 10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure = 50' | sudo tee -a /etc/sysctl.conf
```

9. Reboot.