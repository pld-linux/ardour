# TODO:
# - use external libraries if possible (sigc++1 and gtkmm1)
# - am/ac stuff
# - pl descs
# - .desktop
# - check BR (ladspa - is it really needed at comile time?)
#
%define		_beta beta2
Summary:	Multitrack hard disk recorder
Summary(pl):	Wieloscie¿kowy ...
Name:		ardour
Version:	0.9
Release:	0.%{_beta}.1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/sourceforge/ardour/%{name}-%{version}%{_beta}.tar.bz2
# Source0-md5:	91db0b724e5183e7c92408a986aa17ea
URL:		http://ardour.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	gtk+-devel
BuildRequires:	jack-audio-connection-kit-devel >= 0.66.0
BuildRequires:	ladspa-devel
BuildRequires:	libart_lgpl >= 2.3
BuildRequires:	liblrdf-devel >= 0.3.0
BuildRequires:	libsamplerate-devel >= 0.0.13
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2 >= 2.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A "professional" multitrack, multichannel audio recorder and DAW for
Linux, using ALSA-supported audio interfaces. Supports up to 32 bit
samples, 24+ channels at up to 96kHz, full MMC control,
non-destructive, non-linear editor, LADSPA plugins.

%description -l pl

%prep
%setup -q -n %{name}-%{version}%{_beta}

%build
# ksi dosen't build for a moment
%configure \
	--disable-ksi

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README ReleaseNotes* TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}/pixmaps
%{_datadir}/%{name}/splash.ppm
%{_mandir}/man1/*
%{_sysconfdir}/ardour/*.rc
