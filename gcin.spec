%define version	1.4.5
%define betaver 0
%define rel 2

%if %betaver
%define release %mkrel -c %betaver %rel
%define tarballver %version.%betaver
%else
%define release %mkrel %rel
%define tarballver %version
%endif

%define libname %mklibname %{name} 1

Summary:	An input method server for traditional Chinese
Name:		gcin
Version:	%{version}
Release:	%{release}
License:	LGPLv2+
URL: 		http://www.csie.nctu.edu.tw/~cp76/gcin/
Group:		System/Internationalization
Source0:	http://www.csie.nctu.edu.tw/~cp76/gcin/download/%{name}-%{tarballver}.tar.bz2
Patch0:		gcin-1.4.4-build-qt.patch
Patch1:		gcin-1.4.4-fix-str-fmt.patch
Patch2:		gcin-1.4.4-linkage.patch
Patch3:		gcin-1.4.4-gcc44.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post):	gtk+2.0
Requires(postun): gtk+2.0
BuildRequires:	gtk+2-devel
BuildRequires:	qt3-devel >= 3.3.6-16mdk
BuildRequires:	qt4-devel
BuildRequires:	anthy-devel
Requires:	%{libname} = %{version}-%{release}
Suggests:	%{name}-qt4 = %{version}-%{release}
Requires:	locales-zh
# ease upgrade
Conflicts:	%{libname} < 1.3.5-0.pre7

%description
gcin is a Chinese input method server for traditional Chinese. 
It features a better GTK user interface.


%package -n	%{libname}
Summary:	Gcin library
Group:		System/Internationalization
Conflicts:	%{name} < 1.3.5-0.pre7
Obsoletes:	%mklibname %{name} 0

%description -n %{libname}
gcin is a Chinese input method server for traditional Chinese. 
It features a better GTK user interface.

%package	qt3
Summary:	Qt3 immodule for gcin
Group:		System/Internationalization
Conflicts:	%name < 1.3.5-0.pre7
Requires:	%libname = %{version}-%{release}
Requires:	%name = %{version}-%{release}

%description	qt3
This is the qt3 immodule support for gcin

%package        qt4
Summary:        Qt4 immodule for gcin
Group:          System/Internationalization
Requires:       %libname = %{version}-%{release}
Requires:       %name = %{version}-%{release}

%description    qt4
This is the qt4 immodule support for gcin

%prep
%setup -q -n %{name}-%{tarballver}
%patch0 -p1 -b .qt
%patch1 -p0 -b .str
%patch2 -p0 -b .linkage
%patch3 -p1 -b .gcc44

%build
%define _disable_ld_no_undefined 1
%configure2_5x
# (tv) disable parallel build (broken):
make OPTFLAGS="%{optflags} -fPIC" EXTRA_LDFLAGS="%{?ldflags}"

%install
rm -rf %{buildroot}
# fix installing in proper path on x86_64:
%makeinstall_std libdir=%buildroot%_libdir
rm -fr %buildroot%_docdir/
rm -fr %buildroot%_libdir/menu/

# remove unneeded files
rm -rf %{buildroot}/%{_includedir}

%{find_lang} %{name}

%clean
rm -rf %{buildroot}

%post
# install gtk IM module
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING Changelog.html README*
%{_bindir}/*
%{_datadir}/applications/gcin-setup.desktop
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/gcin
%{_iconsdir}/*
%{_mandir}/man?/*
%{_libdir}/gtk-2.0/immodules/*.so

%files qt3
%defattr(-,root,root)
%{qt3plugins}/inputmethods/*.so

%files qt4
%defattr(-,root,root)
%{qt4plugins}/inputmethods/*.so

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/gcin/*
