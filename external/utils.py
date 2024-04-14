from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

# RESIZE = (1500, 2250)  # нада размеры как то подбирать - так не пойдет
# QUALITY = 10
# PATH = "E:/Temp/img/"


register_heif_opener()


class Convert:
    def __init__(self, path: str, save_path: str, quality: int, resize: tuple,  format: str):
        self._path = os.path.normpath(path)
        self._save_path = os.path.normpath(save_path) if save_path else self._path
        self._quality = quality
        self._resize = resize
        self._format = format

    def convert_to_webp(self, source: Path):
        """
            Convert image to WebP.
        """
        res_file = self._file_path(source, 'webp')
        image = Image.open(source)
        resize_true = all(self._resize)
        new_image = image.resize(self._resize) if resize_true else image

        new_image.save(
            res_file,
            format="webp",
            optimize=True,
            quality=self._quality,
        )

        return res_file

    def convert_to_bmp(self, source: Path):
        """
            Convert image to bmp.
        """
        res_file = self._file_path(source, 'bmp')

        image = Image.open(source)
        resize_true = all(self._resize)
        new_image = image.resize(self._resize) if resize_true else image

        new_image.save(
            res_file,
            format="bmp",
            optimize=True,
            quality=self._quality,
        )

        return res_file

    def convert_to_jpg(self, source: Path):
        """
            Convert image to jpg.
        """
        res_file = self._file_path(source, 'jpg')

        image = Image.open(source)
        resize_true = all(self._resize)
        new_image = image.resize(self._resize) if resize_true else image

        new_image.save(
            res_file,
            format="jpeg",
            optimize=True,
            quality=self._quality,
        )

        return res_file

    def _file_path(self, source: Path, ext: str) -> str:
        """
            Create result path.
        """
        path_repl: str = source.__str__().replace(self._path, '')
        len_suffix = len(source.suffix)
        if path_repl == '':
            if os.path.isfile(self._save_path):
                res_file = os.path.normpath(f'{self._save_path[:-len_suffix]}.{ext}')
            else:
                res_file = os.path.normpath(f'{self._save_path}/{source.stem}.{ext}')
        else:
            res_file = os.path.normpath(f'{self._save_path}/{path_repl[:-len_suffix]}.{ext}')
        os.makedirs(os.path.dirname(res_file), exist_ok=True)
        return res_file
    
    def paths(self, inp_formats: list[str]):
        """Generate list[paths] and return method."""
        _path = Path(self._path)
        paths = []
        if _path.is_file():
            suffix = _path.suffix.replace('.', '').lower()
            if suffix in inp_formats:
                paths = _path.parents[0].glob(_path.name)
        else:
            for frm in inp_formats:
                paths.extend(_path.glob(f"**/*.{frm}"))
        return paths

    def start_convert(self, inp_formats: list[str]) -> dict:
        """implementation by ThreadPoolExecutor."""
        paths = self.paths(inp_formats)
        fn_name = getattr(self, f'convert_to_{self._format}')
        with ThreadPoolExecutor(max_workers=None) as executor:
            results = list(executor.map(fn_name, paths))
        cnt = 0
        for _ in results:
            cnt += 1
        return {'count': cnt}
