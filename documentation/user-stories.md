# User Stories

## As an administrator, I can create and delete user accounts.

### Creating a new user account
```SQL
BEGIN;

INSERT INTO account (name,        login,    password,           email,    superuser, force_password_change)
             VALUES (':USERNAME', ':LOGIN', ':HASHED_PASSWORD', ':EMAIL', 0,         1                    )
;

COMMIT;
```

### Deleting a user account
```SQL
BEGIN;

DELETE
  FROM account
 WHERE account.user_id = :USER_ID
;

COMMIT;
```

## As an administrator, I can reset users password.

This is currently possible by changing the users password and setting a "force password change" boolean, which forces the user to change the password next time the user logs in.
```SQL
BEGIN;

UPDATE account
   SET password = ':NEW_PASSWORD_HASHED',
       force_password_change = 1
 WHERE account.user_id = :USER_ID
;

COMMIT;
```


## As an administrator, I can create new homes and assign users to them.


### Creating a new home
```SQL
BEGIN;

INSERT INTO home (name)
          VALUES (':HOMENAME')
;

COMMIT;
```

### Assigning two users to a home
```SQL
BEGIN;

INSERT INTO home_user (home_id,  user_id)
               VALUES (:HOME_ID, :USER1_ID)
;

INSERT INTO home_user (home_id,  user_id)
               VALUES (:HOME_ID, :USER2_ID)
;

COMMIT;
```



## As a user, I can create, delete, and edit storages belonging to my home.

### Creating a new storage
```SQL
BEGIN;

INSERT INTO storage (home_id,  name)
             VALUES (:HOME_ID, ':NAME')
;

COMMIT;
```

### Editing a storage
```SQL
BEGIN;

UPDATE storage
   SET name = :NEW_NAME
 WHERE storage.storage_id = :STORAGE_ID
;

COMMIT;
```

### Deleting a storage
```SQL
BEGIN;

DELETE
  FROM storage
 WHERE storage.storage_id = :STORAGE_ID
;

COMMIT;
```


## As a user, I can add items to my home storages. The items are based on products anyone has added.
Adding 3 items of two different products to a storage:
```SQL
BEGIN;

INSERT INTO item (product_id,   storage_id,  quantity, best_before)
          VALUES (:PRODUCT1_ID, :STORAGE_ID, 2,        '2019-04-24')
;

INSERT INTO item (product_id,   storage_id,  quantity, best_before)
          VALUES (:PRODUCT2_ID, :STORAGE_ID, 1,        '2019-04-24')
;

COMMIT;
```


## As a user, I can remove items from my home storages.
Removing 1 item out of 3, and 1 item out of 1:
```SQL
BEGIN;

UPDATE item
   SET quantity = 2
 WHERE item.item_id = :ITEM1_ID
;

COMMIT;

BEGIN;

DELETE
  FROM item
 WHERE item.item_id = :ITEM2_ID
;

COMMIT;
```


## As a user, I can add new products.
```SQL
BEGIN;

INSERT INTO product (name,   default_lifetime)
             VALUES (':NAME', :LIFETIME)

COMMIT;
```


## As a user, I can edit products. This can be done anytime regardless whether the products are in use or not, a friendly environment between all the homes and users is expected.
```SQL
BEGIN;

UPDATE product
   SET name='NAME',
       default_lifetime = :LIFETIME
 WHERE product.product_id = :PRODUCT_ID
;

COMMIT;
```


## As a user, I can delete products if they are not in use.
```SQL
BEGIN;

DELETE
  FROM product
 WHERE product.product_id = :PRODUCT_ID
;

COMMIT;
```

## As a user, I can get a listing of items whose lifetime has ended or are about to end.
SQLite variant:
```SQL
SELECT product.name                                    AS name,
       item.quantity                                   AS quantity,
       storage.name                                    AS storage,
       item.best_before                                AS best_before,
       JULIANDAY(item.best_before) - JULIANDAY(DATE()) AS days_remaining
  FROM item
  JOIN product ON product.product_id = item.product_id
  JOIN storage ON storage.storage_id = item.storage_id
 WHERE storage.home_id = :HOME_ID
   AND days_remaining < :DAYS
 ORDER BY days_remaining
```
PostgreSQL variant:
```SQL
SELECT *
  FROM ( SELECT product.name      AS name,
                item.quantity     AS quantity,
                storage.name      AS storage,
                item.best_before  AS best_before,
                CAST(TO_CHAR(item.best_before, 'J') AS INT) - CAST(TO_CHAR(now(), 'J') AS INT) AS days_remaining
           FROM item
           JOIN product ON product.product_id = item.product_id
           JOIN storage ON storage.storage_id = item.storage_id
          WHERE storage.home_id = :home_id
       ) tmp
 WHERE days_remaining < :days
 ORDER BY days_remaining
```


## As a user, I can get a listing of products missing for my home.
```SQL
SELECT home_product.product_id           AS product_id,
       t.product_name                    AS product_name,
       home_product.desired_min_quantity AS desired_min_quantity,
       home_product.desired_max_quantity AS desired_max_quantity,
       t.current_quantity                AS current_quantity
  FROM ( SELECT product.product_id AS product_id,
                product.name       AS product_name,
                SUM(item.quantity) AS current_quantity
           FROM product
           LEFT OUTER JOIN home_product ON product.product_id = home_product.product_id
                                           AND ( home_product.home_id = :home_id OR home_product.home_id IS NULL)
           LEFT OUTER JOIN item ON product.product_id = item.product_id
                                   AND item.storage_id IN ( SELECT storage.storage_id
                                                              FROM storage
                                                             WHERE storage.home_id = :home_id )
          GROUP BY product.product_id
        ) t
  LEFT JOIN home_product ON home_product.product_id = t.product_id
                        AND home_product.home_id = :home_id
 WHERE current_quantity < desired_min_quantity
    OR (current_quantity IS NULL AND desired_min_quantity IS NOT NULL)
```


## As a user, I can adjust my personal user account profile and settings.
```SQL
BEGIN;

UPDATE account
   SET name = ':NAME',
       password = ':PASSWORD_HASHED',
       email = ':EMAIL'
 WHERE account.user_id = :USER_ID
;

COMMIT;
```
