import logging
import os
import sys

import structlog  # type: ignore

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "log")


def configure_logging(log_file_name="app.log"):
    """
    structlog を設定し、ロガーオブジェクトを返す関数。
    コンソール (stdout) と指定されたファイルに出力する。

    Args:
        log_file_name (str): ログファイル名 (例: "app.log")

    Returns:
        structlog.BoundLogger: 設定済みのロガーオブジェクト
    """
    log_file_path = os.path.join(LOG_DIR, log_file_name)

    # Ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,  # Default to stdout, handlers will manage destinations
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.PATHNAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Define formatter using ConsoleRenderer for readability in both console and file
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(colors=False),  # No colors in file
        foreign_pre_chain=structlog.get_config()["processors"],
    )

    # Console handler (using configured formatter)
    handler_stdout = logging.StreamHandler(sys.stdout)
    handler_stdout.setFormatter(formatter)

    # File handler (using the same formatter)
    handler_file = logging.FileHandler(log_file_path, encoding="utf-8")
    handler_file.setFormatter(formatter)

    # Get the root logger, remove existing handlers, and add configured ones
    root_logger = logging.getLogger()
    # Remove default Streamlit handlers if they exist to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.addHandler(handler_stdout)
    root_logger.addHandler(handler_file)
    root_logger.setLevel(logging.INFO)  # Set root logger level

    return structlog.get_logger()
