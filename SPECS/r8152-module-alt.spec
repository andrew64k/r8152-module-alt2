%define module_dir extra

Summary: Driver for Realtek r8152
Name: r8152-module-alt
Version: 2.17.1
Release: 1%{?dist}
License: GPL
# Sources extracted from the Linux kernel %{version}
Source: %{name}-%{version}.tar.gz

Patch0: 0001-compat.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod


%description
Realtek r8152 device drivers for the Linux Kernel version %{kernel_version}.

%prep
%autosetup -n %{name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
mkdir -p %{buildroot}/etc/udev/rules.d
%{__make} RULEDIR=%{buildroot}/etc/udev/rules.d install_rules

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{kernel_version}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko
/etc/udev/rules.d/50-usb-realtek-net.rules

%changelog
* Thu Sep 28 2023 Andrew Lindh <andrew@netplex.net> - 2.17.1-1
- Vendor driver r8152-2.17.1

