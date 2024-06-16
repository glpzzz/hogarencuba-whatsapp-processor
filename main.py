import argparse
from commands import enqueue, dequeue


def main():
    parser = argparse.ArgumentParser(description="CLI for task processing")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("dequeue", help="Dequeue a task")

    args = parser.parse_args()

    if args.command == "dequeue":
        dequeue.process()


if __name__ == "__main__":
    main()
