"""
LDAP client module for connecting, searching, and managing LDAP entries.
"""

import logging
import ssl

from ldap3 import Connection, Server, Tls

logger = logging.getLogger(__name__)


def search_groups(
    server: str,
    search_base: str,
    search_filter: str,
    port: int = 636,
    attributes: list[str] | None = None,
) -> dict[str, list[str]]:
    """Search the LDAP directory for groups and their members."""
    logger.info("Binding LDAP connection to %s", server)
    ldap_server = Server(
        server, port=port, use_ssl=True, tls=Tls(validate=ssl.CERT_REQUIRED)
    )
    conn = Connection(ldap_server, auto_bind=True)
    try:
        conn.search(
            search_base,
            search_filter,
            attributes=attributes if attributes else ["cn", "uniqueMember"],
        )

        user_groups: dict[str, list[str]] = {}
        for entry in conn.entries:
            group = getattr(entry, "cn", None)
            users = getattr(entry, "uniqueMember", None)
            if users:
                for user in users:
                    user_dn = str(user)
                    user_uid = user_dn.split(",", maxsplit=1)[0].split("=")[1]
                    if user_uid not in user_groups:
                        user_groups[user_uid] = []
                    user_groups[user_uid].append(str(group))

        return user_groups
    finally:
        if conn.bound:
            logger.info("Unbinding LDAP connection")
            conn.unbind()
