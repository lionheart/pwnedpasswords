#!/usr/bin/env python3
# vim: ft=python

import argparse
import sys
import logging
import math
import fileinput

from pwnedpasswords import Password
from pwnedpasswords import PasswordNotFound


class PwnedPasswordsCommandLineHandler(object):
    def __init__(self, namespace):
        self.plain_text = namespace.plain_text
        self.verbosity = logging.DEBUG if namespace.verbose else logging.WARNING

        # Configure logging handler for verbose output
        if namespace.verbose:
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(levelname)s:%(name)s:%(message)s'
            )

        try:
            self.password = Password(
                namespace.password, self.plain_text, verbosity=self.verbosity
            )
        except Exception:
            self.password = None

    def check_single_password(self, password):
        try:
            value = password.check()
        except PasswordNotFound:
            print("Password not found.")
            value = 0
        else:
            print(value)
        return value

    def run(self, *args):
        if self.password is None:
            try:
                for line in fileinput.input(files=["-"]):
                    password = Password(
                        line.strip(), self.plain_text, verbosity=self.verbosity
                    )
                    value = self.check_single_password(password)
            except KeyboardInterrupt:
                print("Quitting")
        else:
            value = self.check_single_password(self.password)

        if value > 0:
            # Most systems require exit status to be in the range 0-127, so
            # return 1 plus the base-10 log of the number of entries instead of
            # the full number of entries. This should be handy for scripts and
            # other CLI utilities that need to parse this output.
            sys.exit(1 + int(math.log10(value)))
        else:
            sys.exit(None)


def BoolAction(true_choice):
    class Action(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, option_string == true_choice)

    return Action


def main():
    parser = argparse.ArgumentParser(
        prog="pwnedpasswords",
        description="Checks Pwned Passwords API to see if provided plaintext data was found in a data breach.",
    )
    parser.add_argument(
        "--verbose",
        nargs=0,
        action=BoolAction("--verbose"),
        dest="verbose",
        default=False,
        help="Display verbose output.",
    )
    parser.add_argument(
        "--plain-text",
        nargs=0,
        action=BoolAction("--plain-text"),
        dest="plain_text",
        default=True,
        help="Specify that the provided input is plain text, even if it looks like a SHA-1 hash.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--stdin",
        nargs=0,
        action=BoolAction("--stdin"),
        dest="stdin",
        help="Read provided input from stdin.",
        default=False,
    )
    group.add_argument(
        "password",
        type=str,
        nargs="?",
        help="The password or hashed password to search for.",
    )

    namespace = parser.parse_args()
    handler = PwnedPasswordsCommandLineHandler(namespace)
    handler.run()


if __name__ == "__main__":
    main()
