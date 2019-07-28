#!/usr/bin/python3


class Fang():
    """
    This is a simple class for the refang / defang methods
    """

    @staticmethod
    def defang(url, parameters):
        """
        This defangs the request.
        :param url: String. The Url passed to us before ?
        :param parameters: String. This is any parameters in the URl.
        :returns: String. The full defanged url.
        """
        # build the full string: url?parameters
        result = url.lower() + "?" + parameters.lower()

        # defang it. Replace http with hxxp and . with [.]
        return result.replace("http://", "hxxp://").replace(".", "[.]")

    @staticmethod
    def refang(url, parameters):
        """
        This refangs the request.
        :param url: String. The URL passed to us before?
        :param parameters: String. This is any parameters in the URL
        :returns: String. The full refanged url
        """
        # rebuild the full url then refang it.
        result = url.lower() + "?" + parameters.lower()
        return result.replace("hxxp://", "http://").replace("[.]", ".")
