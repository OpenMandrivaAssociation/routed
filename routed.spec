Summary: The routing daemon which maintains routing tables
Name: routed
Version: 0.17
Release: %mkrel 15
License: BSD
Group: System/Servers
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit
Source: ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-routed-%{version}.tar.bz2
Source1: routed.init
Patch: routed-nonrootbuild.patch
Patch1: routed-BM-fix.patch
#Patch2: routed-gee-man-fork.patch.bz2
Requires(post,preun): chkconfig
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




%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.17-13mdv2011.0
+ Revision: 669431
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-12mdv2011.0
+ Revision: 607371
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-11mdv2010.1
+ Revision: 520210
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.17-10mdv2010.0
+ Revision: 426958
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.17-9mdv2009.0
+ Revision: 225325
- rebuild
- fix no-buildroot-tag

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 0.17-8mdv2008.1
+ Revision: 131813
- fix prereq & file require
- fix prereq on rpm-helper
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

* Thu Jun 28 2007 Andreas Hasenack <andreas@mandriva.com> 0.17-8mdv2008.0
+ Revision: 45573
- rebuild with new serverbuild macro (-fstack-protector-all)


* Sun Jan 28 2007 Olivier Thauvin <nanardon@mandriva.org> 0.17-7mdv2007.0
+ Revision: 114740
- mkrel

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.17-6mdk
- Rebuild

