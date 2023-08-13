# APS (Autodesk Platform Services)-Playground
Repo for exploring Autodesk Platform Services API (Forge) with Python-Flask on server side.
Use docker to deploy and development.

## To run
1) Clone repo and add your `docker.env` file into `app` folder. Add your APS Credentials to `docker.env` file:
```
APS_APP_ID=<your-app-id-here>
APS_APP_SECRET=<your-app-sercet-here>
FLASK_APP_KEY=<any-random-string>
```
2) Run in terminal `docker compose up --build` in root folder.

For development you can use devcontainer with `devcontainer.env` file.

## Simple Viewer
![2023-08-13_21h31_05](https://github.com/iris-inohosa/aps-playground/assets/89853648/a5d3601a-be9b-4774-a1ce-85ba6876e643)
