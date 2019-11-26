# App Engine transparent proxy
Google Cloud Platform AppEngine transparent proxy

Useful to use App Engine service as a facade for Compute Engine instances
or standalone servers having permanent IP address.

The main purpose and benefit of using transparent proxy is to obtain a
*.appspot.com domain name with a valid SSL certificate in order to connect
to Compute Engine HTTP endpoints without additional settings.

## Configuration
Place `endpoints.conf` file, having list of endpoints, to the `appengine-redirect` app directory.
Refer for [appengine-redirect/endpoints.conf.sample](appengine-redirect/endpoints.conf.sample)
sample configuration file.

For each line in config file corresponding endpoint will be configured.

For example for a given configuration
```text
ep310 http://135.187.234.31:8080
ep311 http://135.187.234.31:8001
ep32 https://135.187.234.32
``` 

following endpoints created

```text
https://<my-shiny-name>.appspot.com/ep310/
https://<my-shiny-name>.appspot.com/ep311/
https://<my-shiny-name>.appspot.com/ep32/
```

and all requests similar to `https://<my-shiny-name>.appspot.com/ep310/xxx/yyy/zzz` are going to be 
transparently redirected to `http://135.187.234.31:8080/xxx/yyy/zzz`.