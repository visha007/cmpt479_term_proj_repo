import argparse
from .runner import runTests

def main():
    parser = argparse.ArgumentParser(description="Run only changed tests based on dependency tracking.")
    parser.add_argument('command', choices=['run', 'clean'], help='Command to execute')
    args = parser.parse_args()

    if args.command == 'run':
        runTests()
    elif args.command == 'clean':
        import os
        import shutil
        shutil.rmtree('jsonData', ignore_errors=True)
        print("Cache cleaned.")


if __name__ == "__main__":
    main()