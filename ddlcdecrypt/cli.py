""" CLI interface and entrypoints. """

import argparse
import logging
import pathlib

from ddlcdecrypt import crypto


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
            "--no-verify",
            action="store_false",
            default=True,
            help="skip asset file signature check, decrypt even on invalid key",
            dest="verify"
    )
    parser.add_argument(
            "-v",
            "--verbose",
            action="store_const",
            const=logging.INFO,
            default=logging.WARNING,
            help="display verbose information",
            dest="loglevel"
    )

    return parser.parse_args()


def main(assets: list[pathlib.Path], destdir: pathlib.Path, verify_assets: bool) -> None:
    """
    Core of ddlcdecrypt.

    Args:
        assets: Asset files to decrypt.
        destdir: Directory where to place the decrypted assets.
        verify_assets: Whether to check if the assets can be decrypted.
    """
    if not destdir.exists():
        logging.warning("'%s' not found - creating now.\n", destdir)
        destdir.mkdir()

    for encrypted_asset in assets:
        decrypted_asset = crypto.compose_destination_path(encrypted_asset, destdir)

        logging.info("'%s' -> '%s'", encrypted_asset, decrypted_asset)
        try:
            crypto.decrypt_file(
                    encrypted_asset,
                    decrypted_asset,
                    crypto.UNITYFS_KEY,
                    verify_assets
            )
        except OSError as exception:
            logging.error("'%s': %s", exception.filename, exception.strerror)
        except ValueError as exception:
            logging.warning("%s", exception)


def wrapper() -> None:
    """ Entrypoint for ddlcdecrypt. """
    args = read_args()
    logging.basicConfig(
            format="[%(levelname)s] %(message)",
            level=args.loglevel
    )

    main(args.assets, args.destdir, args.verify)
