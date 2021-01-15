# Spotify Django

This is a project that use an external spotify API. This is a test version that can be extended for a production stage.


Dependencies
------------
- Python 3.6+
- Django 1.11+
- For the API module, Django REST Framework 3.7+ is required.
- For run the application, it's need have docker installed

Setup
------------

Make sure you already has docker and docker-compose installed.

 `sudo apt  install docker.io`
 
  `sudo apt install docker-compose`

First you have to do a download of the docker image:

    `git clone https://gitlab.com/georgericardo26/spotify_api_django.git`

After, you will init the container service:

    `sudo docker-compose up`
    
    
NOTE: On Mac OS you must need share the path in -> preferences > tab File Sharing > add the project path

The main packages
------------
 - `api`: Containing the api serving the handled response to the client
 - `common`: Containing all of the structure to consume the external clients.
 - `web`: Containing a simple web interface.

Endpoints
------------
 - Search albums from Artist or Genre: `api/spotify/search/albums/`
 - List my playlist: `api/spotify/playlists/me/`
 - List tracks from playlist: `api/spotify/playlists/3kAuybtGKVuM53csDD16ma/tracks/`
 - Search artist: `api/spotify/search/artists/`
 - List top-tracks from artist: `api/spotify/artists/7HGNYPmbDrMkylWqeFCOIQ/top-tracks/`

Web Interface
------------
There is a simple web Interface to navigate with it.
![](https://apistaticfiles.s3-us-west-2.amazonaws.com/Captura+de+Tela+2021-01-15+a%CC%80s+11.47.34.png)


> #### Important
> - 1 - I had just 2 days to develop and finish the project, so is missing a few things
> to improve as web documentation (swagger/Open-API), etc..
> - 2 - I've placed some data information in the settings file, this is not a good approach
> but as a local project I didn't insert this variables as env variables.
