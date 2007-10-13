%define version	1.3.5
%define pre_version pre7
%define release	%mkrel -c %{pre_version} 1

%define libname %mklibname %{name} 1

Summary:	An input method server for traditional Chinese
Name:		gcin
Version:	%{version}
Release:	%{release}
License:	LGPL
URL: 		http://www.csie.nctu.edu.tw/~cp76/gcin/
Group:		System/Internationalization
Source0:	http://www.csie.nctu.edu.tw/~cp76/gcin/download/%{name}-%{version}.%{pre_version}.tar.bz2
Patch0:		gcin-1.3.5.pre7-desktop-file.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post):	gtk+2.0
Requires(postun): gtk+2.0
BuildRequires:	X11-devel
BuildRequires:	gtk+2-devel
BuildRequires:	qt3-devel >= 3.3.6-16mdk
Requires:	%{libname} = %{version}-%{release}
Suggests:	%{name}-qt3 = %{version}-%{release}
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

%prep
%setup -q -n %{name}-%{version}.%{pre_version}
%patch0 -p0

%build
%configure2_5x
# (tv) this helps building on x86_64:
#make -C im-client
# (tv) disable parallel build (broken):
make

%install
rm -rf %{buildroot}
# fix installing in proper path on x86_64:
%makeinstall_std libdir=%buildroot%_libdir
rm -fr %buildroot%_docdir/
rm -fr %buildroot%_libdir/menu/

# dispatch qt plugins to the right directory
mkdir -p %{buildroot}%{qt3plugins}/inputmethods/
mv -f %{buildroot}%{_libdir}/qt3/plugins/inputmethods/*.so %{buildroot}%{qt3plugins}/inputmethods/
rm -rf %{buildroot}%{_libdir}/qt3/plugins/inputmethods/

# remove unneeded files
rm -rf %{buildroot}/%{_includedir}

%{find_lang} %{name}

%clean
rm -rf %{buildroot}

%post
# install gtk IM module
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib
%update_menus

%postun
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib
%clean_menus

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING Changelog README
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

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/gcin/*
