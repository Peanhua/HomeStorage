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

### Per item best before dates
Currently all the items share the same lifetime, which is used to calculate the best before date. But when items are bought from a shop, they usually have varying lifetimes based on their creation date. There should be possibility to adjust the best before date when adding items to the storage.

### The force_password_change field in Account table should be True by default
The *force_password_change* in Account table, which forces the user to change password before the user can do anything else, should be True by default. This would force the default root account user to also change the password upon first login. This was not done because it makes testing a lot harder.

### Home specific products
It might be a good idea to have each home their own products. This could still allow the use of common repository of products, from which the home owners would then utilize the ones they want. There should probably also be some way to clone a product, so that variants could be easily made.

### Units and package sizes
Item quantities are without any unit type information. A single item is considered as a one "normal" package of the product in question, for example in Finland milk is often sold in 1 liter packages, sugar in 1 kilogram, etc. However, there are multiple package sizes present, even in Finland, and the package size does matter. This is especially true with reports that try to determine the "amount" of some product. So it would be a good addition to have units and package sizes supported by the software. This issue can somewhat be circumvented by the users via soft rules made by themselves, for example "sugar is always in kilograms", "chocolade powder is always in grams".

### Products of same type
Sometimes there are products that are of same type, where the type doesn't really matter, but the packaging/brand/something else varies between products. Users are now forced to use one type of product for all of those in order to get meaningful reports. For example there could be two bread brands that taste a bit different, but are easily interchangeable by the users, so the users might sometimes opt to take the other brand bread whose best before date is later than the other one, but in the reports they want to just see a generic "bread".

### Smart phone application
A smart phone application would ease the users life a great deal. Users could scan a receipt for adding items to storage, use bar codes on the items to add/remove items to/from storages. And the beforementioned alarms would fit smart phone application well.

These features could also be implemented without a special smart phone application, because all these are basically just picture scanning problems.

### From where to buy -information
Information system from where to buy specific items, for the best prices, could be implemented. First manual input, and then use some form of online gathering system to do it automatically.

### Homes working together
Multiple homes could share their shopping together to share the time and money spent on obtaining new items, and possibly get discounts when buying larger batches.

### Addresses for homes and storages
The homes and storages should have addresses set on them. This would allow showing them on map, and could be utilized in other features as well.

### Single-page application
The front-end should be switched to [single-page application](https://en.wikipedia.org/wiki/Single-page_application) -style for more pleasant user experience.

### Filtering and sorting
All the lists should have filtering, so that users can easily see only relevant information.

### Improve the user interface for the lists without paging
In the add/remove items and editing products desired quantities for homes views all the products are listed without paging or filtering. Filtering would be a first step to improve the user interface. Paging would be another option, but that would make the user interface more difficult to use, and slower. The number of products per installation is most likely not going to be very high because this stock management is aimed for homes, and not for big commercial stores.

### Easier/faster way to add/remove items
Currently the option to add/remove items is to go to the Storages view, and then click either add or remove items. This is a bit "hidden" and might not be so intuitive/easy to find for new users. There maybe could be separate navigation toolbar options for these common tasks, and/or buttons in the dashboard.

### Default home
If a user is part of multiple homes, the user would benefit from having a default home selected automatically because the user is most likely working on one home at a time. The changing of the default home should be easily accessible, for example from the navigation toolbar.

### Per home views
If a user is part of multiple homes, it might be nice for the eye, and help avoid making changes to the wrong home, if the current home was somehow selected (see also *Default home* above), and it changed something visually in the user interface (for example coloring, background image, home specific logo somewhere).
