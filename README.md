BattStatsX
==========

A no-frills battery statistics viewer for OSX, inspired by the GNOME Power Statistics app!

Currently, the application is just a simple python script, but hopefully it will evolve into something much more soon!

Introduction
------------
Since getting a MacBook Pro, I've been always itching to know the actual time it lasts on battery. The activity monitor provides the time since the laptop was last unplugged, but this also includes the time the laptop was on sleep, which does not really give the best measure as to how much the battery really last (As OSX does an amazing job at using very little battery when on sleep). This script runs through the system logs to actually figure out the time the laptop has been on battery and not sleeping!

Run the script
--------------
```bash
python BattStatsX.py
```
or
```bash
chmod +x BattStatsX.py
./BattStatsX.py
```
