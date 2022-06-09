# mqtt_logger

An easy-to-use tool for logging and viewing MQTT data.

Configure mqtt_watch.py to connect to your mqtt server, then start with `python mqtt_watch.py`

To view your data, start the server with `uvicorn main:app --reload` and navigate to http://127.0.0.1:8000

Lastly, configure your alerts and start with `python alert.py`

If you're looking an mqtt server to test this out, [nanomq](https://github.com/emqx/nanomq) is fast and requires no configuration.
