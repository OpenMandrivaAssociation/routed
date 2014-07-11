Summary:	The routing daemon which maintains routing tables
Name:		routed
Version:	0.17
Release:	21
License:	BSD
Group:		System/Servers
Url:		ftp://ftp.uk.linux.org/pub/linux/Networking/netkit
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-routed-%{version}.tar.bz2
Source1:	routed.init
Patch0:		routed-nonrootbuild.patch
Patch1:		routed-BM-fix.patch
Requires(post,preun):	chkconfig
Requires(post,preun):	rpm-helper
Conflicts:	gated

%description
The routed routing daemon handles incoming RIP traffic and broadcasts
outgoing RIP traffic about network traffic routes, in order to maintain
current routing tables.  These routing tables are essential for a
networked computer, so that it knows where packets need to be sent.

The routed package should be installed on any networked machine.

%prep
%setup -qn netkit-%{name}-%{version}
%apply_patches

%build
%serverbuild
./configure \
	--prefix=%{_prefix}
CC=gcc CFLAGS="$RPM_OPT_FLAGS" make

%install
mkdir -p %{buildroot}/{%{_initrddir},%{_mandir}/man8,%{_sbindir}}
make INSTALLROOT=%{buildroot} install
install -m 755 %{SOURCE1} %{buildroot}/%{_initrddir}/routed

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" %{buildroot}%{_initrddir}/*

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%{_sbindir}/*
%{_mandir}/man8/*
%config(noreplace) %{_initrddir}/routed

