%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	ZRTP keys exchange protocol implementation
Name:		bzrtp
Version:	1.0.6
Release:	2
License:	GPLv2
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://linphone.org/releases/sources/bzrtp/bzrtp-%{version}.tar.gz
Source1:	https://linphone.org/releases/sources/bzrtp/bzrtp-%{version}.tar.gz.md5
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

%description -n	%{develname}
This package contains development files for %{name}

%prep
%setup -q
%apply_patches

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
%doc COPYING AUTHORS NEWS README.md
%{_libdir}/lib%{name}.so.*

%files -n %{develname}
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/cmake/%{name}/

