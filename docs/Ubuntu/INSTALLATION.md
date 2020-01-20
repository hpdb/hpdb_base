# HPDB Installation

*These instructions assumes you're running CentOS 7 64-bit*

**Always log in as `hpdb` (the dedicated user for Apache) by running `su - hpdb` before proceeding**

### HPDB Installation

1. Please ensure that your system has the essential software building packages installed properly before proceeding following installation.

2. Download the codebase:
```
cd ~
git clone https://github.com/hieplpvip/hpdb_base.git -b ubuntu base
```

3. Create directories for projects and create symlinks for them:
```
mkdir data queue queue/external database
ln -s `pwd`/data base/data
ln -s `pwd`/queue base/queue
ln -s `pwd`/database base/database
```

4. Download database:
```
cd database
wget https://github.com/hpdb/hpdb_data/archive/master.zip
unzip master.zip
```

5. Install HPDB:
```
cd ~/base
./INSTALL.sh
```

The following tools will be installed:
- Alignment:
    + Clustal Omega
    + Snippy
- Annotation:
    + BLAST+
    + Prodigal
- Classification:
    + Centrifuge
- Utility:
    + Anaconda

and others installed as dependencies of those above.

### MariaDB Configuration

1. Secure MariaDB:
```
sudo mysql_secure_installation
```

- Enter root password (likely none)
- Set root password? Yes
- Enter new root password.
- Re-enter new root password.
- Remove anonymous users? Yes
- Disallow root login remotely? Yes
- Remove test database and access to it? Yes
- Reload privilege table now? Yes

2. Create database for HPDB:
```
mysql -p -u root
```

Enter the password you've just changed.

```
create database if not exists hpdb character set 'utf8' collate 'utf8_unicode_ci';

use hpdb;

create table users(
    id int not null primary key auto_increment,
    email varchar(255) not null unique,
    username varchar(255) not null unique,
    password varchar(255) not null
);

create table sessions(
    sid varchar(255) not null primary key unique,
    userid int not null,
    username varchar(255) not null,
    lastlogin datetime not null,
    CONSTRAINT fsk_uid FOREIGN KEY (userid) REFERENCES users(id),
    CONSTRAINT fsk_uname FOREIGN KEY (username) REFERENCES users(username)
);

create table projects(
    jobid varchar(255) not null primary key unique,
    userid int not null,
    username varchar(255) not null,
    CONSTRAINT fpk_uid FOREIGN KEY (userid) REFERENCES users(id),
    CONSTRAINT fpk_uname FOREIGN KEY (username) REFERENCES users(username)
);

exit;
```

Finally, change password in `scripts/user_management.py`.

### Apache Web Server Configuration

1. Modify/Check sample Apache configuration file:

Double check `$HPDB_BASE/apache_conf/hpdb_httpd.conf` alias directories match the HPDB installation path at line 1, 2, 3, 6, 7, 17, 18 and 30.

2. Give Apache necessary permissions:

The User and Group on lines 67 and 68 in `$HPDB_BASE/apache_conf/httpd.conf` should be `hpdb` (the dedicated user for Apache).

```
# Give APACHE_RUN_USER permission to write
sudo chown -R hpdb $HPDB_BASE/www
sudo chgrp -R hpdb $HPDB_BASE/www
```

3. Copy configuration files to the appropriate directories:
```
sudo cp $HPDB_BASE/apache_conf/hpdb_apache.conf /etc/apache2/conf-available/
sudo cp $HPDB_BASE/apache_conf/apache2.conf /etc/apache2/apache2.conf
ln -s /etc/apache2/conf-available/hpdb_apache.conf /etc/apache2/conf-enabled/
```

4. Restart Apache to activate the new configuration:
```
sudo systemctl restart httpd
```