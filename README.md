# Build a Data Ingestion and Retriveal APP with Django



## Author 🚀

> Olusola Lanre Akinsulere
---



## Technologies
- Django
- DRF
- DRF-Spectacular
- requests
- Pandas
- Docker 
- Docker Compose
- Postgresql

---


---

---

## Setup django app on local
- clone repo from github
- install docker if you haven't
- Upload your csv to a blob storage
- Create your .env based of the .env.sample
- run docker-compose -f docker-compose-deploy.yml build
- after building run docker-compose -f docker-compose-deploy.yml up
- run tests docker-compose -f docker-compose-deploy.yml run --rm app sh -c  "python manage.py test"

- Server will start after this command


---


---


---

## Thought Process

For the ingestion, I setup the files in a blob storage, because If we scaled, putting the files on  a single server, other replicas might not be able to access it, also I used requests to stream from the URL, and the streamed the buffers through pandas data frame. We don't allow duplicated files, once a csv file has been processes, we look it down has processed and wait for the next file to be processed


---

## Contributions

Todo: 

- Use multiprocessing to furhter reduce the time it takes to reduce wait time for larger files
- Make the csv file upload more dynamic, by allowing different csv url, so multiple csv files can be processes

---
 
## Documentation and Video Walkthrough

[documentation-to-view(postman)](https://documenter.getpostman.com/view/23325006/2sA2xe4u5K)
---
[documentation-to-download(postman)](https://lunar-trinity-430229.postman.co/workspace/Team-Workspace~34e62003-3b98-4049-856f-fd72361d5f1e/collection/23325006-18766467-a480-4baf-bc9a-9d6b92669cce?action=share&creator=23325006&active-environment=23325006-4ea21514-be24-48c7-a8bb-1ebcc4da495e)
---
[Video-Walkthrough-part-1](https://www.loom.com/share/10954c3a002347c5901436a0851f47d4?sid=16eb5ef3-8c39-4d8a-82de-c08874aee436)
---

[Video-Walkthrough-part-2](https://www.loom.com/share/6029f04dd1254dcba4f0dcb3ff9c53e8?sid=ebf756a9-ddc9-44b4-9159-f02c7c4dd7ba)
---

