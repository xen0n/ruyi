import pytest

from ruyi.log import RuyiLogger
from ruyi.pluginhost.ctx import PluginHostContext

from ..fixtures import RuyiFileFixtureFactory


@pytest.mark.xfail(
    reason="unsandboxed backend does not support freezing yet",
    strict=True,
)
def test_lang_frozen_values(
    ruyi_file: RuyiFileFixtureFactory,
    ruyi_logger: RuyiLogger,
) -> None:
    with ruyi_file.plugin_suite("lang_tests") as plugin_root:
        phctx = PluginHostContext.new(ruyi_logger, plugin_root)
        # Should fail because in the test plugin we're trying to append to a
        # frozen list.
        with pytest.raises(RuntimeError):
            phctx.get_from_plugin("frozen_values", "val")


@pytest.mark.xfail(
    reason="unsandboxed backend is literally unsandboxed",
    strict=True,
)
def test_lang_trivial_sandbox_escape(
    ruyi_file: RuyiFileFixtureFactory,
    ruyi_logger: RuyiLogger,
) -> None:
    with ruyi_file.plugin_suite("lang_tests") as plugin_root:
        phctx = PluginHostContext.new(ruyi_logger, plugin_root)
        with pytest.raises(RuntimeError):
            phctx.get_from_plugin("trivial_sandbox_escape", "real_builtins")
