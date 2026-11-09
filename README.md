# Metroid Prime: русский перевод для нативного порта

Полный перевод Metroid Prime (GameCube, USA 1.00) для ПК/Android-порта
[Odrannnn/MetroidPrimePort](https://github.com/Odrannnn/MetroidPrimePort): меню, подсказки,
сканы, журнал и титры, все 2141 строка. В шрифты игры дорисована кириллица, надписи на текстурах
(«ЭНЕРГИЯ», «НАЖМИТЕ START», названия регионов в лифтах) перерисованы по-русски. С импортом
Remastered текст рисуется HD-шрифтом с кириллицей.

В репозитории нет данных Nintendo: мод собирается у каждого из его собственного диска.

| | |
|---|---|
| ![Титульный экран](docs/screenshots/title.png) | ![Главное меню](docs/screenshots/menu.png) |
| ![Интерфейс](docs/screenshots/hud.png) | ![Пауза: снаряжение](docs/screenshots/pause.png) |
| ![Журнал](docs/screenshots/logbook.png) | ![Карта и легенда](docs/screenshots/map.png) |

## Что нужно
- порт [Odrannnn/MetroidPrimePort](https://github.com/Odrannnn/MetroidPrimePort/releases): совместимость проверена на **v0.43.0** (9 ноября 2026: все 276 комнат с Remastered и без, меню, HUD, карта, пауза, журнал). На более новых версиях перевод, скорее всего, тоже работает; если что-то сломалось, [откройте issue](https://github.com/454135431515/metroid-prime-ru/issues) с версией порта и логом;
- свой образ **Metroid Prime USA 1.00** (`GM8E01`, ревизия 0) в ISO; другие ревизии и PAL
  не поддерживаются;
- для сборки на Android или из исходников: Python 3 с пакетами Pillow и numpy
  (`pip install Pillow numpy`). На Windows, Linux и macOS Python не нужен, см. ниже.

## Установка без Python (Windows, Linux, macOS)
Мод собирается самим портом, из меню.
1. Скачайте архив импортёра для своей системы со страницы
   [Releases](https://github.com/454135431515/metroid-prime-ru/releases):
   `russian-importer-windows-x86_64.zip`, `-linux-x86_64.tar.gz` или `-macos-arm64.zip`.
2. Распакуйте файл `russian` (Windows: `russian.exe`) в папку `importers` рядом с папкой `mods`
   порта (создайте её; где лежит `mods`, см. ниже).
3. Если играете с Remastered, сначала сделайте его импорт (F1 → Mods → Built-in mods → Prime
   Remastered).
4. F1 → Mods: в списке импортёров у `russian` нажмите **Run**. Поле аргумента можно оставить
   пустым: импортёр возьмёт образ, выбранный в порте. Другой образ — укажите полный путь к `.iso`
   в этом поле.
5. После «Готово» перезапустите игру.

После нового импорта Remastered или обновления перевода нажмите Run ещё раз.

## Сборка из исходников
```sh
python -I tools/extract.py "Metroid Prime (USA).iso" work
python -I tools/build_mod.py work/res text/ru.json <папка mods порта>/russian
```

Сборка создаёт в папке `mods` две папки: `russian` (текст, шрифты, надписи на текстурах) и
`hud-russian` (кадры HUD). Нужны обе; если собирали в другом месте, скопируйте в `mods` обе.

Папка `mods` порта:
- Windows: `user\mods` рядом с `metroid_prime_port.exe`;
- Linux AppImage: `mods` рядом с файлом `.AppImage`;
- Android: `/storage/emulated/0/MetroidPrime/mods` (сначала F1 → System → Data folder →
  общая память).

Язык текста в настройках порта должен остаться английским (по умолчанию): перевод заменяет
английскую секцию.

### Remastered
Если в той же папке `mods` уже есть импорт `remastered-models`, сборка добавляет HD-шрифт с
кириллицей (`russian/font/deface.sdfont`). Он строится из шрифта импорта и появляется только вместе
с ним. Импорт делается до сборки мода; после нового импорта мод нужно пересобрать. Без Remastered
игра использует растровые шрифты с кириллицей.


## Не выкладывайте собранный мод
Собранные папки `russian` и `hud-russian` содержат изменённые файлы игры (шрифты, интерфейс, таблицы строк).
Раздавайте этот репозиторий, а не результат сборки.

## Для разработки
Все проверки: `tools/test.sh` (нужен `work/` от `extract.py`). Тикеты лежат в `docs/tickets/`,
решения в `docs/adr/`, глоссарий в `text/glossary.md`.

## Лицензия
Код (`tools/`) под лицензией MIT, см. `LICENSE`. Перевод и глоссарий (`text/`) под CC BY 4.0,
см. `text/LICENSE`. Metroid Prime является товарным знаком Nintendo; проект с Nintendo не связан.

---

**English.** A complete Russian translation of Metroid Prime (GameCube USA 1.00) for the native
[MetroidPrimePort](https://github.com/Odrannnn/MetroidPrimePort) (compatibility checked on v0.43.0; if a newer port version breaks it, please open an issue). No Nintendo data is
included: put the importer from Releases into the `importers` folder beside the port's `mods`
folder and press F1 > Mods > russian > Run, or build the mod from your own disc with the two
commands above (Python 3, Pillow, numpy) and put the `russian` and `hud-russian` folders into
`mods`. With the Remastered import present,
the build also adds a Cyrillic HD font. Code is MIT, translation text is CC BY 4.0.
