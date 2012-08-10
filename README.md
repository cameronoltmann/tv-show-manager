tv-show-manager
===============

TV Episode Manager - Manages downloaded TV episodes, keeping the best/highest quality copy of each episode

Inventory of concepts:
* Config file - implemented
* Media directory / home - implemented
* Folder structure - implemented
* Series - implemented
* Episodes - implemented
* Repacks/Propers
* Resolutions (hdtv/720p/etc)
* Naming conventions - crudely implemented

Basic operation:
* Navigate tree - implemented
* Iterate through files - implemented
* Collect series names and episode numbers - implemented
* For any episodes with more than one file:- identified
  * Prefer higher res
  * Within a resolution:
    * Prefer proper/repack
* Move obsolete files to junkyard
* After certain time, delete from graveyard

