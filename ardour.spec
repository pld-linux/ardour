Summary:	Multitrack hard disk recorder
Summary(pl):	Wielo¶cie¿kowy magnetofon nagrywaj±cy na twardym dysku
Name:		ardour
Version:	0.9
%define	_beta	beta18
Release:	0.%{_beta}.3
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://ardour.org/releases/%{name}-%{version}%{_beta}.tar.bz2
# Source0-md5:	f0ab7b6fccb67b209b1f11edea49fbf1
Source1:	%{name}.desktop
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-ac_cleanup.patch
Patch3:		%{name}-nptl_fix.patch
URL:		http://ardour.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel >= 1.0.0
#BuildRequires:	gtk-canvas-devel >= 0.1
BuildRequires:	gtkmm1-devel >= 1.2.6
BuildRequires:	jack-audio-connection-kit-devel >= 0.98.0
BuildRequires:	libart_lgpl >= 2.3.16
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
tail -n +837 aclocal.m4 > m4/buildenv.m4
# AM_OPT_FLAGS (patched!)
tail -n +862 libs/pbd/aclocal.m4 | head -n 33 >> m4/buildenv.m4

%{__perl} -pi -e 's/pt_PT/pt/' gtk_ardour/po/LINGUAS
mv -f gtk_ardour/po/{pt_PT,pt}.po

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

# it shouldn't be there
rm -f $RPM_BUILD_ROOT%{_datadir}/ardour/libardour.{la,a}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog DOCUMENTATION/{AUTHORS,CONTRIBUTORS,FAQ,README,TODO,TRANSLATORS}
%lang(es) %doc DOCUMENTATION/{AUTHORS.es,CONTRIBUTORS.es,README.es}
%lang(fr) %doc DOCUMENTATION/README.fr
%lang(it) %doc DOCUMENTATION/README.it
%lang(ru) %doc DOCUMENTATION/README.ru
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/ardour.1*
%lang(es) %{_mandir}/es/man1/ardour.1*
%lang(fr) %{_mandir}/fr/man1/ardour.1*
%lang(ru) %{_mandir}/ru/man1/ardour.1*
%dir %{_sysconfdir}/ardour
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ardour/*.rc
%{_desktopdir}/ardour.desktop
