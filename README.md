# Newsly
## How to use the software
*It is assumed that you already have this software setup and running as per the instructions below.*

Please visit http://localhost:8000, and you will be greeted with following page.
![Login UI](https://i.imgur.com/Ix0PnkD.png)

Login using the credentials that you have created at the setup phase.

Now, after login you will be visited with the following fields.
![img.png](newsly/static/docs/img.png)
You can ignore those that have been marked with a cross.

**The news interaction module is used to power the recommendation api, please don't manipulate it**

Our main focus of concern is in the News Module:
![img.png](newsly/static/docs/img_2.png)

We can add new category, tags and News using this module. 

The category and tags module are very simple, and they don't require much knowhow to use.
#### List of all categories
![category list](https://i.imgur.com/71iuXGC.png)

#### Adding a New Category
![category_add](https://i.imgur.com/c1lc9GF.png)

#### Adding a new TAG
![tag_add](https://i.imgur.com/7TXmqef.png)

### Adding a News
#### Viewing all news
![news_list](https://i.imgur.com/VEOXxsu.png)

You can view all the news in this view. The first box lists all the news. The 2nd column in same row represents who wrote the news and the final represents weather to show this news to user or not, i.e. weather to publish it?

#### Adding a news
In order to add the news, press `Add` button. After which you will be redirected to this UI.
![news_add](https://i.imgur.com/7XwVRVl.png)
![news_add_2](https://i.imgur.com/RTidB7Q.png)

**You are not to fill the fields inside the red box. Those will be automatically processed. After which you can edit them at later.**
After filling up the fields, press the save button.  

#### Push news to be automatically processed
Each news can be processed using state of the art Artificial Intelligence models.

Although AI can do most of the task, a human is required to make sure that what it did is correct and fix this. 

In order to trigger this automatic processing, visit the list view of news and select the news you want to process.
_You can select multiple news._

After which in the dropdown as shown below press the process button and press go
![news processing](https://i.imgur.com/fI9ly5C.png)

After pressing go, we get a confirmation
![news processing result](https://i.imgur.com/SLJuCxP.png)

Now sit back and relax as you let the AI do the job.

#### Process viewing and editing
AI can do amazing things but in some cases they do it wrong. So in order to prevent incorrect news being sent to the user, we need to supervise it.

Hence, after the AI finished processing the author will receive an email, in the address which he added during account creation or was added by admin.

The email will look something like this.
![](https://i.imgur.com/KXEFcAU.png)

The author can now review the AI's work. If this needs any modification, the author or editor can go and edit the news by clicking on the news title in list view.
![](https://i.imgur.com/7OuVQpw.png)

The edit view looks same as the create view, but it has the fields those when we added were empty.
![](https://i.imgur.com/Du40p44.png)

After the edit has been completed, the author has to redo the TTS (if summary has been edited). This is done in similar way as the full process trigger.
![](https://i.imgur.com/mFiL1S9.png)

In this way the author can add news. Now it's time to publish it so the user can view it from the app.

#### Publishing a news (Undrafting it)
In the list view, press the publish button and press go.
![https://i.imgur.com/60L4b46.png](https://i.imgur.com/60L4b46.png)

This will set the is_draft to be false allowing users to now view the news.

_One thing to take note is that, if the Automated processing has not been done or if summary, and tts have not been added, even after publishing it, it won't be shown to users as it is not complete._

## How to Set up
Steps:
1. Clone the GitHub repository
2. Install Python3 and PIP
3. Run `pip install -r requirements.txt`
4. Set up all the environment variables given below.
5. Create a database and set up DATABASE_URL as given by the format in https://pypi.org/project/dj-database-url/
6. Run `python manage.py migrate`
7. Run `python manage.py createsuperuser` and create admin user
8. Run `python manage.py runserver` and connect to the website using http://localhost:8000

### Environment Variables
- `NEWSLY_SECRET_KEY`
  - String block used for cryptographic transactions. Generated random value to be used. 
- `NEWSLY_DEBUG`
  - True | False
- `NEWSLY_ALLOWED_HOST`
  - Comma seperated list of hosts that are allowed to point to the server. 
    - Example "localhost,newsly.pp.ua"
    - Use "*" if you want this to be accessed by any domain. 
- `NEWSLY_DATABASE_URL`
  - URL DSN in the form: `postgres://postgres@database_default:5432/db
`