all: env

env:
	virtualenv --python="/usr/local/bin/python3.3" env && source ./env/bin/activate && pip install -r requirements.txt

docker:
	docker build -t hexgen .

docker-bash:
	docker run -it --entrypoint /bin/bash hexgen

