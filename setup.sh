pip install git+https://github.com/jhuapl-boss/django-oidc.git
pip install git+https://github.com/jhuapl-boss/drf-oidc-auth.git
pip install git+https://github.com/jhuapl-boss/boss-oidc.git

cat environment.txt | xargs -n 1 pip install
