# rate-limiting

A simple rate limiting example in front of FastAPI

### Running

Install docker, checkout this repo, and run

```
docker-compose up -d --build
```

in the root of the directory. Or just hit the [live demo](http://ratelimiting.luxas.xyz:9001)

### About

I organized my project using dependency injection and IoC so that I could swap out different caching dbs and rate limiting algorithms without
needing to change the app code much. I am using a time-bucket algorithm backed by a Redis cache. I recognize that there are pros/cons to this
approach as opposed to some more robust algorithms, but this algorithm gets the job done for a simple service. It works best if you keep the
time-interval (milliseconds) as low as possible.

To see my time-bucket algorithm implementation, please see [here](/business/services/time_bucket_limit.py). To see it being put to work, check
out the middleware that uses it [here](/app/middleware/rate_limit_middleware.py)

### Next Steps

There are a few key items I'd implement next, in no particular order:

1. Automated testing: use pytest and starlette's TestClient to ping the exposed endpoint.
2. Client differentiation: the rate limiter currently takes the requests/millisecond dataclass at initialization time. This is fine, but it would be
   ideal if the user could specify different rates for different clients. This could be achieved by expanding on the TimeBucketContext dataclass, or
   storing a key in the cache with the rate information based on client.
3. More robust error handling. The only error I'm handling particularly well is the "too many requests" (429) error.
4. Client identification: the middleware is currently relying on request.client to get an IP. This will not do it the uvicorn server is behind a
   reverse proxy, as it likely would be. We should instead rely on header values to get IP, session token, or some other identifying piece of info.

### Deployment

In case you're curious, I've packaged this up using docker (see [Dockerfile](/Dockerfile)), am hosting it at over at [dockerhub](https://hub.docker.com/repository/docker/lucasconnellm/rate-limiting), and have deployed it using Portainer on one of my personal Vultr instances.
