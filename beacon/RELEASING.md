# Beacon C++ Release Prerequisites

No official Beacon C++ release exists. The upstream `1.30.0` source version and
imported history are not Beacon release artifacts.

Before a first independent Beacon release:

1. Define a Beacon version and tag namespace distinct from upstream tags; agree on
   source archives, optional binary formats, publishing channels, and maintainers.
   Verify ownership before registering any ecosystem package or command name.
2. Pin release source, upstream baseline, submodules, and build dependencies; retain
   licenses and third-party notices. Record compiler, C++ standard, ABI options,
   operating system, architecture, and supported consumers.
3. Run upstream regression tests and clean installed-artifact acceptance for the
   claimed matrix. Validate actual OTLP delivery to the declared receiver, including
   service identity, trace relationships, shutdown delivery, and error handling.
4. Build immutable artifacts once from the accepted source. Publish checksums,
   provenance, release notes, limitations, and upgrade/rollback instructions. Confirm
   publishing permissions and isolate publication credentials from ordinary testing.
5. Download the published artifacts and repeat acceptance. Never replace an existing
   release artifact to fix a defect; publish a new version.
6. Update the Beacon product index and synchronize bilingual Beacon documentation
   through a PR, citing the published release and actual acceptance evidence.

Profiling, automatic instrumentation, Security, and additional platforms require
separate implementation and validation before any support claim. No inherited
upstream publishing workflow is a Beacon release entry point.
