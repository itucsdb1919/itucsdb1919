Parts Implemented by Ahmet Yemliha Öner
================================

Register, Login and settings pages are created by Ahmet Yemliha Öner. As you can imagine all of these pages are mainly related to users. Also login management system for users is implemented by Ahmet Yemliha Öner using Flask-login.

Signup
------
You have to give all of the requested information in the signup page. These informations will be hold in a database for further applications. Also your username and e-mail must be unique in our database.
Which means you can not register to RentChain using two same e-mail addresses or two same usernames. You can see the signup page of RentChain below.

.. figure:: images/register.png
     :scale: 100 %
     :alt: register page

     Register page for registering to RentChain

Login
------
To access most of the RentChain's pages, you have to be logged in succesfully. If you try to access a page that requires an authorizatiton without being logged in, system redirects you to the signin page.
This implemented for preventing unauthorized access to our lovely RentChain. You can see the signin page of Re below.

.. figure:: images/login.png
     :scale: 100 %
     :alt: login page

     Login page where you will be directed if you are not authorized

In that page if you signin with a valid user account, page will redirect you to the page you requested to see.

Settings
--------
This is the page that users can update their user informations, search other users with their username and delete their own user account from the RentChain.
Users do not have to fill all of the sections in the update option. If a user wants to update a spesific piece of information, it is enough to fill only the corresponding text box.
User's informations in the database will be updated and a message will be shown if operation is succesfull.

If there is an existing user with the given username, some of the informations for the searched user will be shown to the searcher.

Lastly, in the delete section if a user wants to leave our lovely RentChain, he or she can click the button. The user will be logged out and removed from the databese. With logging out, user will be redirected to landing page.
You can see the settings page of RentChain below.

.. figure:: images/settings.png
     :scale: 100 %
     :alt: settings page

     Settings page where users can manage their accounts
