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
    standings = [(int(row[0]), str(row[1]), int(row[2]), int(row[3]))
                 for row in cursor.fetchall()]
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

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Each player appears exactly once in the pairings.
    Each player is paired with another player with an equal or nearly-equal
    win record, that is, a player adjacent to him or her in the standings.
    If there are an odd number of players, assign a bye to the first player
    that has not yet had a bye, starting at the top of the rankings.
    Only one bye is allowed per player per tournament.
  
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
    orderedPlayers = [(int(row[0]), str(row[1]))
                      for row in cursor.fetchall()]
    connection.close()

    playerPairings = []
    i = 0

    if len(orderedPlayers) % 2 == 1:

        byeReceiver = 0
        for j in range(0, len(orderedPlayers)):
            if not testBye(orderedPlayers[j][0]):
                playerPairings.append((orderedPlayers[j][0],
                                       orderedPlayers[j][1],
                                       None,
                                       None))
                byeReceiver = j
                break
        while i < len(orderedPlayers):
            if i == j-1:
                playerPairings.append((orderedPlayers[i][0],
                                       orderedPlayers[i][1],
                                       orderedPlayers[i+2][0],
                                       orderedPlayers[i+2][1]))
                i+=3
            elif i != j:
                playerPairings.append((orderedPlayers[i][0],
                                       orderedPlayers[i][1],
                                       orderedPlayers[i+1][0],
                                       orderedPlayers[i+1][1]))
                i+=2
            else:
                i+=1
    else:
        while i < len(orderedPlayers):
            playerPairings.append((orderedPlayers[i][0],
                                   orderedPlayers[i][1],
                                   orderedPlayers[i+1][0],
                                   orderedPlayers[i+1][1]))
            i+=2 

    return playerPairings
