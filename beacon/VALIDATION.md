# Initial Development Validation

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

## Not validated

- Full upstream unit, functional, or benchmark suites (disabled for this build).
- OTLP exporters or delivery to DataKit, a Collector, or another backend.
- Other operating systems, architectures, compilers, C++ standards, or ABI modes.
- Clean release archive installation, binary packaging, and upgrade/rollback.
- Automatic instrumentation, Profiling, and Beacon Security (not implemented here).

This record is development evidence, not an official Beacon release or production
support commitment. Upstream stability claims are not equivalent to Beacon validation.
