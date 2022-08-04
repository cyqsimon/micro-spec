%global debug_package %{nil}

# Go 1.17 is required for now, otherwise errors on F35
# EPEL7-9 are fine
%if 0%{?rhel} || 0%{?fedora} >= 36
    %global _need_static_go_bin 0
%else
    %global _need_static_go_bin 1
%endif

Name:           micro
Version:        2.0.11
Release:        1%{?dist}
Summary:        Modern and intuitive terminal-based text editor

License:        MIT
URL:            https://micro-editor.github.io/
Source0:        https://github.com/zyedidia/micro/archive/v%{version}.tar.gz

Requires:       hicolor-icon-theme
BuildRequires:  gcc git make
%if ! %{_need_static_go_bin}
BuildRequires:  golang
%endif

%description
micro is a terminal-based text editor that aims to be easy to use and intuitive,
while also taking advantage of the capabilities of modern terminals.

As its name indicates, micro aims to be somewhat of a successor to the nano editor
by being easy to install and use. It strives to be enjoyable as a full-time editor
for people who prefer to work in a terminal, or those who regularly edit files over SSH.

%prep
%autosetup

%if %{_need_static_go_bin}
    _GO_VER="1.19"
    %ifarch x86_64
        _ARCH=amd64
    %endif
    %ifarch aarch64
        _ARCH=arm64
    %endif
    if [[ -z "${_ARCH}" ]]; then
        echo "Unsupported architecture!"
        exit 1
    fi
    _GO_DL_NAME="go${_GO_VER}.linux-${_ARCH}.tar.gz"
    _GO_DL_URL="https://go.dev/dl/${_GO_DL_NAME}"

    curl -Lfo "${_GO_DL_NAME}" "${_GO_DL_URL}"
    tar -xf "${_GO_DL_NAME}"
    # bins in go/bin
%endif

%build
%if %{_need_static_go_bin}
    _GO_BIN_DIR=$(realpath "go/bin")
    export PATH="${_GO_BIN_DIR}:${PATH}"
%endif

%global _commit 225927b
make VERSION=%{version} HASH=%{_commit} build

%check
%if %{_need_static_go_bin}
    _GO_BIN_DIR=$(realpath "go/bin")
    export PATH="${_GO_BIN_DIR}:${PATH}"
%endif

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
* Thu Aug 04 2022 cyqsimon - 2.0.11-1
- Release 2.0.11
