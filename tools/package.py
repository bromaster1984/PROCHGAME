"""Package the tested disk, manual, licences and actual emulator screenshots."""
from pathlib import Path
import zipfile
root = Path(__file__).resolve().parents[1]
files = [root / 'README.md', *sorted((root / 'docs').rglob('*'))]
files += [root / 'dist' / n for n in [
    'PROCH_EPIZOD_1.dsk', 'PROCH_EPIZOD_1.po', 'SHA256SUMS',
    'ekran-tytulowy.png', 'gabinet-test.png', 'zakonczenie-test.png',
    'emulator-results.json',
]]
output = root / 'dist/PROCH_EPIZOD_1.zip'
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        if path.is_file():
            archive.write(path, 'PROCH_EPIZOD_1/' + str(path.relative_to(root)))
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
print(f'Created {output} ({output.stat().st_size} bytes)')
