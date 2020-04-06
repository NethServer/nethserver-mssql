Summary: NethServer MSSQL
Name: nethserver-mssql
Version: 1.0.2
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-cockpit.tar.gz
BuildArch: noarch
URL: %{url_prefix}/%{name} 

Requires: nethserver-base

BuildRequires: nethserver-devtools

%description
MSSQL integration for NethServer

%prep
%setup

%build
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} %{buildroot} > %{name}-%{version}-%{release}-filelist

%clean
rm -rf %{buildroot}

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%attr(0440,root,root) /etc/sudoers.d/50_nsapi_nethserver_mssql


%changelog
* Mon Apr 6 2020 Federico Ballarini <fed.ballarini@gmail.com> - 1.0.2-1
- MSSQL: show databases list in Cockpit - NethServer/dev#6106

* Wed Mar 4 2020 Federico Ballarini <fed.ballarini@gmail.com> - 1.0.1-1
- MSSQL integration for NethServer - NethServer/dev#6078

* Fri Feb 28 2020 Federico Ballarini <fed.ballarini@gmail.com> - 1.0.0-1
- Initial package
