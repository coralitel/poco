from .abstract_command import AbstractCommand
from ..services.command_handler import CommandHandler
from ..services.file_utils import FileUtils
from ..services.console_logger import ColorPrint
from ..services.state import StateHolder
from ..services.state_utils import StateUtils
from ..services.yaml_utils import YamlUtils
from ..services.environment_utils import EnvironmentUtils


class RepoRemove(AbstractCommand):

    sub_command = "repo"
    command = ["remove", "rm"]
    args = ["[<name>]"]
    args_descriptions = {"[<name>]": "Name of the repository."}
    description = "Remove repository from local config."

    def prepare_states(self):
        StateHolder.name = FileUtils.get_parameter_or_directory_name('<name>')
        StateUtils.prepare("compose_handler")

    def resolve_dependencies(self):
        if StateHolder.poco_file is not None and StateHolder.compose_handler.have_script("remove_script"):
            EnvironmentUtils.check_docker()

    def execute(self):
        if StateHolder.poco_file is not None and StateHolder.compose_handler.have_script("remove_script"):
            CommandHandler().run_script("remove_script")
        RepoRemove.remove()

    @staticmethod
    def remove():
        catalog = StateHolder.args.get('<name>')
        if catalog not in list(StateHolder.config.keys()):
            ColorPrint.exit_after_print_messages(message="Catalog not exists with name: " + catalog)
        del StateHolder.config[catalog]
        YamlUtils.write(file=StateHolder.catalog_config_file, data=StateHolder.config)