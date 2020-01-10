Summary: The routing daemon which maintains routing tables
Name: routed
Version: 0.17
Release: 25
License: BSD
Group: System/Servers
URL: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit
Source0: ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-routed-%{version}.tar.bz2
Source1: routed.service
Patch0: routed-nonrootbuild.patch
Patch1: routed-BM-fix.patch
Conflicts: gated

%description
The routed routing daemon handles incoming RIP traffic and broadcasts
outgoing RIP traffic about network traffic routes, in order to maintain
current routing tables.  These routing tables are essential for a
networked computer, so that it knows where packets need to be sent.

The routed package should be installed on any networked machine.

%prep
%setup -q -n netkit-%{name}-%{version}
%autopatch -p1

%build
%setup_compile_flags

sed -i configure -e '/^LDFLAGS=/d'
./configure --prefix=%{_prefix} --with-c-compiler=%{__cc}
%make

%install
mkdir -p %{buildroot}{%{_unitdir},%{_mandir}/man8,%{_sbindir}}
make INSTALLROOT=%{buildroot} install
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

perl -pi -e "s|/etc/rc.d/init.d|%{_unitdir}|" %{buildroot}%{_unitdir}/%{name}.service
sed "s:sysconfig:%{_sysconfdir}/sysconfig:" -i %{buildroot}%{_unitdir}/%{name}.service

mkdir -p %{buildroot}%{_sysconfdir}
cat > %{buildroot}%{_sysconfdir}/routed << EOF
#This is systemd options file for routed
#Config syntax:
#OPTIONS="-q -g"
EOF

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%{_sbindir}/*
%{_mandir}/man8/*
%attr(0644,root,root) %{_unitdir}/%{name}.service
%attr(0644,root,root) %{_sysconfdir}/routed
