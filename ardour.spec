Summary:	Multitrack hard disk recorder
Summary(pl):	Wieloscie¿kowy magnetofon nagrywaj±cy na twardym dysku
Name:		ardour
Version:	0.9
%define	_beta	beta9.1
Release:	0.%{_beta}.1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/ardour/%{name}-%{version}%{_beta}.tar.bz2
# Source0-md5:	411deff954d269b70a330f2718c5674a
Source1:	%{name}.desktop
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-ac_cleanup.patch
Patch3:		%{name}-am18.patch
URL:		http://ardour.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	gtk+-devel >= 1.0.0
#BuildRequires:	gtk-canvas-devel >= 0.1
BuildRequires:	gtkmm1-devel >= 1.2.6
BuildRequires:	jack-audio-connection-kit-devel >= 0.91.0
BuildRequires:	libart_lgpl >= 2.3
BuildRequires:	libpng-devel
BuildRequires:	liblrdf-devel >= 0.3.0
BuildRequires:	libsamplerate-devel >= 0.0.13
BuildRequires:	libsigc++1-devel >= 0.8.8
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.5.0
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A "professional" multitrack, multichannel audio recorder and DAW for
Linux, using ALSA-supported audio interfaces. Supports up to 32 bit
samples, 24+ channels at up to 96kHz, full MMC control,
non-destructive, non-linear editor, LADSPA plugins.

%description -l pl
"Profesjonalny" wielo¶cie¿kowy, wielokana³owy magnetofon oraz DAW dla
Linuksa, wykorzystuj±cy interfejsy d¼wiêkowe obs³ugiwane przez ALSA.
Obs³uguje próbki do 32 bitów, 24+ kana³ów do 96kHz, pe³n± kontrolê
MMC, niedestruktywny, nieliniowy edytor oraz wtyczki LADSPA.

%prep
%setup -q -n %{name}-%{version}%{_beta}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

install -d m4
# extract AM_BUILD_ENVIRONMENT (patched!)
tail -n +760 aclocal.m4 > m4/buildenv.m4
# AC_UNIQUIFY_{LAST,FIRST}
#tail -n +6685 libs/ardour/aclocal.m4 >> m4/buildenv.m4
# AC_POSIX_RTSCHED
tail -n +895 libs/pbd/aclocal.m4 | head -n 118 >> m4/buildenv.m4

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
cd gtk_ardour
%{__aclocal} -I ../m4
%{__autoconf}
%{__automake}
cd ../libs
%{__libtoolize}
%{__aclocal} -I ../m4
%{__autoconf}
%{__automake}
cd ardour
%{__libtoolize}
%{__aclocal} -I ../../m4
%{__autoconf}
%{__automake}
cd ../gtk-canvas
%{__aclocal} -I ../../m4
%{__autoconf}
%{__automake}
cd ../gtkmmext
%{__aclocal} -I ../../m4
%{__autoconf}
%{__automake}
cd ../midi++
%{__aclocal} -I ../../m4
%{__autoconf}
%{__automake}
cd ../pbd
%{__aclocal} -I ../../m4
%{__autoconf}
%{__automake}
cd ../soundtouch
%{__aclocal} -I ../../m4
%{__autoconf}
%{__automake}
cd ../..
# ksi doesn't build for a moment
%configure \
	--disable-ksi \
	%{!?debug:--enable-optimize}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CONTRIBUTORS FAQ README TODO TRANSLATORS
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%dir %{_sysconfdir}/ardour
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ardour/*.rc
%{_desktopdir}/ardour.desktop
