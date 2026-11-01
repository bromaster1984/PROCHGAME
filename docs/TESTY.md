# Weryfikacja wersji 0.1

## Czytelność tekstu

Aktualizacja 1 listopada 2026: wszystkie napisy używają własnej czcionki
pikselowej 5×7 w komórkach 7×8. Napisy plansz są rysowane pełnymi białymi
pikselami na czarnym tle; nie są rastrowane z fontów wektorowych.
Czytelność sprawdzono na rzeczywistych zrzutach HGR z emulatora.

## Budowa i format

- Kompilacja cc65 dla `apple2enh` (65C02): bez ostrzeżeń.
- Test struktury: 560 mapowań sektorów DOS/ProDOS, poprawne bloki startowe,
  osiem plików, brak współdzielonych bloków, zgodność bitmapy wolnego miejsca,
  zgodność wszystkich pięciu plików HGR ze źródłowymi zasobami.
- Niezależny `cadius CHECKVOLUME`: brak zgłoszonych błędów.
- Dwukrotna budowa: identyczny bajt po bajcie obraz `.dsk`.
- `git diff --check`: bez błędów białych znaków.

## Rozgrywka

**Wynik: PASS. Pełne przejście z zapisem i odczytem potwierdzone
przy 1,023 MHz. Wcześniejszy test rozgrywki przeszedł również przy 8 MHz.**

Skrypt `tests/emulator.cjs` uruchamia rzeczywistą dyskietkę w apple2js,
enhanced Apple IIe z kartą AppleMouse II w slocie 4. Wprowadza ruchy i kliknięcia
przez zdarzenia myszy przeglądarki, odczytuje wynik z natywnego programu 65C02.
Nie podmienia stanu zagadki w pamięci. Reset postępu wykonuje publicznym
poleceniem R, a odczyt — L.

Zakres testu: zimny start, wykrycie myszy, niedopuszczenie do zakończenia przed
skopiowaniem listu, przejście całej zagadki, zapis na dyskietce, nowa gra,
odczyt zapisu, dojście do planszy końcowej. Wynik i prędkość procesora:
`dist/emulator-results.json`. Zrzuty `*-test.png` oraz `ekran-tytulowy.png`
pochodzą z emulatora, a nie z makiety interfejsu.

Emulator i zależności do testów przygotowano poza repozytorium:
`/workspace/tools/apple2js`. Po uruchomieniu jego serwera lokalnego na porcie 8123:

```sh
node tests/emulator.cjs
# Pełny test z prędkością zbliżoną do standardowego Apple II:
TEST_KHZ=1023 node tests/emulator.cjs
```

Domyślnie test przyspiesza emulowany procesor do 8 MHz. Obie prędkości mają
te same reguły gry; test nie wymaga grafiki ani timera działającego poza Apple II.
Wynik nie potwierdza działania na fizycznym Apple IIc ani odtworzenia środowiska
w nowym zadaniu. Sprzętowy test IIc, jego konkretnej wersji ROM i myszy
pozostaje do wykonania. Wersja nie zawiera dalszych dyskietek ani pełnego rozdziału.
