# TODO: tests fail (rpm.org vs rpm5 compat problems?)
#
# Conditional build:
%bcond_with	tests	# make tests

%define		gitrev	7ef96a6
Summary:	Creates a common metadata repository
Summary(pl.UTF-8):	Tworzenie wspólnego repozytorium metadanych
Name:		createrepo_c
Version:	0.4.0
Release:	1
License:	GPL v2+
Group:		Applications/System
# git clone https://github.com/Tojaj/createrepo_c
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/createrepo_c/%{name}-%{gitrev}.tar.xz/606d117677ab85e5a9ec15896db644c2/createrepo_c-%{gitrev}.tar.xz
# Source0-md5:	606d117677ab85e5a9ec15896db644c2
Patch0:		%{name}-rpm5.patch
Patch1:		%{name}-python.patch
URL:		https://github.com/Tojaj/createrepo_c
BuildRequires:	bzip2-devel
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	libmagic-devel
BuildRequires:	libxml2-devel >= 2
BuildRequires:	openssl-devel
BuildRequires:	python-devel >= 2
%{?with_tests:BuildRequires:	python-nose}
BuildRequires:	rpm-devel >= 5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sphinx-pdg-2
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
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
Requires:	libmagic-devel
Requires:	libxml2-devel >= 2
Requires:	rpm-devel >= 5
Requires:	sqlite3-devel >= 3
Requires:	xz-devel
Requires:	zlib-devel

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

%description apidocs
API documentation for createrepo_c library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki createrepo_c.

%package -n python-createrepo_c
Summary:	Python bindings for the createrepo_c library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki createrepo_c
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-createrepo_c
Python bindings for the createrepo_c library.

%description -n python-createrepo_c -l pl.UTF-8
Wiązania Pythona do biblioteki createrepo_c.

%package -n bash-completion-createrepo_c
Summary:	Bash completion for createrepo_c commands
Summary(pl.UTF-8):	Bashowe uzupełnianie dla poleceń createrepo_c
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-createrepo_c
Bash completion for createrepo_c commands (createrepo_c, mergerepo_c,
modifyrepo_c).

%description -n bash-completion-createrepo_c -l pl.UTF-8
Bashowe uzupełnianie dla poleceń createrepo_c (createrepo_c,
mergerepo_c, modifyrepo_c).

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%cmake .

%{__make}
%{__make} doc

%if %{with tests}
%{__make} tests
%{__make} test \
	ARGS="-V"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}/createrepo_c
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/createrepo_c
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/createrepo_c
%attr(755,root,root) %{_bindir}/mergerepo_c
%attr(755,root,root) %{_bindir}/modifyrepo_c
%{_mandir}/man8/createrepo_c.8*
%{_mandir}/man8/mergerepo_c.8*
%{_mandir}/man8/modifyrepo_c.8*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_libdir}/libcreaterepo_c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcreaterepo_c.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcreaterepo_c.so
%{_pkgconfigdir}/createrepo_c.pc
%{_includedir}/createrepo_c

%files apidocs
%defattr(644,root,root,755)
%doc doc/html

%files -n python-createrepo_c
%defattr(644,root,root,755)
%dir %{py_sitedir}/createrepo_c
%attr(755,root,root) %{py_sitedir}/createrepo_c/_createrepo_cmodule.so
%{py_sitedir}/createrepo_c/__init__.py[co]

%files -n bash-completion-createrepo_c
%defattr(644,root,root,755)
/etc/bash_completion.d/createrepo_c.bash