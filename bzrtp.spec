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
Version:	5.3.97
Release:	1
License:	GPLv2
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/bzrtp/-/archive/%{version}/bzrtp-%{version}.tar.bz2
Patch0:		bzrtp-5.3.6-cmake-install-pkgconfig-pc-file.patch
Patch1:		bzrtp-5.3.6-cmake-config-location.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(BCToolbox)
BuildRequires:	cmake(libxml2)
BuildRequires:	cmake(PostQuantumCryptoEngine)
BuildRequires:	pkgconfig(sqlite3)

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

%prep
%autosetup -p1

%build
%cmake \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/%{name} \
	-DENABLE_PQCRYPTO:BOOL==%{?with_pqcrypto:ON}%{?!with_pqcrypto:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f  %{buildroot}%{_bindir}/%{name}-tester
rm -fr %{buildroot}%{_datadir}/%{name}-tester/
%endif

%check
%if %{with unit_tests}
pushd build
ctest
popd
%endif

