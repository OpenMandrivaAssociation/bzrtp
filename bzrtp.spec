%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	ZRTP keys exchange protocol implementation
Name:		bzrtp
Version:	4.4.8
Release:	1
License:	GPLv2
Group:		System/Libraries
URL:		https://linphone.org/
# https://gitlab.linphone.org/BC/public/bzrtp
Source0:	https://gitlab.linphone.org/BC/public/bzrtp/-/archive/%{version}/bzrtp-%{version}.tar.bz2
# (wally) install .pc file with cmake
Patch0:		bzrtp-1.0.6-cmake-install-pkgconfig-pc-file.patch
# (wally) alow overriding cmake config file location from cmd line
Patch1:         bzrtp-1.0.6-cmake-config-location.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(bctoolbox)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	bctoolbox-static-devel

%description
bzrtp is a FOSS implementation of ZRTP keys exchange protocol.
The library written in C 89, is fully portable, and can be executed
on many platforms including x86 and ARM processors.

%package -n	%{libname}
Summary:	ZRTP keys exchange protocol implementation
Group:		System/Libraries

%description -n	%{libname}
bzrtp is a FOSS implementation of ZRTP keys exchange protocol.
The library written in C 89, is fully portable, and can be executed
on many platforms including x86 and ARM processors.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	bzrtp-devel = %{version}-%{release}
Requires:	pkgconfig(libxml-2.0)

%description -n	%{develname}
This package contains development files for %{name}

%prep
%autosetup -p1

%build
%cmake \
  -DENABLE_STATIC:BOOL=NO \
  -DENABLE_STRICT:BOOL=NO \
  -DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/%{name}
%make

%install
%make_install -C build

find %{buildroot} -name "*.la" -delete

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

%files -n %{develname}
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_datadir}/cmake/%{name}
