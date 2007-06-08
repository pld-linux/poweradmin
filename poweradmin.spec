Summary:	PowerAdmin - a web-based front-end for the PowerDNS
Summary(pl.UTF-8):	PowerAdmin - oparty na WWW interfejs dla PowerDNS-a
Name:		poweradmin
Version:	1.2.7
Release:	0.9
License:	GPL
Group:		Applications/Databases/Interfaces
Source0:	http://www.poweradmin.org/releases/%{name}-%{version}-patched.tar.gz
# Source0-md5:	105bfc2f5e22816c4f5412d448833fb7
Patch0:		%{name}-addmasterip.patch
Patch1:		%{name}-bugs.patch
URL:		http://www.poweradmin.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	sed >= 4.0
Requires:	php(dbase)
Requires:	php(mysql)
Requires:	php(zlib)
Requires:	php-pear-DB
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
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{images,inc,docs,style}}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

mv install.php.orig install.php
mv inc/config.inc.php $RPM_BUILD_ROOT%{_sysconfdir}
install *.php *.php-pa	$RPM_BUILD_ROOT%{_appdir}
install images/*.*	$RPM_BUILD_ROOT%{_appdir}/images
install style/*.*	$RPM_BUILD_ROOT%{_appdir}/style
install inc/*.*		$RPM_BUILD_ROOT%{_appdir}/inc
ln -s %{_sysconfdir}/config.inc.php $RPM_BUILD_ROOT%{_appdir}/inc/config.inc.php

%clean
rm -rf $RPM_BUILD_ROOT

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
%doc docs/{ChangeLog,README,README-Sequence,REDHAT-README,TODO}
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
