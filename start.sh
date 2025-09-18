cd gateway && sh bin/run.sh root/conf.yaml &

cd webapp || exit 1

if [ ! -d .venv ]; then
    uv venv .venv
fi

. .venv/bin/activate
uv pip install -r requirements.txt

flask --app app run --debug -p 5056 -h 0.0.0.0
