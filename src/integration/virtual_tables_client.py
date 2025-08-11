"""
Virtual tables client.

This module provides a simple client to interact with a virtual data
integration layer (such as Palantir AIP Virtual Tables). It is
designed as a stub for demonstration and unit testing in the
``physical-digital-alignment`` project. In a production setting,
the client would include authentication and query methods to
connect to a real data platform and retrieve data on demand.

Example
-------
The following illustrates how a developer might use the stub
client in their code::

    from integration.virtual_tables_client import VirtualTablesClient

    client = VirtualTablesClient(connection_info={"api_key": "my-key"})
    data = client.query("orders", limit=50)
    # Do something with the retrieved data

Currently, the ``query`` method simply raises a ``NotImplementedError``
to signal that it should be extended for real-world use.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class VirtualTablesClient:
    """A stub client for virtual table integration.

    Parameters
    ----------
    connection_info : Optional[dict], optional
        A dictionary containing connection parameters such as API keys
        or endpoint URLs. Defaults to ``None``.

    Notes
    -----
    This class is intentionally minimal. It provides a clear interface
    for how one might connect to an external data platform in the
    future without committing to a particular implementation in this
    research prototype. Developers can subclass or replace this
    implementation with one that uses an SDK or REST API.
    """

    def __init__(self, connection_info: Optional[Dict[str, Any]] = None) -> None:
        self.connection_info = connection_info or {}

    def query(self, table_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve rows from a virtual table.

        Parameters
        ----------
        table_name : str
            The name of the table to query.
        limit : int, optional
            The maximum number of rows to retrieve, by default 100.

        Returns
        -------
        List[Dict[str, Any]]
            A list of records represented as dictionaries.

        Raises
        ------
        NotImplementedError
            Always raised in this stub implementation.
        """
        raise NotImplementedError(
            "VirtualTablesClient.query is a stub. Provide an implementation "
            "that connects to your data platform to retrieve data."
        )
