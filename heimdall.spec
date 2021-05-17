%global commit0 3997d5cc607e6c603c6e7c0d07e42e9868c62af2
%global date 20210314
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

%global __cmake_in_source_build 1

Name:           heimdall
Version:        1.4.2
Release:        1%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Flash firmware onto Samsung mobile devices
License:        MIT
URL:            https://github.com/Benjamin-Dobell/Heimdall

%if 0%{?tag:1}
Source0:        https://github.com/Benjamin-Dobell/Heimdall/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:        https://github.com/Benjamin-Dobell/Heimdall/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  gcc-c++
BuildRequires:  libusb1-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  zlib-devel

%description
Heimdall is a cross-platform open-source tool suite used to flash firmware (aka
ROMs) onto Samsung mobile devices.

Heimdall connects to a mobile device over USB and interacts with low-level
software running on the device, known as Loke. Loke and Heimdall communicate via
the custom Samsung-developed protocol typically referred to as the 'Odin 3
protocol'.

%prep
%if 0%{?tag:1}
%autosetup -p1 -n Heimdall-%{version}
%else
%autosetup -p1 -n Heimdall-%{commit0}
%endif

%build
%cmake
%cmake_build

%install
%cmake_install

install -p -m 0644 -D %{name}/60-%{name}.rules %{buildroot}%{_udevrulesdir}/60-%{name}.rules

%files
%license LICENSE
%doc Linux/README
%{_bindir}/%{name}
%{_bindir}/%{name}-frontend
%{_udevrulesdir}/60-%{name}.rules

%changelog
* Mon May 17 2021 Simone Caronni <negativo17@gmail.com> - 1.4.2-1.20210314git3997d5c
- First build.
