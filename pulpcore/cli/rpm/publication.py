import gettext
from typing import Optional, Union

import click

from pulpcore.cli.common.context import PulpContext, PulpEntityContext, pass_pulp_context
from pulpcore.cli.common.generic import (
    create_command,
    destroy_command,
    href_option,
    list_command,
    show_command,
)
from pulpcore.cli.rpm.context import PulpRpmPublicationContext, PulpRpmRepositoryContext

_ = gettext.gettext


def _repository_callback(
    ctx: click.Context, param: click.Parameter, value: Optional[str]
) -> Optional[Union[str, PulpEntityContext]]:
    # Pass None and "" verbatim
    if value:
        pulp_ctx: PulpContext = ctx.find_object(PulpContext)
        return PulpRpmRepositoryContext(pulp_ctx, entity={"name": value})
    return value


@click.group()
@click.option(
    "-t",
    "--type",
    "publication_type",
    type=click.Choice(["rpm"], case_sensitive=False),
    default="rpm",
)
@pass_pulp_context
@click.pass_context
def publication(ctx: click.Context, pulp_ctx: PulpContext, publication_type: str) -> None:
    if publication_type == "rpm":
        ctx.obj = PulpRpmPublicationContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option]
create_options = [
    click.option("--repository", required=True, callback=_repository_callback),
    click.option(
        "--version", type=int, help=_("a repository version number, leave blank for latest")
    ),
]

publication.add_command(list_command())
publication.add_command(show_command(decorators=lookup_options))
publication.add_command(create_command(decorators=create_options))
publication.add_command(destroy_command(decorators=lookup_options))
