# bambu-printer-manager AI Agent Guidelines

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

**Documentation Build**:
```bash
mkdocs build  # Generates from mkdocs.yml
```

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

**MQTT Topics**: Commands sent to device/request/** namespace. Telemetry subscribed via device/report/** and devcie/push/**.

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

These references are especially valuable for understanding MQTT message structures, telemetry field mappings, and printer state transitions.

## Security & Sensitive Areas

**Credentials**: Access codes are 8-character strings passed via BambuConfig. Never log or display access_code values.

**SSL/TLS**: MQTT connections use SSL with certificate validation. See ssl.create_default_context() usage in BambuPrinter.__init__.

**Path Traversal**: Validate all user-provided paths, especially in FTPS operations (ftpsclient/_client.py).
