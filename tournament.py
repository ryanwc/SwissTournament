#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteAllMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Match;")
    connection.commit()
    connection.close()


def deleteMatches(tournament):
    """Remove all matches from a specific tournament from the database.

    Args:
      tournament: the tournament to remove all matches from
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Match WHERE TournamentID = %s;",
                   (tournament,))
    connection.commit()
    connection.close()


def deleteAllTournaments():
    """Remove all tournaments from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Tournament;")
    connection.commit()
    connection.close()


def deleteAllPlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Player;")
    connection.commit()
    connection.close()


def deleteAllRegistrations():
    """Remove all player registrations from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Registration;")
    connection.commit()
    connection.close()


def deleteRegistrations(tournament):
    """Remove all registrations for a specific tournament from the database.
    
    Args:
      tournament: the tournament id to remove all registrations from
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Registration WHERE TournamentID = %s;",
                   (tournament,))
    connection.commit()
    connection.close()


def countAllPlayers():
    """Returns the number of recorded players."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Player;")
    numPlayers = cursor.fetchone()[0]
    connection.close()
    return numPlayers


def countAllRegistrations():
    """Returns the number of registrations for all tournaments."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Regsitration;")
    numRegistrations = cursor.fetchone()[0]
    connection.close()
    return numRegistrations


def countRegistrations(tournament):
    """Returns the number of registrations for a specific tournament.

    Args:
      tournament: the tournament id to get # of registrations for
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Regsitration WHERE TournamentID = %s;"
                   , (tournament))
    numTournamentRegistrations = cursor.fetchone()[0]
    connection.close()
    return numTournamentRegistrations


def countAllMatches():
    """Returns the number of matches for all tournaments."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Match;")
    numMatches = cursor.fetchone()[0]
    connection.close()
    return numMatches


def countMatches(tournament):
    """Returns the number of matches for a specific tournament.

    Args:
      tournament: the tournament id to get # of matches for
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Match WHERE TournamentID = %s;",
                   (tournament,))
    numTournamentMatches = cursor.fetchone()[0]
    connection.close()
    return numTournamentMatches


def countAllTournaments():
    """Returns the number of tournaments."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Tournament;")
    numTournamens = cursor.fetchone()[0]
    connection.close()
    return numTournaments


def createPlayerRecord(name):
    """Creates a record of a player.
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Player (PlayerName) values (%s);", (name,))
    connection.commit()
    connection.close()


def createTournament(gameType):
    """Creates a tournament of a specific type of game.
  
    Args:
      gameType: the name of the game played in the tournament.
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Tournament (GameType) values (%s);",
                   (gameType,))
    connection.commit()
    connection.close()


def registerPlayer(player, tournament):
    """Registers a player for a specific tournament.
  
    The database assigns a unique serial id number for the registration.
    A player that is registered for more than one tournament will have
    more than one related registration id.
  
    Args:
      player: the player's id
      tournament: the id of the tournament the player will register for
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Registration (PlayerID, TournamentID) "
                   "values (%s,%s);", (player, tournament))
    connection.commit()
    connection.close()


def allStandings():
    """Returns a list of the player rankings for ALL tournaments.

    Players are sorted by wins, strength of schedule, points scored,
    and time of registration.

    The first entry in the list should be the player in first place in the
    first tournament, or a player tied for first place 
    if there is currently a tie.

    Returns:
      A list of tuples, each of which contains
      (tournament id, registration id, name, wins, matches,
      strength of schedule, and points):
        tournament id: the unique id of a single tournament
        registrationd id: a player's unique id for a tournament
        name: the player's full name (as registered)
        wins: the number of matches a player has won in the tournament
        matches: the number of matches a player has played in the tournament
        strength of schedule: the number of total wins a player's opponents
            have in the tournament
        points: the number of points a player has scored in the tournament
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Standings;")
    standings = [(int(row[0]), int(row[1]), str(row[2]),
                  int(row[3]), int(row[4]),
                  int(row[5]), int(row[6])) for row in cursor.fetchall()]
    connection.close()
    return standings


def tournamentStandings(tournament):
    """Returns a list of the players rankings for a single tournament.

    Players are sorted by wins, strength of schedule, points scored,
    and time of registration.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains
      (registration id, name, wins, matches, strength of schedule, and points):
        registrationd id: a player's unique id for the tournament
        name: the player's full name (as registered)
        wins: the number of matches a player has won in the tournament
        matches: the number of matches a player has played in the tournament
        strength of schedule: the number of total wins a player's opponents
            have in the tournament
        points: the number of points a player has scored in the tournament
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Standings WHERE TournamentID = %s;",
                   (tournament,))
    standings = [(int(row[1]), str(row[2]), int(row[3]), int(row[4]),
                  int(row[5]), int(row[6])) for row in cursor.fetchall()]
    connection.close()
    return standings


def reportMatch(tournament, winner, winnerPoints, loser, loserPoints, isTie):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the id number of the tournament the match is played in
      winner:  the id number of winning player registration
      winnerPoints:  the number of points the winner scored in the match
      loser:  the id number of the losing player registration
      loserPoints:  the number of points the loser scored in the match
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Match "
                   "(TournamentID, Winner, WinnerPoints, Loser, "
                   "LoserPoints, IsATie) values (%s,%s,%s,%s,%s);",
                   (winner, winnerPoints, loser, loserPoints, isTie))
    connection.commit()
    connection.close()


def testBye(winner):
    """ Tests if a player has already had a bye in a specific tournament.

    Helper method for swissPairings(tournament).

    Args:
        winner: the id of the player registration to test
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Match WHERE Winner = %s "
                   "AND Loser is null;", (winner,))
    alreadyHadBye = cursor.fetchone()[0]==1
    connection.close()
    return alreadyHadBye


def testIfPlayed(registrationOne, registrationTwo):
    """Tests if two players have already played a match in a tournament.

    Helper method for swissPairings(tournament).

    Args:
        registrationOne: the id of the first registration for the test
        registrationTwo: the id of the second registration for the test
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM Match "
                   "WHERE Winner = %s AND Loser = %s;", 
                   (registrationOne,registrationTwo))
    alreadyPlayed = cursor.fetchone()[0]==1
    if not alreadyPlayed:
        cursor = connection.cursor()
        cursor.execute("SELECT count(*) FROM Match "
                       "WHERE Winner = %s AND Loser = %s;", 
                       (registrationTwo,registrationOne))
        alreadyPlayed = cursor.fetchone()[0]==1
    connection.close()
    return alreadyPlayed

 
def swissPairings(tournament):
    """Returns a list of pairs of registrations for the next round of a tourny.
  
    Each registration (player in a tourny) is paired exactly one time.
    Players are paired as follows:
    1) If odd number of players, assign the bye to the highest ranked player
    that has not had a bye (only one bye per player per tournament).
    2) Search for pairs who are as closely ranked as possible subject to:
        A) one of the players is the highest ranked un-paired player;
        B) neither player is already paired for this round; and 
        C) the players have not yet played in this tournament.

    Args:
        tournament: the id of the tournament to make pairings for

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique registration id for this tourny
        name1: the first player's name
        id2: the second player's unique registration id
        for this tourny (null if name1 has a bye)
        name2: the second player's name (null if name1 has a bye)
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT RegistrationID, PlayerName FROM Standings "
                   "WHERE TournamentID = %s;", (tournament,))
    # pre-set each player's "already paired" status to False
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
