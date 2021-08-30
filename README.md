# Wagtail openedX site

[![Build Status](https://github.com/martibosch/wagtail-openedx-site/workflows/CI/badge.svg?branch=main)](https://github.com/martibosch/wagtail-openedx-site/actions/workflows/ci.yml)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![GitHub license](https://img.shields.io/github/license/martibosch/wagtail-openedx-site.svg)](https://github.com/martibosch/wagtail-openedx-site/blob/main/LICENSE)

Example Django site for [Wagtail openedX - a lightweight CMS for openedX portals](https://github.com/martibosch/wagtail-openedx).

## Requirements

* docker
* docker-compose

## Deployment instructions

This site is based on the [cookiecutter-django](https://github.com/pydanny/cookiecutter-django/) template, so further valuable information can also be found in [its documentation](https://cookiecutter-django.readthedocs.io/en/latest/?badge=latest).

To deploy this site, first go to `config/settings/base.py` and set `OPENEDX_API_URL` to the URL of the openedX API (**without trailing slash**) from which the content shall be retrieved.

### Local deployment

1. Build the stack:

```bash
docker-compose -f local.yml build
docker-compose -f local.yml up
```

2. Run the migrations:

```bash
docker-compose -f local.yml run django python manage.py migrate
```

3. Create a super user:

```bash
docker-compose -f local.yml run django python manage.py createsuperuser
```

You can now go to https://localhost:8000 to see the live site. To synchronize the courses from the openedX instance defined in the settings, use the view at https://localhost:8000/catalog/sync-courses.

### Production deployment

1. Configure a docker-machine environment. For instance, to deploy in DigitalOcean, the following command can be used:

    ```bash
    docker-machine create --driver digitalocean --digitalocean-region $DO_REGION \
        --digitalocean-image $DO_IMAGE --digitalocean-size $DO_SIZE \
        --digitalocean-access-token $DO_TOKEN --engine-install-url=$ENGINE_URL \
        $MACHINE_NAME
    ```

    with the variables set to (feel free to adjust them to suit your use case):
    * `DO_REGION=fra1`
    * `DO_IMAGE=ubuntu-18-04-x64`
    * `DO_SIZE=s-4vcpu-8gb`
    * `DO_TOKEN` is the [DigitalOcean personal access token](https://docs.digitalocean.com/reference/api/create-personal-access-token/).
    * `ENGINE_URL=https://releases.rancher.com/install-docker/19.03.09.sh`
    * `MACHINE_NAME=wagtail-openedx-site`

2. Point docker to the new machine:

    ```bash
    eval $(docker-machine env wagtail-openedx-site)
    ```

3. Amend the following production environment variables at `.envs/.production/.django` (remember to **keep `.envs/.production/.django` out of version control** to avoid disclosing secret access keys):

    * Create a S3-like storage instance and amend the `DJANGO_AWS_ACCESS_KEY_ID`, `DJANGO_AWS_STORAGE_BUCKET_NAME`, `DJANGO_AWS_S3_REGION_NAME` and `DJANGO_AWS_S3_ENDPOINT_URL`.  Note that the example settings in this repository are based on DigitalOcean Spaces so you might need to adjust them if you are using another cloud provider. Adjustments in the production settings at `config/settings/production.py` might also be required. See [the documentation of `django-storages`](https://django-storages.readthedocs.io/en/latest) for more details about configuring remote storages from different providers.
    * Set the `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` and `WAGTAIL_ADMIN_URL` to some URL-safe cryptographichally strong strings, e.g., using [the `secrets.token_urlsafe` function](https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe).
    * Set `DJANGO_ALLOWED_HOSTS` to your production domain(s).

4. In the `compose/production/traefik.yml` file, change the line:

    ```
    "Host(`wagtail-openedx.africancitieslab.org`) || Host(`www.wagtail-openedx.africancitieslab.org`)"
    ```

    for the production domain(s).

5. Build the stack:

    ```bash
    docker-compose -f production.yml build
    docker-compose -f production.yml up -d
    ```

6. Run the migrations:

    ```bash
    docker-compose -f production.yml run django python manage.py migrate
    ```

7. Create a super user:

    ```bash
    docker-compose -f production.yml run django python manage.py createsuperuser
    ```

## Development instructions

To set up a development environment, install the requirements and initialize pre-commit as follows:

```bash
pip install -r requirements/local.txt
pre-commit install
```

## Acknowledgments

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/pydanny/cookiecutter-django/)
