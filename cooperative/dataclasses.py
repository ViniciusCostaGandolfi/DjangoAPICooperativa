from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BaseData:
    adress: str = 'R. Domingos Rodrigues, 420 - Lapa'
    adress_complement: str = ''
    latitude: float = -23.5219926
    longitude: float = -46.7076168


@dataclass
class DriverData:
    name: str
    itens_list: str
    adress: Optional[str] = None
    adress_complement: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class OrderData:
    name: str
    itens: str
    adress: str
    # volume: float
    phone: str
    adress_complement: str
    latitude: float
    longitude: float


@dataclass
class RouteData:
    orders: List[OrderData]
    driver: DriverData
    base: BaseData = BaseData()
    sorted_route_indexes: Optional[List[int]] = None
    use_longest_point: bool = False
    text_route: str = ''
    google_maps_link: str = ''