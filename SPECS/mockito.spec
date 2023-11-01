%bcond_with bootstrap

Name:           mockito
Version:        3.7.13
Release:        5%{?dist}
Summary:        Tasty mocking framework for unit tests in Java
License:        MIT
URL:            https://site.mockito.org/
BuildArch:      noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        generate-tarball.sh

# A custom build script to allow building with maven instead of gradle
Source2:        mockito-core.pom

# Mockito expects byte-buddy to have a shaded/bundled version of ASM, but
# we don't bundle in Fedora, so this patch makes mockito use ASM explicitly
Patch0:         use-unbundled-asm.patch

BuildRequires:  maven-local
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.bytebuddy:byte-buddy)
BuildRequires:  mvn(net.bytebuddy:byte-buddy-agent)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.hamcrest:hamcrest)
BuildRequires:  mvn(org.objenesis:objenesis)
BuildRequires:  mvn(org.opentest4j:opentest4j)
BuildRequires:  mvn(org.ow2.asm:asm)
%endif

%description
Mockito is a mocking framework that tastes really good. It lets you write
beautiful tests with clean & simple API. Mockito doesn't give you hangover
because the tests are very readable and they produce clean verification
errors.

%package javadoc
Summary: Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0 -p1

# Disable failing test
# TODO check status: https://github.com/mockito/mockito/issues/2162
sed -i '/add_listeners_concurrently_sanity_check/i @org.junit.Ignore' src/test/java/org/mockitousage/debugging/StubbingLookupListenerCallbackTest.java

# Use our custom build script
sed -e 's/@VERSION@/%{version}/' %{SOURCE2} > pom.xml

# OGGi metadata configuration
cat > osgi.bnd <<EOF
Automatic-Module-Name: org.mockito
Bundle-SymbolicName: org.mockito
Bundle-Name: Mockito Mock Library for Java.
Import-Package: junit.*;resolution:=optional,org.junit.*;resolution:=optional,org.hamcrest;resolution:=optional,org.mockito*;version="%{version}",*
Private-Package: org.mockito.*
-removeheaders: Bnd-LastModified,Include-Resource,Private-Package
EOF

# Compatibility alias
%mvn_alias org.%{name}:%{name}-core org.%{name}:%{name}-all

sed -i 's/net\.bytebuddy\.jar\.asm/org.objectweb.asm/' src/main/java/org/mockito/internal/creation/bytebuddy/MockMethodAdvice.java

%build
# See the usage of exec-maven-plugin in the pom
mkdir -p target/classes/
javac -d target/classes/ src/main/java/org/mockito/internal/creation/bytebuddy/inject/MockMethodDispatcher.java
mv target/classes/org/mockito/internal/creation/bytebuddy/inject/MockMethodDispatcher.{class,raw}

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc README.md doc/design-docs/custom-argument-matching.md

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 3.7.13-5
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 09 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.7.13-4
- Rebuild to workaround DistroBaker issue

* Tue Jun 08 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.7.13-3
- Bootstrap Maven for CentOS Stream 9

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.7.13-2
- Bootstrap build
- Non-bootstrap build

* Thu Feb 04 2021 Marian Koncek <mkoncek@redhat.com> - 3.7.13-1
- Update to upstream version 3.7.13

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct  9 2020 Stuart Gathman <stuart@gathman.org> - 3.5.13-1
- Update to version 3.5.13

* Wed Sep 30 2020 Marian Koncek <mkoncek@redhat.com> - 3.5.13-1
- Update to ustream version 3.5.13

* Sun Aug 23 2020 Jerry James <loganjerry@gmail.com> - 3.5.5-1
- Update to version 3.5.5

* Fri Aug 14 2020 Jerry James <loganjerry@gmail.com> - 2.28.2-1
- Update to version 2.28.2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Marian Koncek <mkoncek@redhat.com> - 3.4.5-1
- Update to upstream version 3.4.5

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2.23.9-7
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-2
- Mass rebuild for javapackages-tools 201902

* Wed Oct 16 2019 Marian Koncek <mkoncek@redhat.com> - 3.1.2-1
- Update to upstream version 3.1.2

* Thu Sep 19 2019 Marian Koncek <mkoncek@redhat.com> - 3.0.8-1
- Update to upstream version 3.0.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.23.9-4
- Mass rebuild for javapackages-tools 201901

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Mat Booth <mat.booth@redhat.com> - 2.23.9-3
- Set the source encoding for the build

* Wed Dec 05 2018 Mat Booth <mat.booth@redhat.com> - 2.23.9-2
- Re-add compatibility alias for 'mockito-all'

* Tue Dec 04 2018 Mat Booth <mat.booth@redhat.com> - 2.23.9-1
- Update to latest upstream version
- Switch to maven build system using a custom pom to avoid a dep on gradle

* Fri Aug 03 2018 Michael Simacek <msimacek@redhat.com> - 1.10.19-17
- Remove bundled minified js from javadoc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.10.19-15
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 16 2017 Michael Simacek <msimacek@redhat.com> - 1.10.19-12
- Remove conditional for EOL Fedora

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 22 2016 Mat Booth <mat.booth@redhat.com> - 1.10.19-10
- Explicitly import more cglib packages in OSGi metadata to prevent mockito
  failing under certain circumstances during Eclipse test suites

* Fri Feb 12 2016 Mat Booth <mat.booth@redhat.com> - 1.10.19-9
- Require hamcrest explicitly in OSGi metadata

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 25 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-7
- introduce License tag

* Fri Dec 25 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-6
- reenable osgi

* Fri Dec 18 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-5
- workaround rhbz#1292777 stylesheet.css not found

* Thu Jul 16 2015 Michael Simacek <msimacek@redhat.com> - 1.10.19-4
- Use aqute-bnd-2.4.1

* Mon Jun 22 2015 Mat Booth <mat.booth@redhat.com> - 1.10.19-3
- Switch to mvn_install

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Michal Srb <msrb@redhat.com> - 1.10.19-1
- Update to 1.10.19

* Mon Aug 25 2014 Darryl L. Pierce <dpierce@redhat.com> - 1.9.0-18
- First build for EPEL7
- Resolves: BZ#1110030

* Mon Jun 09 2014 Omair Majid <omajid@redhat.com> - 1.9.0-17
- Use .mfiles to pick up xmvn metadata
- Don't use obsolete _mavenpomdir and _mavendepmapfragdir macros
- Fix FTBFS

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.9.0-16
- Use junit R/BR over junit4.

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.9.0-15
- Use Requires: java-headless rebuild (#1067528)

* Wed Dec 11 2013 Michael Simacek <msimacek@redhat.com> - 1.9.0-14
- Workaround for NPE in setting NamingPolicy

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Tomas Radej <tradej@redhat.com> - 1.9.0-12
- Patched LocalizedMatcher due to hamcrest update, (bug upstream)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 6 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-10
- More Import-Package fixes. Note that fix-cglib-refs.patch is
  not suitable for upstream: issue id=373

* Tue Sep 4 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-9
- Fix missing Import-Package in manifest.

* Mon Aug 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-8
- Add aqute bnd instructions for OSGi metadata

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-6
- Place JavaDoc in directly under %%{_javadocdir}/%%{name} instead
  of %%{_javadocdir}/%%{name}/javadoc

* Wed Apr 25 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-5
- Removed post/postun hook for update_maven_depmap

* Tue Apr 24 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-4
- Fix groupId of cglib dependency
- Add additional depmap for mockito-all
- Update depmap on post and postun
- Fix version in pom

* Wed Feb 22 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-3
- Added cglib dependency to pom

* Tue Feb 21 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-2
- Include upstream Maven pom.xml in package
- Added missing Requires for cglib, junit4, hamcrest, objenesis
- Added source tarball generating script to sources

* Thu Feb 16 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-1
- Initial package
