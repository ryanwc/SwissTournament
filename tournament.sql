-- The database schema for multiple Swiss-style tournament.

-- to reset the database during testing
DROP DATABASE IF EXISTS tournament;
-- create and connect to the database using psql commands
CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS Player CASCADE;
DROP TABLE IF EXISTS Tournament CASCADE;
DROP TABLE IF EXISTS Registration CASCADE;
DROP TABLE IF EXISTS Match CASCADE;
DROP VIEW IF EXISTS PlayerPoints CASCADE;
DROP VIEW IF EXISTS PlayerOpponents CASCADE;
DROP VIEW IF EXISTS PlayerOpponentWins CASCADE;
DROP VIEW IF EXISTS Standings CASCADE;

-- create the tables necessary to support multiple Swiss-style tournaments

-- table holds player info
CREATE TABLE Player (
	PlayerID serial PRIMARY KEY,
	PlayerName varchar(50) NOT NULL,
	PlayerDOB date,
	PlayerEmail varchar(30)
);

-- table holds tournament info
CREATE TABLE Tournament (
	TournamentID serial PRIMARY KEY,
	GameType varchar(30) NOT NULL
);

-- table holds registration info for each tournament
CREATE TABLE Registration (
	RegistrationID serial PRIMARY KEY,
	PlayerID integer NOT NULL REFERENCES Player (PlayerID),
	TournamentID integer NOT NULL REFERENCES Tournament (TournamentID)
);

-- table holds match info
CREATE TABLE Match (
	MatchID serial PRIMARY KEY,
	Winner integer NOT NULL REFERENCES Registration (RegistrationID),
	WinnerPoints integer NOT NULL,
	Loser integer REFERENCES Registration (RegistrationID),
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

CREATE UNIQUE INDEX no_rematches ON Match
	(greatest(Winner, Loser), least(Winner, Loser));

-- view to show how many points each player scored
CREATE OR REPLACE VIEW PlayerPoints as
	SELECT Player.PlayerID,
		Registration.RegistrationID,
		(SELECT sum(Match.WinnerPoints) FROM Match WHERE Match.Winner = Registration.RegistrationID) as PointsScored 
		FROM Player
		JOIN Registration ON Player.PlayerID = Registration.PlayerID
		LEFT JOIN Match ON Player.PlayerID = Match.Winner
		GROUP BY Player.PlayerID, Registration.RegistrationID
	UNION all
	SELECT Player.PlayerID,
		Registration.RegistrationID,
		(SELECT sum(Match.LoserPoints) FROM Match WHERE Match.Loser = Registration.RegistrationID) as PointsScored 
		FROM Player
		JOIN Registration ON Player.PlayerID = Registration.PlayerID
		LEFT JOIN Match ON Player.PlayerID = Match.Loser
		GROUP BY Player.PlayerID, Registration.RegistrationID
;

-- view to show all players paired with each of their opponents
CREATE OR REPLACE VIEW PlayerOpponents as
	SELECT Player.PlayerID,
		Registration.RegistrationID,
		Match.Loser as Opponent
		FROM Player
		JOIN Registration ON Player.PlayerID = Registration.PlayerID
		JOIN Match ON Registration.RegistrationID = Match.Winner
	UNION
	SELECT Player.PlayerID,
		Registration.RegistrationID,
		Match.Winner as Opponent
		FROM Player
		JOIN Registration ON Player.PlayerID = Registration.PlayerID
		JOIN Match ON Registration.RegistrationID = Match.Loser
;

-- view to calculate each player's opponents' total wins
-- (which will be the tiebreaker strength of schedule)
CREATE OR REPLACE VIEW PlayerOpponentWins as
	SELECT PlayerID,
		RegistrationID,
		sum((SELECT count(*)
			FROM Match
			WHERE Winner = PlayerOpponents.Opponent 
				AND IsATie = false))
			as OpponentWins
		FROM PlayerOpponents
		GROUP BY PlayerID, RegistrationID
;

-- view to calculate tournament standings
-- the player in the top row is the leader, the player in the bottom row is in last place
-- ties in total wins are broken by strength of schedule first, total points scored second,
-- then arbitrarily broken by order of registration (earlier registration wins)
CREATE OR REPLACE VIEW Standings as 
	SELECT Registration.RegistrationID,
		Player.PlayerName,
		Tournament.TournamentID,
		(SELECT count(*)
			FROM Match
			WHERE Winner = Player.PlayerID AND IsATie = FALSE)
			as Wins,
		(SELECT count(*)
			FROM Match
			WHERE Winner = Player.PlayerID OR Loser = Player.PlayerID)
			as MatchPlayed,
		PlayerOpponentWins.OpponentWins as StrengthOfSchedule,
		(SELECT sum(PointsScored)
			FROM PlayerPoints
			WHERE RegistrationID = Registration.RegistrationID)
			as TotalPoints
		FROM Player
		LEFT JOIN Registration ON Player.PlayerID = Registration.PlayerID
		LEFT JOIN Tournament ON Registration.TournamentID = Tournament.TournamentID
		LEFT JOIN PlayerOpponentWins 
			ON Registration.RegistrationID = PlayerOpponentWins.RegistrationID
		ORDER BY TournamentID, Wins DESC, StrengthOfSchedule DESC, TotalPoints DESC, RegistrationID
;