-- test script

insert into Player (PlayerName) values ('Ryan');
insert into Player (PlayerName) values ('Kevin');
insert into Player (PlayerName) values ('Alex');
insert into Player (PlayerName) values ('Mattjias');

insert into Matches (Winner, WinnerPoints, Loser, LoserPoints)
	values (1, 2, 2, 0);
insert into Matches (Winner, WinnerPoints, Loser, LoserPoints)
	values (3, 1, 4, 0);
insert into Matches (Winner, WinnerPoints, Loser, LoserPoints)
	values (1, 3, 3, 2);
insert into Matches (Winner, WinnerPoints, Loser, LoserPoints)
	values (2, 1, 4, 0);
insert into Matches (Winner, WinnerPoints, Loser, LoserPoints)
	values (1, 3, 4, 1);
insert into Matches (Winner, WinnerPoints, Loser, LoserPoints)
	values (2, 4, 3, 3);