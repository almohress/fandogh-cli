import click
from .base_commands import FandoghCommand

from .config import *

fandogh = [{'name': 'fandogh', 'url': 'https://api.fandogh.cloud', 'active': True}]
clusters = get_cluster_config().get('clusters')


@click.group("cluster")
def cluster():
    pass


@click.command("add", cls=FandoghCommand)
@click.option('--name', prompt='name', help="Enter name for cluster url")
@click.option('--url', prompt='url', help="Enter cluster URL")
def add(name, url):
    old_clusters = get_cluster_config().get('clusters')
    clusters_names = [d['name'] for d in old_clusters]
    if name in clusters_names:
        click.echo("This name is already exist first you have to delete it")
        return
    if not old_clusters:
        custom_dict = [dict(name=name, url=url, active=False),
                       *fandogh]
    else:
        custom_dict = [dict(name=name, url=url, active=False), *old_clusters]
    get_cluster_config().set('clusters', custom_dict)


@click.command("list", cls=FandoghCommand)
def cluster_list():
    if get_cluster_config().get('clusters') is None:
        get_cluster_config().set('clusters', fandogh)
    for zone in get_cluster_config().get('clusters'):
        message = f' * {zone["name"]}'
        if zone['active']:
            message += ' (active)'
        click.echo(message)


@click.command('active')
def cluster_active():
    for idx, project_type in enumerate(clusters):
        click.echo('-[{}] {}'.format(idx + 1, project_type['name']))
    cluster_name_index = click.prompt('Please choose one of the clusters above',
                                      type=click.Choice(list(map(lambda i: str(i), range(1, len(clusters) + 1)))),
                                      show_choices=False,
                                      )

    [d.update(active=False) for d in clusters]
    clusters[int(cluster_name_index) - 1]['active'] = True
    get_cluster_config().set('clusters', clusters)


@click.command('delete')
def cluster_delete():
    for idx, project_type in enumerate(clusters):
        click.echo('-[{}] {}'.format(idx + 1, project_type['name']))
    cluster_name_index = click.prompt('Please choose one of the clusters above',
                                      type=click.Choice(list(map(lambda i: str(i), range(1, len(clusters) + 1)))),
                                      show_choices=False,
                                      )
    selected_cluster = clusters[int(cluster_name_index) - 1]
    if selected_cluster['active']:
        click.echo("Pay Attention this cluster is ACTIVE you have to change active cluster then try again ")
        return
    if selected_cluster['name'] == 'fandogh':
        click.echo("You can not delete fandogh cluster ")
        return
    del clusters[int(cluster_name_index) - 1]
    get_cluster_config().set('clusters', clusters)


cluster.add_command(add)
cluster.add_command(cluster_list)
cluster.add_command(cluster_active)
cluster.add_command(cluster_delete)
