import streamlit as st
import requests

st.title("Find Related Singers")
st.markdown("Enter a artist's name and this app will display related artists using Spotify API")
st.text('________________________________________________________________________________________')
spotify_token = st.text_input('Enter Spotify Token')

artist_name = st.text_input('Enter Artist Name')
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

def get_related_artists():

    artist_id = get_artist_id(artist_name)
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

get_related_artists()

st.markdown(related_artists)

