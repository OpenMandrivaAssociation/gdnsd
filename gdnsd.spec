%define _disable_ld_no_undefined 1

Name: gdnsd
Version:	3.4.1
Release:	1
Source0: https://github.com/gdnsd/gdnsd/releases/download/v%{version}/%{name}-%{version}.tar.xz
Patch0: gdnsd-3.2.2-compile.patch
Summary: Authoritative-only DNS server with failover support
URL: http://gdnsd.org/
License: GPLv3+
Group: System/Servers
BuildRequires: pkgconfig(libev) >= 4.0
BuildRequires: pkgconfig(liburcu)
BuildRequires: pkgconfig(libsodium)
BuildRequires: cap-devel
BuildRequires: ragel >= 6.0
BuildRequires: rpm-helper
Requires(pre,post): rpm-helper

%description
gdnsd is an Authoritative-only DNS server which does geographic (or other
sorts of) balancing, redirection, weighting, and service-state-conscious
failover at the DNS layer.

gdnsd is written in C using libev and pthreads with a focus on high
performance, low latency service. It does not offer any form of caching or
recursive service, and notably does not support DNSSEC. There's a strong
focus on making the code efficient, lean, and resilient. The code has a
decent regression testsuite with full branch coverage on the core packet
parsing and generation code, and some scripted QA tools for e.g. valgrind
validation, clang-analyzer, etc.

The geographically-aware features also support the emerging EDNS Client
Subnet draft for receiving more-precise network location information
from intermediate shared caches.

%prep
%autosetup -p1
aclocal
automake -a
%configure --with-rundir=/run --with-systemdsystemunitdir=/lib/systemd/system

%build
%make

%install
%makeinstall_std

# Not sure we want a -devel package here...
# Seems fairly pointless if we don't package
# any external plugins
rm -rf %{buildroot}%{_includedir} %{buildroot}%{_mandir}/man3

mkdir -p %{buildroot}%{_sysconfdir}/gdnsd/zones

%files
%{_bindir}/gdnsd_geoip_test
%{_bindir}/gdnsdctl
%{_sbindir}/gdnsd
%{_libexecdir}/gdnsd
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%doc %{_docdir}/gdnsd
/lib/systemd/system/gdnsd.service
%{_sysconfdir}/gdnsd

%pre
%_pre_useradd gdnsd /run/gdnsd /sbin/nologin

%postun
%_postun_userdel gdnsd
