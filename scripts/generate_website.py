import argparse
import codecs
import logging
import os
import sys

from gorgon import builder
from gorgon import json_parser

parser = argparse.ArgumentParser(description='Rebuild the Gorgon Parsing website.')
parser.add_argument('version', type=int,
                    help='Version of the the accumulator')
parser.add_argument('version_output_directory', type=str,
                    help='Directory to store the website for this version')
parser.add_argument('--override', type=bool, default=True,
                    help='Override the target directory')
parser.add_argument('--dry', action="store_true",
                    help="Don't write anything, just try generating.")
parser.add_argument('--console', action="store_true",
                    help="Spawn an IPython console after parsing. For easier debugging.")
parser.add_argument('--assets', default="index,items,powers,skills,abilities,recipes,tooltips",
                    help="Which assets to rebuild.")
args = parser.parse_args()
args.assets = args.assets.split(",")


def Output(filename, data):
    if not args.dry:
        codecs.open(os.path.join(args.version_output_directory, filename),
                    "wb", encoding="utf-8").write(data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    try:
        version = args.version
        parser = json_parser.GorgonJsonParser(version)
        parser.Parse("data/")
        reporter = builder.Builder(parser)

        if args.console:
            from IPython import embed; embed()

        if not args.dry:
            try:
                os.makedirs(args.version_output_directory)
            except OSError:
                pass

        if "index" in args.assets:
            Output("index.html", reporter.IndexReport())
        if "items" in args.assets:
            Output("items.html", reporter.ItemsReport())
        if "powers" in args.assets:
            Output("powers.html", reporter.PowersReport())
        if "abilities" in args.assets:
            Output("abilities.html", reporter.AbilitiesReport())
        if "recipes" in args.assets:
            Output("recipes.html", reporter.RecipesReport())
        if not args.dry and "skills" in args.assets:
            reporter.DumpSkills(os.path.join(args.version_output_directory, "skills/"))

        if not args.dry and "tooltips" in args.assets:
            reporter.DumpItems(os.path.join(args.version_output_directory, "items/"))

        version = args.version

    except Exception:
        import pdb; pdb.post_mortem(sys.exc_info()[2])
        raise
