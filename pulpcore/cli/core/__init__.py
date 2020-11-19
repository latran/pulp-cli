import click

from pulpcore.cli.common import main, pass_pulp_context, PulpContext

from pulpcore.cli.core.artifact import artifact
from pulpcore.cli.core.orphans import orphans
from pulpcore.cli.core.task import task
from pulpcore.cli.core.exporter import exporter
from pulpcore.cli.core.export import export


@click.command()
@pass_pulp_context
def status(pulp_ctx: PulpContext) -> None:
    result = pulp_ctx.call("status_read")
    pulp_ctx.output_result(result)


# Register commands with cli
main.add_command(status)
main.add_command(artifact)
main.add_command(orphans)
main.add_command(task)
main.add_command(exporter)
main.add_command(export)