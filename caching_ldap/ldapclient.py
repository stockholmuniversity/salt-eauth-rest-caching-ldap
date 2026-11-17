"""
LDAP client module for connecting, searching, and managing LDAP entries.
"""

import logging
import ssl

from ldap3 import Connection, Server, Tls

logger = logging.getLogger(__name__ + ".ldap_client")


class LdapClient:
    """
    LDAP client to connect, disconnect, and search for users in an LDAP directory.
    """

    def __init__(self) -> None:
        self.server = None
        self.conn = None

    def connect(self, server: str, port: int = 636) -> None:
        """Explicitly bind connection."""
        if self.conn is None or not self.conn.bound:
            logger.info("Binding LDAP connection to %s", server)
            self.server = Server(
                server,
                port=port,
                use_ssl=True,
                tls=Tls(validate=ssl.CERT_REQUIRED)
            )
            self.conn = Connection(self.server, auto_bind=True)

    def disconnect(self) -> None:
        """Explicitly unbind connection."""
        if self.conn and self.conn.bound:
            logger.info("Unbinding LDAP connection")
            self.conn.unbind()
        self.conn = None

    def search_groups(
        self, search_base: str, search_filter: str, attributes: list[str] | None = None
    ) -> dict[str, list[str]]:
        """Search for entries in the LDAP directory."""
        if not self.conn or not self.conn.bound:
            raise RuntimeError("LDAP connection is not bound")
        self.conn.search(
            search_base,
            search_filter,
            attributes=attributes if attributes else ["cn", "uniqueMember"],
        )

        user_groups = {}
        for entries in self.conn.entries:
            group = getattr(entries, "cn", None)
            users = getattr(entries, "uniqueMember", None)
            if users:
                for user in users:
                    user_dn = str(user)
                    user_uid = user_dn.split(",")[0].split("=")[1]
                    if user_uid not in user_groups:
                        user_groups[user_uid] = []
                    user_groups[user_uid].append(str(group))

        return user_groups
