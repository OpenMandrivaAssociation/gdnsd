Name: gdnsd
Version: 1.10.1
Release: 1
Source0: http://downloads.gdnsd.org/%{name}-%{version}.tar.xz
Source1: gdnsd.service
Summary: Authoritative-only DNS server with failover support
URL: http://gdnsd.org/
License: GPLv3+
Group: System/Servers
BuildRequires: pkgconfig(libev) >= 4.0
BuildRequires: pkgconfig(liburcu)
BuildRequires: cap-devel
BuildRequires: ragel >= 6.0

%track
prog %{name} = {
	url = http://downloads.gdnsd.org/
	regex = %{name}-(__VER__)\.tar\.xz
	version = %{version}
}

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
%setup -q
%configure --with-rundir=/run

%build
%make

%install
%makeinstall_std

mkdir -p %{buildroot}/lib/systemd/system/
install -c -m 644 %{SOURCE1} %{buildroot}/lib/systemd/system/

# Not sure we want a -devel package here...
# Seems fairly pointless if we don't package
# any external plugins
rm -rf %{buildroot}%{_includedir} %{buildroot}%{_mandir}/man3

mkdir -p %{buildroot}%{_sysconfdir}/gdnsd/zones

%files
%{_bindir}/gdnsd_geoip_test
%{_sbindir}/gdnsd
%{_libdir}/gdnsd
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
