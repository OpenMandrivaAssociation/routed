Summary: The routing daemon which maintains routing tables
Name: routed
Version: 0.17
Release: %mkrel 8
License: BSD
Group: System/Servers
URL: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit
Source: ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-routed-%{version}.tar.bz2
Source1: routed.init
Patch: routed-nonrootbuild.patch
Patch1: routed-BM-fix.patch
#Patch2: routed-gee-man-fork.patch.bz2
Prereq: /sbin/chkconfig
Requires(post,preun):	rpm-helper
Conflicts: gated

%description
The routed routing daemon handles incoming RIP traffic and broadcasts
outgoing RIP traffic about network traffic routes, in order to maintain
current routing tables.  These routing tables are essential for a
networked computer, so that it knows where packets need to be sent.

The routed package should be installed on any networked machine.

%prep
%setup -q -n netkit-%{name}-%{version}
%patch -p1
%patch1 -p1
#%patch2 -p1


%build
%serverbuild

./configure --prefix=%{_prefix}
CC=gcc CFLAGS="$RPM_OPT_FLAGS" make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_initrddir},%{_mandir}/man8,%{_sbindir}}
make INSTALLROOT=$RPM_BUILD_ROOT install
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/routed

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" $RPM_BUILD_ROOT%{_initrddir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %name

%preun
%_preun_service %name

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*
%config(noreplace) %{_initrddir}/routed


