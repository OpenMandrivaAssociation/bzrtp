%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	ZRTP keys exchange protocol implementation
Name:		bzrtp
Version:	5.0.53
Release:	1
License:	GPLv2
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/bzrtp/-/archive/%{version}/bzrtp-%{version}.tar.bz2
# (wally) install .pc file with cmake
Patch0:		bzrtp-5.0.18-cmake-install-pkgconfig-pc-file.patch
# (wally) alow overriding cmake config file location from cmd line
Patch1:		bzrtp-5.0.18-cmake-config-location.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(bctoolbox)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	bctoolbox-static-devel

%description
bzrtp is a FOSS implementation of ZRTP keys exchange protocol.
The library written in C 89, is fully portable, and can be executed
on many platforms including x86 and ARM processors.

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	ZRTP keys exchange protocol implementation
Group:		System/Libraries

%description -n	%{libname}
bzrtp is a FOSS implementation of ZRTP keys exchange protocol.
The library written in C 89, is fully portable, and can be executed
on many platforms including x86 and ARM processors.

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

#---------------------------------------------------------------------------

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	bzrtp-devel = %{version}-%{release}
Requires:	pkgconfig(libxml-2.0)

%description -n	%{develname}
This package contains development files for %{name}

%files -n %{develname}
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_datadir}/cmake/%{name}

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-DENABLE_STATIC:BOOL=NO \
	-DENABLE_STRICT:BOOL=ON \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/%{name} \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

find %{buildroot} -name "*.la" -delete

