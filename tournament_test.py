#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def testDelete():
    """Test if deletion from tables works"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    print "1. All matches, registrations, tournaments and " \
        "players can be deleted."


def testCount():
    """Test if count returns numeric type 0 for empty tables"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    cM = countMatches()
    cR = countRegistrations()
    cT = countTournaments()
    cP = countPlayers()
    if cM == '0' or cR == '0' or cT == '0' or cP == '0':
        raise TypeError(
            "Counts should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, counts should return zero.")
    print "2. After deleting, all counts return zero."


def testCreatePlayer():
    """Test if player records can be created"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After creating one player record, countPlayers() should be 1.")
    print "3. After creating one player record, countPlayers() returns 1."


def testCreateTournament():
    """Test if tournaments can be created"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createTournament("Fencing")
    c = countTournaments()
    if c != 1:
        raise ValueError(
            "After creating one tournament, countTournaments() should be 1.")
    print "4. After creating one tournament, countTournaments() returns 1."


def testRegister():
    """Test if player players can be registered to different tournaments"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Chandra Nalaar")
    createPlayerRecord("Ned Flanders")
    createTournament("Fencing")
    createTournament("Ping Pong")
    registerPlayer(1, 1)
    registerPlayer(2, 1)
    registerPlayer(1, 2)
    cTotal = countRegistrations()
    cFence = countRegistrations(1)
    cPing = countRegistrations(2)
    if cTotal != 3 or cFence != 2 or cPing != 1:
        raise ValueError(
            "Incorrect registrations after multiple players " \
            "register for multiple tournaments.")
    print "5. After multiple players register for multiple tournaments, " \
          "count of registrations is correct."


def testRegisterCountDeleteCount():
    """Test table counts after registration and then deletion"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Markov Chaney")
    createPlayerRecord("Joe Malik")
    createPlayerRecord("Mao Tsu-hsi")
    createPlayerRecord("Atlanta Hope")
    createTournament("Fencing")
    createTournament("Ping Pong")
    registerPlayer(1, 1)
    registerPlayer(2, 1)
    registerPlayer(3, 1)
    registerPlayer(4, 1)
    registerPlayer(1, 2)
    registerPlayer(2, 2)
    registerPlayer(3, 2)
    registerPlayer(4, 2)
    cPlayers = countPlayers()
    cRegistrations = countRegistrations()
    cFencing = countRegistrstions(1)
    cPing = countRegistrations(2)
    cTourn = countTournaments()
    if (cPlayers != 4 or cRegistrations != 8 or 
        cFencing != 4 or cPing != 4 or cTourn != 2):
        raise ValueError(
            "After registering four players for two tournaments, " \
            "counts are wrong.")
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    cPlayers = countPlayers()
    cRegistrations = countRegistrations()
    cTourn = countTournaments()
    if cPlayers != 0 or cRegistrations != 0 or cTourn != 0:
        raise ValueError("After deleting, counts should return zero.")
    print "6. Players can be registered and deleted."


def testStandingsBeforeMatches():
    """Test whether standings show players with no matches"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Melpomene Murray")
    createPlayerRecord("Randy Schwartz")
    createTournament("Fencing")
    createTournament("Ping Pong")
    registerPlayer(1, 1)
    registerPlayer(2, 1)
    standings = playerStandings(1)
    if len(standings) < 2:
        raise ValueError("Players should appear in standings for a " \
                         "tournament even if they have not played any " \
                         "matches in that tournament.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 6:
        raise ValueError("Each playerStandings row should have seven columns.")
    [(tournament, id1, name1, wins1, matches1, strength1, points1),
     (tournament, id2, name2, wins2, matches2, strength2, points2)] = standings
    if ( matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0 or
         strength1 != 0 or strength2 != 0 or points1 != 0 or points2 != 0 ):
        raise ValueError(
            "Newly registered players should have no matches, " \
            "wins, strength of schedule, or points.")
    if tournament != 1:
        raise ValueError("Standings do not list correct tournament.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in " \
                         "standings even if they have no matches played.")
    print "7. Newly registered players appear in the standings with no matches."


def testReportMatches():
    """Test if recording matches causes correct changes to standings"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Bruno Walton")
    createPlayerRecord("Boots O'Neal")
    createPlayerRecord("Cathy Burton")
    createPlayerRecord("Diane Grant")
    createTournament("Fencing")
    createTournament("Ping Pong")
    registerPlayer(1, 1)
    registerPlayer(2, 1)
    registerPlayer(3, 1)
    registerPlayer(4, 1)
    registerPlayer(1, 2)
    registerPlayer(2, 2)
    registerPlayer(3, 2)
    registerPlayer(4, 2)
    standingsOne = playerStandings(1)
    standingsTwo = playerStandings(2)
    [id1, id2, id3, id4] = [row[1] for row in standingsOne]
    [id5, id6, id7, id8] = [row[1] for row in standingsTwo]
    reportMatch(id1, 3, id2, 2, False)
    reportMatch(id3, 5, id4, 1, False)
    reportMatch(id5, 2, id6, 1, False)
    reportMatch(id7, 4, id8, 0, False)
    standingsOne = playerStandings(1)
    standingsTwo = playerStandings(2)
    for (t, i, n, w, m, s, p) in standingsOne:
        if t != 1:
            raise ValueError("TournmentID is not correct in standings.")
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each winner should have one win recorded.")
        if i in (id2, id4) and w != 0:
            raise ValueError("Each loser should have zero wins recorded.")
        if ( (i == id1 and p != 3) or
             (i == id2 and p != 2) or
             (i == id3 and p != 5) or
             (i == id4 and p != 1) ):
            raise ValueError("A player in the first tournament " \
                             "has the wrong number of total points.")
        if i in (id1, id3) and s != 0:
            raise ValueError("Winners' strength of schedule should be 0")
        if i in (id2, id4) and s != 1:
            raise ValueError("Losers' strength of schedule should be 1")   
    for (t, i, n, w, m, s, p) in standingsTwo:
        if t != 2:
            raise ValueError("TournmentID is not correct in standings.")
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id5, id7) and w != 1:
            raise ValueError("Each winner should have one win recorded.")
        if i in (id6, id8) and w != 0:
            raise ValueError("Each loser should have zero wins recorded.")
        if ( (i == id1 and p != 2) or
             (i == id2 and p != 1) or
             (i == id3 and p != 4) or
             (i == id4 and p != 0) ):
            raise ValueError("A player in the second tournament " \
                             "has the wrong number of total points.")
        if i in (id1, id3) and s != 0:
            raise ValueError("Winners' strength of schedule should be 0")
        if i in (id2, id4) and s != 1:
            raise ValueError("Losers' strength of schedule should be 1")   
    print "8. After a round of matches in two tournaments, " \
          "players standings are correct."


def testPairings():
    """Test if pairing algorithm works for multiple tournaments"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Twilight Sparkle")
    createPlayerRecord("Fluttershy")
    createPlayerRecord("Applejack")
    createPlayerRecord("Pinkie Pie")
    createTournament("Fencing")
    createTournament("Ping Pong")
    registerPlayer(1, 1)
    registerPlayer(2, 1)
    registerPlayer(3, 1)
    registerPlayer(4, 1)
    registerPlayer(1, 2)
    registerPlayer(2, 2)
    registerPlayer(3, 2)
    registerPlayer(4, 2)
    standingsOne = playerStandings(1)
    standingsTwo = playerStandings(2)
    [Rid1, Rid2, Rid3, Rid4] = [row[1] for row in standingsOne]
    [Rid5, Rid6, Rid7, Rid8] = [row[1] for row in standingsTwo]
    reportMatch(id1, 2, id2, 0, False)
    reportMatch(id3, 3, id4, 2, False)
    reportMatch(id6, 1, id5, 0, False)
    reportMatch(id8, 2, id7, 1, False)
    pairingsOne = swissPairings(1)
    pairingsTwo = swissPairings(2)
    if len(pairingsOne) != 2 or len(pairingsTwo) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(Pid1, Pname1, Pid2, Pname2), (Pid3, Pname3, Pid4, Pname4)] = pairingsOne
    [(Pid5, Pname5, Pid6, Pname6), (Pid7, Pname7, Pid8, Pname8)] = pairingsTwo
    correctPairsOne = set([frozenset([Rid1, Rid3]), frozenset([Rid2, Rid4])])
    actualPairsOne = set([frozenset([Pid1, Pid2]), frozenset([Pid3, Pid4])])
    correctPairsTwo = set([frozenset([Rid6, Rid8]), frozenset([id5, id7])])
    actualPairsTwo = set([frozenset([Pid5, Pid6]), frozenset([Pid7, Pid8])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "9. After one round in two tournaments, pairs are correct."

def testOddNumberPlayers():
    """Test if pairing algorithm handles multiple odd # player tournaments"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Twilight Sparkle")
    createPlayerRecord("Fluttershy")
    createPlayerRecord("Applejack")
    createTournament("Fencing")
    createTournament("Ping Pong")
    registerPlayer(1, 1)
    registerPlayer(2, 1)
    registerPlayer(3, 1)
    registerPlayer(1, 2)
    registerPlayer(2, 2)
    registerPlayer(3, 2)
    pairingsOne = swissPairings(1)
    pairingsTwo = swissPairings(2)
    [(Pid1, Pid2), (Pid3, Pid4)] = [(row[0],row[2]) for row in pairingsOne]
    [(Pid5, Pid6), (Pid7, Pid8)] = [(row[0],row[2]) for row in pairingsTwo]
    if ( pairingsOne[0][2] != None or
         pairingsOne[0][1] != 'Twilight Sparkle' or
         pairingsTwo[0][2] != None or
         pairingsTwo[0][1] != 'Twilight Sparkle' ):
        raise ValueError(
            "The first registered player in a tournament should get a bye " \
            "in the first round if there is an odd number of players in " \
            "that tournament")
    print "10. With an odd number of players, the first registered player " \
          "in a tournament gets a bye in the first round."
    reportMatch(Pid1, 0, Pid2, 0, False)
    reportMatch(Pid3, 1, Pid4, 0, False)
    reportMatch(Pid5, 0, Pid6, 0, False)
    reportMatch(Pid7, 1, Pid8, 0, False)
    pairingsOne = swissPairings(1)
    pairingsOne = swissPairings(2)
    [(Pid1, Pid2), (Pid3, Pid4)] = [(row[0],row[2]) for row in pairingsOne]
    [(Pid5, Pid6), (Pid7, Pid8)] = [(row[0],row[2]) for row in pairingsTwo]
    if ( pairingsOne[0][2] != None or
         pairingsOne[0][1] != 'Fluttershy' or
         pairingsTwo[0][2] != None or
         pairingsTwo[0][1] != 'Fluttershy' ):
        raise ValueError(
            "An incorrect player got a bye in the second round")
    print "11. The correct player got a bye in the second round " \
          "of each tournament."
    reportMatch(Pid1, 0, id2, 0, False)
    reportMatch(Pid3, 3, id4, 0, False)
    reportMatch(Pid5, 0, id6, 0, False)
    reportMatch(Pid7, 3, id8, 0, False)
    pairingsOne = swissPairings(1)
    pairingsOne = swissPairings(2)
    [(Pid1, Pid2), (Pid3, Pid4)] = [(row[0],row[2]) for row in pairingsOne]
    [(Pid5, Pid6), (Pid7, Pid8)] = [(row[0],row[2]) for row in pairingsTwo]
    if ( pairingsOne[0][2] != None or
         pairingsOne[0][1] != 'Applejack' or
         pairingsTwo[0][2] != None or
         pairingsTwo[0][1] != 'Applejack' ):
        raise ValueError(
            "A player got more than one bye")
    print "12. No players got more than one bye in either tournament."


def testTies():
    """Test if pairings and standings for multiple tournies work with ties"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Bruno Walton")
    createPlayerRecord("Boots O'Neal")
    createPlayerRecord("Cathy Burton")
    createPlayerRecord("Diane Grant")
    createTournament("Fencing")
    createTournament("Ping Pong")
    registerPlayer(1, 1)
    registerPlayer(2, 1)
    registerPlayer(3, 1)
    registerPlayer(4, 1)
    registerPlayer(1, 2)
    registerPlayer(2, 2)
    registerPlayer(3, 2)
    registerPlayer(4, 2)
    standingsOne = playerStandings(1)
    standingsOne = playerStandings(2)
    [id1, id2, id3, id4] = [row[1] for row in standingsOne]
    [id5, id6, id7, id8] = [row[1] for row in standingsTwo]
    reportMatch(id1, 3, id2, 2, False)
    reportMatch(id3, 4, id4, 4, True)
    reportMatch(id5, 2, id6, 1, False)
    reportMatch(id7, 3, id8, 3, True)
    standings = playerStandings()
    for (t, i, n, w, m, s, p) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i == id1 and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        if i in (id2, id3, id4) and w != 0:
            raise ValueError("Players that did not win should have zero wins.")
        if ( (i == id1 and p != 3 and t != 1) or
             (i == id2 and p != 2 and t != 1) or
             (i == id3 and p != 4 and t != 1) or
             (i == id4 and p != 4 and t != 1) or
             (i == id5 and p != 2 and t != 2) or
             (i == id6 and p != 1 and t != 2) or
             (i == id7 and p != 3 and t != 2) or
             (i == id8 and p != 3 and t != 2) ):
            raise ValueError("A player has the wrong number of total points.")
        if i in (id1, id3, id4, id5, id7, id8) and s != 0:
            raise ValueError("Non-losers' strength of schedule should be 0")
        if i in (id2, id6) and s != 1:
            raise ValueError("Loser's strength of schedule should be 1")   
    print "13. After a round with ties, players have correct standings."


def testTieBreaks():
    """Test if tie breakers work properly"""
    deleteMatches()
    deleteRegistrations()
    deleteTournaments()
    deletePlayers()
    createPlayerRecord("Twilight Sparkle")
    createPlayerRecord("Fluttershy")
    createPlayerRecord("Applejack")
    createPlayerRecord("Thor")
    createTournament("Fencing")
    createTournament("Ping Pong")
    registerPlayer(1, 1)
    registerPlayer(2, 1)
    registerPlayer(3, 1)
    registerPlayer(4, 1)
    registerPlayer(1, 2)
    registerPlayer(2, 2)
    registerPlayer(3, 2)
    registerPlayer(4, 2)
    pairingsOne = swissPairings(1)
    pairingsTwo = swissPairings(2)
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairingsOne]
    [(id5, id6), (id7, id8)] = [(row[0],row[2]) for row in pairingsTwo]
    reportMatch(id1, 4, id2, 2, False)
    reportMatch(id3, 5, id4, 1, False)
    reportMatch(id5, 5, id2, 3, False)
    reportMatch(id7, 6, id4, 2, False)
    # After one round of tournament 1:
    # 1. Applejack  1 wins, 0 SOS,  5 pts, ID 3
    # 2. Twilight   1 wins, 0 SOS,  4 pts, ID 1
    # 3. Fluttershy 0 wins, 1 SOS,  2 pts, ID 2
    # 4. Thor       0 wins, 1 SOS,  1 pts, ID 4
    # After one round of tournament 2:
    # 1. Applejack  1 wins, 0 SOS,  6 pts, ID 7
    # 2. Twilight   1 wins, 0 SOS,  5 pts, ID 5
    # 3. Fluttershy 0 wins, 1 SOS,  3 pts, ID 6
    # 4. Thor       0 wins, 1 SOS,  2 pts, ID 8
    standings = playerStandings()
    position = [row[1] for row in standings]
    if ( position[0] != 'Applejack' or
         position[1] != 'Twilight Sparkle' or
         position[2] != 'Fluttershy' or
         position[3] != 'Thor' or
         position[4] != 'Applejack' or
         position[5] != 'Twilight Sparkle' or
         position[6] != 'Fluttershy' or
         position[7] != 'Thor' ):
        raise ValueError("Points did not break tie correctly")
    pairingsOne = swissPairings(1)
    pairingsTwo = swissPairings(2)
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairingsOne]
    [(id5, id6), (id7, id8)] = [(row[0],row[2]) for row in pairingsTwo]
    reportMatch(id1, 3, id2, 3, True)
    reportMatch(id3, 2, id4, 1, False)
    reportMatch(id1, 4, id2, 4, True)
    reportMatch(id3, 3, id4, 2, False)
    # After two rounds of tournament 1:
    # 1. Twilight   1 wins,  2 SOS,  7 pts, ID 1
    # 2. Applejack  1 wins,  1 SOS,  8 pts, ID 3
    # 3. Fluttershy 1 wins,  1 SOS,  4 pts, ID 2
    # 4. Thor       0 wins,  2 SOS,  2 pts, ID 4
    # After two rounds of tournament 2:
    # 1. Twilight   1 wins,  2 SOS,  9 pts,  ID 5
    # 2. Applejack  1 wins,  1 SOS,  10 pts, ID 7
    # 3. Fluttershy 1 wins,  1 SOS,  6 pts,  ID 6
    # 4. Thor       0 wins,  2 SOS,  4 pts,  ID 8
    standings = playerStandings()
    position = [row[1] for row in standings]
    if ( position[0] != 'Twilight Sparkle' or
         position[1] != 'Applejack' or
         position[2] != 'Fluttershy' or
         position[3] != 'Thor' or
         position[4] != 'Twilight Sparkle' or
         position[5] != 'Applejack' or
         position[6] != 'Fluttershy' or
         position[7] != 'Thor' ):
        raise ValueError("Strength of schedule did not break tie correctly")
    pairingsOne = swissPairings(1)
    pairingsTwo = swissPairings(2)
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairingsOne]
    [(id5, id6), (id7, id8)] = [(row[0],row[2]) for row in pairingsTwo]
    reportMatch(id2, 7, id1, 0, False)
    reportMatch(id4, 2, id3, 1, False)
    reportMatch(id6, 8, id5, 1, False)
    reportMatch(id8, 3, id7, 2, False)
    # After three rounds of tournament 1:
    # 1. Fluttershy 2 win,  3 SOS,  6 pts, ID 2
    # 2. Applejack  1 win,  4 SOS,  9 pts, ID 3
    # 3. Thor       1 win,  4 SOS,  9 pts, ID 4
    # 4. Twilight   1 win,  4 SOS,  7 pts, ID 1
    # After three rounds of tournament 2:
    # 1. Fluttershy 2 win,  3 SOS,  9 pts,  ID 6
    # 2. Applejack  1 win,  4 SOS,  12 pts, ID 7
    # 3. Thor       1 win,  4 SOS,  12 pts, ID 8
    # 4. Twilight   1 win,  4 SOS,  10 pts, ID 5
    standings = playerStandings()
    position = [row[1] for row in standings]
    if ( position[0] != 'Fluttershy' or
         position[1] != 'Applejack' or
         position[2] != 'Thor' or
         position[3] != 'Twilight Sparkle' or
         position[4] != 'Fluttershy' or
         position[5] != 'Applejack' or
         position[6] != 'Thor' or
         position[7] != 'Twilight Sparkle' ):
        raise ValueError("PlayerID did not break tie correctly")
    print "14. After three rounds including at least one tie, and " \
          "a three-way tie for second based on wins, "  \
          "all tie-breakers work properly."


if __name__ == '__main__':
    testDelete()
    testCount()
    testCreatePlayer()
    testCreateTournament()
    testRegister()
    testRegisterCountDeleteCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testOddNumberPlayers()
    testTies()
    testTieBreaks()
    print "Success!  All tests pass!"


