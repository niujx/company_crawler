create table company_crawler(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_id varchar(64),
  company_name VARCHAR(64),
  product_name TEXT,
  trade VARCHAR(64),
  location VARCHAR(64),
  stage TEXT,
  management_team TEXT,
  introduction TEXT,
  company_url VARCHAR(64),
  ext_info TEXT,
  crawler_url VARCHAR(64),
  create_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  crawler_spider varchar(64)
);


create table crawler_task(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crawler_spider VARCHAR(64),
    create_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    state varchar(1)
)

create table kr36_citys(
   id INTEGER PRIMARY KEY ,
   parentId INTEGER,
   dispOrder INTEGER,
   name varchar(64),
   feature INTEGER
)