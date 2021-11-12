# TCGPlayerTxt-to-YDK
Converts a TCGPlayer Decklist text file into a .ydk file... If that's something you need.

Requires the requests module (https://pypi.org/project/requests/)

Known Issues:

- Some community projects (Dueling Book) can't manage cards with multiple ID's, so some cards are not added to the deck in said projects (Dueling Book). This is not a bug in the script, but I am working on ways to remedy this without depending on others (Dueling Book) fixing their bugs. Ex: API call for Harpie's Feather Duster comes back with ID "18144507", but the card also has the ID "18144506". Other projects can manage the multiple IDs just fine.
- To be found...

Fixed Issues:

1. Main deck is not imported into Dueling Book, only Extra and Side deck.

Future Plans:

- Adapt for other decklist txt file styles if the need be.
- Add a batch convert option (Convert multiple files at a time).
- Make a GUI version of the script (if there is a demand for it).

Future Plans Made Reality:

- Make an optimized query to the api (only receive cards in deck instead of all yugioh cards).
