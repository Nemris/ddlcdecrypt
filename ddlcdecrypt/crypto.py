""" Facilities for decryption and output file handling. """

import pathlib


UNITYFS_KEY = 0x28
DECRYPTED_EXTENSION = ".bin"  # No specific extension for UnityFS files.


def xor(data: bytes, key: int) -> bytes:
    """
    Perform a XOR operation on data.

    Args:
        data: Data to XOR.
        key: Key to use.

    Returns:
        The XORed data.
    """
    return bytes(
            byte ^ key
            for byte in data
    )


def decrypt_file(src: pathlib.Path, dest: pathlib.Path, key: int) -> None:
    """
    Decrypt the file at src with key, writing the result to dest.

    Args:
        src: File to decrypt.
        dest: Where to save the decrypted data.
        key: Integer key to decrypt the data with.
    """
    with src.open("rb") as infile:
        with dest.open("wb") as outfile:
            outfile.write(xor(infile.read(), key))


def compose_destination_path(src: pathlib.Path, destdir: pathlib.Path) -> pathlib.Path:
    """
    Compose the destination path of a decrypted asset file.

    Args:
        src: Encrypted asset file.
        destdir: Destination directory for the decrypted file.

    Returns:
        The full path and filename to store the decrypted asset as.
    """
    return (destdir
            .joinpath(src.name)
            .with_suffix(DECRYPTED_EXTENSION)
    )
