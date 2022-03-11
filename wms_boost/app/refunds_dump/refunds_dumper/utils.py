from app.wms_api.models import ProductsInfo
from .dump_formatter import RefundDict


def insert_barcodes(
        refunds: List[RefundDict],
        products_info: ProductsInfo,
        sku_ids: Dict[int, RefundDict]
) -> None:
    """ Insert barcode from `products_info` to refund from `refunds`
        with corresponding sku_id """
    for item in products_info.iter_items():
        refund = sku_ids.get(item.sku_id)
        refund['barcode'] = item.barcode


def barcode_required(refund: RefundDict) -> bool:
    # barcode required if there is exactly one position in order
    return len(refund['itemList']) == 1
