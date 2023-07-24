# Test OCI configs

## OCI-CLI

1. Add your own key file(파일 복사)

- `oci-cli-res/ryann3-oci.pem`

2. Then execute docker compose

```
docker compose up
```

3. docker exec

```sh
docker exec -it harmonica-api-test-1 /bin/sh
```

4. Execute

```sh
oci fn function get --function-id "ocid1.fnfunc.oc1.iad.aaaaaaaarfg2a56kg252optrso5ed2x7gpxwwwfm5tq6msuks7bmlbbwwcuq"
```

5. Good case

```
{
  "data": {
    "application-id": "ocid1.fnapp.oc1.iad.aaaaaaaagzvju7jc6h4eyvbdy7smu7urmztm3u2d4z67akyh2stvtxxxgjrq",
    "compartment-id": "ocid1.tenancy.oc1..aaaaaaaagkmgmjlchsvkyk2xfuvr5hhlqklr5ppah66n6k47z2dy7xn2wjuq",
    "config": {},
    "defined-tags": {
      "Oracle-Tags": {
        "CreatedBy": "default/ryann3@sookmyung.ac.kr",
        "CreatedOn": "2023-07-07T12:19:57.395Z"
      }
    },
    "display-name": "product-store-operations-python",
    "freeform-tags": {},
    "id": "ocid1.fnfunc.oc1.iad.aaaaaaaarfg2a56kg252optrso5ed2x7gpxwwwfm5tq6msuks7bmlbbwwcuq",
    "image": "iad.ocir.io/idhxkx7uajar/test/product-store-operations-python:0.0.42",
    "image-digest": "sha256:b0c8d5e65f11af2098a9c59f9920d145cd88e9f99f47dad2beefda1ad3b8a273",
    "invoke-endpoint": "https://stvtxxxgjrq.us-ashburn-1.functions.oci.oraclecloud.com",
    "lifecycle-state": "ACTIVE",
    "memory-in-mbs": 256,
    "provisioned-concurrency-config": null,
    "shape": null,
    "source-details": null,
    "time-created": "2023-07-07T12:19:57.710000+00:00",
    "time-updated": "2023-07-07T12:19:57.710000+00:00",
    "timeout-in-seconds": 30,
    "trace-config": {
      "is-enabled": false
    }
  },
  "etag": "16e62d632ed98eeb4ec873fdf12d87071fb4f6612e4b0bf13c6d89e88ebf15e5--gzip"
}
```

## OCI-FN

- (따로 추가해야할 key 파일은 없음)
- oci-fn은 두 가지 테스트를 수행해야한다

1. default: oci 계정과 잘 연동되었는지
2. docker logged-in: docker의 oci 계정에 로그인이 잘 되었는지

### Default

```sh
fn list apps
```

```
NAME		ID
test-cli	ocid1.fnapp.oc1.iad.aaaaaaaagzvju7jc6h4eyvbdy7smu7urmztm3u2d4z67akyh2stvtxxxgjrq
test-cli2	ocid1.fnapp.oc1.iad.aaaaaaaa7lin4nm3oin5wxzlegwewqanhscn2ytp5mkzqpkfxlq4mfnszciq
test-cli3	ocid1.fnapp.oc1.iad.aaaaaaaa5byfgpacp747bvex253ljptspqwo7f2obzxomg2qi2c5makxxwbq
test-cli4	ocid1.fnapp.oc1.iad.aaaaaaaat5inwoosm4n64jyshgit5iq7u4tiux7zxxq7a6hnfnzvsxj5n3bq
test-cli5	ocid1.fnapp.oc1.iad.aaaaaaaansr5vhwezdis56whrcjw4ew4gho3d3g3hiegb2ikasdqg6575aja
test-cli6	ocid1.fnapp.oc1.iad.aaaaaaaahainkivntfk76o5ni6tknnarlhotgp77fvvc57nqrja2ohxlkila
```

```sh
fn invoke test-cli product-store-operations-python
```

```
{"sql_statement": "select name, count from test_user.products", "results": [{"name": "Pen", "count": 100}, {"name": "Pencil", "count": 200}, {"name": "Notebook", "count": 50}, {"name": "Sketch pen", "count": 80}, {"name": "Eraser", "count": 150}]}
```

### Docker logged-in

- 일단은 `docker compose up`에서 `Login Succeeded` 뜨면 로그인 확인된 것이긴 함(수정 필요)

```sh
...
harmonica-api-test-1  | WARNING! Using --password via the CLI is insecure. Use --password-stdin.
harmonica-api-test-1  | WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
harmonica-api-test-1  | Configure a credential helper to remove this warning. See
harmonica-api-test-1  | https://docs.docker.com/engine/reference/commandline/login/#credentials-store
harmonica-api-test-1  |
harmonica-api-test-1  | **Login Succeeded**
harmonica-api-test-1  | INFO:     Will watch for changes in these directories: ['/app']
...
```
