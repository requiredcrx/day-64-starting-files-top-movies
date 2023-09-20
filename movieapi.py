import requests

# url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
#
# header = {
#     "accept": "application/jason",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZmYwMTcxOWNmMWI3ZjU1MmQ5M2ExMTgxYTc1ZTdkZSIsInN1YiI6IjY1MDQ3NDA5YjUxM2E4MDBjNmMxNWQ4YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0skyLMo6uPK7L6WdkKz-n-O5fGVX5pHwoaasRz0p5VE"
# }
# response = requests.get(url=url, headers=header)
# datas = response.json()['results'][0]
#
#
#
#
# print(datas)
#
# year = datas["release_date"].split("-")
#
# print(year)

API_KEY = "3ff01719cf1b7f552d93a1181a75e7de"
api_endpoint = "https://api.themoviedb.org/3/trending/movie/day/1002185"
url = "https://api.themoviedb.org/3/movie/3"
response = requests.get(url=url, params={"api_key": API_KEY, "language": "en-US"})
data = response.json()
print(data["title"], data["release_date"], data["poster_path"], data["overview"])

print(data)