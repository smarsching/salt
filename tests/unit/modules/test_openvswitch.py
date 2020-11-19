import salt.modules.openvswitch as openvswitch
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.mock import MagicMock, patch
from tests.support.unit import TestCase


class OpenVSwitchTestCase(TestCase, LoaderModuleMockMixin):
    """
    Test cases for salt.modules.openvswitch.
    """

    def setup_loader_modules(self):
        return {openvswitch: {}}

    def test_bridge_create(self):
        """
        Test bridge_create function.
        """
        mock = MagicMock(return_value={"retcode": 0})
        with patch.dict(
            openvswitch.__salt__, {"cmd.run_all": mock},
        ):
            self.assertTrue(openvswitch.bridge_create("br0", False))
            mock.assert_called_with("ovs-vsctl add-br br0")
            self.assertTrue(openvswitch.bridge_create("br1", True))
            mock.assert_called_with("ovs-vsctl --may-exist add-br br1")
            self.assertTrue(openvswitch.bridge_create("br2", False, "br0", 42))
            mock.assert_called_with("ovs-vsctl add-br br2 br0 42")

    def test_bridge_to_parent(self):
        """
        Test bridge_to_parent function.
        """
        mock = MagicMock(return_value={"retcode": 0, "stdout": "br0\n"})
        with patch.dict(
            openvswitch.__salt__, {"cmd.run_all": mock},
        ):
            self.assertEqual(openvswitch.bridge_to_parent("br1"), "br0")
            mock.assert_called_with("ovs-vsctl br-to-parent br1")

    def test_bridge_to_vlan(self):
        """
        Test bridge_to_vlan function.
        """
        mock = MagicMock(return_value={"retcode": 0, "stdout": "42\n"})
        with patch.dict(
            openvswitch.__salt__, {"cmd.run_all": mock},
        ):
            self.assertEqual(openvswitch.bridge_to_vlan("br0"), 42)
            mock.assert_called_with("ovs-vsctl br-to-vlan br0")

    def test_db_get(self):
        """
        Test db_get function.
        """
        mock = MagicMock(
            return_value={
                "retcode": 0,
                "stdout": '{"data":[["01:02:03:04:05:06"]],' '"headings":["mac"]}',
            }
        )
        with patch.dict(
            openvswitch.__salt__, {"cmd.run_all": mock},
        ):
            self.assertEqual(
                openvswitch.db_get("Interface", "br0", "mac"), "01:02:03:04:05:06"
            )
            mock.assert_called_with(
                [
                    "ovs-vsctl",
                    "--format=json",
                    "--columns=mac",
                    "list",
                    "Interface",
                    "br0",
                ]
            )

    def test_db_set(self):
        """
        Test db_set function.
        """
        mock = MagicMock(return_value={"retcode": 0})
        with patch.dict(
            openvswitch.__salt__, {"cmd.run_all": mock},
        ):
            openvswitch.db_set("Interface", "br0", "mac", "01:02:03:04:05:06")
            mock.assert_called_with(
                ["ovs-vsctl", "set", "Interface", "br0", 'mac="01:02:03:04:05:06"']
            )
