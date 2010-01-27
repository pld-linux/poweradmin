Summary:	PowerAdmin - a web-based front-end for the PowerDNS
Summary(pl.UTF-8):	PowerAdmin - oparty na WWW interfejs dla PowerDNS-a
Name:		poweradmin
Version:	2.1.4
Release:	1
License:	GPL
Group:		Applications/Databases/Interfaces
Source0:	https://www.poweradmin.org/download/%{name}-%{version}.tgz
# Source0-md5:	55b762bebc290bd1be061cb3363f976a
URL:		http://www.poweradmin.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	sed >= 4.0
Requires:	php(dbase)
Requires:	php(mysql)
Requires:	php(zlib)
Requires:	php-gettext
Requires:	php-pear-MDB2
Requires:	webapps
Requires:	webserver(indexfile)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
PowerAdmin is a web-based front-end for the PowerDNS
(http://www.powerdns.com/) DNS server.

%description -l pl.UTF-8
PowerAdmin to oparty na WWW interfejs dla serwera DNS PowerDNS
(http://www.powerdns.com/).

%prep
%setup -q

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{images,inc,docs,style,locale,install}}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

mv inc/config-me.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/config.inc.php
install *.php 		$RPM_BUILD_ROOT%{_appdir}
install docs/*.sql docs/*.pot		$RPM_BUILD_ROOT%{_appdir}/docs
install images/*.*	$RPM_BUILD_ROOT%{_appdir}/images
install style/*.*	$RPM_BUILD_ROOT%{_appdir}/style
install inc/*.*		$RPM_BUILD_ROOT%{_appdir}/inc
cp -a locale		$RPM_BUILD_ROOT%{_appdir}/locale
install install/*.*	$RPM_BUILD_ROOT%{_appdir}/install
ln -s %{_sysconfdir}/config.inc.php $RPM_BUILD_ROOT%{_appdir}/inc/config.inc.php

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%banner %{name} -e <<'EOF'

To finish your setup point your browser to http://yourserver/poweradmin/install/ .

EOF

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc docs/{CHANGELOG,LICENSE,README}
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
