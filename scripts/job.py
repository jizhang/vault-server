import sys

from vault import app, db

def main():
    try:
        args = sys.argv
        job_name = args.pop(1)
        mod_name = 'vault.jobs.%s' % job_name
        app.ready(db=True, web=False)

        mod = __import__(mod_name, fromlist=['*'])
        mod.run(*sys.argv[1:])
        return 0

    finally:
        db.session.remove()

if __name__ == '__main__':
    with app.app_context():
        sys.exit(main())
