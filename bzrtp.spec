%define major 0
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$

%bcond pqcrypto			1
%bcond strict			1
%bcond unit_tests		1
%bcond unit_tests_install	0

Summary:	ZRTP keys exchange protocol implementation
Name:		bzrtp
Version:	5.4.50
Release:	1
License:	GPLv2
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/bzrtp/-/archive/%{version}/bzrtp-%{version}.tar.bz2
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(BCToolbox)
BuildRequires:	cmake(libxml2)
BuildRequires:	cmake(PostQuantumCryptoEngine)
BuildRequires:	pkgconfig(sqlite3)

BuildSystem:	cmake
BuildOption:	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF}
BuildOption:	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/%{name}
BuildOption:	-DENABLE_PQCRYPTO:BOOL==%{?with_pqcrypto:ON}%{?!with_pqcrypto:OFF}
BuildOption:	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF}

%patchlist
bzrtp-5.3.6-cmake-install-pkgconfig-pc-file.patch
bzrtp-5.3.6-cmake-config-location.patch
%if ! %{with unit_tests_install}
bzrtp-5.4.50-dont-install-tester.patch
%endif

%description
bzrtp is a FOSS implementation of ZRTP keys exchange protocol.
The library written in C 89, is fully portable, and can be executed
on many platforms including x86 and ARM processors.

%if %{with unit_tests} && %{with unit_tests_install}
%files
%{_bindir}/%{name}-tester
%{_datadir}/%{name}-tester/
%endif

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

%package -n	%{devname}
Summary:	Development files for %{name}rem
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	bzrtp-devel = %{version}-%{release}
Requires:	pkgconfig(libxml-2.0)

%description -n	%{devname}
This package contains development files for %{name}

%files -n %{devname}
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_datadir}/cmake/BZRTP

#---------------------------------------------------------------------------

