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
sudo apt-get install -y build-essential cpanminus default-libmysqlclient-dev
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

Install PHP:
```
sudo apt-get install -y php libapache2-mod-php
```

Restart Apache:
```
sudo systemctl restart apache2
```

4. Install MariaDB:
Please refer to [this](https://downloads.mariadb.org/mariadb/repositories/ "Setting up MariaDB repositories") for instruction on how to install MariaDB 10.4.

5. Install Perl modules:
```
cpanm Bio::Perl Net::Ping
cpanm Graph Time::Piece Hash::Merge PerlIO::gzip Heap::Simple::XS File::Next
cpanm Algorithm::Munkres Archive::Tar Array::Compare Clone Convert::Binary::C
cpanm HTML::Template HTML::TableExtract List::MoreUtils PostScript::TextBlock
cpanm SOAP::Lite SVG SVG::Graph Set::Scalar Sort::Naturally Spreadsheet::ParseExcel
cpanm CGI::Simple GraphViz XML::Parser::PerlSAX XML::Simple Term::ReadKey
cpanm Clone Config::General Font::TTF::Font GD GD::Polyline Math::Bezier Math::Round Math::VecStat Params::Validate Readonly Regexp::Common SVG Set::IntSpan Statistics::Basic Text::Format
```

6. Create dedicated user for Apache:
```
sudo adduser hpdb
```

And give it sudo permission:
```
sudo usermod -aG sudo hpdb
```

We need to give `hpdb` sudo permission.

7. Reboot.