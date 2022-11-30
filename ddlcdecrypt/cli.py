""" CLI interface and entrypoints. """

import argparse
import pathlib
import sys

from ddlcdecrypt import crypto


def print_warn(msg: str) -> None:
    """
    Print a warning message on stderr.

    Args:
        msg: Message to print.
    """
    print(f"Warning: {msg}", file=sys.stderr)


def read_args() -> argparse.Namespace:
    """
    Read command-line arguments.

    Returns:
        The parsed command-line arguments.
    """

    parser = argparse.ArgumentParser(
            description="Decrypt DDLC Plus! UnityFS assets."
    )

    parser.add_argument(
            "assets",
            nargs="+",
            type=pathlib.Path,
            help="assets to decrypt"
    )
    parser.add_argument(
            "destdir",
            type=pathlib.Path,
            help="directory where to place the decrypted assets"
    )

    return parser.parse_args()


def main(assets: list[pathlib.Path], destdir: pathlib.Path) -> None:
    """
    Core of ddlcdecrypt.

    Args:
        assets: Asset files to decrypt.
        destdir: Directory where to place the decrypted assets.
    """
    if not destdir.exists():
        print_warn(f"'{destdir}' is missing, creating now.\n")
        destdir.mkdir()

    for encrypted_asset in assets:
        decrypted_asset = crypto.compose_destination_path(encrypted_asset, destdir)

        print(f"Decrypting '{encrypted_asset}' and storing in '{decrypted_asset}'...")
        try:
            crypto.decrypt_file(encrypted_asset, decrypted_asset, crypto.UNITYFS_KEY)
        except OSError as exception:
            print_warn(f"{exception}\n")


def wrapper() -> None:
    """ Entrypoint for ddlcdecrypt. """
    args = read_args()

    main(args.assets, args.destdir)
