# TODO:
# - drpm support?
#
# Conditional build:
%bcond_with	rpm5	# build with rpm5, tests may fail (rpm.org vs rpm5 compat problems?)
%bcond_without	tests	# make tests

Summary:	Creates a common metadata repository
Summary(pl.UTF-8):	Tworzenie wspólnego repozytorium metadanych
Name:		createrepo_c
Version:	1.0.4
Release:	1
License:	GPL v2+
Group:		Applications/System
#Source0Download: https://github.com/rpm-software-management/createrepo_c/releases
Source0:	https://github.com/rpm-software-management/createrepo_c/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	92d4de835d0acb0cc8071dff78500ad3
Patch0:		%{name}-rpm5.patch
URL:		https://github.com/rpm-software-management/createrepo_c
BuildRequires:	bash-completion-devel >= 1:2.0
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	curl-devel
BuildRequires:	doxygen
#BuildRequires:	drpm-devel
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	libmodulemd-devel
BuildRequires:	libxml2-devel >= 2
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%{?with_tests:BuildRequires:	python-nose}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules
%{?with_tests:BuildRequires:	python3-nose}
BuildRequires:	python3-setuptools
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	sphinx-pdg
BuildRequires:	sqlite3-devel >= 3.6.18
BuildRequires:	xz-devel
BuildRequires:	zchunk-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
%{?with_tests:BuildRequires:	zchunk}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C implementation of Createrepo. This utility will generate a common
metadata repository from a directory of RPM packages.

%description -l pl.UTF-8
Implementacja w C programu Createrepo. To narzędzie generuje wspólne
repozytorium metadanych z katalogu pakietów RPM.

%package libs
Summary:	Library for repodata manipulation
Summary(pl.UTF-8):	Biblioteka do operacji na danych repozytorium
Group:		Libraries
Requires:	glib2 >= 1:2.22.0
Requires:	sqlite3-libs >= 3.6.18

%description libs
This package contains the createrepo_c library for applications to
easy manipulate with a repodata.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę createrepo_c, pozwalającą aplikacjom na
łatwe operowanie na danych repozytorium (repodata).

%package devel
Summary:	Header files for createrepo_c library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki createrepo_c
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bzip2-devel
Requires:	curl-devel
Requires:	expat-devel
Requires:	glib2-devel >= 1:2.22.0
Requires:	libxml2-devel >= 2
Requires:	rpm-devel
Requires:	sqlite3-devel >= 3.6.18
Requires:	xz-devel
Requires:	zlib-devel
Requires:	zstd-devel

%description devel
This package contains the createrepo_c C header files. These
development files are for easy manipulation with a repodata.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe C biblioteki createrepo_c. Mają na
celu łatwe operowanie na danych repozytorium (repodata).

%package apidocs
Summary:	API documentation for createrepo_c library
Summary(pl.UTF-8):	Dokumentacja API biblioteki createrepo_c
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for createrepo_c library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki createrepo_c.

%package -n python3-createrepo_c
Summary:	Python 3 bindings for the createrepo_c library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki createrepo_c
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	python-createrepo_c < 0.17.6

%description -n python3-createrepo_c
Python 3 bindings for the createrepo_c library.

%description -n python3-createrepo_c -l pl.UTF-8
Wiązania Pythona 3 do biblioteki createrepo_c.

%package -n bash-completion-createrepo_c
Summary:	Bash completion for createrepo_c commands
Summary(pl.UTF-8):	Bashowe uzupełnianie dla poleceń createrepo_c
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-createrepo_c
Bash completion for createrepo_c commands (createrepo_c, mergerepo_c,
modifyrepo_c).

%description -n bash-completion-createrepo_c -l pl.UTF-8
Bashowe uzupełnianie dla poleceń createrepo_c (createrepo_c,
mergerepo_c, modifyrepo_c).

%prep
%setup -q
%{?with_rpm5:%patch0 -p1}

%build
install -d build
cd build
%cmake .. \
	-DBASHCOMP_DIR=%{bash_compdir} \
	-DPYTHON_DESIRED=3

%{__make}
%{__make} doc

%if %{with tests}
%{__make} tests
%{__make} test \
	ARGS="-V"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/createrepo_c
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/createrepo_c

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/createrepo_c
%attr(755,root,root) %{_bindir}/mergerepo_c
%attr(755,root,root) %{_bindir}/modifyrepo_c
%attr(755,root,root) %{_bindir}/sqliterepo_c
%{_mandir}/man8/createrepo_c.8*
%{_mandir}/man8/mergerepo_c.8*
%{_mandir}/man8/modifyrepo_c.8*
%{_mandir}/man8/sqliterepo_c.8*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_libdir}/libcreaterepo_c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcreaterepo_c.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcreaterepo_c.so
%{_pkgconfigdir}/createrepo_c.pc
%{_includedir}/createrepo_c

%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html

%files -n python3-createrepo_c
%defattr(644,root,root,755)
%dir %{py3_sitedir}/createrepo_c
%attr(755,root,root) %{py3_sitedir}/createrepo_c/_createrepo_c.so
%{py3_sitedir}/createrepo_c/__init__.py
%{py3_sitedir}/createrepo_c/__pycache__
%{py3_sitedir}/createrepo_c-%{version}-py*.egg-info

%files -n bash-completion-createrepo_c
%defattr(644,root,root,755)
%{bash_compdir}/createrepo_c
%{bash_compdir}/mergerepo_c
%{bash_compdir}/modifyrepo_c
%{bash_compdir}/sqliterepo_c
