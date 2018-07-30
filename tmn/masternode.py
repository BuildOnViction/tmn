import docker as dockerpy


class Masternode:
    """
    Manage the docker masternode stack.
    """

    def __init__(self):
        self.client = dockerpy.from_env()

    def ping(self):
        """
        Try to ping the Docker deamon. Check if accessible.

        :returns: is Docker running
        :rtype: bool
        """
        try:
            return self.client.ping()
        except Exception:
            return False
