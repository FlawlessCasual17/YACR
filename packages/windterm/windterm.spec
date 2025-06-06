%global         full_name windterm
%global         app_name WindTerm
%global         debug_package %{nil}

Name:           windterm
Version:        2.7.0
Release:        1%{?dist}
Summary:        A professional cross-platform SSH/Sftp/Shell/Telnet/Tmux/Serial terminal.

License:        MIT, Apache-2.0, LGPL-2.1-or-later, BSD-2-Clause (or BSD-3-Clause)
URL:            https://github.com/kingToolbox/WindTerm

Source0:        https://github.com/kingToolbox/WindTerm/releases/download/%{version}/%{app_name}_%{version}_Linux_Portable_x86_64.zip
Source1:        %{full_name}.desktop
Source2:        %{full_name}

ExclusiveArch:  x86_64

Requires:       qt5-qtbase qt5-qttools

%description
A professional cross-platform SSH/Sftp/Shell/Telnet/Tmux/Serial terminal.

You may need to use the following command to give the application permissions to create the `profiles.config` file:

chown -R "$USER:$USER" /opt/WindTerm

%prep
%setup -q -n ./%{app_name}_%{version}

%install
# Remove build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps

# Compress the `lib` directory to avoid the "broken rpath" error
%__tar -cf ./lib.tar ./lib
%__xz -6 ./lib.tar -c > ./lib.tar.xz
%__rm -r ./lib ./lib.tar

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary (might use a BASH script wrapper if this doesn't work)
%__install -Dm 0755 %{SOURCE2} -t %{buildroot}%{_bindir}
%__chmod +x %{buildroot}%{_bindir}/%{full_name}

# Install application icons
%__install -Dm 0644 %{buildroot}/opt/%{app_name}/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps

%post
# Add executable permissions to the application binary
%__chmod +x /opt/%{app_name}/%{app_name}

if [ -e /opt/%{app_name}/lib.tar.xz ]; then
  # Create the `lib` directory
  %__mkdir_p /opt/%{app_name}/lib
  # Uncompress the `lib.tar.xz` file
  %__tar -xf /opt/%{app_name}/lib.tar.xz "--strip-components=2" -C /opt/%{app_name}/lib
  # Remove the `lib.tar.xz` file
  %__rm /opt/%{app_name}/lib.tar.xz
fi

# Inform the user that they may have to use chown if they want the application to create the `profiles.config` file
echo "You may need to use the following command to give the application permissions to create the `profiles.config` file:"
echo ""
echo "chown -R %{user}:%{user} /opt/%{app_name}"

%postun
if [ -e /opt/%{app_name}/lib ]; then
  # Remove the `lib` directory
  %__rm -r /opt/%{app_name}/lib
fi

if [ -e /opt/%{app_name} ]; then
  %__rm -r /opt/%{app_name}
fi

%files
/opt/%{app_name}
%{_bindir}/%{full_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/1024x1024/apps/%{full_name}.png
%license ./license.txt
