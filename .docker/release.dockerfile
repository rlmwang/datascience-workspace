FROM datascience-prd
ENTRYPOINT source /venv/bin/activate \
    && gunicorn -w 1 -b :5000 -t 30 --reload api.wsgi:app