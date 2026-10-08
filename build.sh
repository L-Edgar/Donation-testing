

pip install -r requirements.txt

#python manage.py collectstatic
python manage.py migrate
python manage.py collectstatic --noinput
echo "=== DIAGNOSTIC ==="
python manage.py findstatic image/homepage.jpg -v 2
ls staticfiles/image
grep -c homepage staticfiles/staticfiles.json
echo "=== END DIAGNOSTIC ==="