"""Render the E2E results as a GitHub step summary or a Slack payload.

Feature and scenario names, and the step that failed, come from pytest-bdd's
Cucumber JSON. The outcome of each scenario comes from the JUnit XML: Cucumber
JSON reports a scenario stopped by ``pytest.skip`` as passed, and it misses
errors raised outside the steps.

Usage: e2e_report.py summary|slack <reports-dir>
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

LABELS = {"failed": "❌ Failed", "skipped": "⏭️ Skipped", "passed": "✅ Passed"}
ICONS = {"failed": "❌", "skipped": "⏭", "passed": "✅"}
MAX_ERROR_CHARS = 200


def junit_outcomes(reports: Path) -> dict[str, str]:
    outcomes = {}
    for path in sorted(reports.glob("*.xml")):
        for tc in ET.parse(path).getroot().iter("testcase"):
            if tc.find("failure") is not None or tc.find("error") is not None:
                outcome = "failed"
            elif tc.find("skipped") is not None:
                outcome = "skipped"
            else:
                outcome = "passed"
            outcomes[tc.get("name", "")] = outcome
    return outcomes


def error_line(message: str) -> str:
    """The assertion pytest reports, e.g. ``AssertionError: Expected 200, ...``."""
    lines = [line[1:].strip() for line in message.splitlines() if line.startswith("E ")]
    if not lines:
        lines = [line.strip() for line in message.splitlines() if line.strip()][-1:]
    text = lines[0] if lines else ""
    if len(text) > MAX_ERROR_CHARS:
        text = text[: MAX_ERROR_CHARS - 1] + "…"
    return text


def collect(reports: Path) -> dict[str, list[dict]]:
    """Group scenarios by feature as {feature: [{name, status, step, error}]}."""
    outcomes = junit_outcomes(reports)
    features: dict[str, list[dict]] = {}
    seen = set()
    for path in sorted(reports.glob("*.json")):
        for feature in json.loads(path.read_text()):
            for element in feature["elements"]:
                seen.add(element["id"])
                steps = element["steps"]
                failed_step = next(
                    (s for s in steps if s["result"]["status"] == "failed"), None
                )
                status = outcomes.get(element["id"], "failed")
                if failed_step is not None:
                    status = "failed"
                features.setdefault(feature["name"], []).append(
                    {
                        "name": element["name"],
                        "status": status,
                        "step": (
                            f"{failed_step['keyword']} {failed_step['name']}"
                            if failed_step
                            else None
                        ),
                        "error": (
                            error_line(failed_step["result"].get("error_message", ""))
                            if failed_step
                            else None
                        ),
                    }
                )
    # A test that never reached its first step has no Cucumber entry.
    for name, outcome in outcomes.items():
        if name not in seen:
            features.setdefault("Other", []).append(
                {"name": name, "status": outcome, "step": None, "error": None}
            )
    return features


def totals(features: dict[str, list[dict]]) -> dict[str, int]:
    scenarios = [s for group in features.values() for s in group]
    failed = sum(s["status"] == "failed" for s in scenarios)
    skipped = sum(s["status"] == "skipped" for s in scenarios)
    return {
        "tests": len(scenarios),
        "failed": failed,
        "skipped": skipped,
        "passed": len(scenarios) - failed - skipped,
    }


def feature_icon(scenarios: list[dict]) -> str:
    return "❌" if any(s["status"] == "failed" for s in scenarios) else "✅"


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def step_summary(features: dict[str, list[dict]]) -> str:
    lines = ["## E2E Test Results\n"]
    if not features:
        lines.append("**❌ No E2E report was produced.**\n")
    for name, scenarios in features.items():
        lines.append(f"### {feature_icon(scenarios)} {name}\n")
        lines.append("| Scenario | Status | Failed step |")
        lines.append("|----------|--------|-------------|")
        for s in scenarios:
            detail = ""
            if s["step"]:
                detail = f"`{s['step']}`"
                if s["error"]:
                    detail += f" — {s['error']}"
            lines.append(
                f"| {md_cell(s['name'])} | {LABELS[s['status']]} | {md_cell(detail)} |"
            )
        lines.append("")
    t = totals(features)
    overall = "✅" if t["failed"] == 0 and features else "❌"
    lines.append("---\n")
    lines.append(
        f"**{overall} Total: {t['passed']}/{t['tests']} passed, "
        f"{t['failed']} failed, {t['skipped']} skipped**\n"
    )
    return "\n".join(lines) + "\n"


def slack_escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slack_payload(features: dict[str, list[dict]]) -> dict:
    t = totals(features)
    if not features:
        overall = "❌ no report produced"
    elif t["failed"] == 0:
        overall = "✅ All passed"
    else:
        overall = f"❌ {t['failed']} failed"
    sections = []
    for name, scenarios in features.items():
        section = [f"{feature_icon(scenarios)} *{slack_escape(name)}*"]
        for s in scenarios:
            section.append(f"  {ICONS[s['status']]} {slack_escape(s['name'])}")
            if s["step"]:
                section.append(f"      ↳ failed at `{slack_escape(s['step'])}`")
                if s["error"]:
                    section.append(f"      {slack_escape(s['error'])}")
        sections.append("\n".join(section))
    run_url = os.environ["RUN_URL"]
    lines = [
        f"*substack-gateway-oss E2E Results - {overall}*",
        f"Total: {t['passed']}/{t['tests']} passed, {t['skipped']} skipped",
        f"Trigger: {os.environ['GITHUB_EVENT_NAME']} · {os.environ['GITHUB_SHA'][:7]}",
        "",
        *sections,
        "",
        f"<{run_url}|View run>",
    ]
    return {"text": "\n".join(lines), "unfurl_links": False, "unfurl_media": False}


def main() -> None:
    mode, reports = sys.argv[1], Path(sys.argv[2])
    features = collect(reports)
    if mode == "summary":
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(step_summary(features))
    elif mode == "slack":
        with open(os.environ["SLACK_PAYLOAD_PATH"], "w") as f:
            json.dump(slack_payload(features), f, ensure_ascii=False)
    else:
        sys.exit(f"unknown mode {mode!r}")


if __name__ == "__main__":
    main()
