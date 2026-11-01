# Komponenty i pochodzenie zasobów

- Powieść **PROCH**: Szymon Broma. Oznaczenie autorstwa widoczne na planszy
  tytułowej i końcowej. Prawa do powieści pozostają przy autorze.
- Kod adaptacji, scenariusz zagadki i proceduralne ilustracje: przygotowane
  dla tego projektu. Nie są ilustracjami z rękopisu.
- cc65: https://github.com/cc65/cc65, rewizja
  `52727a5b407bfeac0dfac1fdd84be8cd2af4f814`. Runtime C i `loader.system` z cc65. Licencja: [cc65.txt](licenses/cc65.txt).
  Lokalny `src/mouse.s` jest własnym interfejsem do firmware AppleMouse II /
  Apple IIc; gra odczytuje mysz bezpośrednio, bez obsługi przerwań.
- ProDOS i sektory startowe: binaria Apple Computer z obrazu systemowego
  `json/disks/prodos.json` projektu apple2js, rewizja
  `ee0aed25f73c69d0245e86a2a5fccb3324c3056c`:
  https://github.com/whscullin/apple2js. Są to składniki systemu Apple,
  nie kod napisany na potrzeby tej gry. Zachowano bajty oryginalnego kernela
  i bloków startowych. Plik systemowy zawiera oryginalne oznaczenia copyright.
- Czcionka: własne wzory pikselowe 5×7 w `tools/pixel_font.py`.
  Nie wymaga fontów systemowych. Plik licencji DejaVu pozostawiono jako
  informację o foncie użytym we wcześniejszej wersji prototypu.
- Emulator użyty w testach: apple2js / Will Scullin i współautorzy.
  Nie jest częścią obrazu gry i nie jest wymagany konkretnie ten emulator.
- Cadius / Brutal Deluxe: niezależne sprawdzenie struktury ProDOS podczas
  rozwoju; nie jest zależnością narzędzia budującego obrazy.

Do odtwarzania środowiska potrzebne są osobno Git, Make, kompilator C,
Python 3 i Pillow. Repozytorium nie zawiera ROM komputera
Apple II ani pełnego PDF powieści.
