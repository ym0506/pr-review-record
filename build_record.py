"""Rebuild the review record from the GitHub API.

Usage: python3 build_record.py        (needs the GitHub CLI `gh`, logged in)
Writes data/prs.csv and data/rounds.csv and prints the summary numbers used in README.md.
The category of each "changes requested" round is my own reading of the review text
and is kept in CATEGORY below, next to the link to that review.
"""
import csv
import datetime as dt
import json
import statistics
import subprocess
from collections import Counter
from pathlib import Path

AUTHOR = "ym0506"
PRS = [
    ("apache/fineract", 6731),
    ("apache/shardingsphere", 38187), ("apache/shardingsphere", 38206), ("apache/shardingsphere", 38223),
    ("apache/shardingsphere", 38326), ("apache/shardingsphere", 38327), ("apache/shardingsphere", 38352),
    ("apache/shardingsphere", 38405), ("apache/shardingsphere", 38449), ("apache/shardingsphere", 38659),
    ("apache/shardingsphere", 38685), ("apache/shardingsphere", 39535), ("apache/shardingsphere", 39764),
    ("dolthub/go-mysql-server", 3442),
    ("open-telemetry/opentelemetry-java-instrumentation", 20020),
    ("kubernetes/kubernetes", 136090), ("kubernetes/kubernetes", 136101),
    ("testcontainers/testcontainers-java", 11484), ("testcontainers/testcontainers-java", 11488),
    ("quarkiverse/quarkus-shardingsphere-jdbc", 357),
    ("HsinDumas/shardingsphere-jdbc-spring-boot-starter", 4),
]

# (pull request, round) -> what the reviewer caught. Rounds are counted per pull request, oldest first.
A = "fix left part of the failure path unrepaired"
B = "would break existing data or existing runs"
C = "broke a neighboring valid input"
D = "tests did not prove the reported symptom"
E = "style rule (trailing whitespace)"
CATEGORY = {
    (38327, 1): B, (38352, 1): B,
    (38449, 1): A, (38449, 2): C, (38449, 3): A, (38449, 4): A, (38449, 5): A,
    (38659, 1): C, (38659, 2): A,
    (38685, 1): E, (38685, 2): D, (38685, 3): E, (38685, 4): D,
}

QUERY = """query($o:String!,$n:String!,$num:Int!){repository(owner:$o,name:$n){pullRequest(number:$num){
 number url state createdAt mergedAt closedAt
 reviews(first:100){nodes{author{login} state submittedAt url
   commit{oid statusCheckRollup{state contexts(first:100){totalCount nodes{__typename
     ... on CheckRun{conclusion} ... on StatusContext{state}}}}}}}
 reviewThreads(first:100){totalCount}
 comments(first:100){nodes{author{login}}}
 timelineItems(first:20,itemTypes:[CLOSED_EVENT]){nodes{... on ClosedEvent{actor{login}}}}
}}}"""


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def fetch(repo, num):
    owner, name = repo.split("/")
    out = subprocess.run(["gh", "api", "graphql", "-f", "query=" + QUERY, "-f", "o=" + owner, "-f", "n=" + name,
                          "-F", f"num={num}"], capture_output=True, text=True, check=True).stdout
    return json.loads(out)["data"]["repository"]["pullRequest"]


def main():
    prs, rounds = [], []
    for repo, num in PRS:
        p = fetch(repo, num)
        others = [r for r in p["reviews"]["nodes"] if r["author"] and r["author"]["login"] != AUTHOR]
        requested = [r for r in others if r["state"] == "CHANGES_REQUESTED"]
        other_comments = [c for c in p["comments"]["nodes"] if c["author"] and c["author"]["login"] != AUTHOR
                          and not c["author"]["login"].endswith(("-robot", "-prow", "easycla"))]
        end = p["mergedAt"] or p["closedAt"]
        days = (ts(end) - ts(p["createdAt"])).total_seconds() / 86400
        closers = [n["actor"]["login"] for n in p["timelineItems"]["nodes"] if n.get("actor")]
        if p["state"] == "MERGED":
            if requested:
                outcome = "merged after changes requested"
            elif p["reviewThreads"]["totalCount"] or other_comments or any(r["state"] == "COMMENTED" for r in others):
                outcome = "merged after comments"
            else:
                outcome = "merged, no change asked"
        else:
            outcome = "not merged, closed by " + (closers[-1] if closers else "?")
        prs.append({"repo": repo, "number": num, "url": p["url"], "opened": p["createdAt"][:10], "closed": end[:10],
                    "days_open": round(days, 1), "outcome": outcome, "changes_requested_rounds": len(requested)})
        for i, r in enumerate(requested, 1):
            roll = (r["commit"] or {}).get("statusCheckRollup")
            if roll:
                results = Counter(x.get("conclusion") or x.get("state") for x in roll["contexts"]["nodes"])
                checks = f"{roll['state']} ({roll['contexts']['totalCount']} checks, {results.get('FAILURE', 0)} failed)"
            else:
                checks = "none recorded"
            rounds.append({"repo": repo, "number": num, "round": i, "date": r["submittedAt"][:10],
                           "caught": CATEGORY.get((num, i), "(declined proposal, see README)"),
                           "checks_on_reviewed_commit": checks, "review": r["url"]})
    data = Path(__file__).parent / "data"
    data.mkdir(exist_ok=True)
    for name, rows in (("prs.csv", prs), ("rounds.csv", rounds)):
        with open(data / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    merged = [p for p in prs if p["outcome"].startswith("merged")]
    print("pull requests:", len(prs), "merged:", len(merged))
    print("outcomes:", dict(Counter(p["outcome"].split(", closed")[0] for p in prs)))
    print("not merged, closed by:", dict(Counter(p["outcome"].split("closed by ")[1] for p in prs if "closed by" in p["outcome"])))
    merged_rounds = [r for r in rounds if (r["number"], r["round"]) in CATEGORY]
    print("changes-requested rounds on merged pull requests:", len(merged_rounds))
    print("caught:", dict(Counter(r["caught"] for r in merged_rounds)))
    print("rounds with all recorded checks passed:", sum(r["checks_on_reviewed_commit"].startswith("SUCCESS") for r in merged_rounds))
    d = sorted(p["days_open"] for p in merged)
    print("days open (merged): median", statistics.median(d), "| within 7 days:", sum(x <= 7 for x in d), "| longest three:", d[-3:])


if __name__ == "__main__":
    main()
