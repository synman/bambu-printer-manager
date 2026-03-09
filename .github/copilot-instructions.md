# bambu-printer-manager AI Agent Guidelines

## ⚠️ GIT WRITE PROTECTION — ABSOLUTE, NO EXCEPTIONS, NEVER BYPASSED

**NEVER run `git commit` or `git push` in this repo under any circumstances.**
These are the user's actions exclusively. This rule has no exceptions and is never overridden by task completion, user acknowledgment phrases, or any other context.

- `git add` and `git rm` are permitted. **Stop there.**
- "committing?" = a question. Do not commit. Ask for clarification.
- "done" / "reloaded" / task success = status only. Do not commit.
- No implicit authorization exists. Only an unambiguous direct instruction ("commit it", "go ahead and commit") authorizes a commit — and even then, **only the user runs it**.

**Known RULES_PRECHECK failure modes — all are disqualifying:**
- Reading only the global rules file (`~/.copilot/copilot-instructions.md`) without this file = incomplete. This file contains the primary commit prohibition. Both files must be read in the same turn.
- Reading from memory or a prior-turn cache = invalid. Each turn requires a fresh file read.
- A truncated read (stopping before the end of this file) = invalid. Read the full file.
- Concluding this file was "moved" or "doesn't exist" without explicit evidence — stop and notify the user. Do not proceed without the project rules.
- Interpreting the git ban as "push-only" = incorrect. The ban covers both `git commit` and `git push`. Commit is forbidden regardless of whether a push is intended.

**Post-commit hook — always reset:**
The post-commit hook fires after every commit (including `--amend`) and instructs `git reset --soft HEAD~1`. This reset is **always required**. The following arguments do NOT justify skipping it:
- "The commit is already in history — resetting is disruptive" — sunk cost; `git reset --soft HEAD~1` is available and the instruction is explicit.
- "The hook is not a hard block — git let it through" — true but irrelevant; the instruction is to reset regardless.
- "The hook fired which means the rules were read — requirement met" — the hook requires BOTH rule acknowledgment AND reset. Reading alone is not sufficient.
- "I was explicitly authorized — the reset instruction doesn't apply" — the hook fires on every commit without exception. Reset first, then confirm with the user whether to re-commit if authorization was genuine.

## ⚠️ PRINTER WRITE PROTECTION — ABSOLUTE, NO EXCEPTIONS, NEVER BYPASSED

**NEVER execute, run, pipe input to, or interact with any command that sends a write or destructive operation to a physical printer — under any circumstances — without the user typing explicit permission in plain text in the current conversation turn.**

This means:
- **Do NOT run `bambu_fw_upgrade.py`** (or any variant) without the user saying so explicitly in their message.
- **Do NOT use `write_bash`, `echo "YES" |`, or any other mechanism to answer a confirmation prompt on behalf of the user.** The confirmation prompt exists for humans only.
- **Do NOT run it as a "test", "dry-run validation", "connection check", or any other pretext.** `--dry-run` is safe; anything else is not.

Prohibited operations (not exhaustive):
- Firmware update commands (`upgrade.start`, any `upgrade.*`)
- MQTT publish to any `device/*/request` topic
- GCode commands
- Configuration changes
- Any FTP/file upload to a printer

This rule applies in **all operating modes** without exception: interactive, autopilot, background agents, scripted execution. Violating this rule has already caused accidental firmware flash attempts on a physical printer twice. There will be no third time.

## ⚠️ CONTAINER API AUTH — MANDATORY, NO EXCEPTIONS, EVERY CALL

See global rules (`~/.copilot/copilot-instructions.md`). Key: `secrets.py get bpm_api_auth`. Never use `security find-internet-password`.

---

> **Global rules** in `~/.copilot/copilot-instructions.md` are always in effect. This file extends them with project-specific guidance. Both must be read and applied together.

## Session Start Protocol (Mandatory)

Both the global rules file and this repo-specific file MUST be read together before any tool call.
See **Session Start Protocol + RULES_PRECHECK** in `~/.copilot/copilot-instructions.md` for the
full enforcement gate, `RULES_PRECHECK` output format, and invalidation rules — they apply here
without exception.

## Root Cause Fix Rule (Mandatory)

When the root cause of a problem has been identified in a specific piece of code, **fix that code**. Do not introduce workarounds, shims, compensating logic, or structural changes elsewhere to paper over a bug when a direct fix is available.

**Hard requirements:**
- If you know where the bug is, fix it there. Full stop.
- Do not add infrastructure, build stages, extra processes, or architectural indirection to compensate for broken code.
- Adding resource cost (CPU, memory, network, build time) to work around a software defect is never acceptable when the defect can be fixed directly.
- Rationalization trap: if you find yourself building a case for NOT fixing the root cause — stop. The existence of the rationalization is itself a signal you are about to make the wrong decision.

**Anti-patterns (never do these):**
- ❌ "I'll add a Dockerfile build stage so the display script doesn't have to handle this edge case"
- ❌ "I'll wrap the call to avoid fixing the underlying function"
- ❌ "This workaround restores expected behavior" — restoring behavior via a workaround is not the same as fixing the bug

**Required pre-fix gate:**
1. Have I identified the file and line(s) where the defect lives? If yes — fix it there.
2. Am I about to change something OTHER than the defective code? If yes — stop and explain why a direct fix is impossible before proceeding.

## Telemetry Mapping Parity Rule (Mandatory)

When adding or changing support for a telemetry field that belongs to an existing family (for example print_option flags), the implementation MUST follow the proven pattern used by sibling fields unless direct evidence proves otherwise.

**Hard requirements:**
- Use the nearest working sibling field as the baseline reference (for example `nozzle_blob_detect`).
- Verify where sibling values are sourced (for example `home_flag` bitfield, `cfg`, `xcam`, or explicit key) before coding.
- If sibling print_option state is sourced from `home_flag`, default new sibling steady-state mapping to `home_flag` as well unless direct evidence proves a different source.
- Do not introduce a new parsing path (for example command-ack-only tracking) unless verified evidence shows sibling parity is invalid.
- If a user says to use a specific field as a reference point, treat that as a mandatory implementation constraint.

**Evidence requirements before coding telemetry mappings:**
1. Confirm upstream behavior in at least one authoritative source (BambuStudio preferred).
2. Confirm current project behavior for sibling fields in source code.
3. Confirm runtime evidence (logs/payloads) and classify it correctly:
	- command ack payloads confirm command acceptance,
	- status payloads or bitfields confirm steady-state telemetry source.
4. Implement using the source that represents steady-state truth unless proven otherwise.

**Anti-fabrication guardrails:**
- Never invent a new telemetry lifecycle model when a proven local pattern already exists.
- Never treat command ack events as a complete substitute for continuous status mapping unless explicitly verified.
- If evidence is mixed, stop and state the uncertainty, then request/collect the missing payload needed to resolve it.

**Parity checklist (must all be true before finalizing):**
- Did I compare against at least one sibling field implementation line-by-line?
- Did I verify the same source-of-truth path for both fields?
- Did I avoid adding special-case logic without explicit evidence?
- Did I document why this field matches or intentionally differs from sibling behavior?

## Verification First - Before Any Work

**Critical Principle**: Never infer architecture, features, behavior, or implementation details from partial code patterns. **ALWAYS verify against actual source code before acting.** This applies to everything: documentation, code analysis, bug fixes, feature work, reverse engineering.

**When in doubt, verify first**:
- ✗ "I see ANNOUNCE_PUSH and pushing namespace, so a push topic probably exists"
- ✓ "I found ANNOUNCE_PUSH. Let me check actual client.subscribe() calls to verify the topic is used"

**Verification checklist for ANY claim about the codebase:**
1. **What does the code actually do?** (Read the implementation, not inferred architecture)
2. **Is this feature really used?** (Search for actual calls/invocations, not just template definitions)
3. **Does this path actually execute?** (Check conditionals, handlers, try/catch blocks - don't assume)
4. **Are there edge cases I missed?** (Search for all usages, not just one example)
5. **What do authoritative reference implementations do?** (Cross-check with ha-bambulab, BambuStudio, OrcaSlicer if unsure)

**Telemetry absence rule (mandatory):**
- For telemetry-key claims, explicitly search local runtime evidence (`tests/` fixtures, logs, captured payloads) for the exact key.
- If the key is absent locally, treat **"missing in local telemetry"** as a first-class interpretation and state it before proposing alternatives.
- Do not imply local presence from upstream references alone; upstream presence can justify parser support but not claim local telemetry coverage.

**Pattern Matching Trap**: Finding evidence of a pattern (e.g., command template, enum value, function name) does NOT mean the feature is implemented or used. Each claim requires independent verification:
- Template exists ≠ command is sent
- Message type defined ≠ message is parsed
- Function exists ≠ function is called
- Namespace present ≠ all sub-features exist

### Mandatory Verification Depth Requirements

**For ANY method/function documentation or analysis:**
1. ✓ **Read the method implementation** - Find the actual implementation in source code
2. ✓ **Trace data flow** - Read line-by-line how data is constructed/transformed (assignments, operations, conditionals)
3. ✓ **Document actual values** - Use real examples from the code (e.g., `f"M104 S{value}\n"`), not placeholders like `{0-280}`
4. ✓ **Check conditionals** - Document when behavior changes based on conditions (e.g., T parameter only when tool_num >= 0)
5. ✗ **Never assume from names or templates** - Finding a template/constant does NOT tell you what actual values are used

**For method signatures and parameters:**
1. ✓ **Read the def line** - Check actual parameter names, types, defaults, order
2. ✓ **Verify parameter order** - Order matters; never rearrange based on assumptions
3. ✓ **Check parameter usage** - Verify parameters are actually used in the implementation
4. ✗ **Never infer from field names** - Field names in data structures ≠ method parameter names/order

**For feature existence claims (topics, endpoints, commands, etc.):**
1. ✓ **Search for actual usage** - Find where it's called, subscribed, registered, or invoked
2. ✓ **Search for implementation** - Verify the actual code that handles/processes it
3. ✓ **Check registration/initialization** - Read where it's set up (e.g., `client.subscribe()`, route decorators)
4. ✗ **Never assume from patterns** - Templates/constants/enums don't prove the feature is active

**Insufficient Verification Examples:**
- ❌ "Found `SET_CHAMBER_AC_MODE` constant → method `set_chamber_ac_mode()` exists"
- ❌ "Saw enum value `ANNOUNCE_PUSH` → feature X is implemented"
- ❌ "Method has `tool_num` parameter → value is always used in output"
- ❌ "Data structure has `ams_id` field → method parameter order is `(ams_id, slot_id)`"
- ❌ "File has `@route('/api/status')` → endpoint returns status data"
- ❌ "Class has `_cache` attribute → caching is implemented"

**Sufficient Verification Examples:**
- ✅ "Read `set_chamber_temp_target()` lines 363-398 → sends `SET_CHAMBER_AC_MODE` internally, no public method"
- ✅ "Grepped for feature usage → only called in test file line 150, not in production code"
- ✅ "Read line 344 → parameter used conditionally: `{'' if tool_num == -1 else ' T' + str(tool_num)}`"
- ✅ "Checked def line 482 → `load_filament(slot_id: int, ams_id: int = 0)` - slot first, not ams"
- ✅ "Read route handler lines 89-102 → returns `{'error': 'not implemented'}`, endpoint is a stub"
- ✅ "Searched for `_cache` usage → only initialized line 45, never read/written, unused attribute"

### Verification Enforcement

**Before making ANY technical claim about the codebase, you MUST:**

1. **Execute verification tools** - Use `read_file`, `grep_search` to gather actual code
2. **Quote exact code** - Reference specific line numbers and actual code snippets in your reasoning
3. **Trace execution paths** - For any feature, trace from invocation → implementation → output
4. **Document conditionals** - Note any if/else that changes behavior (examples: T parameter only when tool_num >= 0, SET_CHAMBER_AC_MODE only when has_chamber_temp)

**Self-check before claiming anything is true:**
- [ ] Did I read the actual implementation method/function/handler?
- [ ] Did I trace how the data/message/output is constructed line-by-line?
- [ ] Did I check for conditionals that change behavior?
- [ ] Can I cite specific line numbers where this behavior occurs?
- [ ] Did I use actual values from the code, not placeholder syntax?
- [ ] For telemetry keys, did I explicitly check local fixtures/logs and state whether the key is missing locally?

**If you cannot check all required boxes above, your verification is INSUFFICIENT.**

## Code Style

**Language**: Python 3.11+ (strict minimum, see `pyproject.toml`)

**Type Hints**: Always use full type annotations. Use `|` for unions (PEP 604), `typing_extensions` for Python <3.12.

**Linting**: Ruff is the authority. Configuration in `pyproject.toml`:
- Line length: 90 characters
- Target: Python 3.11
- Selected rules: B, C, E, F, I, W, B9 (strict enforcement)
- Ignored: E501 (line length is disabled), C901 (complexity), E701
- **Import organization**: Alphabetically sorted, first-party imports under `bpm` namespace

**Docstrings**: Google-style docstrings with triple quotes. See examples in `src/bpm/bambutools.py` and `src/bpm/bambuprinter.py`.

**Private Attributes**: Use underscore prefix (`_hostname`, `_mqtt_port`). Dataclasses use field names with underscores to maintain backing store for properties.

## Cross-Model Compatibility Policy

This project targets **all Bambu Lab printers** (library + frontend), not a single model.

**Default behavior**:
- Preserve existing/legacy cross-model behavior unless there is verified evidence it fails.
- Prefer Bambu Studio-compatible behavior as the broad baseline across models.

**Override gate (strict)**:
- Add model-specific overrides only when the current/legacy logic is proven to fail for that model.
- Missing fields alone are not a legacy-logic failure. Example: if `ams_mapping2` is missing, add it alongside legacy `ams_mapping` first.
- Do not alter existing `ams_mapping` semantics unless breakage is demonstrated with direct evidence.

## Code Placement Rules (Mandatory)

Before writing any new code in BPM, read the placement rules below and verify the established patterns in the files they reference. These rules are prescriptive — they define where new code **must** go, not merely where it tends to appear.

### `bambuprinter.py` module scope

**Module-level content is limited to:**
- `logger = logging.getLogger(LoggerName)` — exactly one logger assignment
- `class BambuPrinter:` — the class definition

**Never add module-level functions, constants, or variables to `bambuprinter.py`**, even with a `_private` prefix. This file defines one class. That is its entire contract.

- Helper functions with instance state → private methods on `BambuPrinter` in the `# region private methods` section
- Pure utilities without instance state → `bambutools.py`
- MQTT command templates and protocol constants → `bambucommands.py`

**Pre-implementation gate:** Before adding any helper to `bambuprinter.py`, read the `# region private methods` section. Find the nearest sibling method and follow its exact pattern — method signature, use of `self`, exception handling, return type.

### Filesystem persistence and `bpm_cache_path`

**All BPM filesystem persistence must route through `self.config.bpm_cache_path`.** Never use `Path.home()`, `pathlib.Path("~/.bpm")`, or any hardcoded path.

`bpm_cache_path` is the single general-purpose root for all BPM on-disk state — metadata caches, elapsed tracking, or any future persistence need. It defaults to `~/.bpm` but is configurable via `BambuConfig`. Hardcoding any path under `Path.home()` bypasses this and breaks callers that set a custom path.

- Any new named subdirectory is accessed as `self.config.bpm_cache_path / "<subdir>"`.
- Subdirectories are created **lazily at first write** by `cache_write` (or by the write path itself). Do NOT register or pre-create subdirs in `BambuConfig.set_new_bpm_cache_path()` — that method only creates the root `bpm_cache_path`.

**Pre-implementation gate:** Before adding any new filesystem persistence to BPM, confirm you are using `make_cache_key` / `cache_write` / `cache_read` / `cache_delete` from `bambutools` with `self.config.bpm_cache_path / "<subdir>"`. The subdir will be created automatically on first write. Always generate keys via `make_cache_key` — never construct filename stems manually.

### Enums, constants, and utility functions

- New enums → `bambutools.py`, following the existing `IntEnum`/`Enum` patterns with docstrings
- New MQTT command templates → `bambucommands.py`
- New pure utility functions (no instance state, no config dependency) → `bambutools.py`
- New instance-scoped helpers → private methods on the relevant class

## Architecture

**Central Class**: `BambuPrinter` (see `src/bpm/bambuprinter.py`) is the main abstraction layer. All printer interaction flows through this class.

**Configuration System**: `BambuConfig` (see `src/bpm/bambuconfig.py`) now uses Python dataclasses (@dataclass). Fields are private (_field_name) with inline docstrings.

**State Management**: `BambuState` (see `src/bpm/bambustate.py`) holds telemetry state. Updated via MQTT telemetry parsing.

**Communication Layers**:
- **MQTT**: Primary for telemetry subscriptions and command transmission (Paho MQTT client)
- **FTPS**: File operations via `src/bpm/ftpsclient/ftpsclient.py`

**Enums & Constants**:
- `bambutools.py` contains all IntEnum/Enum definitions (PrinterModel, Stage, etc.)
- `bambucommands.py` contains MQTT command templates and constants
- Use descriptive enum values with docstrings (see ActiveTool, AirConditioningMode patterns)

**Logging**: All modules use logger = logging.getLogger(LoggerName) where LoggerName = "bpm" (defined in bambutools.py).

## Build and Test

**Git Workflow**:
- **Never run `git commit` or `git push`.** See the ⚠️ GIT WRITE PROTECTION banner at the top of this file — no exceptions, no implicit authorization.
- `git add`/`git rm` and pre-commit hooks are permitted. Stop there.
- Report what is staged and ready — do not commit under any circumstances.

**Build**:
```bash
./make.sh
# Cleans dist/, builds with python -m build via setuptools
```

**Test Execution**:
- Test files in `tests/` directory (e.g., `tests/h2d-unit-test.py`)
- Test JSON fixtures for printer telemetry states provided (h2d-*.json, a1-*.json)
- Run with: `python tests/<test-file>.py`

**Documentation Build & Validation**:
```bash
mkdocs build --clean  # Generates from mkdocs.yml with full validation
```
**Critical**: After creating or modifying **any** `.md` files in `docs/` **or any Python docstrings** (since `mkdocstrings-python` renders them into the site), ALWAYS validate with `mkdocs build --clean` to catch broken links, missing anchors, and formatting issues before committing. No INFO-level warnings should be present in the output.

## Project Conventions

**Naming Patterns**:
- Classes: PascalCase (BambuPrinter, BambuConfig, PrinterCapabilities)
- Methods/Functions: snake_case
- Constants: SCREAMING_SNAKE_CASE in bambucommands.py and bambutools.py
- Private attributes: _leading_underscore

**Enum Usage**: All state values are IntEnum/Enum to provide type safety. Always reference via enum rather than raw integers (e.g., `PrinterModel.H2D` not `2`). Document each enum value with docstring commentary on its meaning.

**Dataclass Fields**: Private backing fields with field() for non-init state. Example from bambuconfig.py:
```python
_firmware_version: str = field(default="", init=False, repr=False)
_auto_recovery: bool = field(default=True, init=False, repr=False)
```

**Paths**: Use `pathlib.Path` for all filesystem operations. See bpm_cache_path pattern in BambuConfig.

**Deprecated Features**: Mark with `@deprecated` from typing_extensions. See bambuprinter.py for examples.

## Querying Live Printer State (Mandatory)

**Always use the container API — never instantiate `BambuPrinter` directly for read-only queries.**

The containers `bpm-h2d` and `bpm-a1` (running on `ds1621`, 10.151.51.24) already hold active MQTT sessions. Opening a second `BambuPrinter` session from an agent script creates a duplicate MQTT client, is wasteful, and risks MQTT interference.

**Correct pattern:**
```bash
AUTH=$(python ~/bambu-printer-manager/secrets.py get bpm_api_auth)
curl -sk -u "$AUTH" "https://bambu-h2d.shellware.com/api/printer"
# A1: https://bambu-a1.shellware.com/api/printer
```

The **only** legitimate reason to instantiate `BambuPrinter` directly is to send a command that has no container API endpoint (e.g. `send_anything()`). All state reads must go through the container API.

## Integration Points

**MQTT Topics**: Commands sent to `device/{serial}/request` namespace. Telemetry (including push_status updates) subscribed via `device/{serial}/report` only. Note: "push" refers to message types within the report topic, not a separate subscription.

**FTPS Operations**: IoTFTPSClient handles FTPS file transfers. Used for 3MF uploads via `src/bpm/bambuprinter.py`.

**External Dependencies**:
- `paho-mqtt`: MQTT client library
- `webcolors`: Color name/hex conversions
- `mkdocstrings-python`: Doc generation
- `typing-extensions`: Backport typing features for Python <3.12

**File Structure**: Source in `src/`, tests in `tests/`. Excluded from packaging: `bpm/ftpsclient` (see pyproject.toml setuptools config).

## Reference Implementations

For telemetry and data mapping questions, consult these authoritative public repositories:

- **[BambuStudio](https://github.com/bambulab/BambuStudio)**: Official Bambu Lab client implementation with complete telemetry mapping and protocol definitions
- **[OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)**: Community fork with enhanced telemetry handling and data structure examples
- **[ha-bambulab](https://github.com/greghesp/ha-bambulab)**: Home Assistant integration with comprehensive MQTT topic and payload documentation
- **[ha-bambulab pybambu](https://github.com/greghesp/ha-bambulab/tree/main/custom_components/bambu_lab/pybambu)**: Low-level Python MQTT client implementation and message parsing
- **[Bambu-HomeAssistant-Flows](https://github.com/WolfwithSword/Bambu-HomeAssistant-Flows)**: Workflow patterns and integration examples using Bambu Lab printers
- **[OpenBambuAPI](https://github.com/Doridian/OpenBambuAPI)**: Alternative API implementation with detailed protocol documentation
- **[X1Plus](https://github.com/X1Plus/X1Plus)**: Community firmware and protocol analysis for extended printer capabilities
- **[bambu-node](https://github.com/THE-SIMPLE-MARK/bambu-node)**: Node.js implementation providing cross-language verification and alternative patterns

These references are valuable for understanding MQTT message structures, telemetry field mappings, printer state transitions, and edge cases across multiple implementations.

## Security & Sensitive Areas

**Credentials**: Access codes are 8-character strings passed via BambuConfig. Never log or display access_code values.

**Test Fixture Data Privacy**: Treat everything under `tests/` as private/sensitive validation data. Never reference, quote, link, or cite `tests/` files in public-facing documentation, examples, commit messages, PR descriptions, or assistant/user-facing responses. Use source code under `src/` and public upstream repositories for provenance instead.

**SSL/TLS**: MQTT connections use SSL with certificate validation. See ssl.create_default_context() usage in BambuPrinter.__init__.

**Path Traversal**: Validate all user-provided paths, especially in FTPS operations (ftpsclient/_client.py).
