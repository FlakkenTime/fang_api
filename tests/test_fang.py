#!/usr/bin/python3

import pytest
from src.fang import Fang


class TestLookup(object):

    def setup(self):
        """
        Not needed
        """
        pass

    def test_basic_url(self):
        """
        test a simple url
        """
        start = "http://test.com"
        expected = "hxxp://test[.]com"
        result = Fang.defang(start, '')
        assert result == expected

        result = Fang.refang(result, '')
        assert result == start

    def test_url_mixed_caps(self):
        """
        Test a URL with mixed capitals into protocol
        """
        start = "HTtP://this.is.a.test.com"
        expected = "hxxp://this[.]is[.]a[.]test[.]com"

        result = Fang.defang(start, '')
        assert result == expected

        result = Fang.refang(result, '')
        assert result == start.lower()

    def test_with_simple_parameters(self):
        """
        Test a URL with extra parameters
        """
        start_url = "http://test.com"
        params = "first=1&second=2"
        expected = "hxxp://test[.]com?first=1&second=2"

        result = Fang.defang(start_url, params)
        assert result == expected

        result = Fang.refang(result.split('?')[0], result.split('?')[1])
        assert result == "%s?%s" % (start_url, params)

    def test_with_url_in_params(self):
        """
        Test a URL with parameters that need to be defanged
        """
        start_url = "http:test.com"
        params = "test=http://bob.com"
        expected = "hxxp:test[.]com?test=hxxp://bob[.]com"

        result = Fang.defang(start_url, params)
        assert result == expected

        result = Fang.refang(result.split('?')[0], result.split('?')[1])
        assert result == "%s?%s" % (start_url, params)
