#
# Conditional build:
%bcond_without	python2	# CPython 2.x modules
%bcond_with	python3	# CPython 3.x modules (now built with sip6 from python3-PyQtWebEngine.spec)

%define		module	PyQtWebEngine
# minimal required sip version
%define		sip_ver	2:4.19.14-1
# last qt version covered by these bindings (minimal required is currently 5.4.0)
# see sip/QtWebEngineCore/QtWebEngineCoremod.sip /%Timeline
%define		qt_ver	5.15.0

%define		_enable_debug_packages	0

Summary:	Python 2 bindings for the Qt5WebEngine module
Summary(pl.UTF-8):	Wiązania Pythona 2 do modułu Qt5WebEngine
Name:		python-%{module}
# keep < 5.15.7 here for python2/sip4 support
Version:	5.15.6
Release:	1
License:	GPL v3
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyqtwebengine/
Source0:	https://files.pythonhosted.org/packages/source/P/PyQtWebEngine/PyQtWebEngine-%{version}.tar.gz
# Source0-md5:	d1e548617de149ba8142a32c1eb9f994
Patch0:		install.patch
URL:		https://www.riverbankcomputing.com/software/pyqtwebengine/
BuildRequires:	Qt5WebEngine-devel >= %{qt_ver}
BuildRequires:	pkgconfig
%if %{with python2}
BuildRequires:	python-PyQt5 >= 5.15
BuildRequires:	python-PyQt5-sip >= %{sip_ver}
BuildRequires:	python-sip-devel >= %{sip_ver}
%endif
%if %{with python3}
BuildRequires:	python3-PyQt5 >= 5.15
BuildRequires:	python3-PyQt5-sip >= %{sip_ver}
BuildRequires:	python3-sip-devel >= %{sip_ver}
%endif
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	qt5-qmake >= %{qt_ver}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sip-PyQt5 >= 5.15
Requires:	python-libs
Requires:	python-PyQt5-sip >= %{sip_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sipfilesdir	%{_datadir}/sip

%description
Python 2 bindings for the Qt5WebEngine module.

%description -l pl.UTF-8
Wiązania Pythona 2 do modułu Qt5WebEngine.

%package -n python3-PyQtWebEngine
Summary:	Python 3 bindings for the Qt5WebEngine module
Summary(pl.UTF-8):	Wiązania Pythona 2 do modułu Qt5WebEngine
Group:		Libraries/Python
Requires:	python3-libs
Requires:	python3-PyQt5-sip >= %{sip_ver}

%description -n python3-PyQtWebEngine
Python 3 bindings for the Qt5WebEngine module.

%description -n python3-PyQtWebEngine -l pl.UTF-8
Wiązania Pythona 2 do modułu Qt5WebEngine.

%package -n sip-PyQtWebEngine
Summary:        SIP files needed to build bindings for Qt5WebEngine
Summary(pl.UTF-8):      Pliki SIP potrzebne do budowania wiązań do Qt5WebEngine
Group:          Development/Languages/Python
Requires:       sip >= %{sip_ver}
Requires:       sip-PyQt5 >= 5.15

%description -n sip-PyQtWebEngine
SIP files needed to build bindings for Qt5WebEngine.

%description -n sip-PyQtWebEngine -l pl.UTF-8
Pliki SIP potrzebne do budowania wiązań do Qt5WebEngine.

%package -n qscintilla2-%{module}-api
Summary:        PyQtWebEngine API file for QScintilla
Summary(pl.UTF-8):      Plik API PyQtWebEngine dla QScintilli
Group:          Libraries/Python
Requires:       qscintilla2-qt5 >= 2.2-2

%description -n qscintilla2-%{module}-api
PyQtWebEngine API file can be used by the QScintilla editor component
to enable the use of auto-completion and call tips when editing
PyQtWebEngine code.

%description -n qscintilla2-%{module}-api -l pl.UTF-8
Plik API PyQtWebEngine może być używany przez komponent edytora
QScintilla aby umożliwić automatyczne dopełnianie i podpowiedzi przy
modyfikowaniu kodu wykorzystującego PyQtWebEngine.

%prep
%setup -q -n PyQtWebEngine-%{version}
%patch -P0 -p1

%build
%if %{with python2}
install -d build-py2
cd build-py2
%{__python} ../configure.py \
	--no-dist-info \
	--verbose \
	-c -j 3 \
	-q "%{_bindir}/qmake-qt5"

%{__make}
cd ..
%endif

%if %{with python3}
install -d build-py3
cd build-py3
%{__python3} ../configure.py \
	--no-dist-info \
	--verbose \
	-c -j 3 \
	-q "%{_bindir}/qmake-qt5"

%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%{__make} -C build-py3 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%endif

%if %{with python2}
%{__make} -C build-py2 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{py_sitedir}/PyQt5/QtWebEngine.so
%attr(755,root,root) %{py_sitedir}/PyQt5/QtWebEngineCore.so
%attr(755,root,root) %{py_sitedir}/PyQt5/QtWebEngineWidgets.so
%{py_sitedir}/PyQt5/QtWebEngine.pyi
%{py_sitedir}/PyQt5/QtWebEngineCore.pyi
%{py_sitedir}/PyQt5/QtWebEngineWidgets.pyi
%endif

%if %{with python3}
%files -n python3-PyQtWebEngine
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/PyQt5/QtWebEngine.so
%attr(755,root,root) %{py3_sitedir}/PyQt5/QtWebEngineCore.so
%attr(755,root,root) %{py3_sitedir}/PyQt5/QtWebEngineWidgets.so
%{py3_sitedir}/PyQt5/QtWebEngine.pyi
%{py3_sitedir}/PyQt5/QtWebEngineCore.pyi
%{py3_sitedir}/PyQt5/QtWebEngineWidgets.pyi
%endif

%files -n sip-PyQtWebEngine
%defattr(644,root,root,755)
%{_sipfilesdir}/PyQt5/QtWebEngine
%{_sipfilesdir}/PyQt5/QtWebEngineCore
%{_sipfilesdir}/PyQt5/QtWebEngineWidgets

%files -n qscintilla2-%{module}-api
%defattr(644,root,root,755)
%{_datadir}/qt5/qsci/api/python/PyQtWebEngine.api
