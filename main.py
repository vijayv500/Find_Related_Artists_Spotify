import streamlit as st
import requests
import json

st.title("One-Click Spotify Playlist Creator")
st.subheader("Create a Spotify playlist with top tracks of any singer/band")


st.markdown("""
* Enter the details below and click the button that prompts you to create a playlist.
* Related artists/bands will also be displayed.
* You need Spotify developer account to get access token. [Refer to this!](https://www.youtube.com/watch?v=yAXoOolPvjU)
""")


spotify_token = st.text_input('Enter Spotify Token')
spotify_user_id = st.text_input('Enter Spotify Username')
artist_name = st.text_input('Enter Singer/Band Name')

related_artists = []

def get_artist_id(artist_name):
    query = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist'
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )
    response_json = response.json()
    artist_id = response_json['artists']['items'][0]['id']

    return artist_id

def get_related_artists(artist_id):

    query = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )
    response_json = response.json()

    for i in range(0, len(response_json['artists'])):
        related_artists.append(response_json['artists'][i]['name'])

    return related_artists

def create_playlist():
    request_body = json.dumps({
        "name": f"Top songs of {artist_name}",
        "description": "high rated",
        "public": True
    })

    query = f"https://api.spotify.com/v1/users/{spotify_user_id}/playlists"
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )
    response_json = response.json()

    return response_json["id"]

def get_top_tracks():
    uris = []
    query = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )
    response_json = response.json()

    for i in range(10):
        uris.append(response_json['tracks'][i]['uri'])

    return uris

def add_songs_to_playlist():
    request_data = json.dumps(uris)
    query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )

    response_json = response.json()

if artist_name !='' and spotify_token != '' and spotify_user_id != '':
    artist_id = get_artist_id(artist_name)
    get_related_artists(artist_id)


    button = st.button(f'Create Spotify Playlist With Top Tracks of {artist_name}')
    if button:
        uris = get_top_tracks()
        playlist_id = create_playlist()
        add_songs_to_playlist()

    st.markdown("Related Artists:")
    st.markdown(related_artists)

st.sidebar.markdown("""
        * [Github Repo](https://github.com/vijayv500/Find_Related_Artists_Spotify)
        * [Twitter](https://twitter.com/vijayv500)
        * [Medium Blog](https://vijayv500.medium.com) 
        * [Instagram](https://www.instagram.com/vijayv500/)
""")





