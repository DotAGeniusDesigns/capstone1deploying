release: flask db upgrade || flask db stamp head || flask db migrate || flask db upgrade && flask seed-db
web: gunicorn app:app --log-level info
