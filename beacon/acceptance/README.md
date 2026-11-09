# Trace Release Acceptance

This directory contains a separate installed-package consumer, a Collector
configuration, an exact-trace verifier, and the selected upstream regression list.
Use only synthetic trace data. Requires Python 3, Docker for the receiver, and
the [source build prerequisites](../INSTALL.md).

## Regression checks

Configure a source build with the installation options, but set
`OTELCPP_BUILD_TESTING=ON` and install GTest/GMock. Then run:

```sh
python3 beacon/acceptance/regressions.py build --parallel 3 --output build/regressions
```

This builds and runs the 38 targets in `regression-targets.txt`. The JSON summary
records tests, failures, and disabled cases. It does not represent the complete
upstream test matrix. Benchmarks and optional-signal/platform suites are excluded.

## Actual OTLP/HTTP reception

Create an empty writable output directory. Start Collector Contrib 0.135.0 with
[this configuration](collector.yaml), mapping the config to `/etc/otelcol/config.yaml`,
the output directory to `/out`, and an available localhost port to container port
4318. The release used image digest
`sha256:89107a3a8f4636a396927edf7025bb9614b8da2d92f4cc3f43109e8d115736e2`.
For example, from the source root:

```sh
mkdir -p build/receiver
docker run -d --name beacon-cpp-acceptance-receiver --user "$(id -u):$(id -g)" \
  -p 127.0.0.1:14318:4318 \
  -v "$PWD/beacon/acceptance/collector.yaml:/etc/otelcol/config.yaml:ro" \
  -v "$PWD/build/receiver:/out" \
  otel/opentelemetry-collector-contrib@sha256:89107a3a8f4636a396927edf7025bb9614b8da2d92f4cc3f43109e8d115736e2 \
  --config=/etc/otelcol/config.yaml
./build/application/beacon_cpp_otlp http://127.0.0.1:14318/v1/traces > build/application.json
docker stop beacon-cpp-acceptance-receiver
python3 beacon/acceptance/verify.py build/receiver/traces.json build/application.json
docker rm beacon-cpp-acceptance-receiver
```

Wait for the receiver to finish starting before running the application. The
verifier requires exactly three spans for the application's unique trace ID,
service identity, distinct nonzero IDs, parent relationships, and `exit-final`
delivery during shutdown. It deliberately reports `backend_verified: false`.

## Failure handling

Use a loopback endpoint without a listener:

```sh
./build/application/beacon_cpp_otlp http://127.0.0.1:1/v1/traces --expect-failure
```

This directly checks that the exporter reports failure within five seconds
(timeout 500 ms, one attempt). Success prints `export_failed` and `bounded` as
true. This is a local refused-connection check, not outage durability, retry,
TLS, authentication, or backend qualification. HTTP client failure/retry
regressions are covered separately by the selected upstream exporter tests.
