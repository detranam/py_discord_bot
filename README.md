# Discord Bot

## General TODO

These are just stretch goals I have in order to improve the bot overall.

- [ ] Convert to Linux to allow it to run on an Pi 3B
- [ ] Change my locally dependent variables to be top-level to allow for custom system locations (Or simply use linux :O )
- [ ] Change file separators (forward or back slash) to be platform independent
- [x] Add a log file to log the specific commands used and who used them
- [x] Document each method to allow syntax highlighting and for easier development
- [ ] Add 'cogs' or other classes to allow commands to be categorized more appropriately

## Music Download TODO

This is currently the main focus of this bot, to allow you to add youtube playlists to your 'profile' then download any new music to it.

- [x] Ensure that it doesn't 'double download' music if we already have it (a profile.json file for each download, a dry run to check what songs we already have)
- [ ] Superior logging on the completion of playlists and download progress
- [ ] Log when new folders are created
- [ ] Add a 'zip file' capability to compress all music into a single file for easy mobility

## Music Player TODO

Currently actually _playing_ music is a little hard, so this is a milestone in the future.

- [ ] Allow for a disconnect in the middle of playing a song
- [ ] Ability to queue music
- [ ] Ability to download the music in queue while playing other songs

## Book Bracket TODO

This was created to facilitate voting for a book club I'm in. This functionally works but doesn't work very well, and isn't finished.
Honestly, this utility could be extrapolated to more than just a 

- [x] Ability to add books
- [x] Ability to create a json 'bracket'
- [ ] Ability to only vote ONCE per user per each bracket battle
- [x] Extract the book bracket code into a new python file
- [ ] Conclude a battle and write who the victor is, increment battle count
- [ ] object in settings file that increments when a battle is concluded
- [ ] Check that once we have done an entire bracket, get all the winners, and create a new bracket, and update the settings
- [ ] Ability to redo bracket based on winners, removing losers
- [ ] Idiot-check using the book settings.json file to make sure we can't vote without anything happening etc
- [ ] Change the voting from a 'command' to a reaction to allow for cleaner message logs

## Ideas on music organization / autodeletion

Each user has a folder that holds their music, so if people request the same songs repeatedly then you'd be able to have them in an easy to access area.
Each song should be saved (then searched for) by the initial thing people searched for it, which would increase song finding.
