# Further development

The following things are not yet done, and are good candidates of advancing the development of Home Storage.

## User stories

### As a user, I can get reports about product usage. The statistics contain quantities of products used over certain period of time, for example how many liters of milk are consumed per month.
To get this report done accurately, the users are required to remove the items from the storages the same day they are used, or there is a way to define the "use day".


### As a user, I can get alarms about my home and storages. The alarms are based on the existing reports, and they are triggered by some limits on values such as "the amount of cakes is below 10kg".
Alarms should probably be implemented with emails, or some push notification to phones.

### As a user, I can request my password to be reset if I have forgotten it. An email is sent to my email account with a new temporary password, which I need to change next time I log in.
This requires managing the configuration for an email server.

## Other improvements/ideas

### Smart phone application
A smart phone application would ease the users life a great deal. Users could scan a receipt for adding items to storage, use bar codes on the items to add/remove items to/from storages. And the beforementioned alarms would fit smart phone application well.

These features could also be implemented without a special smart phone application, because all these are basically just picture scanning problems.

### From where to buy information
Information system from where to buy specific items, for the best prices, could be implemented. First manual input, and then use some form of online gathering system to do it automatically.

### Homes working together
Multiple homes could share their shopping together to share the time and money spent on obtaining new items, and possibly get discounts when buying larger batches.

### Addresses for homes and storages
The homes and storages should have addresses set on them. This would allow showing them on map, and could be utilized in other features as well.

### Single-page application
The front-end should be switched to [single-page application](https://en.wikipedia.org/wiki/Single-page_application) -style for more pleasant user experience.

### Filtering
The lists made of products should have filtering, so that users can easily see only relevant information. Paging would be another option, but that would make the user interface more difficult to use, and slower. The number of products per installation is most likely not going to be very high because this stock management is aimed for homes, and not for big commercial stores.
