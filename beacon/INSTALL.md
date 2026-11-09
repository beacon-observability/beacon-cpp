# Beacon C++ 0.1.0 Source Installation

Beacon C++ 0.1.0 is a source SDK distribution based on OpenTelemetry C++ 1.30.0.
Applications explicitly initialize an SDK and instrument code. CMake targets,
header paths, namespaces, and the SDK-reported version remain OpenTelemetry's;
`1.30.0` in SDK metadata is not the Beacon distribution version.

## Validated configuration

The first release targets Linux x86_64, Debian 13, GCC 14.2.0, CMake 3.31.6,
C++17 standard-library mode, static SDK libraries, default ABI v1, and
OTLP/HTTP Protobuf traces to OpenTelemetry Collector Contrib 0.135.0. The release
notes contain the actual artifact acceptance results and dependency versions.
This is not a claim for other platforms, compilers, receivers, or signals.

Build prerequisites on Debian 13:

```sh
apt-get update
apt-get install -y g++ cmake make libprotobuf-dev protobuf-compiler \
  libcurl4-openssl-dev nlohmann-json3-dev
```

Test tooling additionally uses `libgtest-dev`, `libgmock-dev`, and Python 3.
The archive includes the pinned OpenTelemetry protocol source and its license;
Protobuf, curl, and JSON libraries are external dependencies. Optional submodules
are not bundled or qualified. The archive build below does not fetch them.

## Verify and build

Download `beacon-cpp-0.1.0-source.tar.gz`, `release-manifest.json`, and `SHA256SUMS`
from [the release](https://github.com/beacon-observability/beacon-cpp/releases/tag/v0.1.0)
into one directory. The manually attached source asset includes protocol sources;
GitHub's automatically generated source downloads do not include submodules.

```sh
sha256sum --check SHA256SUMS
tar -xzf beacon-cpp-0.1.0-source.tar.gz
cd beacon-cpp-0.1.0
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_STANDARD=17 \
  -DOTELCPP_WITH_STL=CXX17 -DOTELCPP_BUILD_TESTING=OFF \
  -DOTELCPP_WITH_BENCHMARK=OFF -DOTELCPP_WITH_EXAMPLES=OFF \
  -DOTELCPP_WITH_FUNC_TESTS=OFF -DOTELCPP_WITH_OTLP_HTTP=ON \
  -DOTELCPP_WITH_HTTP_CLIENT_CURL=ON \
  -DOTELCPP_PROTO_PATH="$PWD/third_party/opentelemetry-proto"
cmake --build build --parallel 3
cmake --install build --prefix "$PWD/install"
cmake -S beacon/acceptance -B build/application \
  -DCMAKE_PREFIX_PATH="$PWD/install"
cmake --build build/application --parallel 3
./build/application/beacon_cpp_otlp http://127.0.0.1:4318/v1/traces
```

Start a reachable Collector OTLP/HTTP receiver first. In a container,
`127.0.0.1` refers to that container. The example's trace-specific URL includes
`/v1/traces`; it uses binary Protobuf, explicitly sets service identity, and
shuts down the batch processor after ending the spans. It prints the generated
trace ID, but application exit status alone does not prove reception.

The runnable example creates `request`, its `work` child, and `exit-final` before
provider shutdown. Follow [receiver verification](acceptance/README.md) to check
that all three arrive with the expected service, trace ID, and parent IDs.
Receiver acceptance does not establish storage in a downstream backend.

## Application integration

Use `find_package(opentelemetry-cpp CONFIG REQUIRED)` and link
`opentelemetry-cpp::trace` plus `opentelemetry-cpp::otlp_http_exporter`, as shown in
[the complete CMake consumer](acceptance/CMakeLists.txt) and
[application source](acceptance/main.cc). Initialize one provider, define service
identity, create and end spans around application work, and shut down after
all application spans have ended. Propagation across network boundaries requires
explicit context injection and extraction; it is not automatic instrumentation.

## Upgrade and rollback

Build each accepted Beacon version into a separate prefix. Retain the previous
source asset, checksums, dependency configuration, and application artifact.
Reconfigure and rebuild the application against the new prefix; do not mix headers
and libraries from different SDK versions or ABI modes. Validate the application
and its receiver before deployment. To roll back, restore the previously accepted
application and SDK prefix together and repeat trace verification.

This release does not publish a package-index package, prebuilt agent, or binary
compatibility guarantee. Metrics, Logs, OTLP/gRPC, DataKit, TLS/authentication,
Profiling, Security, and automatic instrumentation are outside first-release
acceptance. No delivery guarantee is implied during receiver outages; the
[acceptance program](acceptance/main.cc) separately checks a bounded export failure.
