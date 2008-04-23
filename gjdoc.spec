%define gcj_support        1
%bcond_with                native

%if %with native
%define gcj_support        0
%endif

Summary:                GNU Javadoc
Name:                   gjdoc
Version:                0.7.9
Release:                %mkrel 1
Epoch:                  0
License:                GPL
Group:                  Development/Java
URL:                    http://savannah.gnu.org/projects/classpath/
Source0:                ftp://ftp.gnu.org/gnu/classpath/gjdoc-%{version}.tar.gz
Source1:                ftp://ftp.gnu.org/gnu/classpath/gjdoc-%{version}.tar.gz.sig
Patch0:                 %{name}-fix-control-z.patch
Patch1:                 %{name}-rm-timestamp.patch
Patch2:                 %{name}-consistent-html.patch
Patch3:                 %{name}-fix-bootclasspath-option.patch
Requires:               antlr
Requires:               jaxp_parser_impl
Requires:               jaxp_transform_impl
Requires:               java >= 0:1.4.2
Requires:               jpackage-utils
Requires(post):         info-install
Requires(preun):        info-install
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%else
%if %without native
BuildArch:              noarch
%endif
%endif
BuildRequires:          antlr
BuildRequires:          chrpath
BuildRequires:          java-devel >= 0:1.4.2
BuildRequires:          jaxp_parser_impl
BuildRequires:          jaxp_transform_impl
BuildRequires:          java-rpmbuild
BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}-root

%description
A documentation generation system for "javadoc"-style comments.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p1

%build
export CLASSPATH=
#export CLASSPATH=$(build-classpath jaxp_parser_impl jaxp_transform_impl)
export JAR=%{jar}
export JAVA=%{java}
export JAVAC=%{javac}
export JAVADOC=%{javadoc}
%ifarch noarch
%{configure} \
%else
%{configure2_5x} \
%endif
--with-antlr-jar=%{_javadir}/antlr.jar \
--enable-xmldoclet \
%if %with native
--enable-native
%else
--disable-native
%endif
%{__sed} -i 's/^pic_flag=\"\"/pic_flag=\"\ \-fPIC\"/' libtool
%{__sed} -i 's/^compiler_c_o=\"no\"/compiler_c_o=\"yes\"/' libtool
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall}

%if %with natuve
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/gjdoc
%endif

pushd %{buildroot}%{_javadir}
%{__ln_s} com-sun-javadoc-%{version}.jar com-sun-javadoc.jar
%{__ln_s} com-sun-tools-doclets-Taglet-%{version}.jar com-sun-tools-doclets-Taglet.jar
%{__ln_s} gnu-classpath-tools-gjdoc-%{version}.jar gnu-classpath-tools-gjdoc.jar
popd

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}
%endif
%if 0
%_install_info gjdoc.info
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%preun
%if 0
%_remove_install_info gjdoc.info
%endif

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%{_bindir}/gjdoc
%{_javadir}/com-sun-javadoc-%{version}.jar
%{_javadir}/com-sun-tools-doclets-Taglet-%{version}.jar
%{_javadir}/gnu-classpath-tools-gjdoc-%{version}.jar
%{_javadir}/com-sun-javadoc.jar
%{_javadir}/com-sun-tools-doclets-Taglet.jar
%{_javadir}/gnu-classpath-tools-gjdoc.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/com-sun-javadoc-%{version}.jar.*
%{_libdir}/gcj/%{name}/com-sun-tools-doclets-Taglet-%{version}.jar.*
%{_libdir}/gcj/%{name}/gnu-classpath-tools-gjdoc-%{version}.jar.*
%endif
%if %with native
%{_libdir}/lib-com-sun-javadoc.la
%{_libdir}/lib-com-sun-javadoc.so
%{_libdir}/lib-com-sun-javadoc.so.0
%{_libdir}/lib-com-sun-javadoc.so.0.0.0
%{_libdir}/lib-com-sun-tools-doclets-Taglet.la
%{_libdir}/lib-com-sun-tools-doclets-Taglet.so
%{_libdir}/lib-com-sun-tools-doclets-Taglet.so.0
%{_libdir}/lib-com-sun-tools-doclets-Taglet.so.0.0.0
%{_libdir}/lib-gnu-classpath-tools-gjdoc.la
%{_libdir}/lib-gnu-classpath-tools-gjdoc.so
%{_libdir}/lib-gnu-classpath-tools-gjdoc.so.0
%{_libdir}/lib-gnu-classpath-tools-gjdoc.so.0.0.0
%endif
%{_infodir}/gjdoc.info*
%{_mandir}/man1/gjdoc*
