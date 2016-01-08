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
	PlayerDOB date,
	PlayerEmail varchar(30),
	MatchesPlayed integer,
	Wins integer,
	Loses integer,
	StrengthOfSchedule integer,
	TotalPoints integer
);

CREATE TABLE Matches (
	MatchID serial PRIMARY KEY,
	Winner integer NOT NULL REFERENCES Player (PlayerID),
	WinnerPoints integer NOT NULL,
	Loser integer NOT NULL REFERENCES Player (PlayerID),
	LoserPoints integer NOT NULL,
	MatchNotes text
);
