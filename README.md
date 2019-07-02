<p align="center">
    <img src="https://cdn.worldvectorlogo.com/logos/capital-one-2.svg" width="150">
  </a>
</p>

<h3 align= "center"> Capital One Software Enginering Summit 2019 Coding Challenge </h3>

This is my submission for the coding challenge for the Capital One Summit Software Engineering Summit of Summer '19. 
This app is live at <https://npsk-app.herokuapp.com/> It functions as an automated information kiosk would at a live site. Users can search keywords and filter by state for events, national parks, and campgrounds. This app supplies basic information such as location and descriptions, as well as accessibility information, weather, contact information, etc.

___

# A Personal Note
This was my first time doing anything remotely web-dev related, so it's a new world to me! At first I was intimidated by building this from scratch with no prior knowledge, but I had great fun getting to learn something on my own. I loved coding something that was a lot more free-form, with design choices up to the programmer, especially after the academic year. Thank you to Capital One for the opportunity to build this app and submit to the Software Engineering Summit!  


# Details About the App

This app allows for keywords search, with a "location filter" to select parks, events, or campgrounds. If the filter is left unselected the app searches all three types of locations. In addition, there is a "state" filter for US States. In terms of design choice, I chose not to use a database because I felt that the number/size of the data entries was not large enough to justify complicating the code and implementation further. If any information (contact info, directions, weather, etc.) is not available the app will instead display an "Information unavailable" message. 

This app provides the following functionality (copied from the challenge spec).
1. Provides tools to assist users in finding specific information, such as state and designation filtering, name and keyword search.
2. Lists details about specific visitor centers, as well as nearby campgrounds.
3. Displays alerts, articles, events, and news releases about a selected destination.
4. Provides educational information about a selected destination, utilizing available lesson plans as well as relevant people and places associated with the location.

I have also included the bonus feature:

- When displaying information, utilize relevant symbols from the NPS Symbol Library to illustrate relevant items.

Finally, what I used to build this app:

- Python/Flask
- HTML/CSS/Javascript
- Bootstrap
