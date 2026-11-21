# Review record of my open-source pull requests, 2026

In 2026 I opened 21 pull requests to open-source projects I do not maintain. This page counts what happened to them in review: how many were merged, how many rounds of requested changes they took, what each round caught, and why seven were not merged.

Everything here comes from the GitHub API. `build_record.py` rebuilds the two files in `data/` and prints the numbers below. The last run was on 21 November 2026.

Not counted: pull requests in my own repositories, in a team repository I belong to, and one documentation fix in another student's study repository. #38326 and #38327 are the same change opened twice on one day, so the 21 pull requests are 20 distinct changes.

## Outcome

| Outcome | Count | Pull requests |
|---|---|---|
| Merged, no change asked | 6 | Fineract [#6731](https://github.com/apache/fineract/pull/6731); ShardingSphere [#38187](https://github.com/apache/shardingsphere/pull/38187), [#38206](https://github.com/apache/shardingsphere/pull/38206), [#38223](https://github.com/apache/shardingsphere/pull/38223), [#39535](https://github.com/apache/shardingsphere/pull/39535), [#39764](https://github.com/apache/shardingsphere/pull/39764) |
| Merged after comments | 3 | ShardingSphere [#38405](https://github.com/apache/shardingsphere/pull/38405); go-mysql-server [#3442](https://github.com/dolthub/go-mysql-server/pull/3442); OpenTelemetry Java instrumentation [#20020](https://github.com/open-telemetry/opentelemetry-java-instrumentation/pull/20020) |
| Merged after "changes requested" reviews | 5 | ShardingSphere [#38327](https://github.com/apache/shardingsphere/pull/38327) (1 round), [#38352](https://github.com/apache/shardingsphere/pull/38352) (1), [#38449](https://github.com/apache/shardingsphere/pull/38449) (5), [#38659](https://github.com/apache/shardingsphere/pull/38659) (2), [#38685](https://github.com/apache/shardingsphere/pull/38685) (4) |
| Not merged | 7 | listed at the end |

14 of 21 were merged: ShardingSphere 11, Fineract 1, OpenTelemetry 1, go-mysql-server 1.

## The 13 "changes requested" rounds on merged pull requests

Each round number links to the review. The group is my own reading of the reviewer's main blocker, one group per round. A fourteenth "changes requested" round, on a pull request that was not merged, is described in the last table.

- A: the fix left part of the failure path unrepaired
- B: the change would break existing data or existing runs
- C: the fix broke a neighboring valid input
- D: the tests did not prove the reported symptom
- E: a style rule

| Pull request | Round | Date | What the reviewer caught | Group | Checks on the reviewed commit |
|---|---|---|---|---|---|
| #38327 | [1](https://github.com/apache/shardingsphere/pull/38327#pullrequestreview-3886569650) | 2026-03-04 | Rows already written with negative Long keys would route to a different shard after an upgrade | B | passed (164 checks, 0 failed) |
| #38352 | [1](https://github.com/apache/shardingsphere/pull/38352#pullrequestreview-3898014576) | 2026-03-05 | Runs other than pull-request runs would no longer be pinned to one commit | B | passed (91 checks, 0 failed) |
| #38449 | [1](https://github.com/apache/shardingsphere/pull/38449#pullrequestreview-3954236341) | 2026-03-16 | Generated names could still exceed the database limit, and existing indexes could no longer be dropped or renamed | A | passed (91 checks, 0 failed) |
| #38449 | [2](https://github.com/apache/shardingsphere/pull/38449#pullrequestreview-3986038153) | 2026-03-21 | A real index name that ends like a generated suffix was shortened by mistake | C | failed (19 checks, 4 failed) |
| #38449 | [3](https://github.com/apache/shardingsphere/pull/38449#pullrequestreview-4000906133) | 2026-03-24 | Long named indexes were still not recovered on the shared metadata path | A | passed (150 checks, 0 failed) |
| #38449 | [4](https://github.com/apache/shardingsphere/pull/38449#pullrequestreview-4522313958) | 2026-06-18 | Recovery failed when every physical index already had the new short name | A | passed (87 checks, 0 failed) |
| #38449 | [5](https://github.com/apache/shardingsphere/pull/38449#pullrequestreview-4531812107) | 2026-06-19 | The create-table path had no candidate name to recover from | A | passed (87 checks, 0 failed) |
| #38659 | [1](https://github.com/apache/shardingsphere/pull/38659#pullrequestreview-4378297379) | 2026-05-28 | The same query without an alias got a wrong column label | C | passed (79 checks, 0 failed) |
| #38659 | [2](https://github.com/apache/shardingsphere/pull/38659#pullrequestreview-4415018233) | 2026-06-03 | The openGauss parser path was left as it was | A | passed (79 checks, 0 failed) |
| #38685 | [1](https://github.com/apache/shardingsphere/pull/38685#pullrequestreview-4352415970) | 2026-05-24 | Trailing whitespace | E | passed (66 checks, 0 failed) |
| #38685 | [2](https://github.com/apache/shardingsphere/pull/38685#pullrequestreview-4364377310) | 2026-05-26 | The originally reported symptom was not tested directly | D | passed (66 checks, 0 failed) |
| #38685 | [3](https://github.com/apache/shardingsphere/pull/38685#pullrequestreview-4371745962) | 2026-05-27 | Trailing whitespace again | E | passed (66 checks, 0 failed) |
| #38685 | [4](https://github.com/apache/shardingsphere/pull/38685#pullrequestreview-4377544937) | 2026-05-28 | One test method covered two scenarios | D | passed (66 checks, 0 failed) |

| Group | Rounds |
|---|---|
| A | 5 |
| B | 2 |
| C | 2 |
| D | 2 |
| E | 2 |

Nine of the 13 rounds (A, B, C) were about behavior that my own tests had not covered.

In 12 of the 13 rounds every check recorded on GitHub for the reviewed commit had passed. The exception is #38449 round 2. Both whitespace rounds are among the 12, so for the nine rounds about behavior (A, B, C) the figure is 8 of 9.

In the three pull requests merged after comments: a maintainer asked for an end-to-end test (#38405); a reviewer asked me to move tests to another file and removed a claim from my description that the pull request did not test (#3442); an automated reviewer pointed out that a configuration fallback read a process-wide setting where it should read the instance passed in (#20020).

## Time

From opening to merge, the median for the 14 merged pull requests was 1.75 days. Ten merged within 7 days, one took 17 days, and three took 60, 89 and 98 days. The 89-day one (#38405) got its only request on the first day and then waited for a reviewer.

Days open are not effort. I did not log hours, so this record cannot say what the review and rework cost.

## The seven not merged

| Pull request | Open for | What happened |
|---|---|---|
| ShardingSphere [#38326](https://github.com/apache/shardingsphere/pull/38326) | same day | I closed it and opened the change again as #38327 |
| Kubernetes [#136090](https://github.com/kubernetes/kubernetes/pull/136090) | 183 days | Closed by the stale bot. No maintainer review |
| Kubernetes [#136101](https://github.com/kubernetes/kubernetes/pull/136101) | 156 days | A reviewer asked me to drop an unrelated commit and the triage was accepted. Then the stale bot closed it with no decision |
| Testcontainers [#11484](https://github.com/testcontainers/testcontainers-java/pull/11484) | 139 days | A reviewer doubted the new tests were worth maintaining. I closed it |
| Testcontainers [#11488](https://github.com/testcontainers/testcontainers-java/pull/11488) | 136 days | A reviewer approved it. It was not merged, and I closed it |
| quarkus-shardingsphere-jdbc [#357](https://github.com/quarkiverse/quarkus-shardingsphere-jdbc/pull/357) | 2 days | I proposed running my library RouteContract as a test upstream. The maintainer said the test belongs in my repository and closed it |
| shardingsphere-jdbc-spring-boot-starter [#4](https://github.com/HsinDumas/shardingsphere-jdbc-spring-boot-starter/pull/4) | 18 days | The same kind of proposal. One round of requested changes: a script that failed on the maintainer's default shell, missing dependency verification, deprecated action versions, duplicated test setup. Then the maintainer declined. The CI job ran on every build, the check added little to the existing tests, and the dependency had one maintainer with no track record. The maintainer wrote that the concern was not implementation quality |

## What this record does not show

- Hours. It has rounds, dates and outcomes only.
- The check results are the ones GitHub shows now for each reviewed commit. A check that was re-run later shows its last result.
- One reviewer wrote all 13 rounds, so the groups say more about one project's standards than about open source in general.
- The grouping is mine. Someone else reading the same reviews could draw the lines differently, which is why each round links to its review. Three rounds were close calls: #38449 round 1 raised an unfinished fix and a compatibility break together (I put it in A, it could be B), and #38449 rounds 4 and 5 were worded as missing proof (I put them in A, they could be D).

## Rebuild

```bash
python3 build_record.py
```

It needs the GitHub CLI (`gh`) logged in. It writes `data/prs.csv` (one row per pull request) and `data/rounds.csv` (one row per "changes requested" round, with the link to the review and the check results).
