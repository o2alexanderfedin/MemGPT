# import typer
#
# typer.secho(
#     "Command `python main.py` no longer supported. Please run `memgpt run`. See https://memgpt.readthedocs.io/en/latest/quickstart/.",
#     fg=typer.colors.YELLOW,
# )


def main_app():
    from memgpt.main import app
    app()


if __name__ == "__main__":
    main_app()