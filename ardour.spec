# TODO
# - make it not to parse /proc/cpuinfo
Summary:	Multitrack hard disk recorder
Summary(pl.UTF-8):	Wielościeżkowy magnetofon nagrywający na twardym dysku
Name:		ardour
Version:	2.1
Release:	0.1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://ardour.org/files/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	18be414a37b832aae23c068ba9fcf8ab
Source1:	%{name}.desktop
Patch0:		%{name}-c++.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-stdint.patch
URL:		http://ardour.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	boost-devel
BuildRequires:	cairomm-devel
BuildRequires:	fftw3-single-devel >= 3
BuildRequires:	flac-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.10.1
BuildRequires:	gtk+2-devel >= 2:2.8.1
BuildRequires:	gtkmm-devel >= 2.8.0
BuildRequires:	jack-audio-connection-kit-devel >= 0.103
BuildRequires:	libart_lgpl >= 2.3.16
BuildRequires:	libgnomecanvas-devel >= 2.0
BuildRequires:	libgnomecanvasmm-devel >= 2.12.0
BuildRequires:	liblo-devel
BuildRequires:	liblrdf-devel >= 0.4.0
BuildRequires:	libraptor-devel >= 1.4.2
BuildRequires:	libsamplerate-devel >= 0.1.2
BuildRequires:	libsigc++-devel >= 2.0
# included libsndfile needs patch (wants FLAC__seekable_stream_decoder_set_read_callback)
# (in ardour itself only one UI option depends on HAVE_FLAC)
# internal one used
#BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	libxslt-devel
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	python >= 2.3.4
BuildRequires:	scons >= 0.96
BuildRequires:	soundtouch-devel >= 1.3.1
Requires:	jack-audio-connection-kit-libs >= 0.103
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
%setup -q
%patch0 -p1
# NEEDS UPDATE for scons
#%patch1 -p1
%patch2 -p1

%build
# Make sure we have /proc mounted - it searches for flags from there
if [ ! -f /proc/cpuinfo ]; then
	echo "You need to have /proc mounted in order to build this package!"
	exit 1
fi

CXX="%{__cxx}" \
CC="%{__cc}" \
%scons \
	PREFIX=%{_prefix} \
	SYSLIBS=1 \
%ifarch %{x8664}
	DIST_TARGET=x86_64
%else
%ifarch %{ix86}
	DIST_TARGET=i386
%else
	DIST_TARGET=none
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%scons install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	GTK=yes
#	KSI=yes

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

# it shouldn't be there
rm -f $RPM_BUILD_ROOT%{_datadir}/ardour/libardour.{la,a}

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
