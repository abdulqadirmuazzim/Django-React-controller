artists = [
    {
        "external_urls": {
            "spotify": "https://open.spotify.com/artist/4kpoYPOSgCl2jYvCm6Cp05"
        },
        "href": "https://api.spotify.com/v1/artists/4kpoYPOSgCl2jYvCm6Cp05",
        "id": "4kpoYPOSgCl2jYvCm6Cp05",
        "name": "Muhammad Al Muqit",
        "type": "artist",
        "uri": "spotify:artist:4kpoYPOSgCl2jYvCm6Cp05",
    },
    {
        "external_urls": {
            "spotify": "https://open.spotify.com/artist/033yJpOqIQr5XW6KbvBljo"
        },
        "href": "https://api.spotify.com/v1/artists/033yJpOqIQr5XW6KbvBljo",
        "id": "033yJpOqIQr5XW6KbvBljo",
        "name": "Hamoud Al Qahtani",
        "type": "artist",
        "uri": "spotify:artist:033yJpOqIQr5XW6KbvBljo",
    },
]

artist_string = ""
for i, artist in enumerate(artists):
    name = artist.get("name")
    artist_string += f"{name}, "
    print(name)

print(artist_string)
