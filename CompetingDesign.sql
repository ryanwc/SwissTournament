-- The database schema for a Swiss-style tournament.

-- to reset the database during testing
DROP DATABASE IF EXISTS tournament
-- create and connect to the database using psql command line commands
CREATE DATABASE tournament;
\c tournament;

-- create the tables necessary to support a Swiss-style tournament

-- table holds player info
CREATE TABLE Player (
	PlayerID serial PRIMARY KEY,
	PlayerName vachar(50) NOT NULL,
	PlayerDOB date NOT NULL,
	PlayerEmail varchar(30)
);

-- table holds match info
CREATE TABLE Matches (
	MatchID serial PRIMARY KEY,
	Winner integer NOT NULL REFERENCES Player (PlayerID),
	WinnerPoints integer NOT NULL CHECK (WinnerPoints >= 0),
	Loser integer NOT NULL REFERENCES Player (PlayerID),
	LoserPoints integer NOT NULL CHECK (LoserPoints >= 0),
	MatchNotes text
);

-- view to calculate how many points each player scored in their wins
CREATE OR REPLACE VIEW PlayerWinPoints as
	SELECT Player.PlayerID as Winner, Matches.WinnerPoints, Matches.LoserID as Opponent 
	FROM Player LEFT JOIN Matches ON Player.PlayerID = Matches.Winner
	GROUP BY Winner
;

-- view to calculate how many points each player scored in their loses
CREATE OR REPLACE VIEW PlayerLossPoints as
	SELECT Player.PlayerID as Loser, Matches.LoserPoints, Matches.WinnerID as Opponent
	FROM Player LEFT JOIN Matches ON Player.PlayerID = Matches.Loser
	GROUP BY Loser
;

-- view to get players paired with opponents and the opponent's total wins (no duplicates)
CREATE OR REPLACE VIEW PlayerOpponents as
	SELECT Players.ID,
		PlayerWinPoints.Opponent FROM PlayerWinPoints,
		(SELECT count(*) FROM Matches WHERE Winner in PlayerWinPoints.Loser) as OpponentWins
		FROM PlayerWinPoints
	UNION
	SELECT PlayerLossPoints.Opponent as PlayerID,
		PlayerLossPoints.Winner as Opponent FROM PlayerLossPoints,
		(SELECT count(*) FROM Matches WHERE Winner in PlayerLossPoints.Loser) as OpponentWins
		FROM PlayerLossPoints;
;

-- view to calculate tournament standings
-- the player in the top row is the leader, the player in the bottom row is in last place
-- ties in total wins are broken by strength of schedule first and total points scored second
CREATE OR REPLACE VIEW Standings as 
	SELECT Player.PlayerName,
		(SELECT count(*) FROM Matches WHERE (Winner = Player.PlayerID) OR (Loser = Player.PlayerID)) as MatchesPlayed,
		(SELECT count(*) FROM Matches WHERE Winner = Player.PlayerID) as Wins,
		(SELECT count(*) FROM Matches WHERE Loser = Player.PlayerID) as Loses,
		PlayerOpponents.OpponentWins,
		(SELECT sum(points) FROM
			(SELECT PlayerWinPoints.WinnerPoints, PlayerLossPoints.LoserPoints
				FROM 
				WHERE (Winner = Player.PlayerID) OR (Loser = Player.PlayerID)) as TotalPoints
	FROM Player
		LEFT JOIN Matches on Player.PlayerID = Matches.
		LEFT JOIN PlayerOpponentWins on Player.PlayerID = PlayerOpponents.PlayerID
		LEFT JOIN PlayerWinPoints
		LEFT JOIN PlayerLossPoints
;