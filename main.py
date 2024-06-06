from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#print(client_id, client_secret) # Just to check that client id and secret is recognized

def get_token(): # Get access to authorization token
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
        
    }
    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token): # Get authorization header
    return {"Authorization":"Bearer " + token}

def search_for_artist(token, artist_name): # Search for artist
    url = "https://api.spotify.com/v1/search" # from the API
    headers = get_auth_header(token) # header of my authentication
    query = f"q={artist_name}&type=artist&limit=1" # actual query for this function
    
    query_url = url + "?" + query # concatenate
    result = get(query_url, headers=headers) # get request
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists.")
        return None
    return json_result[0]

    #print(json_result)

def get_songs_by_artist(token, artist_id): # Get top tracks of searched artist
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_recommendation(token, track_id): # Get list of recommendation songs based on given track
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    query = f"limit=10&market=US&seed_tracks={track_id}" #Output 10 songs recommended by the given track seed
    
    query_url = url + "?" + query
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


# Learning functions and how to call/print
token = get_token()
#print(token)
result = search_for_artist(token, "Joji")
#print(result["name"])
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
#print(songs)
#for idx, song in enumerate(songs):
#    print(f"{idx+1}.{song['name']}")

#-----------RECOMMENDATION-------------#
# Manually entering track seed
#song_id = "3r8RuvgbX9s7ammBn07D3W" # ditto
#song_id = "1dGr1c8CrMLDpV6mPbImSI" # Lover by Taylor Swift
#song_id = "3AO2MYgrCiTorCUura1szR" # Fck Boys by Blxst
song_id = "3AO2MYgrCiTorCUura1szR,50XeBuSbhueY24KqJZcEAd" # Testing list of songs work
recommended_songs = get_recommendation(token, song_id)

# Print recommended songs with Artist name
for idx, song in enumerate(recommended_songs):
    print(f"{idx+1}.{song['name']} - {', '.join([artist['name'] for artist in song['artists']])}")