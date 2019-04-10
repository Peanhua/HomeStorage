# User Stories

## As an administrator, I can create and delete user accounts.

### Creating a new user account
```
BEGIN;

INSERT INTO account (name,        login,    password,           email,    superuser, force_password_change)
             VALUES (':USERNAME', ':LOGIN', ':HASHED_PASSWORD', ':EMAIL', 0,         1                    )
;

COMMIT;
```

### Deleting a user account
```
BEGIN;

DELETE
  FROM account
 WHERE account.user_id = :USER_ID
;

COMMIT;
```

## As an administrator, I can reset users password.

This is currently possible by changing the users password and setting a "force password change" boolean, which forces the user to change the password next time the user logs in.
```
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
```
BEGIN;

INSERT INTO home (name)
          VALUES (':HOMENAME')
;

COMMIT;
```

### Assigning two users to a home
```
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
```
BEGIN;

INSERT INTO storage (home_id,  name)
             VALUES (:HOME_ID, ':NAME')
;

COMMIT;
```

### Deleting a storage
```
BEGIN;

DELETE
  FROM storage
 WHERE storage.storage_id = :STORAGE_ID
;

COMMIT;
```


## As a user, I can add items to my home storages. The items are based on products anyone has added.
Adding 3 items of two different products to a storage:
```
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
```
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
```
BEGIN;

INSERT INTO product (name,   default_lifetime)
             VALUES (':NAME', :LIFETIME)

COMMIT;
```


## As a user, I can edit products. This can be done anytime regardless whether the products are in use or not, a friendly environment between all the homes and users is expected.
```
BEGIN;

UPDATE product
   SET name='NAME',
       default_lifetime = :LIFETIME
 WHERE product.product_id = :PRODUCT_ID
;

COMMIT;
```


## As a user, I can delete products if they are not in use.
```
BEGIN;

DELETE
  FROM product
 WHERE product.product_id = :PRODUCT_ID
;

COMMIT;
```

## As a user, I can get a listing of items whose lifetime has ended or are about to end.
```
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


## As a user, I can get a listing of products missing for my home.
```
SELECT product.product_id                AS product_id,
       product.name                      AS product_name,
       home_product.desired_min_quantity AS desired_min_quantity,
       home_product.desired_max_quantity AS desired_max_quantity,
       SUM(item.quantity)                AS current_quantity
  FROM product
  LEFT OUTER JOIN home_product ON product.product_id = home_product.product_id
                                  AND ( home_product.home_id = :HOME_ID OR home_product.home_id IS NULL)
  LEFT OUTER JOIN item ON product.product_id = item.product_id
                          AND item.storage_id IN ( SELECT storage.storage_id
                                                     FROM storage
                                                    WHERE storage.home_id = :HOME_ID )
 GROUP BY product.product_id
 HAVING current_quantity < desired_min_quantity
     OR (current_quantity IS NULL AND desired_min_quantity IS NOT NULL)
```


## As a user, I can get reports about product usage. The statistics contain quantities of products used over certain period of time, for example how many liters of milk are consumed per month.
Not yet implemented.


## As a user, I can get alarms about my home and storages. The alarms are based on the existing reports, and they are triggered by some limits on values such as "the amount of cakes is below 10kg".
Not yet implemented.


## As a user, I can adjust my personal user account profile and settings.
```
BEGIN;

UPDATE account
   SET name = ':NAME',
       password = ':PASSWORD_HASHED',
       email = ':EMAIL'
 WHERE account.user_id = :USER_ID
;

COMMIT;
```


## As a user, I can request my password to be reset if I have forgotten it. An email is sent to my email account with a new temporary password, which I need to change next time I log in.
Not yet implemented.
