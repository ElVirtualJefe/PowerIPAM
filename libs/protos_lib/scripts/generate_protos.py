"""
Script to generate protobuf files for the PowerIPAM project.
"""

import os
from logging import basicConfig, getLogger

try:
    from logging_lib import get_logger, configure_logging
except ImportError:
    basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=os.getenv("LOG_LEVEL", "INFO").upper()
    )
    logger = getLogger("protos_lib.generate_protos")
else:
    configure_logging(
        service_name="protos-lib-generator",
        environment=os.getenv("ENVIRONMENT", "development"),
        level=os.getenv("LOG_LEVEL", "DEBUG").upper(),
        log_format="console",
        logger_name="protos_lib.generate_protos",
    )
    logger = get_logger("protos_lib.generate_protos")

from pathlib import Path
from argparse import ArgumentParser
from time import monotonic
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTO_ROOT = ROOT / "proto"
DEFAULT_OUTPUT_ROOT = ROOT / "src" / "protos_lib" / "generated"

logger.debug(f"ROOT: {ROOT}")
logger.debug(f"DEFAULT_PROTO_ROOT: {DEFAULT_PROTO_ROOT}")
logger.debug(f"DEFAULT_OUTPUT_ROOT: {DEFAULT_OUTPUT_ROOT}")

def parse_args() -> ArgumentParser:
    parser = ArgumentParser(description="Generate protobuf files for the PowerIPAM project.")
    parser.add_argument(
        "--proto-root",
        type=Path,
        default=DEFAULT_PROTO_ROOT,
        help="Root directory of the proto files."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Root directory for the generated protobuf files."
    )
    return parser.parse_args()

def generate(proto_root: Path, output_dir: Path) -> None:
    proto_root = proto_root.resolve()
    output_dir = output_dir.resolve()

    if not proto_root.is_dir():
        raise FileNotFoundError(f"Proto source directory does not exist: {proto_root}")

    proto_files = sorted(proto_root.rglob("*.proto"))
    if not proto_files:
        raise FileNotFoundError(f"No .proto files found under: {proto_root}")

    # Use paths relative to proto_root, preserving version directories in generated imports.
    relative_proto_files = [path.relative_to(proto_root).as_posix() for path in proto_files]
    logger.info("Found %d protobuf source file(s) under %s", len(proto_files), proto_root)
    for proto_file in relative_proto_files:
        logger.debug("Protobuf source: %s", proto_file)

    try:
        import grpc_tools
    except ImportError as exc:
        raise RuntimeError(
            "grpcio-tools is required to generate protobuf files.  "
            "Please install it with: python -m pip install grpcio-tools"
        ) from exc

    google_proto_include = Path(grpc_tools.__file__).resolve().parent / "_proto"
    command = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={proto_root.as_posix()}",
        f"--proto_path={google_proto_include.as_posix()}",
        f"--python_out={output_dir.as_posix()}",
        f"--grpc_python_out={output_dir.as_posix()}",
        *relative_proto_files
    ]

    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Generating Python protobuf files and gRPC stubs into %s", output_dir)
    logger.debug("Running protoc command: %s", " ".join(command))
    started_at = monotonic()

    try:
        result = subprocess.run(
            command,
            cwd=proto_root,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as exc:
        if exc.stdout:
            logger.info("protoc stdout: \n%s", exc.stdout.rstrip())
        if exc.stderr:
            logger.error("protoc reported errors: \n%s", exc.stderr.rstrip())
        logger.exception("Protobuf generation failed with exit code %s", exc.returncode)
        raise

    if result.stdout.strip():
        logger.debug("protoc stdout: \n%s", result.stdout.rstrip())
    if result.stderr.strip():
        logger.warning("protoc stderr: \n%s", result.stderr.rstrip())

    for version_dir in sorted(path for path in output_dir.iterdir() if path.is_dir()):
        init_file = version_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Generated protobuf modules"""\n', encoding="utf-8")
            logger.debug("Created Python package initializer: %s", init_file)

    generated_files = sorted(path for path in output_dir.rglob("*.py") if path.is_file())
    elapsed = monotonic() - started_at
    logger.info(
        "Protobuf generation completed: %d Python file(s) in %.2f seconds",
        len(generated_files),
        elapsed
    )
    for generated_file in generated_files:
        logger.debug("Generated Python file: %s", generated_file.relative_to(output_dir))


def main() -> int:
    args = parse_args()
    logger.debug("Parsed arguments:")
    logger.debug("proto_root: %s", args.proto_root)
    logger.debug("output_root: %s", args.output_root)

    try:
        generate(args.proto_root, args.output_root)
    except Exception as e:
        logger.exception("Error generating protobuf files: %s", e)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
