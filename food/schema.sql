DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE if exists seller;
DROP TABLE if exists trade;

CREATE TABLE user (
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  user_phone INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
  is_seller INTEGER NOT NULL
);

CREATE TABLE product (
  product_create TIMESTAMP PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
  seller_phone INTEGER NOT NULL ,
  producetime TIMESTAMP NOT NULL,
  qualitytime TIMESTAMP NOT NULL,
  type TEXT NOT NULL,
  productname TEXT NOT NULL,
  price float NOT NULL ,
  product_intro TEXT,
  FOREIGN KEY (seller_phone) REFERENCES seller (seller_phone)
);

CREATE TABLE seller (
  storename TEXT NOT NULL ,
  location TEXT NOT NULL ,
  seller_phone INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT ,
  seller_intro TEXT ,
  LL TEXT NOT NULL ,
  begintime TIMESTAMP NOT NULL ,
  endtime TIMESTAMP NOT NULL
);

CREATE TABLE trade (
    product_create TIMESTAMP NOT NULL ,
    user_phone INTEGER NOT NULL ,
    seller_phone INTEGER NOT NULL ,
    trade_time TIMESTAMP PRIMARY KEY,
    cancel INTEGER,
    trade_number INTEGER NOT NULL ,
    FOREIGN KEY (product_create) REFERENCES product (product_create),
    FOREIGN KEY (user_phone) REFERENCES user (user_phone),
    FOREIGN KEY (seller_phone) REFERENCES seller (seller_phone)
);