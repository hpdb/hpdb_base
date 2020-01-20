# System requirements

### 1. Hardware Requirements
- Ubuntu 64-bit
- 2+ computing CPUs
- 8GB+ memory
- 100GB+ disk space

*Please ensure that your system has the essential software packages installed properly before running the installing script. The following should be installed by a system administrator (requires sudo).*

### 2. Install Prerequisites

*We strongly recommend you update and upgrade your operating system software. These upgrades can provide security and software fixes that might prevent future problems.*

1. Update software:
```
sudo apt-get -y update
```

2. Install build essential libraries and dependancies:
```
sudo apt-get install -y build-essential
```

3. Install Apache2:
```
sudo apt-get install -y apache2 apache2-dev
sudo a2enmod cgid proxy proxy_http headers
```

Install `mod_xsendfile` for Apache:
```
wget https://raw.githubusercontent.com/nmaier/mod_xsendfile/master/mod_xsendfile.c
sudo apxs -cia mod_xsendfile.c
```

Restart Apache:
```
sudo systemctl restart apache2
```

4. Install MariaDB:
Please refer to [this](https://downloads.mariadb.org/mariadb/repositories/ "Setting up MariaDB repositories") for instruction on how to install MariaDB 10.4.

5. Create dedicated user for Apache:
```
sudo adduser hpdb
```

And give it sudo permission:
```
sudo usermod -aG sudo hpdb
```

We need to give `hpdb` sudo permission.

6. Reboot.