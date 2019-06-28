
#!/bin/bash

docker stop evaluationlinks
docker rm evaluationlinks

docker run -d  --name evaluationlinks -p 8081:5000 evaluationlinks
