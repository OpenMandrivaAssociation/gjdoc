%define gcj_support        1
%bcond_with                native

%if %with native
%define gcj_support        0
%endif

Summary:                GNU Javadoc
Name:                   gjdoc
Version:                0.7.9
Release:                %mkrel 4
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


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.7.9-4mdv2011.0
+ Revision: 618953
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:0.7.9-3mdv2010.0
+ Revision: 424992
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0:0.7.9-2mdv2009.1
+ Revision: 264544
- rebuild early 2009.0 package (before pixel changes)

* Wed Apr 23 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.7.9-1mdv2009.0
+ Revision: 196793
- new version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.7.8-5mdv2008.1
+ Revision: 120885
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:0.7.8-4mdv2008.0
+ Revision: 87380
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Tue Sep 11 2007 David Walluck <walluck@mandriva.org> 0:0.7.8-3mdv2008.0
+ Revision: 84355
- disable broken infopage install

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:0.7.8-2mdv2008.0
+ Revision: 82795
- update to new version

* Fri May 04 2007 David Walluck <walluck@mandriva.org> 0:0.7.8-1mdv2008.0
+ Revision: 22260
- no need to remove info dir
- 0.7.8


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 0.7.7-14.2mdv2007.1
+ Revision: 143953
- patch3: -bootclasspath option should accept an argument

* Thu Mar 08 2007 David Walluck <walluck@mandriva.org> 0:0.7.7-14.1mdv2007.1
+ Revision: 137675
- add gjdoc-consistent-html.patch
- rebuild without native
  use %%bcond_with

* Sat Nov 04 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-12mdv2007.1
+ Revision: 76409
- update
- Import gjdoc

* Tue Apr 25 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-9mdv2007.0
- use chrpath
- rebuild for libgcj.so.7

* Wed Apr 12 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-8mdk
- add ^Z patch
- don't package .la files

* Thu Feb 23 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-7mdk
- rebuild as native
- fix gcj support

* Fri Jan 27 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-6mdk
- source java-functions, set_javacmd
- Requires: jpackage-utils

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-5mdk
- package, but don't install info page (broken)

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-4mdk
- fix requires

* Wed Jan 11 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-3mdk
- require java/java-devel

* Mon Jan 09 2006 David Walluck <walluck@mandriva.org> 0:0.7.7-2mdk
- work around post-script failures

* Mon Dec 19 2005 David Walluck <walluck@mandriva.org> 0:0.7.7-1mdk
- 0.7.7

* Tue Nov 08 2005 David Walluck <walluck@mandriva.org> 0:0.7.6-2mdk
- use aot-compile instead of native
- install jar symlinks
- set correct java paths for build (runtime currently not correct)

* Sat Oct 22 2005 David Walluck <walluck@mandriva.org> 0:0.7.6-1mdk
- 0.7.6

* Mon Sep 12 2005 David Walluck <walluck@mandriva.org> 0:0.7.5-2mdk
- fix libgcj requirement

* Mon Sep 12 2005 David Walluck <walluck@mandriva.org> 0:0.7.5-1mdk
- 0.7.5

* Mon May 23 2005 David Walluck <walluck@mandriva.org> 0:0.7.4-5.1mdk
- use macros for info pages
- add patch to handle single quotes in options (Julian Scheid)
- add patch to handle lack of whitespace before member names (Julian)
- add patches to ignore option case and deal with some error cases (Julian
  Scheid)

* Thu May 05 2005 David Walluck <walluck@mandriva.org> 0:0.7.4-3.1mdk
- release

* Wed Apr 27 2005 Andrew Overholt <overholt@redhat.com> 0.7.4-3
- Remove ppc64 as it appears to be hanging during the build.
  Will investigate.

* Tue Apr 26 2005 Andrew Overholt <overholt@redhat.com> 0.7.4-2
- Add patches from head (Julian Scheid).

* Mon Apr 25 2005 Andrew Overholt <overholt@redhat.com> 0.7.4-1
- New version.

* Tue Mar 15 2005 Andrew Overholt <overholt@redhat.com> 0.7.3-1
- New version.

* Wed Mar 09 2005 Andrew Overholt <overholt@redhat.com> 0.7.2-1
- New version.

* Thu Mar 03 2005 Andrew Overholt <overholt@redhat.com> 0.7.1-4
- Add workaround for extraneous directory on x86_64.
- Remove ia64 due to gcc backend bug.

* Wed Mar 02 2005 Andrew Overholt <overholt@redhat.com> 0.7.1-3
- %%files tweaking.

* Tue Mar 01 2005 Andrew Overholt <overholt@redhat.com> 0.7.1-2
- Bump for gcc4 -> gcc.
- Re-add libtool hack.

* Fri Feb 25 2005 Andrew Overholt <overholt@redhat.com> 0.7.1-1
- Import new version.

* Wed Feb 09 2005 Andrew Overholt <overholt@redhat.com> 0.7.1-0.pre3.1
- Import 0.7.1-pre3.
- Remove libtool breakage workaround.

* Tue Feb 08 2005 Andrew Overholt <overholt@redhat.com> 0.7.1-0.pre2.4
- Add workaround for libtool breakage.
- Exclude s390 and s390x.

* Mon Feb 07 2005 Andrew Overholt <overholt@redhat.com> 0.7.1-0.pre2
- New upstream version.
- Add README.

* Sat Feb 05 2005 Andrew Overholt <overholt@redhat.com> 0.7.1-0.pre1
- Initial build of upstream pre-release.
- Import gbenson's previous specfile.

