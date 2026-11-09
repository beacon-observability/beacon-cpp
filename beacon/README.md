# Beacon C++ Development

The initial product scope is a source-maintained C++ API/SDK and exporters for
explicit application instrumentation. The full upstream source and history are
preserved; there is no GitHub fork relationship. No prebuilt Beacon agent or
package-index distribution is published.

## Local SDK build

Requirements for this initial check: Linux, a C++17 compiler, CMake 3.16 or later,
and a build tool. This is a narrow development configuration, not a support matrix.
It disables optional network exporters and uses the C++17 standard library to
avoid fetching optional dependencies.

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_STANDARD=17 \
  -DOTELCPP_WITH_STL=CXX17 -DOTELCPP_BUILD_TESTING=OFF \
  -DOTELCPP_WITH_BENCHMARK=OFF -DOTELCPP_WITH_EXAMPLES=ON \
  -DOTELCPP_WITH_FUNC_TESTS=OFF
cmake --build build --parallel 4
./build/examples/simple/example_simple
cmake --install build --prefix "$PWD/build/install"
cmake -S beacon/smoke -B build/consumer -DCMAKE_PREFIX_PATH="$PWD/build/install"
cmake --build build/consumer --parallel 4
./build/consumer/beacon_cpp_smoke
```

The installed-package consumer must print a `beacon-cpp-smoke` span and
`service.name: beacon-cpp-smoke`. This validates source build, CMake installation,
and explicit trace export to stdout; it does not validate OTLP or a backend.
See [the validation record](VALIDATION.md) for actual results.

For additional build configurations consult the preserved [upstream installation
guide](../INSTALL.md). Optional third-party versions are recorded in
[third_party_release](../third_party_release), with submodule commits pinned in Git.
When needed, initialize only the required submodules; do not update them to moving
branch heads. Full upstream tests require additional dependencies and are separate
from the development smoke check above.

## Automation

Inherited workflows are preserved as inactive files in
[upstream-github](upstream-github/), together with upstream review and bot settings.
No inherited package publication, container upload, issue automation, or upstream
maintainer assignment is active. Review destinations, permissions, identities, and
cost before introducing Beacon CI or restoring any upstream automation.
