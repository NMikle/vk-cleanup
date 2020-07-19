#!/usr/bin/env python3
import time

import click
import progressbar
import vk


@click.command()
@click.option('--login', required=True, help='Vk user login to proceed with', type=str)
@click.option('--password', '-p', required=True, prompt='Vk User password', hide_input=True,
              help='User password to proceed with', type=str)
@click.option('--app', required=True, help='Id of your vk application', type=int)
def main(app, login, password):
    vk_api = init_vk_api(app, login, password)
    user_id = fetch_user_id(vk_api)
    user_videos = fetch_user_videos(user_id, vk_api)
    delete_user_videos(user_id, user_videos, vk_api)


def delete_user_videos(user_id, user_videos, vk_api):
    click.echo('Deleting...')
    time.sleep(1)
    deleted_per_second = 0
    for video in progressbar.progressbar(user_videos):
        vk_api.video.delete(video_id=video['id'], owner_id=video['owner_id'], target_id=user_id)
        deleted_per_second += 1
        if deleted_per_second == 5:
            time.sleep(1.2)
            deleted_per_second = 0


def fetch_user_id(vk_api):
    user = vk_api.users.get()[0]
    click.echo('Received user %s' % user)
    return user['id']


def fetch_user_videos(user_id, vk_api):
    user_videos_response = vk_api.video.get(user_id=user_id, count=200)
    user_videos = user_videos_response['items']
    click.echo("User has %s videos. Received %s" % (user_videos_response['count'], len(user_videos)))
    return user_videos


def init_vk_api(app, login, password):
    session = vk.AuthSession(app_id=app, user_login=login, user_password=password, scope='video')
    return vk.API(session, v='5.35', lang='en', timeout=10)


if __name__ == '__main__':
    main()
