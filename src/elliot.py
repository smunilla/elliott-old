from subprocess import call, check_output
from requests_kerberos import HTTPKerberosAuth
import click
import requests

ERRATA_ADD_BUG_URL = 'https://errata.devel.redhat.com/api/v1/erratum/%s/add_bug'

@click.group()
@click.pass_context
@click.option("--advisory",
              help="ID for the advisory to operate on")
@click.option("--target_release",
              multiple=True,
              help="Target release versions (e.g. 3.9.x)")
@click.option('--verbose', '-v', default=False, is_flag=True, help='Enables verbose mode.')
@click.help_option('--help', '-h')
def cli(ctx, advisory, target_release, verbose):
    ctx.obj = {}
    ctx.obj['advisory'] = advisory
    ctx.obj['target_release'] = target_release
    ctx.obj['verbose'] = verbose

@cli.command("addnewbugs", help="Add new MODIFED bugs to the advisory")
@click.pass_context
def addnewbugs(ctx):
    advisory = ctx.obj['advisory']
    target_releases = ctx.obj['target_release']

    target_releases_str = ''
    #target_releases_string="target_release=3.4.z&target_release=3.5.z&target_release=3.6.z"
    for r in target_releases:
        target_releases_str += 'target_release={0}&'.format(r)

    query_url = 'https://bugzilla.redhat.com/buglist.cgi?bug_status=MODIFIED&classification=Red%20Hat&f1=component&f2=component&f3=component&f4=cf_verified&keywords=UpcomingRelease&keywords_type=nowords&known_name=All%203.x%20MODIFIED%20Bugs&list_id=8111122&o1=notequals&o2=notequals&o3=notequals&o4=notequals&product=OpenShift%20Container%20Platform&query_based_on=All%203.x%20MODIFIED%20Bugs&query_format=advanced&short_desc=%5C%5Bfork%5C%5D&short_desc_type=notregexp&{0}&v1=RFE&v2=Documentation&v3=Security&v4=FailedQA&version=3.0.0&version=3.1.0&version=3.1.1&version=3.2.0&version=3.2.1&version=3.3.0&version=3.3.1&version=3.4.0&version=3.4.1&version=3.5.0&version=3.5.1&version=3.6.0&version=3.6.1&version=3.7.0&version=3.7.1&version=unspecified'.format(target_releases_str)

    click.echo(query_url)

    new_bugs = check_output(['bugzilla', 'query', '--ids', '--from-url="{0}"'.format(query_url)]).splitlines()

    # post back to errata api
    for bug in new_bugs:
        for release in target_releases:
          click.echo("Flagging Bug #{0} with aos-{1}".format(bug, release))
          call(['bugzilla', 'modify', '--flag', 'aos-{0}+'.format(release), bug])

        click.echo("Adding Bug #{0}".format(bug))
        payload = {'bug': bug}
        r = requests.post(ERRATA_ADD_BUG_URL % advisory, auth=HTTPKerberosAuth(), json=payload)


cli.add_command(addnewbugs)

if __name__ == '__main__':
    # This is expected behaviour for context passing with click library:
    # pylint: disable=unexpected-keyword-arg
    cli(obj={})