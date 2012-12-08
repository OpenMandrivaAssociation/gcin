%define libname %mklibname %{name} 1

Summary:	An input method server for traditional Chinese
Name:		gcin
Version:	1.6.4
Release:	1
License:	LGPLv2+
Group:		System/Internationalization
URL: 		http://hyperrate.com/dir.php?eid=67
Source0:	http://www.csie.nctu.edu.tw/~cp76/gcin/download/%{name}-%{version}.tar.bz2
Patch1:		gcin-1.6.4-fix-str-fmt.patch
Patch3:		gcin-1.4.4-gcc44.patch
Patch4:		gcin_libdir.patch
Requires(post):	gtk+2.0
Requires(postun): gtk+2.0
BuildRequires:	gtk+2-devel
BuildRequires:	qt4-devel
BuildRequires:	anthy-devel
BuildRequires:	pkgconfig(xtst)
Requires:	%{libname} = %{version}-%{release}
Suggests:	%{name}-qt4 = %{version}-%{release}
Requires:	locales-zh

%description
gcin is a Chinese input method server for traditional Chinese. 
It features a better GTK user interface.

%package -n	%{libname}
Summary:	Gcin library
Group:		System/Internationalization

%description -n %{libname}
gcin is a Chinese input method server for traditional Chinese. 
It features a better GTK user interface.

%package	qt4
Summary:	Qt4 immodule for gcin
Group:		System/Internationalization
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description    qt4
This is the qt4 immodule support for gcin

%prep
%setup -q
%patch1 -p0 -b .str
%patch3 -p1 -b .gcc44
%patch4 -p0 -b .libdir

%build
%define _disable_ld_no_undefined 1
%configure2_5x
# (tv) disable parallel build (broken):
make OPTFLAGS="%{optflags} -fPIC" EXTRA_LDFLAGS="%{?ldflags}" CC="gcc %{?ldflags}" CCLD="gcc %{?ldflags}"

%install
# fix installing in proper path on x86_64:
%makeinstall_std libdir=%{buildroot}%{_libdir}
rm -fr %{buildroot}%{_docdir}/
rm -fr %{buildroot}%{_libdir}/menu/

# remove unneeded files
rm -rf %{buildroot}/%{_includedir}

%post
# install gtk IM module
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%postun
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%files
%doc AUTHORS COPYING Changelog.html README*
%{_bindir}/*
%{_datadir}/applications/gcin-setup.desktop
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/gcin
%{_iconsdir}/*
%{_mandir}/man?/*
%{_libdir}/gtk-2.0/immodules/*.so

%files qt4
%{qt4plugins}/inputmethods/*.so

%files -n %{libname}
%{_libdir}/gcin/*


%changelog
* Tue Oct 25 2011 Andrey Bondrov <abondrov@mandriva.org> 1.6.4-1mdv2012.0
+ Revision: 707116
- New version 1.6.4, use updated patches

* Thu May 05 2011 Funda Wang <fwang@mandriva.org> 1.6.3-1
+ Revision: 668747
- new version 1.6.3

* Wed May 04 2011 Funda Wang <fwang@mandriva.org> 1.6.2-1
+ Revision: 665389
- new version 1.6.2
- new version 1.6.0

* Thu Sep 23 2010 Funda Wang <fwang@mandriva.org> 1.5.6-1mdv2011.0
+ Revision: 580727
- more patch
- New verison 1.5.6

* Sat Jul 17 2010 Funda Wang <fwang@mandriva.org> 1.5.4-1mdv2011.0
+ Revision: 554473
- new version 1.5.4

* Mon May 17 2010 Funda Wang <fwang@mandriva.org> 1.4.9-1mdv2010.1
+ Revision: 544935
- new version 1.4.9

* Wed Feb 03 2010 Funda Wang <fwang@mandriva.org> 1.4.6-3mdv2010.1
+ Revision: 499860
- build with gtk >= 2.19.3

* Mon Jan 11 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-2mdv2010.1
+ Revision: 489706
- rebuilt against libjpeg v8

* Sun Jan 03 2010 Funda Wang <fwang@mandriva.org> 1.4.6-1mdv2010.1
+ Revision: 486048
- new version 1.4.6 final

* Fri Dec 18 2009 Funda Wang <fwang@mandriva.org> 1.4.6-0.pre17.1mdv2010.1
+ Revision: 479878
- New version 1.4.6 pre17

* Thu Sep 24 2009 Olivier Blin <blino@mandriva.org> 1.4.5-3mdv2010.0
+ Revision: 448377
- rediff libdir patch
- fix broken lib64 detection (from Arnaud Patard)

* Sun Aug 16 2009 Funda Wang <fwang@mandriva.org> 1.4.5-2mdv2010.0
+ Revision: 416868
- rebuild for libjpeg7

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Remove old macros

* Wed Jun 03 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.5-1mdv2010.0
+ Revision: 382525
- update to new version 1.4.5

  + Christophe Fergeau <cfergeau@mandriva.com>
    - fix build with gcc 4.4

* Thu Feb 12 2009 Funda Wang <fwang@mandriva.org> 1.4.4-1mdv2009.1
+ Revision: 339644
- add anthy support
- more underlink fix
- New version 1.4.4
- rediff patch0
- new version 1.4.3 pre12

* Sun Sep 28 2008 Funda Wang <fwang@mandriva.org> 1.4.3-0.pre6.1mdv2009.0
+ Revision: 288992
- fix file list
- New version 1.4.3 pre 6

* Thu Aug 21 2008 Funda Wang <fwang@mandriva.org> 1.4.3-0.pre5.1mdv2009.0
+ Revision: 274959
- New version 1.4.3 pre5
- rediff qt dir patch
- enalbe qt4 immodule

* Sat Jun 21 2008 Funda Wang <fwang@mandriva.org> 1.4.2-1mdv2009.0
+ Revision: 227677
- New version 1.4.2
- New version 1.4.1
- adopt to new libqt3 paths

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Funda Wang <fwang@mandriva.org> 1.4.0-0.pre2.1mdv2008.1
+ Revision: 171520
- New version 1.4.0 pre2

* Sun Jan 20 2008 Funda Wang <fwang@mandriva.org> 1.3.8-1mdv2008.1
+ Revision: 155287
- New version 1.3.8

* Sat Dec 29 2007 Funda Wang <fwang@mandriva.org> 1.3.8-0.pre9.1mdv2008.1
+ Revision: 139167
- New version 1.3.8 pre9

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Funda Wang <fwang@mandriva.org> 1.3.8-0.pre4.1mdv2008.1
+ Revision: 120498
- New version pre4

* Sun Dec 09 2007 Funda Wang <fwang@mandriva.org> 1.3.8-0.pre2.1mdv2008.1
+ Revision: 116689
- New version 1.3.8 pre2

* Sat Dec 08 2007 Funda Wang <fwang@mandriva.org> 1.3.8-0.pre1.1mdv2008.1
+ Revision: 116397
- New version 1.3.8 pre1

* Tue Dec 04 2007 Funda Wang <fwang@mandriva.org> 1.3.7.1-1mdv2008.1
+ Revision: 115316
- update to new version 1.3.7.1

* Sat Oct 13 2007 Funda Wang <fwang@mandriva.org> 1.3.5-1mdv2008.1
+ Revision: 97827
- New version 1.3.5

* Sat Oct 13 2007 Funda Wang <fwang@mandriva.org> 1.3.5-0.pre7.1mdv2008.1
+ Revision: 97815
- add missing patch
- New version 1.3.5 pre7

* Sat Aug 04 2007 Funda Wang <fwang@mandriva.org> 1.3.5-0.pre5.1mdv2008.0
+ Revision: 58911
- New version 1.3.5 pre5

* Tue Jul 10 2007 Funda Wang <fwang@mandriva.org> 1.3.5-0.pre4.2mdv2008.0
+ Revision: 51004
- New version

* Wed May 23 2007 Funda Wang <fwang@mandriva.org> 1.3.5-0.pre2.2mdv2008.0
+ Revision: 29996
- Bump release
- kill old menu
  move lib files
- New upstream version

* Sun May 13 2007 Funda Wang <fwang@mandriva.org> 1.3.5-0.pre1.1mdv2008.0
+ Revision: 26503
- New upstream version

* Wed Apr 18 2007 Funda Wang <fwang@mandriva.org> 1.3.4-1mdv2008.0
+ Revision: 14318
- New release 1.3.4.


* Thu Apr 05 2007 Funda Wang <fundawang@mandriva.org> 1.3.4-0.pre5.1mdv2007.1
+ Revision: 150694
- new version.

* Wed Mar 14 2007 Funda Wang <fundawang@mandriva.org> 1.3.4-0.pre4.1mdv2007.1
+ Revision: 143333
- X11-devel instead
- buildrequires x11-devel.
- new releae 1.3.4 pre4
- qt-immodule directory fix
- bunizp2 the patches.
- new release

  + Thierry Vignaud <tvignaud@mandriva.com>
    - Import gcin

* Sat Oct 14 2006 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 1.2.7-1mdv2007.0
- new release

* Fri Aug 18 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.2.2-1mdv2007.0
- switch to XDG
- new release (UTUMI Hirosi <utuhiro78@yahoo.co.jp>)

* Tue May 30 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.2.0-1mdv2007.0
- new release
- drop patches 0 & 1 (no more needed)
- patch 3: fix build on x86_64 (use -fPIC)

* Tue Feb 07 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.1.6-1mdk
- new release
- disable broken parallel build

* Mon Nov 07 2005 Thierry Vignaud <tvignaud@mandriva.com> 1.1.1-1mdk
- new release

* Tue Oct 11 2005 Thierry Vignaud <tvignaud@mandriva.com> 1.0.9-1mdk
- new release
- rediff patches 1 & 2

* Tue Sep 13 2005 Thierry Vignaud <tvignaud@mandriva.com> 1.0.3-3mdk
- rebuild b/c of qt-immodule (#18486)

* Thu Sep 01 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.0.3-2mdk
- 64-bit fixes
- split requires(post,postun)
- fix location of qt plugins (lib64 fixes)

* Sat Aug 20 2005 You-Cheng Hsieh <yochenhsieh@xuite.net> 1.0.3-1mdk
- new release

* Tue Jul 19 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-1mdk
- new release

* Sun Jul 10 2005 Abel Cheung <deaddog@mandriva.org> 1.0.0-1mdk
- New release

* Sat Jul 09 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.5-3mdk
- patch 0: fix build on x86_64
- fix installing on x86_64

* Fri Jul 01 2005 Abel Cheung <deaddog@mandriva.org> 0.9.5-2mdk
- Drop patch, menu should be in english and translated afterwards,
  so regenerate menu inside package instead

* Sat May 14 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.5-1mdk
- new release
- kill patch 1 (merged upstream)

* Tue May 10 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.3-1mdk
- new release (#15828)
- patch 1: fix compiling with gcc-4.0

* Tue Apr 19 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.1-1mdk
- new release

* Sun Mar 06 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.8.6-1mdk
- new release
- disable parallel build since it's broken in 0.8.6
- patch 0: fix upcase in menu entries

* Fri Mar 04 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.8.4-1mdk
- first spec for Mandrakelinux
- based on the spec by Steven Shiau/Chung-Yen Chang. Thanks!

