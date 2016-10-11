# TODO
# - make it not to parse /proc/cpuinfo
Summary:	Multitrack hard disk recorder
Summary(pl.UTF-8):	Wielościeżkowy magnetofon nagrywający na twardym dysku
Name:		ardour
Version:	5.4.0
Release:	0.1
License:	GPL
Group:		X11/Applications/Sound
Source0:	https://community.ardour.org/srctar/Ardour-%{version}.tar.bz2
# Source0-md5:	ca71c6aa7f804a81539a0c25ea2427a5
Source1:	%{name}.desktop
URL:		http://ardour.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	aubio-devel >= 0.4.0
BuildRequires:	boost-devel
BuildRequires:	cairo-devel >= 1.12.0
BuildRequires:	cairomm-devel >= 1.8.4
BuildRequires:	curl-devel >= 7.0.0
BuildRequires:	dbus-devel
BuildRequires:	fftw3-single-devel
BuildRequires:	flac-devel >= 1.2.1
BuildRequires:	fontconfig-devel
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	gtk+2-devel >= 2:2.12.1
BuildRequires:	gtkmm-devel >= 2.8
BuildRequires:	gtkmm-devel >= 2.8
BuildRequires:	jack-audio-connection-kit-devel >= 0.121
BuildRequires:	libarchive-devel >= 3.0.0
BuildRequires:	liblo-devel >= 0.26
BuildRequires:	liblrdf-devel >= 0.4.0
BuildRequires:	libogg-devel >= 1.1.2
BuildRequires:	libsamplerate-devel >= 0.1.7
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	libsndfile-devel >= 1.0.18
BuildRequires:	libusb-devel
BuildRequires:	libxml2-devel
BuildRequires:	lilv-devel >= 0.21.3
BuildRequires:	lv2-devel >= 1.0.0
BuildRequires:	lv2-devel >= 1.10.0
BuildRequires:	pangomm-devel >= 1.4
BuildRequires:	rubberband-devel
BuildRequires:	serd-devel >= 0.14.0
BuildRequires:	sratom-devel >= 0.2.0
BuildRequires:	suil-devel >= 0.6.0
BuildRequires:	taglib-devel >= 1.6
BuildRequires:	vamp-devel >= 2.1
BuildRequires:	xorg-lib-libX11-devel >= 1.1
Requires:	jack-audio-connection-kit-libs >= 0.121
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A "professional" multitrack, multichannel audio recorder and DAW for
Linux, using ALSA-supported audio interfaces. Supports up to 32 bit
samples, 24+ channels at up to 96kHz, full MMC control,
non-destructive, non-linear editor, LADSPA plugins.

%description -l pl.UTF-8
"Profesjonalny" wielościeżkowy, wielokanałowy magnetofon oraz DAW dla
Linuksa, wykorzystujący interfejsy dźwiękowe obsługiwane przez ALSA.
Obsługuje próbki do 32 bitów, 24+ kanałów do 96kHz, pełną kontrolę
MMC, niedestruktywny, nieliniowy edytor oraz wtyczki LADSPA.

%prep
%setup -q -n Ardour-%{version}

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"

./waf configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--configdir=%{_sysconfdir}/etc \
	--includedir=%{_datadir} \
	--datadir=%{_datadir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--lv2 \
	--lv2dir=%{_libdir}/lv2 \
	--cxx11

./waf build -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

#FIXME

#install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
#cp -a gtk2_ardour/icons/ardour_icon_48px.png $RPM_BUILD_ROOT%{_pixmapsdir}/ardour.png

## it shouldn't be there
#rm -f $RPM_BUILD_ROOT%{_datadir}/ardour/libardour.{la,a}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc DOCUMENTATION/{AUTHORS,CONTRIBUTORS,FAQ,TRANSLATORS}
%lang(es) %doc DOCUMENTATION/{AUTHORS.es,CONTRIBUTORS.es,README.es}
%lang(fr) %doc DOCUMENTATION/README.fr
%lang(it) %doc DOCUMENTATION/README.it
%lang(ru) %doc DOCUMENTATION/README.ru
%dir %{_sysconfdir}/ardour2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour2/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour2/*.rc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour2/ardour.bindings
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour2/ardour.menus
%attr(755,root,root) %{_bindir}/ardour2
%{_datadir}/ardour2
%{_desktopdir}/ardour.desktop
%{_pixmapsdir}/ardour.png

%dir %{_libdir}/ardour2
%attr(755,root,root) %{_libdir}/ardour2/ardour-2.1
%attr(755,root,root) %{_libdir}/ardour2/libardour.so
%attr(755,root,root) %{_libdir}/ardour2/libardour_cp.so
%attr(755,root,root) %{_libdir}/ardour2/libgtkmm2ext.so
%attr(755,root,root) %{_libdir}/ardour2/libmidi++.so
%attr(755,root,root) %{_libdir}/ardour2/libpbd.so
%attr(755,root,root) %{_libdir}/ardour2/libsndfile-ardour.so
%dir %{_libdir}/ardour2/engines
%attr(755,root,root) %{_libdir}/ardour2/engines/libclearlooks.so
%dir %{_libdir}/ardour2/surfaces
%attr(755,root,root) %{_libdir}/ardour2/surfaces/libardour_genericmidi.so
%attr(755,root,root) %{_libdir}/ardour2/surfaces/libardour_mackie.so
%attr(755,root,root) %{_libdir}/ardour2/surfaces/libardour_powermate.so
%attr(755,root,root) %{_libdir}/ardour2/surfaces/libardour_tranzport.so
