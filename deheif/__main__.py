#!/usr/bin/env python3

# Copyright 2023 Stefan Götz <github.nooneelse@spamgourmet.com>

# This file is part of deheif.

# deheif is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.

# deheif is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with deheif. If not, see <https://www.gnu.org/licenses/>.

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import List


def _main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        filename=str(Path.home() / "deheif.log"),
        format="%(asctime)s %(levelname)s:%(message)s",
    )

    top_dir: Path = Path(sys.argv[1])
    assert top_dir.exists()

    files: List[Path] = _find_heif_files(top_dir)
    _convert(files)
    _delete(files)


def _find_heif_files(top_dir: Path) -> List[Path]:
    return list(top_dir.rglob("*.HEIC"))


def _convert(files: List[Path]) -> None:
    for file in files:
        inp = str(file)
        out = file.parent / (file.stem + ".jpg")
        out_path = Path(out)
        if not out_path.exists():
            logging.info("Converting %s to %s...", inp, out)
            subprocess.run(["convert", inp, out], check=True)
            os.utime(out, (file.stat().st_atime, file.stat().st_mtime))


def _delete(files: List[Path]) -> None:
    def _get_mtime(path: Path) -> int:
        return int(path.stat().st_mtime)

    files.sort(key=_get_mtime)
    files_to_delete = files[:-10]
    for file in files_to_delete:
        logging.info("Deleting %s...", file)
        file.unlink()


if __name__ == "__main__":
    _main()
