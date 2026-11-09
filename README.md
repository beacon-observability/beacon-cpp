# Beacon C++

Beacon C++ is an independent downstream of the complete official
[OpenTelemetry C++](https://github.com/open-telemetry/opentelemetry-cpp) API, SDK,
and exporters. It preserves upstream Git history, source layout, package identities,
and the [Apache-2.0 license](LICENSE).

The first Beacon source release is **[v0.1.0](https://github.com/beacon-observability/beacon-cpp/releases/tag/v0.1.0)**.
It provides a fixed source archive with checksums and provenance. Release acceptance
is limited to Linux x86_64, Debian 13, GCC 14.2.0, C++17, ABI v1, static SDK libraries,
and OTLP/HTTP Protobuf traces to Collector Contrib 0.135.0.
Applications explicitly integrate the SDK and instrument their source code. This
source release does not introduce automatic instrumentation, Profiling, or Beacon
Security. Upstream capabilities and platform claims are not Beacon acceptance evidence.

## Use the source release

Follow the [versioned installation guide](https://github.com/beacon-observability/beacon-cpp/blob/v0.1.0/beacon/INSTALL.md)
for prerequisites, checksum verification, source build, application integration,
receiver checks, and rollback. Use the manually attached release archive, which
includes pinned protocol sources; GitHub's automatic source archives omit them.
No prebuilt binaries or package-index packages are published.

## Development

- [Development and local build](beacon/README.md)
- [Upstream baseline and synchronization](beacon/UPSTREAM.md)
- [Release prerequisites](beacon/RELEASING.md)
- [Validation scope and evidence](beacon/VALIDATION.md)
- [Original upstream README](README.upstream.md)
- [Beacon product index](https://github.com/beacon-observability/beacon)

The adopted upstream baseline is **v1.30.0**. Its version numbers identify the
upstream SDK, not a Beacon release. Existing OpenTelemetry CMake targets and
namespaces remain unchanged. Development documentation tracks `main` and may change.
