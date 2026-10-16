"""Shared filesystem paths for Free Claude Code configuration."""

from pathlib import Path

CWC_CONFIG_DIRNAME = ".cwc"
LEGACY_FCC_CONFIG_DIRNAME = ".fcc"
FCC_ENV_FILENAME = ".env"
LEGACY_REPO_DIRNAME = "free-claude-code"
LEGACY_XDG_CONFIG_DIRNAME = ".config"
MESSAGING_STATE_DIRNAME = "agent_workspace"
FCC_LOGS_DIRNAME = "logs"
SERVER_LOG_FILENAME = "server.log"
SERVER_STARTUP_LOG_FILENAME = "startup.log"
CODEX_MODEL_CATALOG_FILENAME = "codex-model-catalog.json"
AUTH_DIRNAME = "auth"
OPENAI_AUTH_FILENAME = "openai.json"
OPENAI_AUTH_LOCK_FILENAME = "openai.lock"
CONFIG_LOCK_FILENAME = "config.lock"
SERVER_STARTUP_LOCK_FILENAME = "server.startup.lock"
SERVER_OWNER_LOCK_FILENAME = "server.owner.lock"
FCC_TEMP_DIRNAME = "tmp"
LAUNCHER_TEMP_DIRNAME = "launchers"
CODE_STATE_DIRNAME = "code"
FCC_DATABASE_FILENAME = "fcc.db"
CODE_DATABASE_FILENAME = "code.db"
CODE_LOCK_FILENAME = "code.lock"


def config_dir_path() -> Path:
    """Return the default user config directory."""

    home = Path.home()
    config_dir = home / CWC_CONFIG_DIRNAME
    legacy_dir = home / LEGACY_FCC_CONFIG_DIRNAME
    if legacy_dir.is_dir() and not legacy_dir.is_symlink():
        if not config_dir.exists():
            try:
                legacy_dir.rename(config_dir)
            except FileExistsError:
                _merge_legacy_config_dir(legacy_dir, config_dir)
            except FileNotFoundError:
                pass
        else:
            _merge_legacy_config_dir(legacy_dir, config_dir)
    return config_dir


def _merge_legacy_config_dir(legacy_dir: Path, config_dir: Path) -> None:
    config_dir.mkdir(parents=True, exist_ok=True)
    for legacy_item in legacy_dir.iterdir():
        config_item = config_dir / legacy_item.name
        if not config_item.exists() and not config_item.is_symlink():
            try:
                legacy_item.rename(config_item)
            except FileNotFoundError:
                pass
        elif (
            legacy_item.is_dir()
            and not legacy_item.is_symlink()
            and config_item.is_dir()
            and not config_item.is_symlink()
        ):
            _merge_legacy_config_dir(legacy_item, config_item)
            try:
                legacy_item.rmdir()
            except OSError:
                pass
    try:
        legacy_dir.rmdir()
    except OSError:
        pass


def managed_env_path() -> Path:
    """Return the default user-managed env file path."""

    return config_dir_path() / FCC_ENV_FILENAME


def config_lock_path() -> Path:
    """Return the cross-process managed-config migration lock path."""

    return config_dir_path() / CONFIG_LOCK_FILENAME


def server_startup_lock_path() -> Path:
    """Return the lock launchers hold while starting one shared fcc-server."""

    return config_dir_path() / SERVER_STARTUP_LOCK_FILENAME


def server_owner_lock_path() -> Path:
    """Return the lock held by one server through all configuration restarts."""

    return config_dir_path() / SERVER_OWNER_LOCK_FILENAME


def launcher_temp_dir_path() -> Path:
    """Return the base directory for private native launcher configuration."""

    return config_dir_path() / FCC_TEMP_DIRNAME / LAUNCHER_TEMP_DIRNAME


def fcc_database_path() -> Path:
    """Return the shared FCC database path."""
    return config_dir_path() / FCC_DATABASE_FILENAME


def legacy_code_database_path() -> Path:
    """Return the former Code database path for startup relocation."""
    return config_dir_path() / CODE_STATE_DIRNAME / CODE_DATABASE_FILENAME


def code_lock_path() -> Path:
    """Return the exclusive Code sessions process-lock path."""
    return config_dir_path() / CODE_STATE_DIRNAME / CODE_LOCK_FILENAME


def legacy_env_paths() -> tuple[Path, ...]:
    """Return legacy user env paths that can be migrated to ~/.cwc/.env."""

    home = Path.home()
    return (
        home / LEGACY_REPO_DIRNAME / FCC_ENV_FILENAME,
        home / LEGACY_XDG_CONFIG_DIRNAME / LEGACY_REPO_DIRNAME / FCC_ENV_FILENAME,
    )


def messaging_state_dir_path() -> Path:
    """Return the managed messaging state directory."""

    return config_dir_path() / MESSAGING_STATE_DIRNAME


def server_log_path() -> Path:
    """Return the canonical server log path."""

    return config_dir_path() / FCC_LOGS_DIRNAME / SERVER_LOG_FILENAME


def server_startup_log_path() -> Path:
    """Return the latest automatic owner's output before runtime logging starts."""

    return config_dir_path() / FCC_LOGS_DIRNAME / SERVER_STARTUP_LOG_FILENAME


def codex_model_catalog_path() -> Path:
    """Return the generated Codex model catalog path."""

    return config_dir_path() / CODEX_MODEL_CATALOG_FILENAME


def claude_desktop_disconnect_path() -> Path:
    return config_dir_path() / "claude-desktop-disconnect.json"


def openai_auth_path() -> Path:
    """Return FCC's private ChatGPT credential file path."""

    return config_dir_path() / AUTH_DIRNAME / OPENAI_AUTH_FILENAME


def openai_auth_lock_path() -> Path:
    """Return the cross-process lock path for ChatGPT credentials."""

    return config_dir_path() / AUTH_DIRNAME / OPENAI_AUTH_LOCK_FILENAME


def github_copilot_auth_path() -> Path:
    """Return FCC connection state; native Copilot retains credentials."""
    return config_dir_path() / AUTH_DIRNAME / "github_copilot.json"
