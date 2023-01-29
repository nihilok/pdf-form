#!/usr/bin/env python3
import subprocess
import time

import click


def wait_for_logs(cmd, msg):
    logs = subprocess.check_output(cmd)
    while msg not in logs.decode('utf-8'):
        time.sleep(0.1)
        logs = subprocess.check_output(cmd)


@click.group()
def tests():
    pass


@tests.command()
def pytest():
    print("Running all tests")
    subprocess.call(["pytest"])


@tests.command()
def mypy():
    print("Running mypy")
    subprocess.call(["mypy", "."])


@tests.command()
def run_tests():
    print("Unit tests:\n")
    cmd = ["pytest"]
    subprocess.call(cmd)
    wait_for_logs(cmd, "test session starts")
    print("\n")
    print("Type checking:\n")
    subprocess.call(["mypy", "."])


if __name__ == "__main__":
    tests()
