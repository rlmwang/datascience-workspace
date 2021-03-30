FROM datascience-prd
ENTRYPOINT source /venv/bin/activate \
    && gunicorn -w 3 -b :5000 -t 30 --reload app:app