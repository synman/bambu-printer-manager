# bambu-printer-manager AI Agent Guidelines

## KISS Principle (Mandatory)

**KISS is a hard requirement with no exceptions**: Keep It Simple and Straightforward.

For every change, always prefer the simplest solution that fully satisfies verified requirements.

**Required KISS behavior:**
- Do the minimum effective change first; avoid speculative architecture.
- Prefer clear, direct logic over clever or abstract patterns.
- Reuse existing code paths/components before creating new ones.
- Avoid adding flags, layers, helpers, or indirection unless required by demonstrated need.
- Keep public behavior stable unless change is explicitly required.
- If two solutions are valid, choose the one with fewer moving parts.

**KISS enforcement check before finalizing work:**
- Is every added line necessary to satisfy the request?
- Did I avoid introducing complexity for hypothetical future use?
- Can a maintainer understand this quickly without deep context?
- Is there a simpler implementation that preserves correctness?

## Quality-First Mode (Mandatory)

For **all work** (simple or complex), prioritize quality over speed.

**Hard requirements:**
- Prefer correctness, conciseness, repeatability, and thorough analysis over fast turnaround.
- Verify assumptions with source evidence before editing, even for small changes.
- Keep responses concise but complete; do not skip required validation to save time.
- Use deterministic, minimal patches that are easy to review and reproduce.

## Response Scope Rule (Mandatory)

Close responses with the task result only. Do not append unsolicited recommendations, optional follow-up offers, or unrelated "next step" suggestions.

**Hard requirements:**
- Do not include "If you want, I can..." style add-ons unless the user explicitly asked for options.
- Do not propose extra cleanups, refactors, audits, or expansions that were not requested.
- If additional work is genuinely required to complete the requested task, state that requirement directly and briefly.
- Keep endings factual and scoped to what was requested, changed, and validated.

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

## Strict Execution Mode (Mandatory)

Use this workflow for every non-trivial request:
1. **Verify first**: gather concrete evidence with `grep_search` + `read_file` before proposing or applying changes.
2. **Patch minimally**: implement the smallest targeted change that satisfies verified requirements.
3. **Validate immediately**: run diagnostics/tests relevant to touched files right after editing.
4. **Do not speculate**: if evidence is insufficient or contradictory, stop and collect the missing payload/code path before changing logic.

**Hard requirements:**
- No speculative architecture or inferred behavior changes without source proof.
- No broad multi-area edits when a single focused patch is sufficient.
- For protocol/telemetry work, always establish source-of-truth hierarchy first (steady-state status/bitfield over command ack).
- After changes, report what was verified, what was changed, and what validation ran.

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

## Source of Truth & Verification (Implementation-Specific)

**For this project specifically**:

## Cross-Model Compatibility Policy

This project targets **all Bambu Lab printers** (library + frontend), not a single model.

**Default behavior**:
- Preserve existing/legacy cross-model behavior unless there is verified evidence it fails.
- Prefer Bambu Studio-compatible behavior as the broad baseline across models.

**Override gate (strict)**:
- Add model-specific overrides only when the current/legacy logic is proven to fail for that model.
- Missing fields alone are not a legacy-logic failure. Example: if `ams_mapping2` is missing, add it alongside legacy `ams_mapping` first.
- Do not alter existing `ams_mapping` semantics unless breakage is demonstrated with direct evidence.

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
**Critical**: After creating or modifying any `.md` files in `docs/`, ALWAYS validate with `mkdocs build --clean` to catch broken links, missing anchors, and formatting issues before committing. No INFO-level warnings should be present in the output.

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
