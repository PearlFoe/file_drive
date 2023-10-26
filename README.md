# file_drive

## Deployment
Create virual environment and activate it
```shell
python3 -m venv venv
source venv/bin/activate
```

Install dependences
```shell
pip3 install -r requirements.txt
```

### Server
To run server use
```shell
gunicorn app:get_app --chdir src/server/ --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
```