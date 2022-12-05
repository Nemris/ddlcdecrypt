""" Facilities for decryption and output file handling. """

import pathlib
import typing


UNITYFS_KEY = 0x28
UNITYFS_MAGIC = b"UnityFS"
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


def decrypt_file(src: pathlib.Path, dest: pathlib.Path, key: int, check_magic: bool) -> None:
    """
    Decrypt the file at src with key, writing the result to dest.

    Args:
        src: File to decrypt.
        dest: Where to save the decrypted data.
        key: Integer key to decrypt the data with.
        check_magic: Whether to check the file's signature prior to
            decrypting it.

    Raises:
        OSError: When there are issues during handling of the source or
            destination files.
        ValueError: When a mismatch is detected in the source file's
            signature.
    """
    with src.open("rb") as infile:
        if check_magic and not is_magic_valid(infile):
            raise ValueError(f"'{src}': invalid magic for key 0x{UNITYFS_KEY:02x}")

        with dest.open("wb") as outfile:
            outfile.write(xor(infile.read(), key))


def is_magic_valid(file: typing.BinaryIO) -> bool:
    """
    Check if an encrypted asset contains the expected signature.

    Args:
        file: Asset to check.

    Returns:
        True if the asset contains the expected signature, False
            otherwise.
    """
    encrypted_magic = xor(UNITYFS_MAGIC, UNITYFS_KEY)

    position = file.tell()
    magic = file.read(len(encrypted_magic))
    file.seek(position)

    return magic == encrypted_magic


def compose_destination_path(src: pathlib.Path, destdir: pathlib.Path) -> pathlib.Path:
    """
    Compose the destination path of a decrypted asset file.

    Args:
        src: Encrypted asset file.
        destdir: Destination directory for the decrypted file.

    Returns:
        The full path and filename to store the decrypted asset as.
    """
    return (
            destdir
            .joinpath(src.name)
            .with_suffix(DECRYPTED_EXTENSION)
    )
