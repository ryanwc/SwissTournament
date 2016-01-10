#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Matches;")
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Player;")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Player;")
    numPlayers = cursor.fetchone()[0]
    connection.close()
    return numPlayers


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by the SQL database schema, not in the Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Player (PlayerName) values (%s);", (name,))
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Standings;")
    standings = [(int(row[0]), str(row[1]), int(row[2]), int(row[3]),
                 int(row[4]), int(row[5])) for row in cursor.fetchall()]
    connection.close()
    return standings


def reportMatch(winner, winnerPoints, loser, loserPoints, isTie):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Matches "
                   "(Winner, WinnerPoints, Loser, LoserPoints, IsATie) "
                   "values (%s,%s,%s,%s,%s);",
                   (winner, winnerPoints, loser, loserPoints, isTie))
    connection.commit()
    connection.close()


def testBye(winner):
    """ Tests if a player has already had a bye in this tournament.

    Args:
        winner: the id nuber of the player to test
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Matches "
                   "WHERE Winner = %s AND Loser is null;", 
                   (winner,))
    alreadyHadBye = cursor.fetchone()[0]==1
    connection.close()
    return alreadyHadBye


def testIfPlayed(playerOne, playerTwo):
    """Tests if two players have already played a match
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Matches "
                   "WHERE Winner = %s AND Loser = %s;", 
                   (playerOne,playerTwo))
    alreadyPlayed = cursor.fetchone()[0]==1
    if not alreadyPlayed:
        cursor = connection.cursor()
        cursor.execute("SELECT count(*) FROM Matches "
                       "WHERE Winner = %s AND Loser = %s;", 
                       (playerTwo,playerOne))
        alreadyPlayed = cursor.fetchone()[0]==1
    connection.close()
    return alreadyPlayed

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Each player appears exactly once in the pairings.
    Players are paired as follows:
    1) If odd number of players, assign the bye to the highest ranked player
    that has not had a bye (only one bye per player per tournament).
    2) Search for pairs who are as closely ranked as possible subject to:
        A) one of the players is the highest ranked un-paired player;
        B) neither player is already paired for this round; and 
        C) the players have not yet played in this tournament.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id (null if name1 has a bye)
        name2: the second player's name (null if name1 has a bye)
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT PlayerID, PlayerName FROM Standings;")
    orderedPlayers = [[int(row[0]), str(row[1]), False]
                      for row in cursor.fetchall()]
    connection.close()

    playerPairings = []
    # assign the bye, if needed, to highest ranked player
    if len(orderedPlayers) % 2 == 1:
        for j in range(0, len(orderedPlayers)):
            if not testBye(orderedPlayers[j][0]):
                playerPairings.append((orderedPlayers[j][0],
                                       orderedPlayers[j][1],
                                       None,
                                       None))
                orderedPlayers[j][2] = True
                break
    # pair the highest ranked player who has not yet been paired
    # with the next highest ranked player who has also not yet been paired
    # and which creates a pair that has not yet played.
    i = 0
    while i < len(orderedPlayers):
        if not orderedPlayers[i][2]:
            k = i+1
            while orderedPlayers[k][2]:
                k+=1
            while testIfPlayed(orderedPlayers[i][0], orderedPlayers[k][0]):
                k+=1
            playerPairings.append((orderedPlayers[i][0],
                                   orderedPlayers[i][1],
                                   orderedPlayers[k][0],
                                   orderedPlayers[k][1]))
            orderedPlayers[i][2] = True
            orderedPlayers[k][2] = True
        i+=1
    return playerPairings
