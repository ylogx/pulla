# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Pulla is a CLI that walks a folder, finds every immediate subfolder that is a git repo, and runs `git pull` in each of them concurrently. Typical usage: `pulla` (pulls everything under cwd), `pulla -f <folder>`, `pulla -v` for verbose git output, `pulla -l {1,2,3}` for verbosity level, `pulla -V` for version.

## Commands

Package/dependency management is via `uv` with `pyproject.toml` (hatchling build backend) — there is no `setup.py` or `requirements.txt`.

```sh
uv sync                    # install deps + dev deps into .venv
uv run pytest              # run the full test suite
uv run pytest tests/test_pulla.py::test_pull_done_when_verbosity_level_set_one  # single test
make test                  # same as `uv run pytest`
make coverage               # uv run coverage run -m pytest && coverage report
make build                  # uv build -> dist/*.whl and *.tar.gz
make install                 # builds, then `uv tool install --force` the wheel
make clean                   # remove __pycache__, *.pyc, dist/, build/
```

Coverage config (`.coveragerc`) omits `tests/` and requires branch coverage; note the key is `ignore_errors`, not `ignore-errors` (the latter is silently ignored by coverage.py).

## Architecture

Four modules in `pulla/`, each with a single responsibility:

- **`main.py`** — the Typer CLI. `app = typer.Typer(...)` is the actual console-script entry point (`pulla = "pulla.main:app"` in `pyproject.toml`, and `run.py` calls `app()` too) — **not** the `main()` function. Calling `main()` directly bypasses Click's argument parsing, defaults, and callbacks entirely, since Typer command functions remain plain callables once decorated. Tests must drive the CLI through `typer.testing.CliRunner().invoke(app, [...])`, not by calling `main()` with kwargs.
- **`pulla.py`** — the `Pulla` class, the core logic:
  - `pull_all(folder)` walks the directory tree (`os.walk`, non-recursive by default — `recursive=True` is accepted by the constructor but never exposed via the CLI), collects every immediate subfolder that has a `.git` dir, then runs all of them concurrently with a single `asyncio.gather(*(self.do_pull_in(d) for d in git_dirs))`.
  - `do_pull_in(directory)` / `perform_git_pull(directory)` run `git pull` via `asyncio.create_subprocess_exec('git', 'pull', ..., cwd=directory, ...)` — no shell string, so directory names can't cause shell injection. `cwd=` is used instead of git's `-C` flag or `os.chdir()`, since `os.chdir()` mutates process-wide state and would race across concurrently-running pulls now that everything happens in one process.
  - Verbosity controls whether git's own stdout/stderr are inherited (`--verbose`, verbosity != 0) or sent to `DEVNULL` (silent).
  - `get_formatted_status_message` returns a **Rich markup string** (e.g. `'[green]Success[/green]'`), not rendered ANSI — rendering happens later, in the logger's `RichHandler`.
- **`logger.py`** — wraps stdlib `logging` with a `rich.logging.RichHandler` so markup from `pulla.py` actually renders. The handler/level are (re)attached lazily inside `print_log()`, guarded on `if not self.logger_handle.handlers`, rather than once in `__init__`. This is load-bearing, not just style: `logging.Logger` pickles by name only, so code that relies on cross-process handler state (this bit us when the concurrency model was `multiprocessing.Process`) would silently lose its handler. Keep this pattern if you touch this file.
  - Verbosity levels map to logging levels: `low`(1)→`WARNING`, `medium`(2)→`INFO`, `high`(3)→`DEBUG`. Status lines log at `low` verbosity; the `----` separators log at `high`.
- **`utils.py`** — just `is_this_a_git_dir()`.

`pulla/__init__.py` resolves `__version__` via `importlib.metadata.version('pulla')` (falls back to `'0.0.0'` if not installed) — do not reintroduce `pkg_resources`; it was removed because newer `setuptools` no longer ships it.

### Concurrency model

Everything runs in a single process via `asyncio` (`asyncio.gather` + `asyncio.create_subprocess_exec`), not `multiprocessing` — pulling repos is I/O-bound, and running one OS process per repo was both wasteful and the root cause of the logger-pickling bug described above. `main.py` bridges Typer's sync command function into async via `asyncio.run(_pull(puller, directory))`.

### Testing conventions

- Tests are plain pytest functions/`assert` (no `unittest.TestCase`), with `pytest.fixture` replacing `setUp`.
- Async methods (`Pulla.pull_all`, `.do_pull_in`, `.perform_git_pull`) are tested by wrapping the call in `asyncio.run(...)` inside an otherwise-sync test function — there's no `pytest-asyncio` dependency.
- `unittest.mock.patch()` auto-detects `async def` targets and returns `AsyncMock` automatically (Python ≥3.8), so patching e.g. `pulla.pulla.Pulla.perform_git_pull` "just works" for async methods. The one place this needs help: patching the whole `Pulla` class (`@patch('pulla.main.Pulla')`) requires `autospec=True`, otherwise the mocked instance's async methods come back as plain `MagicMock` and `await`ing them raises `TypeError`.
- Mocking `asyncio.create_subprocess_exec` requires manually building an object whose `.wait()` is an `AsyncMock` (see `tests/test_pulla.py`) — the return value of an `AsyncMock` call is a plain `MagicMock` by default, not itself async.
