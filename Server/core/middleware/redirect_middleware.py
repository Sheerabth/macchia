from fastapi import Path
from core.sync.messaging import get_host
from uuid import UUID
from config import Config
from typing import Optional, Tuple


async def redirect_middleware(file_id: UUID = Path(...)) -> Optional[Tuple]:
    node_id = str(int(file_id.hex, 16) % Config.TOTAL_NODES)

    print("Node ID: ", node_id)

    if node_id != Config.NODE_ID:
        return get_host(node_id).split(':')

    # redirect not needed
    return None


