# NomeroffNet REST API

Based on https://github.com/ria-com/nomeroff-net.

## Getting started

### Pick a version.

If you want to use CPU version.

```bash
ln -sf docker-compose.cpu.yml docker-compose.yml
```

If you want to use GPU version. You need to have [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) installed.

```bash
ln -sf docker-compose.gpu.yml docker-compose.yml
```

### Configure app.

```bash
cp .env.dist .env
```
    
   
### (Optional) Enable dev mode.

```bash
ln -s docker-compose.dev.yml docker-compose.override.yml 
```

### Start container.

```bash 
docker-compose up
```
    
### Make an API call.

```bash    
time curl http://localhost:3116/read?url=https://raw.githubusercontent.com/ria-com/nomeroff-net/master/examples/images/example1.jpeg
```    
    
    