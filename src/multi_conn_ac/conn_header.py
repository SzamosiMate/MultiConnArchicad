import asyncio
from enum import Enum
from typing import Self, Any

from multi_conn_ac.core_commands import  CoreCommands
from multi_conn_ac.basic_types import ArchiCadID, APIResponseError, ProductInfo, Port, create_object_or_error_from_response, \
    ArchicadLocation
from multi_conn_ac.standard_connection import StandardConnection

class Status(Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    FAILED=  'failed'
    UNASSIGNED = 'unassigned'

class ConnHeader:

    def __init__(self, port: Port, initialize: bool = True):
        self.port: Port = port
        self.status: Status = Status.PENDING
        self.core: CoreCommands = CoreCommands(self.port)
        self.standard: StandardConnection = StandardConnection(self.port)

        if initialize:
            self.product_info: ProductInfo | APIResponseError = asyncio.run(self.get_product_info())
            self.archicad_id: ArchiCadID | APIResponseError = asyncio.run(self.get_archicad_id())
            self.archicad_location: ArchicadLocation | APIResponseError = asyncio.run(self.get_archicad_location())

    @classmethod
    async def async_init(cls, port: Port) -> Self:
        instance = cls(port, initialize=False)
        instance.product_info = await instance.get_product_info()
        instance.archicad_id = await instance.get_archicad_id()
        instance.archicad_location = await instance.get_archicad_location()
        return instance

    def connect(self) -> None:
        if self.is_product_info_initialized():
            self.standard.connect(self.product_info)
            self.status = Status.ACTIVE
        else:
            self.status = Status.FAILED

    def disconnect(self) -> None:
        self.standard.disconnect()
        self.status = Status.PENDING

    def unassign(self) -> None:
        self.standard.disconnect()
        self.status = Status.UNASSIGNED

    def is_fully_initialized(self) -> bool:
        return self.is_product_info_initialized() and self.is_id_and_location_initialized()

    def is_product_info_initialized(self) -> bool:
        return isinstance(self.product_info, ProductInfo)

    def is_id_and_location_initialized(self) -> bool:
        return isinstance(self.archicad_id, ArchiCadID) and isinstance(self.archicad_location, ArchicadLocation)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ConnHeader):
            if self.is_fully_initialized() and other.is_fully_initialized():
                if (self.product_info == other.product_info and
                    self.archicad_id == other.archicad_id and
                    self.archicad_location == other.archicad_location):
                    return True
        return False

    async def get_product_info(self) -> ProductInfo | APIResponseError:
        result = await self.core.post_command(command="API.GetProductInfo")
        return await create_object_or_error_from_response(result, ProductInfo)

    async def get_archicad_id(self) -> ArchiCadID | APIResponseError:
        result = await self.core.post_tapir_command(command='GetProjectInfo')
        return await create_object_or_error_from_response(result, ArchiCadID)

    async def get_archicad_location(self) -> ArchicadLocation | APIResponseError:
        result = await self.core.post_tapir_command(command='GetArchicadLocation')
        return await create_object_or_error_from_response(result, ArchicadLocation)
