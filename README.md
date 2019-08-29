# Installation with Docker
First build frontend and backend image :
```bash
docker build -t 329719/demo .
```
Then run docker-compose.yaml :
```bash
docker-compose up
```
# Add a new tool to the Demo
## Backend side
First we assume you have a dockerized LIAAD model like an API REST. A good template to start would be at LucDomingo/Docker_Pampo
.
Add your container as a service inside docker-compose.yaml :
```yaml
...
  <service_name>:
    image: <image_name>
...
```
The service is running at the port exposed by the container. Thus you can add a new entry inside utils.py using the following url :
```bash
http://<service_name>:<exposed_port>/...
```
## Frontend side
First create a new file into demo/src/components/demos :
```javascript
const apiUrl = () => `${API_ROOT}/predict/pampo` // endpoint API_ROOT is defined inside demo/src/api-config.js
const title = "Pampo" // Model title 
var bib_article = ...  // to cite paper of the model
const description = ( 
    <span>
      <span>
       .........
      </span>
    </span>
) // Model description
const fields = [] // Input fields define inside DemoInput.js
const Output = ({ responseData }) => {} // Define Output
```
Then add your model inside demo/src/models.js and build again 329719/demo.
