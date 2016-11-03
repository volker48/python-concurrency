# Python concurrency

This is the code used as examples in the [toptal](http://www.toptal.com/) engineering blog post I wrote
[http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python](http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python).


### Running the examples
The examples have all been tested under Python 3.4.2 running on OS X. They _should_ work on other operating systems, but I haven't tested it everywhere.

1. Get an [Imgur](https://imgur.com/account/settings/apps) API Key
2. Install dependencies with `pip install -r requirements.txt`
3. Run an example `IMGUR_CLIENT_ID=your_client_id threading_imgur.py`
	1. For the `rq_imgur.py` example you will also need to be running a redis server 

