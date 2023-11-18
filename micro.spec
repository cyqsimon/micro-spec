%global debug_package %{nil}

Name:           micro
Version:        2.0.13
Release:        2%{?dist}
Summary:        Modern and intuitive terminal-based text editor

License:        MIT
URL:            https://micro-editor.github.io/
Source0:        https://github.com/zyedidia/micro/archive/v%{version}.tar.gz

Requires:       hicolor-icon-theme
BuildRequires:  git golang make

%global _api_base_url https://api.github.com/repos/zyedidia/micro/git
%global _tag_sha %(curl -Ssf %{_api_base_url}/ref/tags/v%{version} | jq -re '.object.sha')
%global _commit_sha %(curl -Ssf %{_api_base_url}/tags/%{_tag_sha} | jq -re '.object | select(.type == "commit") | .sha')
%global _commit_sha_short %(head -c 7 <<< %{_commit_sha})

%description
micro is a terminal-based text editor that aims to be easy to use and intuitive,
while also taking advantage of the capabilities of modern terminals.

As its name indicates, micro aims to be somewhat of a successor to the nano editor
by being easy to install and use. It strives to be enjoyable as a full-time editor
for people who prefer to work in a terminal, or those who regularly edit files over SSH.

%prep
%autosetup

%build
make VERSION=%{version} HASH=%{_commit_sha_short} build

%check
make test

%install
# bin
install -Dpm 755 %{name} %{buildroot}%{_bindir}/%{name}

# icon
install -Dpm 644 assets/micro-logo-mark.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
install -Dpm 644 -t %{buildroot}%{_datadir}/applications assets/packaging/micro.desktop

# manpage
mkdir -p %{buildroot}%{_mandir}/man1
install -Dpm 644 -t %{buildroot}%{_mandir}/man1 assets/packaging/micro.1

# doc
mkdir -p %{buildroot}%{_docdir}/%{name}
cp -rp runtime/help %{buildroot}%{_docdir}/%{name}/

%files
%license LICENSE LICENSE-THIRD-PARTY
%doc README.md
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1*
%{_docdir}/%{name}/*

%changelog
* Sat Nov 18 2023 cyqsimon - 2.0.13-2
- Automatically obtain commit SHA

* Sun Oct 22 2023 cyqsimon - 2.0.13-1
- Release 2.0.13

* Fri Sep 22 2023 cyqsimon - 2.0.12-2
- Release 2.0.12

* Thu Aug 04 2022 cyqsimon - 2.0.11-1
- Release 2.0.11
