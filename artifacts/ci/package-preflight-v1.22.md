# Package preflight (v1.22.0)

Ran against executable source
`2a859060e9e3b16f5a5365fe33bdf6b4663efbd3` on 2026-07-14 (WSL2 Linux).

**Publishing intent:** GitHub Release attaches packages on the `v*` tag.
Registry publication remains opt-in (`PUBLISH_PACKAGES=true` + credentials) and
is **disabled** for this tag.

## Tool versions

| Tool | Version |
|------|---------|
| Python | 3.12.3 |
| .NET SDK | 8.0.126 |
| OpenJDK (javac) | 17 (runtime also has 21 JRE) |
| Apache Maven | 3.8.7 |
| rustc / cargo | 1.95.0 |

## Artifacts

| Format | Artifact | SHA-256 |
|--------|----------|---------|
| Python wheel | `case_uco-1.22.0-py3-none-any.whl` | `ab05fb0f2d9370359b2de25bdc526256e6d422bf74587a0030c836b8feffd708` |
| Python sdist | `case_uco-1.22.0.tar.gz` | `620b833203d0736cb7f95d3b89375022686b82d325bf3361bcc2724e70718986` |
| NuGet | `CaseUco.1.22.0.nupkg` | `b18722abb8d0f17d6654012ca68c0b41e409466486020e1cbb675c4e939af265` |
| Maven JAR | `case-uco-1.22.0.jar` | `8e421afbe2209f5ac883136b38f3ebabd10fb902a02578a108d1bf1743cbb8cc` |
| Rust crate | `case-uco-1.22.0.crate` | `45c42a6e408b89ffff9273b57f1d93c17479f848e5ccb45f2f86104294a27665` |

## Commands and results

### Python

```bash
python -m build python -o /tmp/case-uco-v122-preflight/python-dist
python3 -m venv /tmp/case-uco-v122-preflight/py-clean
pip install case_uco-1.22.0-py3-none-any.whl
# import CASEGraph; create Tool; serialize → load → serialize
pip check
```

| Check | Result |
|-------|--------|
| Build wheel + sdist | OK |
| Clean venv install | OK (`case-uco==1.22.0`) |
| Import + graph round-trip | OK |
| `pip check` | OK (no broken requirements) |

### C#

```bash
dotnet pack csharp/CaseUco/CaseUco.csproj -c Release -o .../nuget
dotnet new console -f net8.0
dotnet add package CaseUco --version 1.22.0 --source .../nuget
dotnet build -c Release && dotnet run -c Release
```

| Check | Result |
|-------|--------|
| Pack `CaseUco.1.22.0.nupkg` | OK |
| Clean consumer restore/build/run | OK (`csharp consumer OK`) |

### Java

```bash
mvn -f java/pom.xml package -DskipTests
mvn -f java/pom.xml install -DskipTests   # local .m2 for consumer
# clean consumer pom depends on org.caseontology:case-uco:1.22.0
mvn -DskipTests compile exec:java
```

| Check | Result |
|-------|--------|
| Build `case-uco-1.22.0.jar` | OK |
| Clean Maven consumer compile/run | OK (`java consumer OK`; JDK 17 javac) |

### Rust

```bash
cd rust && cargo package --allow-dirty
cd rust && cargo publish --dry-run --allow-dirty
cd rust && cargo audit
```

| Check | Result |
|-------|--------|
| `cargo package` | OK (verify compile of packaged sources) |
| `cargo publish --dry-run` | OK (upload aborted intentionally) |
| `cargo audit` | OK (0 vulnerabilities; Rust Security workflow is path-filtered to `rust/**` and did not re-run on the critic-only executable SHA) |

## Exact-SHA CI evidence (executable source)

| Check | URL / result |
|-------|----------------|
| CI | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29362720114 — **success** (11/11 jobs) |
| CodeQL | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29362720174 — **success** (python, csharp, java-kotlin) |
| Code-scanning open alerts | `gh api .../code-scanning/alerts?state=open` → **0** at `2026-07-14T20:13:15Z` |
| Critic oracle artifact | `critic-oracle-report` id `8323033763` |
| Accepted repair artifact | `critic-repair-charged-with-accepted` id `8323034246` |
| Advisory bench artifact | `python-bench-small` id `8322924272` |
