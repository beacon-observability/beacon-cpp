# Beacon C++ Release Prerequisites

Beacon C++ uses independent `v0.x.y` release tags. The initial source distribution
is `v0.1.0`; the upstream `1.30.0` source version and `upstream/*` refs are separate.
The release maintainer publishes the accepted source and evidence through the
`beacon-observability/beacon-cpp` GitHub repository; no package-index identity is used.

For each independent Beacon release:

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

## Initial source asset

With the protocol submodule initialized at its recorded commit, create the archive
from a clean, committed revision:

```sh
python3 beacon/package_source.py --revision HEAD --output /path/to/release-assets
```

The packager consumes Git objects rather than working-tree files, bundles only
the protocol submodule needed for the declared build, normalizes archive metadata,
and produces `beacon-cpp-0.1.0-source.tar.gz`. Before a later version, update the
packager's distribution version and repeat acceptance; never overwrite v0.1.0.

Record the full source commit, upstream and protocol commits, dependency/toolchain
versions, validated scope, regression counts, receiver image digest, artifact hash,
and actual reception result in `release-manifest.json`. Create `SHA256SUMS` for
the source asset and manifest. Validate the extracted archive, attach exactly those
accepted files to the release, and repeat verification from downloaded public assets.
Do not use GitHub's automatic source archive for the bundled-protocol build.
