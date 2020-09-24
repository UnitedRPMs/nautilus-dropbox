%global lib /usr/lib
%define glib_version 2.14.0
%define nautilus_version 2.16.0
%define libgnome_version 2.16.0
%define pygtk2_version 2.12
%define pygpgme_version 0.1

%global commit0 52b774e05b7c626f566b8a6d9f6fb66879d2f938
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:		nautilus-dropbox
Version:	2.10.0
Epoch:		1
Release:	3%{?dist}
Summary:	Dropbox integration for Nautilus
Group:		User Interface/Desktops
License:	GPLv3
URL:		https://www.dropbox.com/
Source0:	https://github.com/dropbox/nautilus-dropbox/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:	dropbox.service
Source2:	dropbox@.service
Patch:		python_fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)

BuildRequires:  pkgconfig(python3)
BuildRequires:	nautilus-devel >= %{nautilus_version}
BuildRequires:	glib2-devel >= %{glib_version}
BuildRequires:  cairo-devel
BuildRequires:  gtk2-devel
BuildRequires:  atk-devel
BuildRequires:  pango-devel
BuildRequires:	pygtk2-devel 
BuildRequires:  libtool
BuildRequires:  pygobject2-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:	gnome-common
BuildRequires:  desktop-file-utils
BuildRequires:  python3-docutils
BuildRequires:	python3-gobject
Requires:	nautilus-extensions >= %{nautilus_version}
Requires:	dropbox >= %{version}-%{release}


%description
Nautilus Dropbox is an extension that integrates
the Dropbox web service with your GNOME Desktop.

%package -n dropbox
Summary:        Client for Linux
Group:          User Interface/Desktops
BuildArch:      noarch
Requires:	pygtk2 >= %{pygtk2_version}
Requires:       hicolor-icon-theme
Requires:	glib2 >= %{glib_version}
Recommends:	python3-pygpgme

%description -n dropbox
Dropbox allows you to sync your files online and across
your computers automatically.

%prep
%autosetup -n %{name}-%{commit0} -p1
./autogen.sh

%build

export DISPLAY=$DISPLAY
PYTHON=%{__python3} %configure --disable-static
make %{?_smp_mflags}

%install

%{make_install}

install -Dm644 %{S:1} %{buildroot}/usr/lib/systemd/user/dropbox.service
install -Dm644 %{S:2} %{buildroot}/usr/lib/systemd/system/dropbox@.service

find $RPM_BUILD_ROOT%{_libdir} -type f -name '*.la' -delete -print

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n dropbox
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun -n dropbox
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf \$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{_libdir}/nautilus/extensions-3.0/*.so*

%files -n dropbox
%{_datadir}/icons/hicolor/*
%{_datadir}/nautilus-dropbox/emblems/*
%{_bindir}/dropbox
%{_datadir}/applications/dropbox.desktop
%{_datadir}/man/man1/dropbox.1.gz
%{lib}/systemd/user/dropbox.service
%{lib}/systemd/system/dropbox@.service

%changelog

* Mon Sep 21 2020 David Va <davidva AT tuta DOT io> 2.10.0-3
- Updated to current commit
- Migration to python3

* Fri Nov 16 2018 David Va <davidva AT tuta DOT io> 2.10.0-2
- Updated to current commit

* Wed Sep 26 2018 David Va <davidva AT tuta DOT io> 2.10.0-1
- Updated to 2.10.0

* Thu Jul 26 2018 David Va <davidva AT tuta DOT io> 1.6.2-1
- Updated to 1.6.2
- Epoch solves the bad and old version

* Wed Jan 18 2017 David Vásquez <davidva AT tutanota DOT com> - 2015.10.28-2
- Upstream 

* Tue Mar 29 2016 Dropbox <support@dropbox.com> - 2015.10.28-1
- Initial build
