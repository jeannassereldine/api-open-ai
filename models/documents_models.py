from typing import Annotated, List, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, model_validator
from pydantic_mongo import PydanticObjectId



# -----------------------------
# Letter of Credit (LC)
# -----------------------------
class LetterOfCredit(BaseModel):
    lc_number: str
    issue_date: datetime
    expiry_date: datetime
    place_of_expiry: str
    applicant_name: str
    applicant_address: str
    beneficiary_name: str
    beneficiary_address: str
    issuing_bank: str
    advising_bank: Optional[str]
    amount: float
    currency: str
    lc_type: str
    goods_description: str
    port_of_loading: str
    port_of_discharge: str
    latest_shipment_date: Optional[datetime]
    incoterms: Optional[str]
    documents_required: List[str]
    payment_terms: str

  

# -----------------------------
# Commercial Invoice
# -----------------------------
class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float


class CommercialInvoice(BaseModel):
    invoice_number: str
    invoice_date: datetime
    exporter_name: str
    exporter_address: str
    importer_name: str
    importer_address: str
    items: List[InvoiceItem]
    total_amount: float
    currency: str
    terms_of_payment: str
    shipment_details: Optional[str]
    incoterms: Optional[str]


# -----------------------------
# Bill of Lading
# -----------------------------
class BillOfLading(BaseModel):
    bl_number: str
    issue_date: datetime
    shipper_name: str
    shipper_address: str
    consignee_name: str
    consignee_address: str
    notify_party: Optional[str]
    port_of_loading: str
    port_of_discharge: str
    vessel_name: str
    voyage_number: str
    goods_description: str
    number_of_packages: Optional[int]
    gross_weight: Optional[float]
    freight_terms: str = "Prepaid"
    originals_issued: Optional[int]

   

# -----------------------------
# Certificate of Origin
# -----------------------------
class CertificateOfOrigin(BaseModel):
    certificate_number: str
    issue_date: datetime
    exporter_name: str
    exporter_address: str
    consignee_name: str
    consignee_address: str
    goods_description: str
    origin_country: str
    authorized_signature: Optional[str]
    issuing_chamber: Optional[str]

# -----------------------------
# Documents Model
# -----------------------------
class DocumentsModel(BaseModel):
    id: Optional[PydanticObjectId] = None
    letter_of_credit: LetterOfCredit
    commercial_invoice: CommercialInvoice
    bill_of_lading: BillOfLading
    certificate_of_origin: CertificateOfOrigin
    images: Optional[List[str]] = Field(default_factory=list)