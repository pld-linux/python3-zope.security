#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define module	zope.security
Summary:	Zope Security framework
Summary(pl.UTF-8):	Szkielet bezpieczeństwa dla Zope
Name:		python3-%{module}
Version:	7.3
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/zope-security/
Source0:	https://files.pythonhosted.org/packages/source/z/zope.security/zope_security-%{version}.tar.gz
# Source0-md5:	4e25ce70785860aa320d5c8523cdc800
URL:		https://www.zope.dev/
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools
BuildRequires:	python3-zope.proxy-devel >= 5.2
%if %{with tests}
BuildRequires:	python3-BTrees
BuildRequires:	python3-zope.component
BuildRequires:	python3-zope.configuration
BuildRequires:	python3-zope.i18nmessageid
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.location
BuildRequires:	python3-zope.proxy >= 5.2
BuildRequires:	python3-zope.schema >= 4.2.0
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-zope.component
BuildRequires:	python3-zope.i18nmessageid
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.location
BuildRequires:	python3-zope.proxy >= 5.2
BuildRequires:	python3-zope.schema >= 4.2.0
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Security framework provides a generic mechanism to implement
security policies on Python objects.

%description -l pl.UTF-8
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
%setup -q -n zope_security-%{version}

# src/zope/proxy/proxy.h is installed as zope.proxy/proxy.h
%{__sed} -i -e 's,zope/proxy/proxy\.h,zope.proxy/proxy.h,' src/zope/security/_proxy.c

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%py3_install

%{__mv} $RPM_BUILD_ROOT%{py3_sitedir}/zope/security/examples $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%{__rm} -r $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/__pycache__

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zope/security/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zope/security/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
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

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,*.html,*.js}
%endif
