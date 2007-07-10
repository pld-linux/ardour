Summary:	Multitrack hard disk recorder
Summary(pl.UTF-8):	Wielościeżkowy magnetofon nagrywający na twardym dysku
Name:		ardour
Version:	2.0.3
Release:	0.1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://ardour.org/files/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	d047d3f9e7b5b4bf80980c5b267c1068
Source1:	%{name}.desktop
Patch3:		%{name}-nptl_fix.patch
URL:		http://ardour.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	boost-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel >= 2.8.0
BuildRequires:	gtkmm-devel >= 2.8.0
BuildRequires:	jack-audio-connection-kit-devel >= 0.98.0
BuildRequires:	libart_lgpl >= 2.3.16
BuildRequires:	libgnomecanvas-devel >= 2.0
BuildRequires:	liblrdf-devel >= 0.3
BuildRequires:	liblo-devel 
BuildRequires:	libpng-devel
BuildRequires:	libsamplerate-devel >= 0.1.2
BuildRequires:	libsigc++1-devel >= 0.8.8
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.5.0
BuildRequires:	python >= 2.3.4
BuildRequires:	pkgconfig >= 0.20
BuildRequires:	scons >= 0.96
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
%patch3 -p1

%build
%{scons}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{scons} install \
	DESTDIR=$RPM_BUILD_ROOT \
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ardour/*.rc
%{_desktopdir}/ardour.desktop
