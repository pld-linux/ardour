Summary:	Multitrack hard disk recorder
Summary(pl.UTF-8):	Wielościeżkowy magnetofon nagrywający na twardym dysku
Name:		ardour
Version:	5.12.0
Release:	3
License:	GPL
Group:		X11/Applications/Sound
Source0:	https://community.ardour.org/srctar/Ardour-%{version}.tar.bz2
# Source0-md5:	cb45f31a59dd5a0da07422e4ac1c44fd
Source1:	%{name}.desktop
Patch0:		localedir.patch
Patch1:		no_proc_build.patch
Patch2:		ffmpeg_paths.patch
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
BuildRequires:	gtk+2-devel >= 2:2.18
BuildRequires:	gtkmm-devel >= 2.8
BuildRequires:	itstool >= 2.0.0
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
BuildRequires:	lv2-devel >= 1.10.0
BuildRequires:	pangomm-devel >= 1.4
BuildRequires:	rubberband-devel
BuildRequires:	serd-devel >= 0.14.0
BuildRequires:	sord-devel >= 0.8.0
BuildRequires:	sratom-devel >= 0.2.0
BuildRequires:	suil-devel >= 0.6.0
BuildRequires:	taglib-devel >= 1.6
BuildRequires:	udev-devel
BuildRequires:	vamp-devel >= 2.1
BuildRequires:	xorg-lib-libX11-devel >= 1.1
Requires:	jack-audio-connection-kit-libs >= 0.121
Suggests:	harvid
Suggests:	xjadeo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles	%{_libdir}/(ardour5|lv2)
%define		_noautoreq 	^libardour.* libaudiographer.so.0 libcanvas.so.0 libevoral.so.0 libgtkmm2ext.so.0 libmidipp.so.4 libpbd.so.4 libptformat.so.0 libqmdsp.so.0 libtimecode.so libwaveview.so.0 libwidgets.so.0

# Unresolved symbols:
#	_Z10vstfx_exitv
#	_Z10vstfx_initPv
#	_Z20vstfx_destroy_editorP9_VSTState
# those are defined in the executable
%define         skip_post_check_so      libardour.so.*

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

%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"

./waf configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--configdir=%{_sysconfdir} \
	--includedir=%{_datadir} \
	--datadir=%{_datadir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--lv2 \
	--lv2dir=%{_libdir}/lv2 \
	--cxx11 \
	--freedesktop

./waf build -v
./waf i18n -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

./waf install -v \
	--destdir=$RPM_BUILD_ROOT \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--configdir=%{_sysconfdir} \
	--includedir=%{_datadir} \
	--datadir=%{_datadir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a gtk2_ardour/icons/application-x-ardour_48px.png $RPM_BUILD_ROOT%{_pixmapsdir}/ardour.png

rm -r $RPM_BUILD_ROOT%{_localedir}/{pt_PT,zh}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%dir %{_sysconfdir}/ardour5
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour5/ardour.keys
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour5/ardour.menus
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour5/clearlooks.rc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour5/default_ui_config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour5/system_config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour5/trx.menus
%attr(755,root,root) %{_bindir}/ardour5
%attr(755,root,root) %{_bindir}/ardour5-lua
%{_datadir}/ardour5
%{_desktopdir}/ardour.desktop
%{_pixmapsdir}/ardour.png

# everything executable there
%attr(755,root,root) %{_libdir}/ardour5

%dir %{_libdir}/lv2/*.lv2
%attr(755,root,root) %{_libdir}/lv2/*.lv2/*.so
%{_libdir}/lv2/*.lv2/*.ttl
