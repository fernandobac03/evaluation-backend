
#!/bin/bash

docker stop evaluationlinks
docker rm evaluationlinks

docker run -d  --name evaluationlinks -p 5000:5000 evaluationlinks python3 -m pdb evaluationSameAs/index.py
