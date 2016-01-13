-- test script

-- insert potential players
insert into Player (PlayerName) values ('Ryan');
insert into Player (PlayerName) values ('Kevin');
insert into Player (PlayerName) values ('Alex');
insert into Player (PlayerName) values ('Mattijs');

-- create the tournaments
insert into Tournament (GameType) values ('Badmitton');
insert into Tournament (GameType) values ('Fencing');	

-- register players for tournaments
insert into Registration (PlayerID, TournamentID) values (1, 1);
insert into Registration (PlayerID, TournamentID) values (2, 1);
insert into Registration (PlayerID, TournamentID) values (3, 1);
insert into Registration (PlayerID, TournamentID) values (4, 1);
insert into Registration (PlayerID, TournamentID) values (1, 2);
insert into Registration (PlayerID, TournamentID) values (2, 2);
insert into Registration (PlayerID, TournamentID) values (3, 2);
insert into Registration (PlayerID, TournamentID) values (4, 2);

-- report badmitton matches
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (1, 2, 2, 0, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (3, 1, 4, 0, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (1, 3, 3, 2, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (2, 1, 4, 0, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (1, 3, 4, 1, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (2, 4, 3, 3, False);

-- report fencing matches
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (5, 12, 6, 3, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (7, 9, 8, 4, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (5, 11, 7, 10, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (6, 8, 8, 2, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (5, 14, 8, 12, False);
insert into Match (Winner, WinnerPoints, Loser, LoserPoints, IsATie)
	values (6, 11, 7, 7, False);