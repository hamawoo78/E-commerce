# PROJECT TITLE : Platform for Unique Item Creator
#### Video Demo:  <URL> https://youtu.be/cAsBxHKiW9k
#### Description:


Hello, this is Nae. My web application is built using Python Flask, JavaScript, SQL, and HTML.
The application is similar to platforms like eBay, Etsy, or Facebook Marketplace, where users can browse and discover unique items.
I created this application to solidify my knowledge and gain hands-on experience in building a web application that can be used as a foundation for future projects.

As a creator of crochet items and drawings, I have always wanted to have my own website.
So, I chose this application to understand how existing web applications like eBay or Etsy are built.

During the development process, I faced several challenges, especially in creating and managing the routing for different functionalities.
However, by tackling each issue and finding solutions, I was able to learn a lot and enhance my skills.

Now, let me provide a more detailed breakdown of how my web application works:

Data Storage: The application uses a Flask app and stores data in an SQL database.
There are three tables in the database: "users," "items," and "itemTypes."
The users table stores information about registered users, including their unique IDs, usernames, and hashed passwords. The items table contains details about the items listed on the platform, such as the item name, picture URL, type, cost, description, URL, and the associated user ID.
The itemTypes table is used to categorize items by storing the different item types or categories available.

By using the itemTypes table, you allow for flexibility in managing and organizing item categories, even though my current website may have a limited number of categories. This structure enables scalability in the future, accommodating a larger number of categories as the website expands.

Main Page: The main page of the application displays all the available items.
Users can sort the items by cost to find items within their preferred price range.
By clicking on an item's picture, users can view the details of that specific item.
If they wish to make a purchase, clicking on a button will redirect them to the seller's own website.

Seller's Page: Sellers can create their own accounts, allowing them to manage their listed items.
Initially, when a new account is created, there are no items listed under that account.
Also, there are some requirement, which is you miss adding passward, website tell you " 〇〇 is required"

Adding Items: Sellers can add their items by clicking on the "Add Item" button. They need to provide information such as the item name, image URL, item type, cost, description, and external URL (e.g., where you can buy this items). If any required information is missing, the seller will be notified to complete it before adding the item. Once all the information is provided, the item will be added to the website.

Editing Items: Sellers have the option to edit the information of their listed items.
By clicking on the "Edit" button, they can modify the details such as the item name, image URL, type, cost, description, and external URL.
After making the necessary changes, the item information will be updated accordingly.

Removing Items: Sellers can also choose to delete their items from the website.
By clicking on the "Remove" button, the respective item will be permanently removed from the website by clicking "yes".

I hope this description provides a clearer understanding of my web application.
Thank you, and I would greatly appreciate any feedback you have to offer.