# Beacon C++

Beacon C++ is an independent downstream of the complete official
[OpenTelemetry C++](https://github.com/open-telemetry/opentelemetry-cpp) API, SDK,
and exporters. It preserves upstream Git history, source layout, package identities,
and the [Apache-2.0 license](LICENSE).

**Under development. No official Beacon C++ release has been published.**
Applications explicitly integrate the SDK and instrument their source code. This
initial import does not introduce automatic instrumentation, Profiling, or Beacon
Security. Upstream capabilities and platform claims are not Beacon acceptance evidence.

## Development

- [Development and local build](beacon/README.md)
- [Upstream baseline and synchronization](beacon/UPSTREAM.md)
- [Release prerequisites](beacon/RELEASING.md)
- [Initial validation record](beacon/VALIDATION.md)
- [Original upstream README](README.upstream.md)
- [Beacon product index](https://github.com/beacon-observability/beacon)

The adopted upstream baseline is **v1.30.0**. Its version numbers identify the
upstream SDK, not a Beacon release. Existing OpenTelemetry CMake targets and
namespaces remain unchanged. Development documentation tracks `main` and may change.
