-- The database schema for a Swiss-style tournament.

-- to reset the database during testing
DROP DATABASE IF EXISTS tournament
-- create and connect to the database using psql command line commands
CREATE DATABASE tournament;
\c tournament;

-- create the tables necessary to support a Swiss-style tournament

CREATE TABLE Player (
	PlayerID serial PRIMARY KEY,
	PlayerName vachar(50) NOT NULL,
	PlayerDOB date NOT NULL,
	PlayerEmail varchar(30),
	MatchesPlayed integer NOT NULL CHECK (MatchesPlayed = (Wins+Loses)),
	Wins integer CHECK NOT NULL (Wins = (MatchesPlayed-Loses)),
	Loses integer CHECK NOT NULL (Loses = (MatchesPlayed-Wins)),
	StrengthOfSchedule integer NOT NULL CHECK (StrengthOfSchedule >= 0),
	TotalPoints integer NOT NULL CHECK (TotalPoints >= 0)
);

CREATE TABLE Matches (
	MatchID serial PRIMARY KEY,
	Winner integer NOT NULL REFERENCES Player (PlayerID),
	WinnerPoints integer NOT NULL CHECK (WinnerPoints >= 0),
	Loser integer NOT NULL REFERENCES Player (PlayerID),
	LoserPoints integer NOT NULL CHECK (LoserPoints >= 0),
	MatchNotes text
);

