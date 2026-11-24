"""Rework after the first "changes requested" review, from the GitHub API.

Usage: python3 rework.py   (needs the GitHub CLI `gh`, logged in)
For each merged pull request that got a "changes requested" review, counts the commits dated
after the first such review and the lines they changed. Merge commits from the base branch are
left out. Writes data/rework.csv and prints the totals used in README.md.
"""
import csv
import json
import subprocess
from pathlib import Path

REPO = "apache/shardingsphere"
PRS = [38327, 38352, 38449, 38659, 38685]
AUTHOR = "ym0506"


def gh(path, paginate=True):
    cmd = ["gh", "api"] + (["--paginate"] if paginate else []) + [path]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    return json.loads(out.replace("][", ",")) if paginate else json.loads(out)


def main():
    rows = []
    for n in PRS:
        reviews = gh(f"repos/{REPO}/pulls/{n}/reviews?per_page=100")
        first = min(r["submitted_at"] for r in reviews if r["state"] == "CHANGES_REQUESTED")
        approved = max(r["submitted_at"] for r in reviews if r["state"] == "APPROVED")
        commits = gh(f"repos/{REPO}/pulls/{n}/commits?per_page=100")
        before_lines = after_lines = after_commits = merges = 0
        for c in commits:
            detail = gh(f"repos/{REPO}/commits/{c['sha']}", paginate=False)
            if len(detail["parents"]) > 1:
                merges += 1
                continue
            lines = detail["stats"]["additions"] + detail["stats"]["deletions"]
            if c["commit"]["committer"]["date"] > first:
                after_commits += 1
                after_lines += lines
            else:
                before_lines += lines
        rows.append({"number": n, "first_changes_requested": first[:10], "approved": approved[:10],
                     "commits_before": len(commits) - merges - after_commits, "lines_before": before_lines,
                     "rework_commits": after_commits, "rework_lines": after_lines, "merge_commits_left_out": merges})
    out = Path(__file__).parent / "data" / "rework.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)
    tb = sum(r["lines_before"] for r in rows)
    ta = sum(r["rework_lines"] for r in rows)
    print("rework commits:", sum(r["rework_commits"] for r in rows), "| lines before first review:", tb,
          "| rework lines:", ta, "| rework / before:", round(ta / tb, 2))


if __name__ == "__main__":
    main()
