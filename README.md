# AdvEx-Alpha

Alpha version of [AdvEx](https://github.com/dnc1994/AdvEx), which validates the critical path of the product.

## Test Steps

1. Set up AWS credentials in `~/.aws/config`.
2. Set up `POSTGRES_URL`, `POSTGRES_USER`, `POSTGRES_PW`, `POSTGRES_DB` in environment variables.
3. Run `python db.py init` once.
4. Run `python db.py test` to see that the feedback for #1 submission is empty.
5. Start mock worker with `python worker.py`.
6. Send message with `python web_server.py`.
7. Run `python db.py test` again to see that the feedback has been updated. Also you should be able to observe that model and index files are downloaded to `tmp/`.

## Notebooks

`notebooks/` includes several Jupyter notebooks that give example of interacting with AWS resources like S3, SQS and RDS.
