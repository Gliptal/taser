TASER
======

**TA**cview **S**l**E**ds **R**enderer: dynamically generate `.xml` files to visually render SLED attack profiles in the Tacview 3D environment. This tool will generate the attack wire, and track, release, abort, and floor altitude blocks relative to a specific target in a specific NTTR conventional range.

Place `taser.exe` inside Tacview's `Data/Static Objects` folder:

![folder](http://i.imgur.com/UoaYtNk.jpg)

Open an elevated (administrator) cmd window in the folder:

![admin](http://i.imgur.com/WdNJzux.jpg)

Execute the application by typing `taser.exe` and passing all required and any optional parameters:

![cmd](http://i.imgur.com/lK5lKhR.jpg)

If no errors occur the application will generate an `.xml` and exit:

![result](http://i.imgur.com/DPDaZKN.jpg)

Analyze your attack runs with Tacview:

![tacview](http://i.imgur.com/B4emnDk.jpg)

USAGE
======

`taser.py [-h] [-o file] [-l ft] [-e °] -b nm -r ft -t ft -p ft -a ft -f ft range target`

`range` is the short name of the range containing the target (e.g. "64C")
`target` is the name of the target, with dashes "-" replacing spaces " " (e.g. "West-Bomb-Circle")

| required | flag | shorthand | purpose | unit | default |
| :---: | :---: | :---: | --- | :---: | :---: |
| YES | --base | -b | SLED's *base* distance | nm | |
| YES | --roll | -r | SLED's *roll-in* MSL altitude | ft | |
| YES | --track | -t | SLED's *track* MSL altitude | ft | |
| YES | --pickle | -p | SLED's *release* MSL altitude | ft | |
| YES | --abort | -a | SLED's *abort* MSL altitude | ft | |
| YES | --floor | -f | SLED's *mimimum* MSL altitude | ft | |
| | --out | -o | name of the generated `.xml` file | | "sled" |
| | --leeway | -l | available +/- leeway for the SLED's *roll-in*, *release*, and *track* altitudes | ft | 200ft |
| | --entry | -e | available +/- leeway for the range's attack heading at the SLED's *roll-in* altitude | ° | 10° |

Help is also available from the CLI itself by providing the `-h` (`--help`) flag.

FRAMEWORK
======

Development framework powered by [python](https://www.python.org/) and the following non-embedded plugins:

- [colorclass](https://pypi.python.org/pypi/colorclass)
- [dicttoxml](https://pypi.python.org/pypi/dicttoxml)
- [geopy](https://github.com/geopy/geopy)
- [PyYAML](http://pyyaml.org/)

BUILD
======

`.exe` packaging powered by [PyInstaller](http://www.pyinstaller.org/):

`pyinstaller --clean --workpath="../build" --distpath="../dist" --specpath="../dist" --add-data="../source/data;data" --onefile --icon="../dist/icon.ico" taser.py`

`.exe` versioning powered by [Simple Version Resource Tool](https://www.codeproject.com/articles/37133/simple-version-resource-tool-for-windows):

`verpatch.exe taser.exe /va /langid 0x0809 /high 0.6.0-beta1 /s desc "Generate Tacview .xml files to render SLED profiles." /s product "TAcview SlEds Renderer" /s (c) "CC Attribution-ShareAlike 4.0" /pv "0.6.0.0"`

DATA
======

The full targets data is not available in this public repository. Contact the [476th vFG](http://www.476vfightergroup.com/content.php) for further information.

CHANGELOG
======

Versioning follows [semantic versioning](http://semver.org/) rules.

[CHANGELOG.MD](https://github.com/Gliptal/tsr/blob/master/CHANGELOG.md)

CONTACTS
======

- [Mattia Affabris](https://github.com/Gliptal) - [donate](https://www.paypal.me/Gliptal)

LICENSE
======

[![license](https://i.creativecommons.org/l/by-sa/4.0/80x15.png)](http://creativecommons.org/licenses/by-sa/4.0/)

Taser by [Mattia Affabris](mailto:affa@outlook.it) is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

Based on a work at [https://github.com/Gliptal/taser](https://github.com/Gliptal/taser).
