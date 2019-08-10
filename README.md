# NomeroffNet REST API

Based on https://github.com/ria-com/nomeroff-net.

## Getting started

1. Configure app.

    `cp .env.dist .env`
    
   
1. (Optional) Enable dev mode.

    `ln -s docker-compose.dev.yml docker-compose.override.yml`    

1. Start container.
 
    `docker-compose up`
    
1. Make an API call.
    
    `time curl http://localhost:3116/read?url=https://raw.githubusercontent.com/ria-com/nomeroff-net/master/examples/images/example1.jpeg`
    
    
    