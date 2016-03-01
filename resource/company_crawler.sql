create table company_crawler(
  id int PRIMARY KEY     NOT NULL,
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