import requests
import webbrowser


base_url = "https://api.mangadex.org"
mangadex_url = "https://mangadex.org/title"

# BASIC SEARCH
title = "Dungeon Meshi" # Obviously we need a "frontend" to get this input, this is an example to show you it works

# Get IDs of manga that match the title "Dungeon Meshi"
r = requests.get(
    f"{base_url}/manga",
    params={"title": title}
)

print([manga["id"] for manga in r.json()["data"]])

# Just to show you it works, this opens the first result in your browser
manga_ids = [manga["id"] for manga in r.json()["data"]]
if manga_ids:
    first_manga_url = f"{mangadex_url}/{manga_ids[0]}"
    print("Opening the first result in your browser:", first_manga_url)
    webbrowser.open(first_manga_url)
else:
    print("No manga found with the title:", title)



# ADVANCED SEARCH
included_tag_names = ["Action", "Romance"] # Again, we need a "frontend" to get this input
excluded_tag_names = ["Harem"]

tags = requests.get(
    f"{base_url}/manga/tag"
).json()

included_tag_ids = [
    tag["id"]
    for tag in tags["data"]
    if tag["attributes"]["name"]["en"]
       in included_tag_names
]

excluded_tag_ids = [
    tag["id"]
    for tag in tags["data"]
    if tag["attributes"]["name"]["en"]
       in excluded_tag_names
]


# Get IDs of manga that match the included and excluded tag IDs
r = requests.get(
    f"{base_url}/manga",
    params={
        "includedTags[]": included_tag_ids,
        "excludedTags[]": excluded_tag_ids,
    },
)

print([manga["id"] for manga in r.json()["data"]])


# Sorting
order = {
    "rating": "desc",
    "followedCount": "desc",
}
final_order_query = {}

for key, value in order.items():
    final_order_query[f"order[{key}]"] = value

# Get IDs of manga that match the included and excluded tag IDs, sorted by rating and followed count
r = requests.get(
    f"{base_url}/manga",
    params={
        **{
            "includedTags[]": included_tag_ids,
            "excludedTags[]": excluded_tag_ids,
        },
        **final_order_query,
    },
)

print([manga["id"] for manga in r.json()["data"]])


# Filtering
# THIS IS VERY IMPORTANT TO REMOVE PORN

filters = {
    "publicationDemographic[]": ["seinen"],
    "status[]": ["completed"],
    "contentRating[]": ["safe"],
}

# Get IDs of manga that match the filters
r = requests.get(
    f"{base_url}/manga", params=filters
)

print([manga["id"] for manga in r.json()["data"]])
