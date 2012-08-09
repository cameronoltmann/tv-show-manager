tv-show-manager
===============

TV Episode Manager - Manages downloaded TV episodes, keeping the best/highest quality copy of each episode

Inventory of concepts:
* Config file - implemented
* Media directory / home - implemented
* Folder structure
* Series
* Episodes
* Repacks/Propers
* Resolutions (hdtv/720p/etc)
* Naming conventions

Basic operation:
* Navigate tree
* Iterate through files
* Collect series names and episode numbers
* For any episodes with more than one file:
  * Prefer higher res
  * Within a resolution:
    * Prefer proper/repack
* Move obsolete files to junkyard
* After certain time, delete from graveyard

