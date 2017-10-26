# COMS6998_CloudComputing_hw1

It's a TwittMap web application built by Liqi Chen (lc3267) and Kejia Chen (kc3136) for COMS6998 Cloud Computing course at Columbia University. 

Users can choose from 10 key words ('serendipity','AlphaGo Zero','HKUST','Columbia University','Cloud Computing','Drunken Noodles','Facebook','Eason Chan','X-man','Gotham') to display the locations of twitts that contains the keyword on the map, and can focus on the twitts within a certain region by clicking on the map.

Everytime users do querying, the app will stream several new twitts data into the database and display to user.

Technical details:
Flask for web app development
ElasticSearch for database