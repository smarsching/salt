import salt.states.openvswitch_db as openvswitch_db
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.mock import MagicMock, patch
from tests.support.unit import TestCase


class OpenVSwitchDBTestCase(TestCase, LoaderModuleMockMixin):
    """
    Test cases for salt.states.openvswitch_db.
    """

    def setup_loader_modules(self):
        return {openvswitch_db: {"__opts__": {"test": False}}}

    def test_managed(self):
        """
        Test managed function.
        """
        get_mock = MagicMock(return_value="01:02:03:04:05:06")
        set_mock = MagicMock(return_value=None)
        with patch.dict(
            openvswitch_db.__salt__,
            {"openvswitch.db_get": get_mock, "openvswitch.db_set": set_mock},
        ):
            ret = openvswitch_db.managed(
                name="br0", table="Interface", data={"mac": "01:02:03:04:05:06"}
            )
            set_mock.assert_not_called()
            self.assertTrue(ret["result"])
            self.assertTrue("changes" not in ret or not ret["changes"])
            ret = openvswitch_db.managed(
                name="br0", table="Interface", data={"mac": "01:02:03:04:05:07"}
            )
            set_mock.assert_called_with("Interface", "br0", "mac", "01:02:03:04:05:07")
            self.assertTrue(ret["result"])
            self.assertEqual(
                ret["changes"],
                {"mac": {"old": "01:02:03:04:05:06", "new": "01:02:03:04:05:07"}},
            )
