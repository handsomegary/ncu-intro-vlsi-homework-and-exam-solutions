"""Check public HSPICE prerequisites without launching CAD or reading model contents."""
import argparse
from simulation_environment import (add_environment_check, default_hspice,
                                    default_model, resolve_simulation_args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hspice', default=default_hspice())
    parser.add_argument('--model', default=default_model())
    add_environment_check(parser)
    args = parser.parse_args()
    args.check_environment = True
    resolve_simulation_args(parser, args)


if __name__ == '__main__':
    main()
