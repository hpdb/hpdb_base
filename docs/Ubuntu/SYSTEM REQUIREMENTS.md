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
sudo apt-get -y update && sudo apt-get -y upgrade
```

2. Install build essential libraries and dependancies:
```
sudo apt-get install -y build-essential libreadline-gplv2-dev libx11-dev \
  libxt-dev libgsl-dev libfreetype6-dev libncurses5-dev gfortran \
  inkscape libwww-perl libxml-libxml-perl libperlio-gzip-perl \
  zlib1g-dev zip unzip libjson-perl libpng-dev cpanminus default-jre \
  wget curl csh liblapack-dev libblas-dev libatlas-base-dev \
  libcairo2-dev libssh2-1-dev libssl-dev libcurl4-openssl-dev bzip2 \
  bioperl rsync libbz2-dev liblzma-dev time libterm-readkey-perl \
  liblwp-protocol-https-perl gnuplot libjson-xs-perl libio-socket-ip-perl \
  vim php texinfo zlib1g-dev openjdk-11-jdk texlive default-libmysqlclient-dev \
  texlive-fonts-extra libboost-all-dev cron less libxml2-dev \
  libdatetime-perl libxml-simple-perl libdigest-md5-perl git parallel
```

3. Install Apache2:
```
sudo apt-get install -y apache2 apache2-dev
sudo a2enmod cgid proxy proxy_http headers file_cache cache_disk
```

Install `mod_xsendfile` for Apache:
```
wget https://raw.githubusercontent.com/nmaier/mod_xsendfile/master/mod_xsendfile.c
sudo apxs -cia mod_xsendfile.c
```

Install PHP:
```
sudo apt-get install -y php libapache2-mod-php php-mbstring
```

Restart Apache:
```
sudo systemctl restart apache2
systemctl start apache-htcacheclean
```

4. Install MariaDB:
Please refer to [this](https://downloads.mariadb.org/mariadb/repositories/ "Setting up MariaDB repositories") for instruction on how to install MariaDB 10.4.

5. Install Perl modules:
```
sudo cpanm -f Bio::Perl Net::Ping \
              Graph Time::Piece Hash::Merge PerlIO::gzip Heap::Simple::XS File::Next \
              Algorithm::Munkres Archive::Tar Array::Compare Clone Convert::Binary::C \
              HTML::Template HTML::TableExtract List::MoreUtils PostScript::TextBlock \
              SOAP::Lite SVG SVG::Graph Set::Scalar Sort::Naturally Spreadsheet::ParseExcel \
              CGI::Simple GraphViz XML::Parser::PerlSAX XML::Simple Term::ReadKey Clone \
              Config::General Font::TTF::Font GD GD::Polyline Math::Bezier Math::Round \
              Math::VecStat Params::Validate Readonly Regexp::Common SVG Set::IntSpan \
              Statistics::Basic Text::Format Array::Utils Exception::Class File::Basename \
              File::Copy File::Find::Rule File::Grep File::Path File::Slurper File::Spec \
              File::Temp File::Which FindBin Getopt::Long Graph Graph::Writer::Dot List::Util \
              Log::Log4perl Moose Moose::Role Text::CSV PerlIO::utf8_strict Devel::OverloadInfo Digest::MD5::File
sudo cpanm -f Bio::Roary
```

6. Create dedicated user for Apache:
```
sudo adduser hpdb
```

And give it sudo permission:
```
sudo usermod -aG sudo hpdb
```

7. Reboot.