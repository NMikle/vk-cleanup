#!/usr/bin/env python3

import click
import vk

from scopes import Video, Group


@click.command()
@click.option('--login', required=True, help='Vk user login to proceed with', type=str)
@click.option('--app', required=True, help='Id of your vk application', type=int)
@click.option('--scope', '-d', '-r', required=True, help='Type of Vk collection to be removed. This parameter also '
                                                         'specifies the scope for the API access token',
              type=click.Choice(['video', 'groups'], case_sensitive=False))
@click.option('--password', '-p', required=True, prompt='Vk User password', hide_input=True,
              help='User password to proceed with', type=str)
def main(app, login, password, scope):
    vk_api = init_vk_api(app, login, password, scope)
    user_id = fetch_user_id(vk_api)
    collection = init_requested_scope(scope, vk_api)
    collection.remove(user_id, collection.fetch(user_id))


def init_requested_scope(scope, vk_api):
    if scope == 'video':
        return Video(vk_api.video)
    elif scope == 'groups':
        return Group(vk_api.groups)
    else:
        raise NotImplementedError


def fetch_user_id(vk_api):
    user = vk_api.users.get()[0]
    click.echo('Received user %s' % user)
    return user['id']


def init_vk_api(app, login, password, scope):
    session = vk.AuthSession(app_id=app, user_login=login, user_password=password, scope=scope)
    return vk.API(session, v='5.35', lang='en', timeout=10)


if __name__ == '__main__':
    main()
