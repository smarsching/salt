import salt.states.openvswitch_bridge as openvswitch_bridge
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.mock import MagicMock, patch
from tests.support.unit import TestCase


class OpenVSwitchBridgeTestCase(TestCase, LoaderModuleMockMixin):
    """
    Test cases for salt.states.openvswitch_bridge.
    """

    def setup_loader_modules(self):
        return {openvswitch_bridge: {"__opts__": {"test": False}}}

    def test_present(self):
        """
        Test present function.
        """
        # Test bridge without parent already existing.
        create_mock = MagicMock()
        exists_mock = MagicMock(return_value=True)
        to_parent_mock = MagicMock(return_value="br0")
        to_vlan_mock = MagicMock(return_value=0)
        with patch.dict(
            openvswitch_bridge.__salt__,
            {
                "openvswitch.bridge_create": create_mock,
                "openvswitch.bridge_exists": exists_mock,
                "openvswitch.bridge_to_parent": to_parent_mock,
                "openvswitch.bridge_to_vlan": to_vlan_mock,
            },
        ):
            ret = openvswitch_bridge.present(name="br0")
            create_mock.assert_not_called()
            self.assertTrue(ret["result"])
        # Test bridge without parent not existing yet.
        create_mock = MagicMock(return_value=True)
        exists_mock = MagicMock(return_value=False)
        with patch.dict(
            openvswitch_bridge.__salt__,
            {
                "openvswitch.bridge_create": create_mock,
                "openvswitch.bridge_exists": exists_mock,
            },
        ):
            ret = openvswitch_bridge.present(name="br0")
            create_mock.assert_called_with("br0", parent=None, vlan=None)
            self.assertTrue(ret["result"])
            self.assertTrue(ret["changes"])
        # Test bridge already existing with parent already existing.
        create_mock = MagicMock()
        exists_mock = MagicMock(return_value=True)
        to_parent_mock = MagicMock(return_value="br0")
        to_vlan_mock = MagicMock(return_value=42)
        with patch.dict(
            openvswitch_bridge.__salt__,
            {
                "openvswitch.bridge_create": create_mock,
                "openvswitch.bridge_exists": exists_mock,
                "openvswitch.bridge_to_parent": to_parent_mock,
                "openvswitch.bridge_to_vlan": to_vlan_mock,
            },
        ):
            # Bridge exists, but parent and VLAN do not match, so we expect a
            # result of False.
            ret = openvswitch_bridge.present(name="br1")
            create_mock.assert_not_called()
            self.assertFalse(ret["result"])
            # Bridge exists and parent VLAN matches
            ret = openvswitch_bridge.present(name="br1", parent="br0", vlan=42)
            create_mock.assert_not_called()
            self.assertTrue(ret["result"])
        # Test bridge without parent not existing yet.
        create_mock = MagicMock(return_value=True)
        exists_mock = MagicMock(return_value=False)
        with patch.dict(
            openvswitch_bridge.__salt__,
            {
                "openvswitch.bridge_create": create_mock,
                "openvswitch.bridge_exists": exists_mock,
            },
        ):
            ret = openvswitch_bridge.present(name="br1", parent="br0", vlan=42)
            create_mock.assert_called_with("br1", parent="br0", vlan=42)
            self.assertTrue(ret["result"])
            self.assertTrue(ret["changes"])
