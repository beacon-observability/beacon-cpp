# Beacon C++ 0.1.0 Validation

The release targets Linux x86_64, Debian 13, GCC 14.2.0, CMake 3.31.6,
C++17 standard-library mode, Release static libraries, ABI v1, and OTLP/HTTP
Protobuf traces to OpenTelemetry Collector Contrib 0.135.0. The source baseline
is upstream `v1.30.0` (`c7b64ec660c1b6c65dff0932b3d1c3483bc6db64`), with
protocol submodule `790608c4d51e6ffc12210b541e8514cbed9e91a4`.

## Release evidence

The immutable [v0.1.0 release notes](https://github.com/beacon-observability/beacon-cpp/releases/tag/v0.1.0)
and attached `release-manifest.json` record actual regression counts, source and
artifact provenance, dependency versions, exact trace IDs, and downloaded-asset
acceptance. Publication requires successful completion of all checks below;
this checklist alone is not a statement that a test passed.

- Run the 38 selected upstream targets listed in
  [regression-targets.txt](acceptance/regression-targets.txt), including trace API,
  context propagation, resource identity, samplers, batch processing and stress,
  protocol recordables, and OTLP/HTTP exporter tests. Record failures and disabled cases.
- Build from the extracted source asset with its bundled protocol sources and
  external dependencies, install to an isolated prefix, and compile the separate
  [CMake consumer](acceptance/CMakeLists.txt) against that installed package.
- Run the [application](acceptance/main.cc) against the pinned real Collector and
  verify the exact three-span trace, service identity, parent relationships, and
  final pre-exit batch delivery using [verify.py](acceptance/verify.py).
- Verify that an exporter reports failure within a bounded time for a refused
  local connection. This does not establish durable retry or recovery guarantees.
- Download the published assets, verify SHA-256 hashes, and repeat source-build,
  installed-consumer, receiver, and failure acceptance from that archive.

Run commands and receiver image identity are in the
[acceptance guide](acceptance/README.md) and [installation guide](INSTALL.md).

## Acceptance limits

This selected test set is not the full upstream matrix. Metrics, Logs, gRPC,
DataKit or backend storage, TLS/authentication, other platforms/toolchains/ABI
modes, binary package compatibility, Profiling, Security, and automatic
instrumentation are outside first-release acceptance. SDK metadata and CMake
package version remain upstream `1.30.0`; Beacon distribution version is `0.1.0`.
The bootstrap record below is older, narrower evidence and does not define the
release acceptance scope.

---

# Bootstrap Development Validation

Baseline: upstream `v1.30.0`, commit
`c7b64ec660c1b6c65dff0932b3d1c3483bc6db64`.

Environment: Linux x86_64 (Ubuntu 24.04), GCC 13.3.0, CMake 3.31.6,
C++17 standard-library mode, Release build, static libraries, default ABI v1.
Commands are documented in [the development guide](README.md).

Validation date: 2026-11-09.

| Check | Result |
| --- | --- |
| Configure and build API/SDK, default exporters, and enabled examples | Passed |
| Run upstream `example_simple` | Passed; stdout spans have trace and parent identities |
| Install static libraries, headers, and CMake package into an isolated prefix | Passed |
| Configure and build a separate consumer with `find_package(opentelemetry-cpp)` | Passed |
| Run installed-package consumer and shut down provider | Passed; exit code 0 |
| Inspect consumer output | `beacon-cpp-smoke` span, matching `service.name`, nonzero 128-bit trace ID and 64-bit span ID |
| Relative documentation links and `git diff --check` | Passed |

The consumer source is in [smoke](smoke/). It links the installed trace SDK and
ostream exporter, rather than using source-tree include paths.

## Not validated during bootstrap

- Full upstream unit, functional, or benchmark suites (disabled for this build).
- OTLP exporters or delivery to DataKit, a Collector, or another backend.
- Other operating systems, architectures, compilers, C++ standards, or ABI modes.
- Clean release archive installation, binary packaging, and upgrade/rollback.
- Automatic instrumentation, Profiling, and Beacon Security (not implemented here).

This record is development evidence, not an official Beacon release or production
support commitment. Upstream stability claims are not equivalent to Beacon validation.
