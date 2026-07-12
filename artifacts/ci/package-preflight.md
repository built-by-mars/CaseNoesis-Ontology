# Package preflight (v1.21.0 RC)

Ran before tagging. Workspace: CASE-UCO-Libraries.

| Format | Command | Result |
|--------|---------|--------|
| Python sdist+wheel | `python -m build python` (venv) | `case_uco-1.21.0-py3-none-any.whl` + sdist |
| Python clean install | venv `pip install` wheel | `from case_uco import CASEGraph` OK |
| NuGet | `dotnet pack ... -c Release` | `CaseUco.1.21.0.nupkg` |
| Maven | `mvn -f java/pom.xml package -DskipTests` | `case-uco-1.21.0.jar` |
| Rust crate | `cargo package` | `case-uco-1.21.0.crate` |
| Rust publish dry-run | `cargo publish --dry-run --allow-dirty` | verify OK; upload aborted (dry-run) |

**Publishing intent:** release workflow attaches packages on `v*` tag; registry publish remains opt-in (`PUBLISH_PACKAGES=true` + credentials). Confirm credentials before tagging if publishing is required.
