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
    parser.add_argument(
            "-f",
            "--force-decrypt",
            action="store_true",
            help="skip verifying the decryption key and decrypt anyway"
    )

    return parser.parse_args()


def main(assets: list[pathlib.Path], destdir: pathlib.Path, force_decrypt: bool) -> None:
    """
    Core of ddlcdecrypt.

    Args:
        assets: Asset files to decrypt.
        destdir: Directory where to place the decrypted assets.
        force_decrypt: Whether to force the decryption process.
    """
    if not destdir.exists():
        print_warn(f"'{destdir}' is missing, creating now.\n")
        destdir.mkdir()

    for encrypted_asset in assets:
        if (
                not force_decrypt
                and not crypto.can_key_decrypt_asset(encrypted_asset, crypto.UNITYFS_KEY)
        ):
            print_warn(f"skipping '{encrypted_asset}': invalid key.\n")
            continue

        decrypted_asset = crypto.compose_destination_path(encrypted_asset, destdir)

        print(f"Decrypting '{encrypted_asset}' and storing in '{decrypted_asset}'...")
        try:
            crypto.decrypt_file(encrypted_asset, decrypted_asset, crypto.UNITYFS_KEY)
        except OSError as exception:
            print_warn(f"{exception}\n")


def wrapper() -> None:
    """ Entrypoint for ddlcdecrypt. """
    args = read_args()

    main(args.assets, args.destdir, args.force_decrypt)
