%define major	1
%define libname %mklibname %{name}-im-client %{major}
%define devname %mklibname %{name}-im-client -d

Summary:	An input method server for traditional Chinese
Name:		gcin
Version:	2.8.1
Release:	1
License:	LGPLv2+
Group:		System/Internationalization
Url: 		http://hyperrate.com/dir.php?eid=67
Source0:	http://www.csie.nctu.edu.tw/~cp76/gcin/download/%{name}-%{version}.tar.xz
Patch3:		gcin-1.4.4-gcc44.patch

BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(anthy)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(xtst)
Requires:	locales-zh
Suggests:	%{name}-gtk2 = %{version}-%{release}
Suggests:	%{name}-gtk3 = %{version}-%{release}
Suggests:	%{name}-qt4 = %{version}-%{release}
Conflicts:	%{_lib}gcin1 < 2.8.0-1

%description
gcin is a Chinese input method server for traditional Chinese. 
It features a better GTK user interface.

%package -n	%{libname}
Summary:	Gcin library
Group:		System/Internationalization
Obsoletes:	%{_lib}gcin1 < 2.8.0-1

%description -n %{libname}
gcin is a Chinese input method server for traditional Chinese. 
It features a better GTK user interface.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package	gtk2
Summary:	Gtk2 immodule for gcin
Group:		System/Internationalization
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):	gtk+2.0
Conflicts:	%{name} < 2.8.0-1

%description    gtk2
This is the gtk2 immodule support for gcin.

%package	gtk3
Summary:	Gtk3 immodule for gcin
Group:		System/Internationalization
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):	gtk+3.0
Conflicts:	%{name} < 2.8.0-1

%description    gtk3
This is the gtk3 immodule support for gcin.

%package	qt4
Summary:	Qt4 immodule for gcin
Group:		System/Internationalization
Requires:	%{name} = %{version}-%{release}

%description    qt4
This is the qt4 immodule support for gcin.

%prep
%setup -q
%apply_patches

chmod 644 AUTHORS COPYING Changelog.html README*

%build
%configure2_5x

%make

%install
%makeinstall_std 
rm -fr %{buildroot}%{_docdir}/

# install gtk IM module
%post gtk2
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%post gtk3
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-3.0/gtk.immodules.%{_lib}

%postun gtk2
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%postun gtk3
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-3.0/gtk.immodules.%{_lib}

%files
%doc AUTHORS COPYING Changelog.html README*
%{_bindir}/*
%{_datadir}/applications/gcin-tools.desktop
%{_datadir}/gcin
%{_iconsdir}/*
%{_libdir}/gcin/anthy-module.so
%{_libdir}/gcin/gcin1.so
%{_libdir}/gcin/gcin2.so
%{_libdir}/gcin/intcode-module.so

%files gtk2
%{_libdir}/gtk-2.0/immodules/*.so

%files gtk3
%{_libdir}/gtk-3.0/immodules/*.so

%files qt4
%{qt4plugins}/inputmethods/*.so

%files -n %{libname}
%{_libdir}/gcin/libgcin-im-client.so.%{major}*

%files -n %{devname}
%{_libdir}/gcin/libgcin-im-client.so

