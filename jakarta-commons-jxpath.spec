# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section   devel
%define base_name commons-jxpath

Name:           jakarta-%{base_name}
Version:        1.2
Release:        3.0.5
Epoch:          0
Summary:        Simple XPath interpreter

Group:          Development/Java
License:        Apache Software License
URL:            https://jakarta.apache.org/commons/jxpath/
Source0:        commons-jxpath-1.2-src.zip
Source1:        commons-jxpath-1.2.pom
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  java-rpmbuild
BuildRequires:  ant >= 0:1.6, ant-junit >= 0:1.6, junit
BuildRequires:  xml-commons-apis
BuildRequires:  xerces-j2
BuildRequires:  servletapi5
BuildRequires:  jsp
BuildRequires:  jdom >= 0:1.0
BuildRequires:  jakarta-commons-beanutils
BuildRequires:  jakarta-commons-logging
BuildRequires:  jakarta-commons-collections >= 0:2.1.1
Requires:       xml-commons-apis
Requires:       xerces-j2
Requires:       servletapi5
Requires:	jsp
Requires:       jdom >= 0:1.0
Requires:       jakarta-commons-beanutils
Requires:       jakarta-commons-logging
Requires:       jakarta-commons-collections >= 0:2.1.1

%description
Defines a simple interpreter of an expression language called XPath. 
JXPath applies  XPath  expressions to graphs of objects of all kinds: 
JavaBeans, Maps, Servlet contexts, DOM etc, including mixtures thereof.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}

%prep
%setup -q -n %{base_name}-%{version}
#touch build.properties
#echo jaxp.jaxp.jar = $(find-jar xml-commons-apis) >> build.properties 
#echo jaxp.xslt.jar = $(find-jar xml-commons-apis) >> build.properties 
#echo jdom.jar = $(find-jar jdom) >> build.properties 
#echo servlet.jar = $(find-jar servletapi4) >> build.properties 
#echo junit.jar = $(find-jar junit) >> build.properties 
#echo commons-beanutils.jar = $(find-jar commons-beanutils) >> build.properties 
#echo commons-collections.jar = $(find-jar commons-collections) >> build.properties 
#echo commons-logging.jar = $(find-jar commons-logging) >> build.properties 

%build
export OPT_JAR_LIST="ant/ant-junit junit ant-launcher"
export CLASSPATH=$(build-classpath \
xerces-j2 \
servletapi5 \
jsp \
xml-commons-apis \
jdom \
commons-beanutils \
commons-logging \
commons-collections \
ant-launcher)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
%ant -Dbuild.sysclasspath=first -Dant.build.javac.source=1.4 -Dant.build.javac.target=1.4 test jar javadoc


%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 target/%{base_name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{base_name}-%{version}.jar
ln -s %{base_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{base_name}.jar
  %add_to_maven_depmap %{base_name} %{base_name} %{version} JPP/%{base_name} %{base_name}
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{base_name}.pom

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.2-3.0.4mdv2011.0
+ Revision: 619760
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0:1.2-3.0.3mdv2010.0
+ Revision: 429588
- rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0:1.2-3.0.2mdv2009.0
+ Revision: 267206
- rebuild early 2009.0 package (before pixel changes)

* Sat May 24 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.2-2.0.2mdv2009.0
+ Revision: 210807
- add maven pom

* Tue May 13 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.2-2.0.1mdv2009.0
+ Revision: 206660
- add java-rpmbuild BR
- reenable javadoc
- add ant-launcher to the classpath
- fix group
- import jakarta-commons-jxpath


