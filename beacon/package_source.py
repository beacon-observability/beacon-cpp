#!/usr/bin/env python3
"""Package committed source and its pinned protocol submodule; never use dirty files."""
import argparse
import copy
import gzip
import io
from pathlib import Path
import subprocess
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument("--revision", default="HEAD")
parser.add_argument("--output", required=True, type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent

def git(*cmd, cwd=root):
    return subprocess.check_output(["git", "-C", str(cwd), *cmd])

revision = git("rev-parse", args.revision + "^{commit}").decode().strip()
line = git("ls-tree", revision, "third_party/opentelemetry-proto").decode().split()
protocol_revision = line[2]
protocol = root / "third_party/opentelemetry-proto"
assert git("rev-parse", "HEAD", cwd=protocol).decode().strip() == protocol_revision
stamp = int(git("show", "-s", "--format=%ct", revision))
args.output.mkdir(parents=True, exist_ok=True)
target = args.output / "beacon-cpp-0.1.0-source.tar.gz"
with target.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="") as zipped:
    with tarfile.open(fileobj=zipped, mode="w|") as output:
        for source, rev, prefix in [(root, revision, "beacon-cpp-0.1.0/"),
                                    (protocol, protocol_revision, "beacon-cpp-0.1.0/third_party/opentelemetry-proto/")]:
            with tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", rev, cwd=source))) as archive:
                for member in archive:
                    entry = copy.copy(member)
                    entry.name = prefix + member.name
                    if entry.islnk():
                        entry.linkname = prefix + entry.linkname
                    entry.mtime = stamp
                    entry.uid = entry.gid = 0
                    entry.uname = entry.gname = ""
                    entry.pax_headers = {}
                    output.addfile(entry, archive.extractfile(member) if member.isfile() else None)
print(target)
