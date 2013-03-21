drop table if exists dreams;
create table dreams (
  id integer primary key autoincrement,
  title string not null,
  count integer not null
);
