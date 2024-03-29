import argparse
import json
import sys
from pathlib import Path

__author__ = "Thomas @takluyver Kluyver"
__licese__ = "BSD-3-Clause"

from IPython.utils.tempdir import TemporaryDirectory
from jupyter_client.kernelspec import KernelSpecManager

kernel_json = {
	"argv": [sys.executable, "-m", "iTTS", "-f", "{connection_file}"],
	"display_name": "iTTS",
	"language": "plain",
	"codemirror_mode": None
}


def install_my_kernel_spec(user=True, prefix=None):
	with TemporaryDirectory() as td:
		td = Path(td)
		td.chmod(0o755)
		with (Path(td) / "kernel.json").open("wt", encoding="utf-8") as f:
			json.dump(kernel_json, f, sort_keys=True, indent="\t")
		# TODO: Copy resources once they're specified

		print("Installing IPython kernel spec")
		m = KernelSpecManager()
		if user:
			m.install_kernel_spec(str(td), "iTTS", user=user)
		elif prefix:
			m.install_kernel_spec(str(td), "iTTS", prefix=str(prefix))
		else:
			return 1


def _is_root():
	try:
		return os.geteuid() == 0
	except AttributeError:
		return False  # assume not an admin on non-Unix platforms


def main(argv=None):
	parser = argparse.ArgumentParser(description="Install KernelSpec for Bash Kernel")
	prefix_locations = parser.add_mutually_exclusive_group()

	prefix_locations.add_argument("--user", help="Install KernelSpec in user homedirectory", action="store_true")
	prefix_locations.add_argument("--sys-prefix", help="Install KernelSpec in sys.prefix. Useful in conda / virtualenv", action="store_true", dest="sys_prefix")
	prefix_locations.add_argument("--prefix", help="Install KernelSpec in this prefix", default=None)

	args = parser.parse_args(argv)

	user = False
	prefix = None
	if args.sys_prefix:
		prefix = sys.prefix
	elif args.prefix:
		prefix = args.prefix
	elif args.user or not _is_root():
		user = True

	sys.exit(install_my_kernel_spec(user=user, prefix=prefix))


if __name__ == "__main__":
	main()
