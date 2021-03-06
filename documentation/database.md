# Database

<div>Database diagram:</div>
<img src="database.svg" alt="Database diagram" width="700" />

The *superuser* field in *account* table is *True* when the user is a superuser and has the rights to manage users and homes.

When the *force_password_change* in *account* table is set to *True*, the user is required to change the password before the user can do anything else. After the user in question has changed the password, the *force_password_change* field is set to *False*. The field is set to *True* for all new users created via the softwares user interface.

All the item quantities used are integers, and are not tied to any special unit like "liter", "kilogram", etc.

The *default_lifetime* field in *product* table is in days.

When items are taken out from a storage, it is done using the *best_before* date so that the oldest items are used first. For details, see the file `application/storage/models.py`, methods adjust_stock() and decrease_item_count().

There is no denormalization of the database done. The most heavy queries are done around the *home_product*, *item*, and *product* tables. Especially, an often done query is with *item* and *product* tables, so for example the *product.name* field could be denormalized into the *item* table to possibly gain some performance increase.


## Indices

<table>
  <tr><th>Index name                </th><th>Index type</th><th>Table       </th><th>Fields    </th></tr>
  <tr><td>ix_account_login          </td><td>unique    </td><td>account     </td><td>login     </td></tr>
  <tr><td>ix_home_product_home_id   </td><td>index     </td><td>home_product</td><td>home_id   </td></tr>
  <tr><td>ix_home_product_product_id</td><td>index     </td><td>home_product</td><td>product_id</td></tr>
  <tr><td>ix_home_user_home_id      </td><td>index     </td><td>home_user   </td><td>home_id   </td></tr>
  <tr><td>ix_home_user_user_id      </td><td>index     </td><td>home_user   </td><td>user_id   </td></tr>
  <tr><td>ix_item_product_id        </td><td>index     </td><td>item        </td><td>product_id</td></tr>
  <tr><td>ix_item_storage_id        </td><td>index     </td><td>item        </td><td>storage_id</td></tr>
  <tr><td>ix_storage_home_id        </td><td>index     </td><td>storage     </td><td>home_id   </td></tr>
</table>

The *ix_account_login* unique index is used to make sure that no two accounts have the same login.


## Create table SQL

### SQLite variants

```SQL
CREATE TABLE product (
        product_id       INTEGER NOT NULL, 
        name             VARCHAR(80) NOT NULL, 
        default_lifetime INTEGER NOT NULL, 
        PRIMARY KEY (product_id)
);

CREATE TABLE home (
        home_id INTEGER NOT NULL, 
        name    VARCHAR(80) NOT NULL, 
        PRIMARY KEY (home_id)
);

CREATE TABLE account (
        user_id               INTEGER NOT NULL, 
        name                  VARCHAR(80) NOT NULL, 
        login                 VARCHAR(40) NOT NULL, 
        password              VARCHAR(128) NOT NULL, 
        email                 VARCHAR(80) NOT NULL, 
        superuser             BOOLEAN NOT NULL, 
        force_password_change BOOLEAN NOT NULL, 
        PRIMARY KEY (user_id), 
        CHECK (superuser IN (0, 1)), 
        CHECK (force_password_change IN (0, 1))
);

CREATE UNIQUE INDEX ix_account_login ON account (login);

CREATE TABLE home_user (
        homeuser_id INTEGER NOT NULL, 
        home_id     INTEGER NOT NULL, 
        user_id     INTEGER NOT NULL, 
        PRIMARY KEY (homeuser_id), 
        FOREIGN KEY(home_id) REFERENCES home (home_id)    ON DELETE CASCADE, 
        FOREIGN KEY(user_id) REFERENCES account (user_id) ON DELETE CASCADE
);

CREATE INDEX ix_home_user_user_id ON home_user (user_id);

CREATE INDEX ix_home_user_home_id ON home_user (home_id);

CREATE TABLE home_product (
        homeproduct_id       INTEGER NOT NULL, 
        home_id              INTEGER NOT NULL, 
        product_id           INTEGER NOT NULL, 
        desired_min_quantity INTEGER, 
        desired_max_quantity INTEGER, 
        PRIMARY KEY (homeproduct_id), 
        FOREIGN KEY(home_id)    REFERENCES home (home_id)       ON DELETE CASCADE, 
        FOREIGN KEY(product_id) REFERENCES product (product_id) ON DELETE CASCADE
);

CREATE INDEX ix_home_product_product_id ON home_product (product_id);

CREATE INDEX ix_home_product_home_id ON home_product (home_id);

CREATE TABLE storage (
        storage_id INTEGER NOT NULL, 
        home_id    INTEGER NOT NULL, 
        name       VARCHAR(80) NOT NULL, 
        PRIMARY KEY (storage_id), 
        FOREIGN KEY(home_id) REFERENCES home (home_id) ON DELETE CASCADE
);

CREATE INDEX ix_storage_home_id ON storage (home_id);

CREATE TABLE item (
        item_id     INTEGER NOT NULL, 
        product_id  INTEGER NOT NULL, 
        storage_id  INTEGER NOT NULL, 
        quantity    INTEGER NOT NULL, 
        best_before DATE NOT NULL, 
        PRIMARY KEY (item_id), 
        FOREIGN KEY(product_id) REFERENCES product (product_id), 
        FOREIGN KEY(storage_id) REFERENCES storage (storage_id) ON DELETE CASCADE
);

CREATE INDEX ix_item_storage_id ON item (storage_id);

CREATE INDEX ix_item_product_id ON item (product_id);
```

### PostgreSQL variants

```SQL
CREATE TABLE product (
       product_id       SERIAL NOT NULL,
       name             VARCHAR(80) NOT NULL,
       default_lifetime INTEGER NOT NULL,
       PRIMARY KEY (product_id)
);

CREATE TABLE home (
       home_id SERIAL NOT NULL,
       name    VARCHAR(80) NOT NULL,
       PRIMARY KEY (home_id)
);

CREATE TABLE account (
       user_id               SERIAL NOT NULL,
       name                  VARCHAR(80) NOT NULL,
       login                 VARCHAR(40) NOT NULL,
       password              VARCHAR(128) NOT NULL,
       email                 VARCHAR(80) NOT NULL,
       superuser             BOOLEAN NOT NULL,
       force_password_change BOOLEAN NOT NULL,
       PRIMARY KEY (user_id)
);

CREATE UNIQUE INDEX ix_account_login ON account (login);

CREATE TABLE home_user (
       homeuser_id SERIAL NOT NULL,
       home_id     INTEGER NOT NULL,
       user_id     INTEGER NOT NULL,
       PRIMARY KEY (homeuser_id),
       FOREIGN KEY(home_id) REFERENCES home (home_id) ON DELETE CASCADE,
       FOREIGN KEY(user_id) REFERENCES account (user_id) ON DELETE CASCADE
);

CREATE INDEX ix_home_user_home_id ON home_user (home_id);

CREATE INDEX ix_home_user_user_id ON home_user (user_id);

CREATE TABLE home_product (
       homeproduct_id       SERIAL NOT NULL,
       home_id              INTEGER NOT NULL,
       product_id           INTEGER NOT NULL,
       desired_min_quantity INTEGER,
       desired_max_quantity INTEGER,
       PRIMARY KEY (homeproduct_id),
       FOREIGN KEY(home_id) REFERENCES home (home_id) ON DELETE CASCADE,
       FOREIGN KEY(product_id) REFERENCES product (product_id) ON DELETE CASCADE
);

CREATE INDEX ix_home_product_product_id ON home_product (product_id);

CREATE INDEX ix_home_product_home_id ON home_product (home_id);

CREATE TABLE storage (
       storage_id SERIAL NOT NULL,
       home_id    INTEGER NOT NULL,
       name       VARCHAR(80) NOT NULL,
       PRIMARY KEY (storage_id),
       FOREIGN KEY(home_id) REFERENCES home (home_id) ON DELETE CASCADE
);

CREATE INDEX ix_storage_home_id ON storage (home_id);

CREATE TABLE item (
       item_id     SERIAL NOT NULL,
       product_id  INTEGER NOT NULL,
       storage_id  INTEGER NOT NULL,
       quantity    INTEGER NOT NULL,
       best_before DATE NOT NULL,
       PRIMARY KEY (item_id),
       FOREIGN KEY(product_id) REFERENCES product (product_id),
       FOREIGN KEY(storage_id) REFERENCES storage (storage_id) ON DELETE CASCADE
);

CREATE INDEX ix_item_storage_id ON item (storage_id);

CREATE INDEX ix_item_product_id ON item (product_id);
```


## Default data inserts
```SQL
INSERT INTO account (name, login, password, email, superuser, force_password_change)
             VALUES ('Superuser', 'root', '$2b$12$ZLRQf/zxUaah4PbweKKRH.qUxYtdvj0BmdrqHsQSgrSHpL6FfX9ZG', 'root@not.set.invalid', 1, 0);
```
