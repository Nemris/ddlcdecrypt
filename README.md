# ddlcdecrypt

A quick and dirty Python 3.10+ decryptor for encrypted Doki Doki Literature Club Plus! Unity asset
files.

## Disclaimer and motivations

I originally created this tool as a way to prepare the assets bundles for extraction, for personal
use.

In no way shall I be responsible for your use of any assets you extract. Make sure to review
[Team Salvato's IP guidelines][1] concerning the "Additional Notes About DDLC Plus".

## Installation

Simply head to the [releases][2] page and download the latest release's .whl file. Then, to install
for the current user of a Linux-based system, execute:

```bash
python3 -m pip install --user <filename>
```

If your system is Windows, simply replace `python3` with `python.exe`.

## Usage

A brief help message can be displayed by running:

```bash
ddlcdecrypt -h
```

Here, valid assets files are those ending in .cy. Additionally, the output directory shall be
created if missing, including any intermediate directories.

Once processed, the resulting .bin files can be loaded and inspected in your Unity assets explorer
of choice.

### Overriding key verification

This tool contains basic verification to ensure that the files supplied to it can be decrypted with
the hardcoded key. If a file appears to be invalid, a warning is emitted and the file is skipped.

While this behavior is most likely what you want, you can force such files to be processed by
passing the `--no-verify` flag - but be warned that the resulting files may be unusable.

_Open an issue if you notice a warning concerning an invalid key._

### Displaying progress information

This tool doesn't normally output info unless errors occur, you can display the file being
processed by passing the `-v` flag.

## License

This program is licensed under the terms of the [MIT][3] license.

Check [LICENSE.txt][4] for further info.


[1]:https://teamsalvato.com/ip-guidelines/
[2]:https://github.com/Nemris/ddlcdecrypt/releases
[3]:https://choosealicense.com/licenses/mit/
[4]:./LICENSE.txt
