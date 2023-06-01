#!/bin/sh
# entrypoint.sh

# Run migrations
python manage.py migrate

# Then run the main container command (passed to us as arguments)
exec "$@"
