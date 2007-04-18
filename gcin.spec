%define version	1.3.4
#%define pre_version pre5
#%define release	%mkrel -c %{pre_version} 1
%define release %mkrel 1

%define libname_orig lib%{name}
%define libname %mklibname %{name} 1

Summary:	An input method server for traditional Chinese
Name:		gcin
Version:	%{version}
Release:	%{release}
License:	LGPL
URL: 		http://www.csie.nctu.edu.tw/~cp76/gcin/
Group:		System/Internationalization
Source0:	http://www.csie.nctu.edu.tw/~cp76/gcin/download/%{name}-%{version}.tar.bz2
# There is no need keep source{1,2,3}, because we manage IMEs through different way than Fedora
#Source1:	xcin2gcin
#Source2:	gcin.sh
#Source3:	set-gcin-sys-xim
#Patch2:		gcin-1.0.9-64bit-fixes.patch
#Patch3:		gcin-1.2.0-fix-x86_64-build.patch
#Patch4:		gcin-1.3.4-fix-gcinlibdir.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post):	gtk+2.0
Requires(postun): gtk+2.0
BuildRequires:	X11-devel
BuildRequires:	gtk+2-devel
BuildRequires:	qt3-devel >= 3.3.6-16mdk
Requires:	%{libname} = %{version}
Requires:	locales-zh
# ease upgrade
Conflicts:	%{libname} < 0.9.5-2mdk

%description
gcin is a Chinese input method server for traditional Chinese. 
It features a better GTK user interface.


%package -n	%{libname}
Summary:	Gcin library
Group:		System/Internationalization
Provides:	%{libname_orig} = %{version}-%{release}
Conflicts:	%{name} < 0.9.5-2mdk
Obsoletes:	%mklibname %{name} 0

%description -n %{libname}
gcin is a Chinese input method server for traditional Chinese. 
It features a better GTK user interface.

%prep
%setup -q -n %{name}-%{version}
#%patch2 -p1 -b .64bit-fixes
#%patch3 -p1 -b .fpic
#%patch4 -p0 -b .configure-fix

%build
%configure2_5x
# (tv) this helps building on x86_64:
make -C im-client
# (tv) disable parallel build (broken):
make

%install
rm -rf %{buildroot}
# fix installing in proper path on x86_64:
%makeinstall_std libdir=%buildroot%_libdir
rm -fr %buildroot%_libdir/menu
rm -fr %buildroot%_docdir/

# remove menu from package
rm -f %{buildroot}%{_menudir}/*

# There is no need keep source{1,2,3}, because we manage IMEs through different way than Fedora
#install -m 755 %SOURCE1 %{buildroot}/%{_bindir}/
#install -m 755 %SOURCE2 %{buildroot}/%{_bindir}/
#install -m 755 %SOURCE3 %{buildroot}/%{_bindir}/
#ln -s xcin2gcin %{buildroot}/%{_bindir}/gcin2xcin

# menu
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << _EOF_
?package(%{name}): \
 icon="gcin.png" \
 title="GCIN setup" \
 longtitle="GCIN setup" \
 needs="x11" \
 section="System/Configuration/Other" \
 command="%{_bindir}/gcin-setup"\
 xdg="true"
_EOF_

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="Settings" \
  --add-category="X-MandrivaLinux-System-Configuration-Other"\
  --remove-category=Applications \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

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
%{_libdir}/gtk-2.0/immodules/*.so
%{qt3plugins}/inputmethods/*
%{_mandir}/man?/*
%{_menudir}/*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/gcin/*
