# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument("source_path", type=click.Path(exists=True))
@click.argument("external_path", type=click.Path(exists=True))
@click.argument("processed_path", type=click.Path())
def main(source_path, external_path, processed_path):
    """Runs data processing scripts to turn source data into
    processed data ready to be analyzed.
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    project_dir = Path(__file__).resolve().parents[2]
    load_dotenv(find_dotenv())

    main()
