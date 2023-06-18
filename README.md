---
title: Chatroles Vdb
emoji: 🦀
colorFrom: blue
colorTo: pink
sdk: gradio
sdk_version: 3.33.1
python_version: 3.10.6
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## local test

run the app:

```shell
python3 app.py
```

visit site at: http://127.0.0.1:7860

### upsert API call

```shell
curl -X POST -H 'Content-type: application/json' --data '{ "data": ["Jill111", { "meta": { "id": "Jill111" }, "content": {"goal": "for test", "skills": [ "for test skills 10 chars least." ] } }] }' http://127.0.0.1:7860/run/predict
```

### search API call

```shell
curl -X POST -H 'Content-type: application/json' --data '{ "data": [{"goal": "for test", "skills": [ "for test skills 10 chars least." ] }, 3] }' http://127.0.0.1:7860/run/predict_1
```

### embed text array to vectors

```shell
curl -X POST -H 'Content-type: application/json' --data '{ "data": [["Jill","haha"]] }' https://127.0.0.1:7860/run/predict_2
```

## online test

```shell
curl -X POST -H 'Content-type: application/json'  -H 'Authorization: Bearer xxxxxxx' --data '{ "data": ["Jill1", { "meta": {"id":"Jill1", "nick":"erer"}, "content": {"goal": "for test", "skills": [ "for test skills 10 chars least." ] } }] }' https://thisis-it-chatroles-vdb.hf.space/run/predict
curl -X POST -H 'Content-type: application/json'  -H 'Authorization: Bearer xxxxxxx' --data '{ "data": [{"goal": "for test", "skills": [ "for test skills 10 chars least." ] }, 3] }' https://thisis-it-chatroles-vdb.hf.space/run/predict_1

```

### gradio interface

https://huggingface.co/spaces/thisis-it/chatroles-vdb
