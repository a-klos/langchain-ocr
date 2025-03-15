#!/bin/bash

docker run --user $(id -u):$(id -g) --rm -v $PWD:/local openapitools/openapi-generator-cli@sha256:b35aee2d0f6ffadadcdad9d8fc3c46e8d48360c20b5731a5f47c809d51f67a04 generate -i openapi-spec.yaml -g python-fastapi -o /local --additional-properties=packageName=rag_core_api,generateSourceCodeOnly=True
