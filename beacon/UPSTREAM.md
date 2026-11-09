# Upstream Maintenance

- Official source: https://github.com/open-telemetry/opentelemetry-cpp
- Adopted release: [v1.30.0](https://github.com/open-telemetry/opentelemetry-cpp/releases/tag/v1.30.0)
- Adopted commit: `c7b64ec660c1b6c65dff0932b3d1c3483bc6db64`
- Local baseline ref: `upstream/v1.30.0` (upstream tag; not a Beacon release).
- Model: complete-source independent downstream with retained Git history.
- License: Apache-2.0; retain upstream and dependency notices.
- Initial Beacon changes: product documentation, installed-package smoke consumer,
  and deactivation of upstream-specific GitHub automation. No SDK behavior changes.
- No pre-existing Beacon C++ implementation was imported.

The source model permits future native SDK changes while retaining upstream build
layout and attribution. Existing library, target, namespace, and upstream version
identities remain unchanged; no new package name is registered.

## Synchronization

1. Add `upstream` pointing to the official source if it is absent. Select an official
   release, inspect its notes and full commit, and fetch its tag without overwriting
   an existing baseline ref.
2. Update local `main` with `git pull --ff-only origin main`, then create an isolated
   task worktree and branch. Merge the reviewed upstream tag there; do not replace
   the source tree or discard Beacon changes.
3. Resolve source conflicts, preserve licensing, and inspect changes to dependency
   pins, GitHub settings, and publication destinations. Newly introduced upstream
   workflows must be reviewed and deactivated before pushing.
4. Run the documented SDK build and installed-package smoke check, plus upstream
   regression tests and optional exporter tests relevant to the change. Record
   commands, environment, failures, and untested scope.
5. Update this baseline record and validation evidence and submit a review PR.
   A completed merge does not constitute a Beacon release.

Rollback an unsuccessful synchronization by abandoning its task branch, leaving
published tags and artifacts unchanged. Revert a merged change through a reviewed
commit rather than rewriting shared history.
