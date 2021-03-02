#Update the URL of origin remote using SSH instead of HTTPS;

git remote set-url origin git@github.com:username/repo.git

#Make Git store the username and password and it will never ask for them.

git config --global credential.helper store
git config --global credential.helper cache
