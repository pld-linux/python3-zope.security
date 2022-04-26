#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	zope.security
Summary:	Zope Security framework
Summary(pl.UTF-8):	Szkielet bezpieczeństwa dla Zope
Name:		python-%{module}
Version:	5.2
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.security/zope.security-%{version}.tar.gz
# Source0-md5:	b1efbaddf1f5e855f5479b7813b5dbb5
URL:		https://www.zope.dev/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-zope.proxy-devel >= 4.3.0
%if %{with tests}
BuildRequires:	python-BTrees
BuildRequires:	python-zope.component
BuildRequires:	python-zope.configuration
BuildRequires:	python-zope.i18nmessageid
BuildRequires:	python-zope.interface
BuildRequires:	python-zope.location
BuildRequires:	python-zope.proxy >= 4.3.0
BuildRequires:	python-zope.schema >= 4.2.0
BuildRequires:	python-zope.testing
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	python3-zope.proxy-devel >= 4.3.0
%if %{with tests}
BuildRequires:	python3-BTrees
BuildRequires:	python3-zope.component
BuildRequires:	python3-zope.configuration
BuildRequires:	python3-zope.i18nmessageid
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.location
BuildRequires:	python3-zope.proxy >= 4.3.0
BuildRequires:	python3-zope.schema >= 4.2.0
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	python3-zope.component
BuildRequires:	python3-zope.i18nmessageid
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.location
BuildRequires:	python3-zope.proxy >= 4.3.0
BuildRequires:	python3-zope.schema >= 4.2.0
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
Obsoletes:	Zope-Proxy < 3.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Security framework provides a generic mechanism to implement
security policies on Python objects.

%description -l pl.UTF-8
Szkielet Zope Security zapewnia ogólny mechanizm do implementowania
polityk bezpieczeństwa obiektów Pythona.

%package -n python3-%{module}
Summary:	Zope Security framework
Summary(pl.UTF-8):	Szkielet bezpieczeństwa dla Zope
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
The Security framework provides a generic mechanism to implement
security policies on Python objects.

%description -n python3-%{module} -l pl.UTF-8
Szkielet Zope Security zapewnia ogólny mechanizm do implementowania
polityk bezpieczeństwa obiektów Pythona.

%package apidocs
Summary:	API documentation for Python zope.security module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.security
Group:		Documentation

%description apidocs
API documentation for Python zope.security module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.security.

%prep
%setup -q -n %{module}-%{version}

# src/zope/proxy/proxy.h is installed as zope.proxy/proxy.h
%{__sed} -i -e 's,zope/proxy/proxy\.h,zope.proxy/proxy.h,' src/zope/security/_proxy.c

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{py_sitedir}/zope/security/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__rm} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*.py[co]

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/zope/security/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/zope/security/tests
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{py3_sitedir}/zope/security/examples $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%{__rm} -r $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/__pycache__

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zope/security/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zope/security/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py_sitedir}/zope/security
%{py_sitedir}/zope/security/*.py[co]
%{py_sitedir}/zope/security/*.zcml
%attr(755,root,root) %{py_sitedir}/zope/security/_proxy.so
%attr(755,root,root) %{py_sitedir}/zope/security/_zope_security_checker.so
%{py_sitedir}/zope.security-%{version}-py*.egg-info
%{py_sitedir}/zope.security-%{version}-py*-nspkg.pth
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py3_sitedir}/zope/security
%{py3_sitedir}/zope/security/*.py
%{py3_sitedir}/zope/security/*.zcml
%{py3_sitedir}/zope/security/__pycache__
%attr(755,root,root) %{py3_sitedir}/zope/security/_proxy.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/zope/security/_zope_security_checker.cpython-*.so
%{py3_sitedir}/zope.security-%{version}-py*.egg-info
%{py3_sitedir}/zope.security-%{version}-py*-nspkg.pth
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,*.html,*.js}
%endif
