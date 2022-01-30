import typer


def echo_success(message: str) -> None:
    styled_message = typer.style(message, fg=typer.colors.GREEN, bold=True)
    typer.echo(styled_message)


def echo_error(message: str) -> None:
    styled_message = typer.style(message, fg=typer.colors.RED, bold=True)
    typer.echo(styled_message)
