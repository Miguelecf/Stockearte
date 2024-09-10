# Stockearte

### Setup

#### Server in python

##### required

- install_requires=[
  'grpcio',
  'grpcio-tools',
  ]

##### generated protos

- cd path/to/project-root/server
- python generate_protos.py

##### run

- cd src
- python server.py

---

#### client in node

##### required

- node 20 (recommend node version switch -> nvm)

##### run

- cd path/to/project-root/client
- npm install
- npm start

---

#### UI

##### required

- node 20 (recommend node version switch -> nvm)

##### run

- cd path/to/project-root/UI
- npm install
- npm dev

---
