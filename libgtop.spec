# Note that this is NOT a relocatable package
%define ver      2.40.0
%define  RELEASE SNAP
%define  rel     %{?CUSTOM_RELEASE} %{!?CUSTOM_RELEASE:%RELEASE}
%define prefix   /usr

Summary: LibGTop library
Name: libgtop
Version: %ver
Release: %rel
License: GPL
Group: X11/Libraries
Source: ftp://ftp.gnome.org/pub/GNOME/sources/libgtop/libgtop-%{ver}.tar.gz
BuildRoot: /tmp/libgtop-root
Packager: Martin Baulig <martin@home-of-linux.org>
URL: http://www.home-of-linux.org/gnome/libgtop/
Prereq: /sbin/install-info
Docdir: %{prefix}/doc

%description

A library that fetches information about the running system such as
cpu and memory usage, active processes etc.

On Linux systems, these information are taken directly from the /proc
filesystem while on other systems a server is used to read those
information from /dev/kmem or whatever. 

%package devel
Summary: Libraries, includes, etc to develop LibGTop applications
Group: X11/libraries
Requires: libgtop

%description devel
Libraries, include files, etc you can use to develop GNOME applications.

%package examples
Summary: Examples for LibGTop
Group: X11/libraries
Requires: libgtop

%description examples
Examples for LibGTop.


%changelog

* Tue Aug 19 1998 Martin Baulig <martin@home-of-linux.org>

- released LibGTop 0.25.0

* Sun Aug 16 1998 Martin Baulig <martin@home-of-linux.org>

- first version of the RPM

%prep
%setup

%build
# Needed for snapshot releases.
if [ ! -f configure ]; then
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=%prefix --without-linux-table --with-libgtop-examples --with-libgtop-smp
else
%ifarch alpha
  CFLAGS="$RPM_OPT_FLAGS" ./configure --host=alpha-redhat-linux --prefix=%prefix --without-linux-table --with-libgtop-inodedb --with-libgtop-examples --with-libgtop-smp
%else
  CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix --without-linux-table --with-libgtop-examples --with-libgtop-smp
%endif
fi

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install

#
# msf - remove these as they are really supposed to come from gnome-libs
#
# martin - don't remove since they are no longer installed if build
#          with GNOME
#
# rm -f $RPM_BUILD_ROOT/%{prefix}/lib/libgnomesupport.a
# rm -f $RPM_BUILD_ROOT/%{prefix}/lib/libgnomesupport.la
# rm -f $RPM_BUILD_ROOT/%{prefix}/lib/libgnomesupport.so.0
# rm -f $RPM_BUILD_ROOT/%{prefix}/lib/libgnomesupport.so.0.0.0

rm -fr $RPM_BUILD_ROOT/%{prefix}/include/libgtop

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%doc RELNOTES-0.25 RELNOTES-1.0 AUTHORS ChangeLog NEWS README
%doc TODO NEWS.old copyright.txt
%doc src/inodedb/README.inodedb

%{prefix}/lib/lib*.so.*
%{prefix}/share/*
%{prefix}/bin/*

%files devel
%defattr(-, root, root)

%{prefix}/lib/lib*.so
%{prefix}/lib/*a
%{prefix}/lib/*.sh
%{prefix}/lib/*.def
%{prefix}/include/*

%files examples
%defattr(-,root,root)

%{prefix}/libexec/libgtop
