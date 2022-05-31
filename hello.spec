Name:           hello
Version:        1.0
Release:        1
Summary:        My Script
License:        -

Source0:        hello.sh

BuildArch:      noarch

Buildroot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Hello World

%install
install -D -pm 755 %{SOURCE0} %{buildroot}/usr/local/bin/hello.sh

%files
/usr/local/bin/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon May 30 2022 root
- Add hello.sh

%post
/usr/local/bin/hello.sh
