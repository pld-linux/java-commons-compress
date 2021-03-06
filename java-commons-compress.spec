#
# Conditional build:
%bcond_with	javadoc		# don't build javadoc

%define		srcname		commons-compress
Summary:	Java API for working with compressed files and archivers
Name:		java-%{srcname}
Version:	1.8.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://archive.apache.org/dist/commons/compress/source/%{srcname}-%{version}-src.tar.gz
# Source0-md5:	f5aaa32681260f71cdc440493f475c42
URL:		http://commons.apache.org/compress/
BuildRequires:	java-xz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Apache Commons Compress library defines an API for working with
ar, cpio, Unix dump, tar, zip, gzip, XZ, Pack200 and bzip2 files.

%package javadoc
Summary:	API documentation for %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{srcname}-%{version}-src

%build
required_jars="xz"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

# do what 'mvn package' would
install -d target/{classes,test-classes}
%javac -d target/classes -encoding UTF-8 $(find src/main -type f -name "*.java")
%jar -cvf target/%{srcname}-%{version}.jar -C target/classes .

%install
rm -rf $RPM_BUILD_ROOT
# jar
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p target/commons-compress-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -a target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
