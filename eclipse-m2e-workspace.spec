%{?scl:%scl_package eclipse-m2e-workspace}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

%global short_name m2e-workspace

Name:           %{?scl_prefix}eclipse-m2e-workspace
Version:        0.4.0
Release:        4.%{baserelease}%{?dist}
Summary:        M2E CLI workspace resolver
License:        EPL
URL:            https://www.eclipse.org/m2e/
BuildArch:      noarch

Source0:        http://git.eclipse.org/c/m2e/org.eclipse.m2e.workspace.git/snapshot/%{short_name}-%{version}.tar.bz2
Source1:        http://www.eclipse.org/legal/epl-v10.html

Patch0:         takari.patch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(javax.inject:javax.inject)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven:maven-core)
BuildRequires:  %{?scl_prefix_maven}mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  %{?scl_prefix_maven}mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  %{?scl_prefix_maven}mvn(org.eclipse.aether:aether-api)
BuildRequires:  %{?scl_prefix_maven}mvn(org.eclipse.sisu:sisu-maven-plugin)

%description
Workspace dependency resolver implementation for Maven command line
build.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
This package provides %{summary}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{short_name}-%{version}

%patch0 -p1

cp -a %{SOURCE1} .
pushd org.eclipse.m2e.workspace.cli
# Remove support for Maven 3.0.x (requires Sonatype Aether, which is
# not available in Fedora)
%pom_remove_dep org.sonatype.aether
rm src/main/java/org/eclipse/m2e/workspace/internal/Maven30WorkspaceReader.java

# Avoid takari
%pom_remove_plugin io.takari.maven.plugins:takari-lifecycle-plugin
%pom_xpath_set pom:project/pom:packaging jar
%pom_add_plugin :maven-compiler-plugin '
<configuration>
<source>1.7</source>
<target>1.7</target>
</configuration>'
%pom_add_plugin org.eclipse.sisu:sisu-maven-plugin '
        <executions>
          <execution>
            <id>generate-index</id>
            <goals>
              <goal>main-index</goal>
            </goals>
          </execution>
        </executions>'
popd
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
pushd org.eclipse.m2e.workspace.cli
%mvn_build
popd
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
pushd org.eclipse.m2e.workspace.cli
%mvn_install
popd
%{?scl:EOF}


%files -f org.eclipse.m2e.workspace.cli/.mfiles
%doc epl-v10.html

%files javadoc -f org.eclipse.m2e.workspace.cli/.mfiles-javadoc
%doc epl-v10.html

%changelog
* Fri Jan 20 2017 Mat Booth <mat.booth@redhat.com> - 0.4.0-4.2
- Avoid takari plugins

* Fri Jan 20 2017 Mat Booth <mat.booth@redhat.com> - 0.4.0-4.1
- Auto SCL-ise package for rh-eclipse46 collection

* Tue Jul 19 2016 Michael Simacek <msimacek@redhat.com> - 0.4.0-4
- Regenerate buildrequires

* Fri Feb 19 2016 Michael Simacek <msimacek@redhat.com> - 0.4.0-3
- Fix FTBFS

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Sopot Cela <scela@redhat.com>- 0.4.0-1
- Upgrade to 0.4.0 for Mars. 1 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 06 2015 Michael Simacek <msimacek@redhat.com> - 0.2.0-1
- Initial packaging
