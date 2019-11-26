drop table if exists posts;
create table posts (
  id integer primary key autoincrement,
  name not null,
  location text not null
);