#!/bin/bash

if [ "$seed_database" == "false" ]; then
  echo ">>> Running migrate and seed"
  php artisan migrate --seed
fi

echo ">>> Starting app..."
php artisan serve --host=0.0.0.0

