# p2000 [![Build Status](https://travis-ci.org/hvanderlaan/p2000.svg?branch=master)](https://travis-ci.org/hvanderlaan/p2000)
python script that will show the dutch ems pager services

```bash
$ ./p2000.py [region code]
$ ./p2000.py [1-25, 40]
$ ./p2000.py [grip|tis|knrm]
```

### requirements
     - working internet connection
     - p2000lib/p2000.py
     - p2000.cfg

### todo
- [ ] add live modus for continues updates
- [ ] add database support for saving history (mysql or sqlite3)

### alterations of dutch alert regions
The default region is set to 'whole netherlands' this can be changed by adding the region code as a parameter

The following regions can be used:

### region information

|region code|name of region             |
|:---------:|:-------------------------:|
|1          |groningen                  |
|2          |friesland                  |
|3          |drenthe                    |
|4          |ijsselland                 |
|5          |twente                     |
|6          |noord-en-oost-gelderland   |
|7          |gelderland-midden          |
|8          |gelderland-zuid            |
|9          |utrecht                    |
|10         |noord-holland-noord        |
|11         |aaanstreek-waterland       |
|12         |kennemerland               |
|13         |amsterdam-amstelland       |
|14         |gooi-en-vechtstreek        |
|15         |haaglanden                 |
|16         |hollands-midden            |
|17         |rotterdam-eijnmond         |
|18         |zuid-holland-zuid          |
|19         |zeeland                    |
|20         |midden-en-west-brabant     |
|21         |brabant-noord              |
|22         |brabant-zuidoost           |
|23         |limburg-noord              |
|24         |zuid-limburg               |
|25         |flevoland                  |
|40         |geheel-nederland           |
|51         |grip                       |
|53         |tis                        |

### licensing and credits
p2000 is licensed under the GPLv3:
```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For the full license, see the LICENSE file.
```

[more info about the regions](https://nl.wikipedia.org/wiki/Veiligheidsregio)

[great thanks to p2000mobiel.nl for theire website](http://p2000mobiel.nl)
