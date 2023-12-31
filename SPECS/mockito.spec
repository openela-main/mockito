Name:           mockito
Version:        1.10.19
Release:        17%{?dist}
Summary:        A Java mocking framework

License:        MIT
URL:            http://%{name}.org
Source0:        %{name}-%{version}.tar.xz
Source1:        make-%{name}-sourcetarball.sh
Patch0:         fixup-ant-script.patch
Patch1:         fix-bnd-config.patch
Patch2:         %{name}-matcher.patch
# Workaround for NPE in setting NamingPolicy in cglib
Patch3:         setting-naming-policy.patch
# because we have old objenesis
Patch4:         fix-incompatible-types.patch

BuildArch:      noarch
BuildRequires:  javapackages-local
BuildRequires:  java-devel
BuildRequires:  ant
BuildRequires:  objenesis
BuildRequires:  cglib
BuildRequires:  junit
BuildRequires:  hamcrest
BuildRequires:  aqute-bnd

Requires:       objenesis
Requires:       cglib
Requires:       junit
Requires:       hamcrest

%description
Mockito is a mocking framework that tastes really good. It lets you write
beautiful tests with clean & simple API. Mockito doesn't give you hangover
because the tests are very readable and they produce clean verification
errors.

%package javadoc
Summary:        Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0
%patch1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%pom_add_dep net.sf.cglib:cglib:3.1 maven/mockito-core.pom
find . -name "*.java" -exec sed -i "s|org\.%{name}\.cglib|net\.sf\.cglib|g" {} +
mkdir -p lib/compile

%pom_xpath_remove 'target[@name="javadoc"]/copy' build.xml

%build
build-jar-repository lib/compile objenesis cglib junit hamcrest/core
ant jar javadoc

# Convert to OSGi bundle
pushd target
bnd wrap \
 --version %{version} \
 --output %{name}-core-%{version}.bar \
 --properties ../conf/%{name}-core.bnd \
 %{name}-core-%{version}.jar
mv %{name}-core-%{version}.bar %{name}-core-%{version}.jar

# Explicit Require-Bundle on hamcrest
unzip mockito-core-%{version}.jar META-INF/MANIFEST.MF
sed -i -e '2iRequire-Bundle: org.hamcrest.core' META-INF/MANIFEST.MF
jar umf META-INF/MANIFEST.MF mockito-core-%{version}.jar
popd

sed -i -e "s|@version@|%{version}|g" maven/%{name}-core.pom
%mvn_artifact maven/%{name}-core.pom target/%{name}-core-%{version}.jar
%mvn_alias org.%{name}:%{name}-core org.%{name}:%{name}-all

%install
%mvn_install -J target/javadoc

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
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
