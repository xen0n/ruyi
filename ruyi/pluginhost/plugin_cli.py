import argparse

from ..config import GlobalConfig
from ..ruyipkg.repo import MetadataRepo


def cli_admin_run_plugin_cmd(gc: GlobalConfig, args: argparse.Namespace) -> int:
    cmd_name = args.cmd_name
    cmd_args = args.cmd_args

    mr = MetadataRepo(gc)
    return mr.run_plugin_cmd(cmd_name, cmd_args)
