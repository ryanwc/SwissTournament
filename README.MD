# Overview

SwissTournament is the backend (database and Python wrapper code) for a Swiss-style tournament system.

## SwissTournament Database Details

This database supports multiple swiss-style tournaments with even or odd numbers of players and matches that end in ties.  The database also features a Standings table with multiple tie breakers.

**Rankings**

In each tournament, players are ranked as follows:

1) A player with more wins is ranked higher than a player with less wins
2) If players have equal wins, a player who has a higher strength of schedule (calculated as a player's oppoents' total wins) is ranked higher
3) If players have equal wins and strength of schedule, a player with more total points scored in all of his or her matches is ranked higher
4) If players have equal wins, strength of schedule, and points scored, a player who registered earlier (as judged by a lower RegistrationID) is ranked higher.

**Ties**

Ties do not count as a win for either player involved in the match.

**Byes*

Byes count as a "win" for the receiving player, but the player scores no points.   player can have only one bye per tournament. 

**Pairings**

Pairings for each round of each tournament are calculated by a Python implementation of a Swiss-pairing algorithm.  Each registration (i.e., each player in a tournament) is paired exactly one time for each round.  Players are paired as follows:

1) If there is an odd number of players, the highest ranked player that has not had a bye is paired with no one (i.e., gets a bye).
2) Pair players that are as close in rank as possible are subject to:
	A) one of the players in the new pair is the highest ranked un-paired player;
	B) neither player is already paired for this round; and 
	C) the players have not yet played in this tournament (i.e., no re-matches).

# Technical Requirements for this Code

The database schema was written in PostgreSQL, and the wrapper language used to access the database is Python.  So, to use this code as-is, users should ensure they have the following installed on their machine:

1. Python
2. PostgreSQL (another database may work, but you would probably have to modify the SQL code and modify how Python connects to the database)

# Getting, Understanding, and Using the Code

You can download the source code for SwissTournament at [this GitHub repo from ToolsForInsight](https://github.com/ToolsForInsight/SwissTournament).  You should unzip all the files in this repo to the same directory on your computer.

**Explanation of Important Files**

1. tournament.sql:
	- Defines the schema for a PostgresSQL database that can holds information about multiple Swiss-style tournaments.
2. tournament.py:
	- Provides convenient methods to manage player registrations, match reporting, rankings, and pairings for the next round of a tournament.
3. tournament_test.py:
	- Provides a suite of tests to ensure tournament.py and tournament.sql correclty manage registration, reporting, rankings, and pairings for multiple Swiss-style tournaments.
4. testScript.sql:
	- A scratch pad for testing SQL statements.

**Managing a Swiss-style Tournament with this Code**

To use this code to manage a Swiss-style tourament, you should:

1. Download and unzip all of the files in this repo into the same directory.
2. From the command line, navigate to the directory into which you unzipped all the files from this repo.
3. Start the psql command-line client, which talks to the PostgreSQL database, by typing "psql" and pressing enter.
4. Create the database by typing "\i tournament.sql" into the psql interpreter and pressing enter.

Now the database has been created, and you can write your own code (probably in Python) by importing all the functions in tournament.py to create and register players, create tournaments, report matches, view standings, and pair players for the next round of a tournament.

If you want to see a working example of the code working without writing your own tournament, you can do the following (assuming you are still in the psql interpreter and within the directory to which you unzipped all the files):

1. type "\q" and press enter to exit the psql interpreter.
2. Type "python tournament_test.py"

# License

This software is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl.html).  Accordingly, you are free to run, study, share, and modify this software only if you give these same freedoms to users of *your* implementation of this software.
