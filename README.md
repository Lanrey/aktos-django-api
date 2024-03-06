# Build a Data Ingestion and Retriveal APP with Django



## Author 🚀

> Olusola Lanre Akinsulere
---



## Technologies
- Django
- DRF
- DRF-Spectacular
- requests
- Pandsa
- Docker 
- Docker Compose
- Postgresql

---


---

---

## Setup django app on local
- clone repo from github
- install docker if you haven't
- run docker-compose -f docker-compose-deploy.yml build
- after building run docker-compose -f docker-compose-deploy.yml up
- Swrver will start after this command


---


---


---

## Thought Process

For the ingestion, I setup the files in a blob storage, because If we scaled, putting the files on  a single server, other replicas might not be able to access it, also I used requests to stream from the URL, and the streamed the buffers through pandas data frame


---

## Contributions

Todo: 

- Use multiprocessing to furhter reduce the time it takes to reduce wait time for larger files

---

## Challenges



---

