%define _disable_ld_no_undefined 1

Summary:	Authoritative-only DNS server with failover support
Name:		gdnsd
Version:	3.8.0
Release:	3
License:	GPLv3+
Group:		System/Servers
URL:		http://gdnsd.org/
Source0:	https://github.com/gdnsd/gdnsd/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:	%{name}.sysusers
Patch0:		gdnsd-3.2.2-compile.patch

BuildRequires:	pkgconfig(libev) >= 4.0
BuildRequires:	pkgconfig(liburcu)
BuildRequires:	pkgconfig(libsodium)
BuildRequires:	cap-devel
BuildRequires:	ragel >= 6.0
BuildRequires:	systemd-rpm-macros
Requires(pre):	systemd
%systemd_requires

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

%build
%configure \
	--with-rundir=%{_rundir} \
	--with-systemdsystemunitdir=%{_unitdir}

%make_build

%install
%make_install

install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

# Not sure we want a -devel package here...
# Seems fairly pointless if we don't package
# any external plugins
rm -rf %{buildroot}%{_includedir} %{buildroot}%{_mandir}/man3

mkdir -p %{buildroot}%{_sysconfdir}/gdnsd/zones

%pre
%sysusers_create_package %{name} %{SOURCE6}

%files
%{_sysusersdir}/%{name}.conf
%{_bindir}/gdnsd_geoip_test
%{_bindir}/gdnsdctl
%{_sbindir}/gdnsd
%{_libexecdir}/gdnsd
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%doc %{_mandir}/man8/*
%doc %{_docdir}/gdnsd
%{_unitdir}/gdnsd.service
%{_sysconfdir}/gdnsd
