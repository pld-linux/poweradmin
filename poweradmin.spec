Summary:	PowerAdmin - a web-based front-end for the PowerDNS
Summary(pl):	PowerAdmin - oparty na WWW interfejs dla PowerDNS-a
Name:		poweradmin
Version:	1.2.7
Release:	0.2
License:	GPL
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/poweradmin/%{name}-%{version}.tar.gz
# Source0-md5:	0e639b7a245b7ccda0af4b50221d2cea
Source1:	%{name}.conf
Patch0:		%{name}-addmasterip.patch
URL:		http://www.poweradmin.org/
#Requires:	apache >= 1.3.27-4
Requires:	apache-mod_dir >= 1.3.27-4
Requires:	php4
Requires:	php4-mysql
Requires:	php4-pcre
#Requires:	php4-common
Requires:	php4-zlib
Requires:	php4-dbase
Requires:	php-pear
Requires:	php-pear-PEAR
Requires:	php-pear-DB
Requires:	mysql >= 3.23.2
Requires:	mysql-client >= 3.23.56-1
#Requires: 	sed
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_poweradmindir	/usr/share/PowerAdmin

%description
PowerAdmin is a web-based front-end for the PowerDNS
(http://www.powerdns.com/) DNS server.

%description -l pl
PowerAdmin to oparty na WWW interfejs dla serwera DNS PowerDNS
(http://www.powerdns.com/).

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_poweradmindir}/{images,inc,docs,style} $RPM_BUILD_ROOT%{_sysconfdir}/httpd

install *.php *.php-pa 	$RPM_BUILD_ROOT%{_poweradmindir}
install docs/{ChangeLog,README,README-Sequence,REDHAT-README,TODO} $RPM_BUILD_ROOT%{_poweradmindir}/docs
install images/*.* 	$RPM_BUILD_ROOT%{_poweradmindir}/images
install	style/*.* 	$RPM_BUILD_ROOT%{_poweradmindir}/style
install inc/*.* 	$RPM_BUILD_ROOT%{_poweradmindir}/inc

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi


%files
%defattr(644,root,root,755)
%{_poweradmindir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/%{name}.conf
