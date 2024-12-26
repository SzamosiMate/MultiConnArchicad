import asyncio
from enum import Enum
from typing import Self

from multi_conn_ac.core_commands import  CoreCommands
from multi_conn_ac.basic_types import ArchiCadID, APIResponseError, ProductInfo, Port, create_object_or_error_from_response
from multi_conn_ac.archicad_connection import ArchiCADConnection

class Status(Enum):
    PENDING: str = 'pending'
    ACTIVE: str = 'active'
    FAILED: str = 'failed'
    UNASSIGNED: str = 'unassigned'

class ConnHeader:

    def __init__(self, port: Port, initialize: bool = True):
        self.port: Port = port
        self.status: Status = Status.PENDING
        self.core = CoreCommands(self.port)
        self.archicad = ArchiCADConnection(self.port)

        if initialize:
            self.ProductInfo: ProductInfo | APIResponseError = asyncio.run(self.get_product_info())
            self.ArchiCadID: ArchiCadID | APIResponseError = asyncio.run(self.get_archicad_id())

    @classmethod
    async def async_init(cls, port: Port) -> Self:
        instance = cls(port, initialize=False)
        instance.ProductInfo = await instance.get_product_info()
        instance.ArchiCadID = await instance.get_archicad_id()
        return instance

    def connect(self) -> None:
        if isinstance(self.ProductInfo, APIResponseError):
            self.ProductInfo = asyncio.run(self.get_product_info())
        if isinstance(self.ProductInfo, ProductInfo):
            self.archicad.connect(self.ProductInfo)
            self.status = Status.ACTIVE
        else:
            self.status = Status.FAILED

    def disconnect(self) -> None:
        self.archicad.disconnect()
        self.status = Status.PENDING

    def unassign(self) -> None:
        self.archicad.disconnect()
        self.status = Status.UNASSIGNED

    async def get_product_info(self) -> ProductInfo | APIResponseError:
        result = await self.core.post_command(command="API.GetProductInfo")
        return await create_object_or_error_from_response(result, ProductInfo)

    async def get_archicad_id(self) -> ArchiCadID | APIResponseError:
        result = await self.core.post_tapir_command(command='GetProjectInfo')
        return await create_object_or_error_from_response(result, ArchiCadID)

