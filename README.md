- [TASER](https://github.com/Gliptal/taser#taser)
- [INSTALL](https://github.com/Gliptal/taser#install)
- [USAGE](https://github.com/Gliptal/taser#usage)
- [EXAMPLES](https://github.com/Gliptal/taser#examples)
- [BUILD](https://github.com/Gliptal/taser#build)
- [DATA](https://github.com/Gliptal/taser#data)
- [CHANGELOG](https://github.com/Gliptal/taser#changelog)
- [CONTACTS](https://github.com/Gliptal/taser#contacts)
- [LICENSE](https://github.com/Gliptal/taser#license)

TASER
======

**TA**cview **S**L**E**Ds **R**enderer: dynamically generate [Tacview](http://www.tacview.net/) `.xml` files to render SLED attack profiles. All SLEDs parameters must be specified using the "SLED parameters" [flags](https://github.com/Gliptal/taser#usage); the target can be chosen from the conventional NTTR ranges ("range" option), or specified through a set of lat/lon coordinates ("coord" option). The resulting .xml renders in Tacview the ideal attack wire, among all relevant decision altitudes; leeway options are also available to restrict or relax the rendered wire's constraints.

![tacview](http://i.imgur.com/fM73mBE.jpg)

INSTALL
======

Download the latest [release](https://github.com/Gliptal/taser/releases) (1.0.0-rel1).

Place `taser.exe` inside Tacview's `Data/Static Objects` folder:

![folder](http://i.imgur.com/UoaYtNk.jpg)

USAGE
======

Open an elevated ("as administrator") command prompt (or PowerShell) window in Tacview's `Data/Static Objects` folder:

![admin](http://i.imgur.com/WdNJzux.jpg)

Run `taser.exe` by passing all required and any optional parameters (see [CLI](https://github.com/Gliptal/taser#cli)):

![cmd](http://i.imgur.com/ifD7Y0Z.jpg)

![result](http://i.imgur.com/VuHqmKg.jpg)

Analyze your attack runs with Tacview:

![tacview](http://i.imgur.com/fM73mBE.jpg)

CLI
======

`taser.exe [-h] [-v] [-d] [-f :str] [-c] [-ah :°] [-lh :°] [-la :ft] -ad :ft -bd :nm -ba :ft -ta :ft -ra :ft -aa :ft -ma :ft {range,coords}`

```
optional arguments:
  -h, --help                 show this help message and exit
  -v, --version              show program's version number and exit
  -d, --debug                show detailed error messages
  -f :str, --filename :str   specify the name of the output file [default:
                             "sled"]
  -c, --declutter            declutter the abort and minimum altitudes
                             rendering

other parameters (optional):
  -ah :°, --attackhdg :°     specify the attack heading (overrides the range's
                             default in "range" mode) [°]
  -lh :°, --leewayhdg :°     specify the leeway left and right of the attack
                             heading at the SLED's base altitude [° | default:
                             10°]
  -la :ft, --leewayalt :ft   specify the leeway above and below the SLED's
                             base, track, and release altitudes [ft | default:
                             200ft]

SLED parameters (required):
  -ad :ft, --aimdist :ft     SLED's aim-off distance [ft]
  -bd :ft, --basedist :ft    SLED's base distance [ft]
  -ba :ft, --basealt :ft     SLED's base altitude [ft MSL]
  -ta :ft, --trackalt :ft    SLED's track altitude [ft MSL]
  -ra :ft, --releasealt :ft  SLED's release altitude [ft MSL]
  -aa :ft, --abortalt :ft    SLED's abort altitude [ft MSL]
  -ma :ft, --minalt :ft      SLED's minimum altitude [ft MSL]

target mode:
  {range,coords}
    range                    choose the target from those in the conventional
                             NTTR ranges
    coords                   specify the target through a set of lat/lon
                             coordinates
```

`taser.exe range [-h] code target`

```
positional arguments:
  code        the code of the range
  target      the name of the target

optional arguments:
  -h, --help  show this help message and exit
```

`taser.exe coords [-h] latitude longitude`

```
positional arguments:
  latitude    the latitude coordinate of the target [xx.xx.xx.N]
  longitude   the longitude cooordinate of the target [xxx.xx.xx.W]
  altitude    the altitude of the target [ft MSL]

optional arguments:
  -h, --help  show this help message and exit
```

EXAMPLES
======

82_30DB4 SLED on West Bomb Circle in range 64C, default range attack heading, 15° leeway at wire entry:

![82_30DB4](http://i.imgur.com/5MMawCX.png)

`taser.exe -c -lh 15 -ad 1600 -bd 8507 -ba 8700 -ta 7100 -ra 6200 -aa 5900 -ma 4000 range 64C West-Bomb-Circle`

B2_30DB2 SLED on a target located at 35°10'22"N 116°50'11"W @ 5000ft MSL, 90° attack heading:

![B2_30DB2](http://i.imgur.com/sQStBo5.png)

`taser.exe -c -ah 90 -ad 1000 -bd 7898 -ba 9900 -ta 8300 -ra 7400 -aa 7100 -ma 6000 coords 35.10.22.N 116.50.11.W 5000`

BUILD
======

Development framework powered by [python](https://www.python.org/) and the following plugins:
- [colorclass](https://pypi.python.org/pypi/colorclass)
- [dicttoxml](https://pypi.python.org/pypi/dicttoxml)
- [geopy](https://github.com/geopy/geopy)
- [PyYAML](http://pyyaml.org/)
- [yamlordereddictloader](https://pypi.python.org/pypi/yamlordereddictloader)

`.exe` packaging powered by [PyInstaller](http://www.pyinstaller.org/):
`pyinstaller --clean --workpath="../build" --distpath="../dist" --specpath="../dist" --add-data="../source/data;data" --onefile --icon="../dist/icon.ico" taser.py`

`.exe` versioning powered by [Simple Version Resource Tool](https://www.codeproject.com/articles/37133/simple-version-resource-tool-for-windows):
`verpatch.exe dist/taser.exe /va /langid 0x0809 /high x.x.x /s desc "Generate Tacview .xml files to render SLED profiles." /s product "TAcview SLEDs Renderer" /s copyright "CC Attribution-ShareAlike 4.0" /pv "x.x.x-x"`

Automated `make.bat` and `test.bat` scripts can and must be ran from the project's root folder.

DATA
======

The ranges data is not available in this public repository. Contact the [476th vFG](http://www.476vfightergroup.com/content.php) for further information.

CHANGELOG
======

[CHANGELOG.md](https://github.com/Gliptal/tsr/blob/master/CHANGELOG.md) versioning follows [semantic versioning](http://semver.org/) rules.

CONTACTS
======

- [Mattia Affabris](https://github.com/Gliptal) - [donate](https://www.paypal.me/Gliptal)

LICENSE
======

[![license](https://i.creativecommons.org/l/by-sa/4.0/80x15.png)](http://creativecommons.org/licenses/by-sa/4.0/)

Taser by [Mattia Affabris](mailto:affa@outlook.it) is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
Based on a work at [https://github.com/Gliptal/taser](https://github.com/Gliptal/taser).
