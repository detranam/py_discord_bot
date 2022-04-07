# Discord Bot

## General TODO

- [ ] Convert to Linux to allow it to run on an Pi 3B
- [ ] Remove code to allow bot to be public
- [ ] Change my locally dependent variables to be top-level to allow for custom system locations
- [ ] Add a log file to log the specific commands used and who used them

## Music Download TODO

- [x] Ensure that it doesn't 'double download' music if we already have it (a profile.json file for each download, a dry run to check what songs we already have)
- [ ] Superior logging on the completion of playlists and download progress
- [ ] Log when new folders are created

## Music Player TODO

- [ ] Allow for a disconnect in the middle of playing a song
- [ ] Ability to queue music
- [ ] Ability to download the music in queue while playing other songs

## Book Bracket TODO

- [x] Ability to add books
- [x] Ability to create a json 'bracket'
- [ ] Ability to only vote ONCE per user per each bracket battle
- [ ] Extract the book bracket code into a new python file
- [ ] Conclude a battle and write who the victor is, increment battle count
- [ ] object in settings file that increments when a battle is concluded
- [ ] Check that once we have done an entire bracket, get all the winners, and create a new bracket, and update the settings
- [ ] Ability to redo bracket based on winners, removing losers
- [ ] Idiot-check using the book settings.json file to make sure we can't vote without anything happening etc

## Ideas on music organization / autodeletion

Each user has a folder that holds their music, so if people request the same songs repeatedly then you'd be able to have them in an easy to access area.
Each song should be saved (then searched for) by the initial thing people searched for it, which would increase song finding.
Ideally put all search terms into a big json file loaded at the beginning, add to it when a new song is found and downloaded, then write it out when bot disconnects
