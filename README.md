### aws-managedblockchain-proxy

Proxies and signs request to a manged blockchain node

```shell
docker build -t aws-managedblockchain-proxy .

# Env vars
docker run --rm -ti \
  -e 'AWS_ACCESS_KEY_ID=<YOUR ACCESS KEY ID>' \
  -e 'AWS_SECRET_ACCESS_KEY=<YOUR SECRET ACCESS KEY>' \
  -e 'ENDPOINT=<HTTP Endpoint>' \
  -p 8086:8086 \
  aws-managedblockchain-proxy

# Shared Credentials
docker run --rm -ti \
  -v ~/.aws:/root/.aws \
  -p 8086:8086 \
  -e 'AWS_PROFILE=<SOME PROFILE>' \
  -e 'ENDPOINT=<HTTP Endpoint>' \
  aws-managedblockchain-proxy
```