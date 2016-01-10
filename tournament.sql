-- The database schema for a Swiss-style tournament.

-- to reset the database during testing
DROP DATABASE IF EXISTS tournament;
-- create and connect to the database using psql command line commands
CREATE DATABASE tournament;
\c tournament;


DROP TABLE IF EXISTS Player CASCADE;
DROP TABLE IF EXISTS Matches CASCADE;
DROP VIEW IF EXISTS PlayerPoints CASCADE;
DROP VIEW IF EXISTS PlayerOpponents CASCADE;
DROP VIEW IF EXISTS PlayerStandings CASCADE;

-- create the tables necessary to support a Swiss-style tournament

-- table holds player info
CREATE TABLE Player (
	PlayerID serial PRIMARY KEY,
	PlayerName varchar(50) NOT NULL,
	PlayerDOB date,
	PlayerEmail varchar(30)
);

-- table holds match info
CREATE TABLE Matches (
	MatchID serial PRIMARY KEY,
	Winner integer NOT NULL REFERENCES Player (PlayerID),
	WinnerPoints integer NOT NULL,
	Loser integer REFERENCES Player (PlayerID),
	LoserPoints integer NOT NULL,
	IsATie boolean NOT NULL,
	MatchNotes text,
	CHECK (WinnerPoints >= 0 AND LoserPoints >=0),
	CHECK (NOT(Loser = NULL AND LoserPoints > 0)),
	CHECK (NOT(Loser = NULL AND WinnerPoints > 0)),
	CHECK (NOT(IsATie = true AND WinnerPoints != LoserPoints)),
	CHECK (NOT(IsATie = false AND Loser != NULL
	           AND WinnerPoints <= LoserPoints))
);

CREATE UNIQUE INDEX no_rematches ON Matches
	(greatest(Winner, Loser), least(Winner, Loser));

-- view to show how many points each player scored
CREATE OR REPLACE VIEW PlayerPoints as
	SELECT Player.PlayerID, Matches.WinnerPoints as PointsScored 
		FROM Player JOIN Matches ON Player.PlayerID = Matches.Winner
	UNION all
	SELECT Player.PlayerID, Matches.LoserPoints as PointsScored
		FROM Player JOIN Matches ON Player.PlayerID = Matches.Loser
;

-- view to show all players paired with each of their opponents
CREATE OR REPLACE VIEW PlayerOpponents as
	SELECT Player.PlayerID, Matches.Loser as Opponent
		FROM Player
		JOIN Matches ON Player.PlayerID = Matches.Winner
	UNION
	SELECT Player.PlayerID, Matches.Winner as Opponent
		FROM Player
		JOIN Matches ON Player.PlayerID = Matches.Loser
;

-- view to calculate each player's opponents' total wins
-- (which will be the tiebreaker strength of schedule)
CREATE OR REPLACE VIEW PlayerOpponentWins as
	SELECT PlayerID,
		sum((SELECT count(*)
			FROM Matches
			WHERE Winner = PlayerOpponents.Opponent 
				AND IsATie = false))
			as OpponentWins
		FROM PlayerOpponents
		GROUP BY PlayerID
;

-- view to calculate tournament standings
-- the player in the top row is the leader, the player in the bottom row is in last place
-- ties in total wins are broken by strength of schedule first, total points scored second,
-- then arbitrarily broken by order of registration (earlier registration wins)
CREATE OR REPLACE VIEW Standings as 
	SELECT Player.PlayerID,
		Player.PlayerName,
		(SELECT count(*)
			FROM Matches
			WHERE Winner = Player.PlayerID AND IsATie = FALSE)
			as Wins,
		(SELECT count(*)
			FROM Matches
			WHERE Winner = Player.PlayerID OR Loser = Player.PlayerID)
			as MatchesPlayed,
		PlayerOpponentWins.OpponentWins as StrengthOfSchedule,
		(SELECT sum(PointsScored)
			FROM PlayerPoints
			WHERE PlayerID = Player.PlayerID)
			as TotalPoints
		FROM Player
		LEFT JOIN PlayerOpponentWins 
			ON Player.PlayerID = PlayerOpponentWins.PlayerID
		ORDER BY Wins DESC, StrengthOfSchedule DESC, TotalPoints DESC, PlayerID
;