#!/usr/bin/env python3
"""Verify Collector file-exported spans against an application's exact trace ID."""
import argparse
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("collector", type=Path)
parser.add_argument("application", type=Path)
args = parser.parse_args()
expected = json.loads(args.application.read_text().strip().splitlines()[-1])
assert expected["shutdown_ok"] is True
trace_id = expected["trace_id"]
root_id = expected["root_span_id"]
assert re.fullmatch(r"[0-9a-f]{32}", trace_id) and int(trace_id, 16)
assert re.fullmatch(r"[0-9a-f]{16}", root_id) and int(root_id, 16)
spans = []
for line in args.collector.read_text().splitlines():
    for resource in json.loads(line).get("resourceSpans", []):
        attrs = {a["key"]: a["value"] for a in resource["resource"].get("attributes", [])}
        for scope in resource.get("scopeSpans", []):
            for span in scope.get("spans", []):
                if span["traceId"] != trace_id:
                    continue
                assert attrs["service.name"]["stringValue"] == "beacon-cpp-acceptance"
                assert attrs["service.version"]["stringValue"] == "0.1.0"
                assert scope["scope"]["name"] == "beacon-cpp-acceptance"
                assert int(span["endTimeUnixNano"]) >= int(span["startTimeUnixNano"]) > 0
                assert re.fullmatch(r"[0-9a-f]{16}", span["spanId"])
                assert int(span["spanId"], 16)
                spans.append(span)
assert len(spans) == 3, f"Expected exactly 3 spans, got {len(spans)}"
by_name = {s["name"]: s for s in spans}
assert set(by_name) == {"request", "work", "exit-final"}
assert len({s["spanId"] for s in spans}) == 3
assert by_name["request"]["spanId"] == root_id
assert by_name["request"].get("parentSpanId", "") in ("", "0000000000000000")
for name in ["work", "exit-final"]:
    assert by_name[name]["parentSpanId"] == root_id
assert {a["key"]: a["value"] for a in by_name["work"]["attributes"]}["beacon.acceptance"]["boolValue"] is True
print(json.dumps({"verified": True, "receiver": "OpenTelemetry Collector", "trace_id": trace_id,
                  "spans": 3, "service_identity": True, "parent_relationships": True,
                  "shutdown_delivery": True, "backend_verified": False}, indent=2))
