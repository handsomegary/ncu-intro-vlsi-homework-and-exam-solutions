"""Shared, non-executing prerequisite checks for the public HSPICE drivers."""
import json
import os
from pathlib import Path
import shutil


def default_hspice():
    return os.environ.get('HSPICE') or shutil.which('hspice') or shutil.which('hspice.com')


def default_model():
    return os.environ.get('CIC018_MODEL')


def resolve_hspice(value):
    if not value:
        raise ValueError('Supply --hspice PATH, set HSPICE, or put hspice on PATH.')
    selected = Path(value).expanduser()
    executable = str(selected) if selected.is_file() else shutil.which(str(value))
    if not executable or not Path(executable).is_file():
        raise ValueError('HSPICE executable not found. Supply --hspice with your installed executable.')
    selected = Path(executable).resolve()
    if os.name != 'nt' and not os.access(selected, os.X_OK):
        raise ValueError('The selected HSPICE executable is not executable.')
    return str(selected)


def resolve_model(value):
    if not value:
        raise ValueError('Supply --model PATH or set CIC018_MODEL to your authorized process model.')
    selected = Path(value).expanduser().resolve()
    if not selected.is_file():
        raise ValueError('Process model not found. Supply --model with your authorized local CIC018 file.')
    if "'" in selected.as_posix():
        raise ValueError("Move or link the model to a path without an apostrophe for HSPICE .lib quoting.")
    return selected


def add_environment_check(parser):
    parser.add_argument('--check-environment', action='store_true',
                        help='Check executable/model locations, then exit without simulation or writes.')


def resolve_simulation_args(parser, args, skip=False):
    """Validate before a driver creates output. Checks never start the simulator."""
    if skip and not args.check_environment:
        # Analytical/deck-preparation modes do not require a licensed environment.
        # This placeholder is only a declaration in unexecuted generated decks.
        args.model = Path(args.model or 'CIC018_MODEL_REQUIRED.l').expanduser().resolve()
        return
    try:
        args.hspice = resolve_hspice(args.hspice)
        args.model = resolve_model(args.model)
    except ValueError as exc:
        parser.error(str(exc))
    if args.check_environment:
        print(json.dumps({'status':'ready_to_attempt_simulation',
                          'hspice':args.hspice,'model':str(args.model),
                          'license_and_model_compatibility':'not probed'}, indent=2))
        parser.exit(0)
