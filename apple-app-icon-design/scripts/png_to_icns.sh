#!/bin/zsh

set -euo pipefail

readonly script_directory="${0:A:h}"
readonly cache_directory="/private/tmp/png-to-icns-module-cache"

mkdir -p "${cache_directory}"

SWIFT_MODULECACHE_PATH="${cache_directory}" \
CLANG_MODULE_CACHE_PATH="${cache_directory}" \
    exec /usr/bin/swift "${script_directory}/png_to_icns.swift" "$@"
