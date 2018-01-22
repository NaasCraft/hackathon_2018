// Installing and creating the scoringdb database
// 1- install sqlite: apt-get install sqlite
// 2- create the db using sqlite3: sqlite3 scoringdb.db < ./scoring.sql 
// 3- check everything okay: sqlite3 scoringdb.db 'select * from PiEvents'
// 					                 sqlite3 scoringdb.db 'select * from Games'
 

CREATE TABLE IF NOT EXISTS PiEvents (
 event_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
 sensor_id integer NOT NULL,
 event_timestamp TEXT NOT NULL
 );


INSERT INTO PiEvents (sensor_id, event_timestamp) Values (1,'2018-01-22 15:00:15.000');
INSERT INTO PiEvents (sensor_id, event_timestamp) Values (1,'2018-01-22 15:00:15.200');
INSERT INTO PiEvents (sensor_id, event_timestamp) Values (1,'2018-01-22 15:00:30.000');
INSERT INTO PiEvents (sensor_id, event_timestamp) Values (2,'2018-01-22 15:00:30.000');
INSERT INTO PiEvents (sensor_id, event_timestamp) Values (1,'2018-01-22 15:00:40.000');
INSERT INTO PiEvents (sensor_id, event_timestamp) Values (2,'2018-01-22 15:00:45.000');

CREATE TABLE IF NOT EXISTS Games (
 game_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
 user1 text DEFAULT 'User1',
 user2 text DEFAULT 'User2',
 game_name TEXT,
 starttime_timestamp TEXT,
 stoptime_timestamp TEXT,
 paused int DEFAULT 1
 );

INSERT INTO Games (user1, user2, game_name, starttime_timestamp, stoptime_timestamp, paused) Values ('David', 'Goliath', 'David against Goliath', '2018-01-22 15:00:00.000',  '2018-01-22 16:00:00.000', 1);
INSERT INTO Games (user1, user2, game_name, starttime_timestamp, stoptime_timestamp, paused) Values ('David', 'Alexandre', 'Alexandre against David', '2018-01-22 17:00:00.000',  NULL, 0);
INSERT INTO Games (user1, user2, game_name, starttime_timestamp, stoptime_timestamp, paused	) Values ('Pierre', 'John', 'Pierre against John', '2018-01-21 15:00:00.000',  '2018-01-21 16:00:00.000', 1);


