celery -A celery_tasks.tasks worker -l info
sudo service fdfs_trackerd start
sudo service fdfs_storaged start
sudo /usr/local/nginx/sbin/nginx