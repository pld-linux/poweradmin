Summary:	PowerAdmin is a web-based front-end for the PowerDNS
Summary(pl):	PowerAdmin to oparty na web interfejs dla PowerDNS
Name:		poweradmin
Version:	1.2.7
Release:	0.1
License:	GPL
Group:		Applications/Databases/Interfaces
Source0:	http://unc.dl.sourceforge.net/sourceforge/poweradmin/%{name}-%{version}.tar.gz
# Source0-md5:	0e639b7a245b7ccda0af4b50221d2cea
URL:		http://www.poweradmin.org
#Requires:	apache >= 1.3.27-4
Requires:	apache-mod_dir >= 1.3.27-4
Requires:	php4
Requires:	php4-mysql
Requires:	php4-pcre
#Requires:	php4-common
Requires:	php4-zlib
Requires:	php4-dbase
Requires:	php-pear
#Requiers: 	php-pear-PEAR
Requires:	php-pear-DB
Requires:	mysql >= 3.23.2
Requires:	mysql-client >= 3.23.56-1
#Requires: 	sed
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%define _poweradmindir /usr/share/PowerAdmin

%description
PowerAdmin is a web-based front-end for the PowerDNS
(www.powerdns.com) DNS server.

%description -l pl
PowerAdmin to oparty na web interfejs dla PowerDNS
(www.powerdns.com) DNS serwer.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_poweradmindir}/{images,inc,docs,style}

install *.php *.php-pa 	$RPM_BUILD_ROOT%{_poweradmindir}
install docs/{ChangeLog,README,README-Sequence,REDHAT-README,TODO} $RPM_BUILD_ROOT%{_poweradmindir}/docs
install images/*.* 	$RPM_BUILD_ROOT%{_poweradmindir}/images
install	style/*.* 	$RPM_BUILD_ROOT%{_poweradmindir}/style
install inc/*.* 	$RPM_BUILD_ROOT%{_poweradmindir}/inc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_poweradmindir}
%{_poweradmindir}
