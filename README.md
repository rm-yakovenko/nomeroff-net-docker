# NomeroffNet REST API

Based on https://github.com/ria-com/nomeroff-net.

## Getting started

1. Configure app.

    `cp .env.dist .env`
    
1. (Optional) If you have a modern CPU, try enabling INTEL_TENSORFLOW. It gives some performance boost.

    ```yaml
    # .env
    INTEL_TENSORFLOW=1 
    ```
    
1. (Optional) Enable dev mode.

    `ln -s docker-compose.dev.yml docker-compose.override.yml`    

1. Start container.
 
    `docker-compose up`
    
1. Make an API call.
    
    `time curl http://localhost:3116/read?url=https://automoto.r.worldssl.net/auto/Chevrolet-Lacetti-ne_ukazan-none-2007-16-23414105.jpeg`
    
    
    