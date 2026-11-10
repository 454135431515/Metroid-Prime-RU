# Metroid Prime: русский перевод для нативного порта

Полный перевод Metroid Prime (GameCube, USA 1.00) для ПК/Android-порта
[Odrannnn/MetroidPrimePort](https://github.com/Odrannnn/MetroidPrimePort): меню, подсказки,
сканы, журнал и титры, все 2141 строка. В шрифты игры дорисована кириллица, надписи на текстурах
(«ЭНЕРГИЯ», «НАЖМИТЕ START», названия регионов в лифтах) перерисованы по-русски. С импортом
Remastered текст рисуется HD-шрифтом с кириллицей.

Перевод самостоятельный: сделан с нуля по английскому тексту игры, не основан на переводе
Mastertranslate и никак с ним не связан.

В репозитории нет данных Nintendo: мод собирается у каждого из его собственного диска.

| | |
|---|---|
| ![Титульный экран](docs/screenshots/title.png) | ![Главное меню](docs/screenshots/menu.png) |
| ![Интерфейс](docs/screenshots/hud.png) | ![Пауза: снаряжение](docs/screenshots/pause.png) |
| ![Журнал](docs/screenshots/logbook.png) | ![Карта и легенда](docs/screenshots/map.png) |

## Что нужно
- порт [Odrannnn/MetroidPrimePort](https://github.com/Odrannnn/MetroidPrimePort/releases): последняя проверенная версия — **v0.44.0** (см. «Совместимость»). С v0.44.0 по-русски и строки самого порта: «Выйти из игры», его пункты в паузе, легенда карты; на старых версиях они остаются английскими. На более новых версиях перевод, скорее всего, тоже работает; если что-то сломалось, [откройте issue](https://github.com/454135431515/metroid-prime-ru/issues) с версией порта и логом;
- свой образ **Metroid Prime USA 1.00** (`GM8E01`, ревизия 0) в ISO; другие ревизии и PAL
  не поддерживаются;
- Python 3 с пакетами Pillow и numpy: `pip install Pillow numpy`.

## Совместимость
Последняя проверка: порт **v0.44.0**, 10 ноября 2026, — **пройдена**.
- Все 276 комнат загружаются с импортом Remastered и без: вылетов и ошибок загрузки ресурсов нет.
- Главное меню и «Выйти из игры» проверены в игре; пункты паузы и легенда карты — по ширине текста в
  шрифтах мода.
- Все проверки `tools/test.sh` прошли.

Известное: комната `83F6FF6F/3C785450` при автоматическом обходе иногда отвечает пустой ошибкой
перехода; прямой переход в неё работает, так было и на прошлых версиях порта.

## Сборка
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

На Android мод собирается на ПК: скопируйте папку импорта `remastered-models` с телефона в папку,
куда собираете мод, соберите и верните на телефон `russian` и `hud-russian`. Тысячи мелких файлов
по MTP копируются плохо: удобнее возить один zip и распаковывать его на месте.


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
[MetroidPrimePort](https://github.com/Odrannnn/MetroidPrimePort) (compatibility checked on v0.44.0, which also lets the port's own strings be translated; if a newer port version breaks it, please open an issue). It is an independent translation made from scratch, not based on or affiliated with the
Mastertranslate translation. No Nintendo data is
included: build the mod from your own disc with the two commands above (Python 3, Pillow, numpy)
and put the `russian` and `hud-russian` folders into the port's `mods` folder. With the Remastered import present,
the build also adds a Cyrillic HD font. Code is MIT, translation text is CC BY 4.0.
