TASER
======

**TA**cview **S**l**E**ds **R**enderer: dynamically generate `.xml` files to visually render SLED attack profiles in the Tacview 3D environment. This tool will generate the attack wire, and track, release, abort, and floor altitude blocks relative to a specific target in a specific NTTR conventional range.

INSTALL
======

[Download](https://github.com/Gliptal/taser/releases) the latest release.

Place `taser.exe` inside Tacview's `Data/Static Objects` folder:

![folder](http://i.imgur.com/UoaYtNk.jpg)

USAGE
======

Open an elevated (administrator) cmd window in the folder:

![admin](http://i.imgur.com/WdNJzux.jpg)

Execute the application by typing `taser.exe` and passing all required and any optional parameters:

![cmd](http://i.imgur.com/ifD7Y0Z.jpg)

If no errors occur the application will generate an `.xml` and exit:

![result](http://i.imgur.com/VuHqmKg.jpg)

Analyze your attack runs with Tacview:

![tacview](http://i.imgur.com/fM73mBE.jpg)

CLI
======

`taser.py [-h] [-v] [-fn str] [-la ft] [-lh °] [-ah °] [-dc] -bd nm -ba ft -ta ft -ra ft -aa ft -ma ft range target`

`range` is the short name of the range containing the target (e.g. "64C")

`target` is the name of the target, with dashes "-" replacing spaces " " (e.g. "West-Bomb-Circle")

| required | flag | shorthand | purpose | unit | default |
| :---: | :---: | :---: | --- | :---: | :---: |
| Y | --basedist | -bd | SLED's *base* distance | nm | |
| Y | --basealt | -ba | SLED's *base* MSL altitude | ft | |
| Y | --trackalt | -ta | SLED's *track* MSL altitude | ft | |
| Y | --releasealt | -ra | SLED's *release* MSL altitude | ft | |
| Y | --abortalt | -aa | SLED's *abort* MSL altitude | ft | |
| Y | --minalt | -ma | SLED's *mimimum* MSL altitude | ft | |
| Y | --aimdist | -ad | *aim-off* distance | ft | |
| | --leewayalt | -la | available +/- leeway for the SLED's *base*, *track*, and *release* altitudes | ft | 200ft |
| | --leewayhdg | -lh | available +/- leeway for the range's attack heading at the SLED's *base* altitude | ° | 10° |
| | --attackhdg | -ah | required attack heading, overrides the range's default | ° | |
| | --declutter | -dc | declutter the target area by rendering the *abort* and *minimum* altitudes as planes | | |
| | --filename | -fn | name of the generated `.xml` file | | "sled" |

| flag | shorthand | purpose |
| :---: | :---: | --- |
| --help | -h | show the help message |
| --version | -v | show the version number |
| --debug | -d | show more exhaustive error messages |

FRAMEWORK
======

Development framework powered by [python](https://www.python.org/) and the following non-embedded plugins:

+ [colorclass](https://pypi.python.org/pypi/colorclass)
+ [dicttoxml](https://pypi.python.org/pypi/dicttoxml)
+ [geopy](https://github.com/geopy/geopy)
+ [PyYAML](http://pyyaml.org/)
+ [yamlordereddictloader](https://pypi.python.org/pypi/yamlordereddictloader/0.1.1)

BUILD
======

`.exe` packaging powered by [PyInstaller](http://www.pyinstaller.org/):

`pyinstaller --clean --workpath="../build" --distpath="../dist" --specpath="../dist" --add-data="../source/data;data" --onefile --icon="../dist/icon.ico" taser.py`

`.exe` versioning powered by [Simple Version Resource Tool](https://www.codeproject.com/articles/37133/simple-version-resource-tool-for-windows):

`verpatch.exe taser.exe /va /langid 0x0809 /high x.x.x-x /s desc "Generate Tacview .xml files to render SLED profiles." /s product "TAcview SlEds Renderer" /s (c) "CC Attribution-ShareAlike 4.0" /pv "x.x.x.x"`

Automated `make.bat` and `test.bat` scripts can be ran from the root folder.

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
