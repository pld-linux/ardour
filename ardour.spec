# TODO:
# - use external libraries if possible (sigc++1 and gtkmm1)
# - .desktop
# - check BR (ladspa - is it really needed at compile time?)
# - optflags (in gtk_ardour, libs/{ardour,gtkmmext,midi++,pbd,soundtouch}
#
%define		_beta beta2
Summary:	Multitrack hard disk recorder
Summary(pl):	Wieloscie¿kowy magnetofon nagrywaj±cy na twardym dysku
Name:		ardour
Version:	0.9
Release:	0.%{_beta}.1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/ardour/%{name}-%{version}%{_beta}.tar.bz2
# Source0-md5:	91db0b724e5183e7c92408a986aa17ea
Patch0:		%{name}-system-libs.patch
URL:		http://ardour.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	gtk+-devel >= 1.0.0
BuildRequires:	gtkmm1-devel >= 1.2.6
BuildRequires:	jack-audio-connection-kit-devel >= 0.66.0
BuildRequires:	ladspa-devel
BuildRequires:	libart_lgpl >= 2.3
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
Linuksa, wykorzystuj±cy interfejsu d¼wiêkowe obs³ugiwane przez ALSA.
Obs³uguje próbki do 32 bitów, 24+ kana³ów do 96kHz, pe³n± kontrolê
MMC, niedestruktywny, nieliniowy edytor oraz wtyczki LADSPA.

%prep
%setup -q -n %{name}-%{version}%{_beta}
%patch -p1

install -d m4
# extract AM_BUILD_ENVIRONMENT (patched!)
tail +787 aclocal.m4 > m4/buildenv.m4
# AC_UNIQUIFY_{LAST,FIRST}
tail +6685 libs/ardour/aclocal.m4 >> m4/buildenv.m4
# AC_POSIX_RTSCHED
tail +870 libs/pbd/aclocal.m4 | head -118 >> m4/buildenv.m4

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
	--disable-ksi

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README ReleaseNotes* TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/pixmaps
%{_datadir}/%{name}/splash.ppm
%{_mandir}/man1/*
%dir %{_sysconfdir}/ardour
%{_sysconfdir}/ardour/*.rc
