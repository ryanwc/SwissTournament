#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 6:
        raise ValueError("Each playerStandings row should have six columns.")
    [(id1, name1, wins1, matches1, strength1, points1),
     (id2, name2, wins2, matches2, strength2, points2)] = standings
    if ( matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0 or
         strength1 !=0 or strength2 !=0 or points1 != 0 or points2 !=0 ):
        raise ValueError(
            "Newly registered players should have no matches, " \
            "wins, strength of schedule, or points.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, 3, id2, 2, False)
    reportMatch(id3, 5, id4, 1, False)
    standings = playerStandings()
    for (i, n, w, m, s, p) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        if i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
        if ( (i == id1 and p != 3) or
             (i == id2 and p != 2) or
             (i == id3 and p != 5) or
             (i == id4 and p != 1) ):
            raise ValueError("A player has the wrong number of total points.")
        if i in (id1, id3) and s != 0:
            raise ValueError("Winners' strength of schedule should be 0")
        if i in (id2, id4) and s != 1:
            raise ValueError("Losers' strength of schedule should be 1")   
    print "7. After a match, players have correct standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, 2, id2, 0, False)
    reportMatch(id3, 3, id4, 2, False)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."

def testOddNumberPlayers():
    """Test if the pairing algorithm correctly handles odd number of players
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    pairings = swissPairings()
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairings]
    if pairings[0][2] != None or pairings[0][1] != 'Twilight Sparkle':
        raise ValueError(
            "The first registered player should get a bye in the first round "
            "if there is an odd number of players")
    print "9. With an odd number of players, the first registered player gets " \
          "a bye in the first round"
    reportMatch(id1, 0, id2, 0, False)
    reportMatch(id3, 1, id4, 0, False)
    pairings = swissPairings()
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairings]
    if pairings[0][2] != None or pairings[0][1] != 'Fluttershy':
        raise ValueError(
            "An incorrect player got a bye in the second round")
    print "10. The correct player got a bye in the second round"
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairings]
    reportMatch(id1, 0, id2, 0, False)
    reportMatch(id3, 3, id4, 0, False)
    pairings = swissPairings()
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairings]
    if pairings[0][2] != None or pairings[0][1] != 'Applejack':
        raise ValueError(
            "A player got more than one bye")
    print "11. No players got more than one bye"


def testTies():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, 3, id2, 2, False)
    reportMatch(id3, 4, id4, 4, True)
    standings = playerStandings()
    for (i, n, w, m, s, p) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i == id1 and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        if i in (id2, id3, id4) and w != 0:
            raise ValueError("Players that did not win should have zero wins.")
        if ( (i == id1 and p != 3) or
             (i == id2 and p != 2) or
             (i == id3 and p != 4) or
             (i == id4 and p != 4) ):
            raise ValueError("A player has the wrong number of total points.")
        if i in (id1, id3, id4) and s != 0:
            raise ValueError("Non-losers' strength of schedule should be 0")
        if i == id2 and s != 1:
            raise ValueError("Loser's strength of schedule should be 1")   
    print "12. After a round with ties, players have correct standings."


def testTieBreaks():
    """Test if players' opponents' total wins are correct
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Thor")
    pairings = swissPairings()
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairings]
    reportMatch(id1, 4, id2, 2, False)
    reportMatch(id3, 5, id4, 1, False)
    # After one round:
    # 1. Applejack  1 wins, 0 SOS,  5 pts, ID 3
    # 2. Twilight   1 wins, 0 SOS,  4 pts, ID 1
    # 3. Fluttershy 0 wins, 1 SOS,  2 pts, ID 2
    # 4. Thor       0 wins, 1 SOS,  1 pts, ID 4
    standings = playerStandings()
    position = [row[1] for row in standings]
    if ( position[0] != 'Applejack' or
         position[1] != 'Twilight Sparkle' or
         position[2] != 'Fluttershy' or
         position[3] != 'Thor' ):
        raise ValueError("Points did not break tie correctly")
    pairings = swissPairings()
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairings]
    reportMatch(id1, 3, id2, 3, True)
    reportMatch(id3, 2, id4, 1, False)
    # After two rounds:
    # 1. Twilight   1 wins,  2 SOS,  7 pts, ID 1
    # 2. Applejack  1 wins,  1 SOS,  8 pts, ID 3
    # 3. Fluttershy 1 wins,  1 SOS,  4 pts, ID 2
    # 4. Thor       0 wins,  2 SOS,  2 pts, ID 4
    standings = playerStandings()
    position = [row[1] for row in standings]
    if ( position[0] != 'Twilight Sparkle' or
         position[1] != 'Applejack' or
         position[2] != 'Fluttershy' or
         position[3] != 'Thor' ):
        raise ValueError("Strength of schedule did not break tie correctly")
    pairings = swissPairings()
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairings]
    reportMatch(id2, 7, id1, 0, False)
    reportMatch(id4, 2, id3, 1, False)
    # After three rounds:
    # 1. Fluttershy 2 win,  3 SOS,  6 pts, ID 2
    # 2. Applejack  1 win,  4 SOS,  9 pts, ID 3
    # 3. Thor       1 win,  4 SOS,  9 pts, ID 4
    # 4. Twilight   1 win,  4 SOS,  7 pts, ID 1
    standings = playerStandings()
    position = [row[1] for row in standings]
    if ( position[0] != 'Fluttershy' or
         position[1] != 'Applejack' or
         position[2] != 'Thor' or
         position[3] != 'Twilight Sparkle' ):
        raise ValueError("PlayerID did not break tie correctly")
    print "13. After three rounds including at least one tie, and " \
          "a three-way tie for second based on wins, "  \
          "all tie-breakers work properly."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testOddNumberPlayers()
    testTies()
    testTieBreaks()
    print "Success!  All tests pass!"


