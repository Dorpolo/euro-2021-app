# euro-2021-app
<hr>

Django based web-application for creating friednly leagues for Euro 2020 score predictions.

The platform enables to create, manage and share the following basic features:

1. Creating a new league.
2. Joining an existing league.
3. Add score prediction forms (for each tournoment stage, separtly).
4. Edit your score prediction forms.
4. Edit your private profile.
5. Edit your league profile.

<hr>

* Real results data is based on external API service (https://statorium.com/euro-2020-api-football-data).
* Postgres DB serves as a storage. can be easily configered using the settings.py Django's file.
* The applcation have a standert out of the box Django's login mechnizem.

<hr>

The application includes the following pages:

1. Home page
  * All league tables (supports one to many mechnizem) 
  * All league users.
  * Dynamic buttons for score prediction insertion.
  * Next/ Prev game cards (including real score vs. predicted and hyper links for statistics)
  
2. Statistics
  * League tables.
  * Next/ Prev game stats
    * Score distribution 
    * Winner distribution.
  * Live match 
    * Shows users prediction in real time and elimnates score that are not relevant anymore.
  * Player selection
    * Top scorer
    * Top Assist
    
3. Terms
  * Holds all competition rules and logic.
  

