from .start import Start
from ..services.state_utils import StateUtils
from ..services.state import StateHolder
from ..services.package_handler import PackageHandler
from ..services.file_utils import FileUtils


class Unpack(Start):

    command = "unpack"
    args = ["[<name>]"]
    args_descriptions = {"[<name>]": "Name of the project in the catalog."}
    description = "Unpack archive, install images to local repository."

    def prepare_states(self):
        StateHolder.name = FileUtils.get_parameter_or_directory_name('<name>')
        StateUtils.prepare("compose_handler")

    def execute(self):
        PackageHandler().unpack()
