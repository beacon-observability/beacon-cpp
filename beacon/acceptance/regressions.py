#!/usr/bin/env python3
"""Build and run the explicit trace release regression set without claiming all tests."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("build", type=Path)
parser.add_argument("--parallel", default="3")
parser.add_argument("--output", required=True, type=Path)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
targets = Path(__file__).with_name("regression-targets.txt").read_text().split()
subprocess.run(["cmake", "--build", str(args.build), "--parallel", args.parallel,
                "--target", *targets], check=True)
summary = {"targets": [], "tests": 0, "failures": 0, "disabled": 0}
for name in targets:
    candidates = [p for p in args.build.rglob(name) if p.is_file() and os.access(p, os.X_OK)]
    assert len(candidates) == 1, (name, candidates)
    report = (args.output / (name + ".json")).resolve()
    subprocess.run([str(candidates[0].resolve()), "--gtest_output=json:" + str(report)],
                   check=True, timeout=180)
    result = json.loads(report.read_text())
    summary["targets"].append(name)
    for key in ["tests", "failures", "disabled"]:
        summary[key] += result[key]
(args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
