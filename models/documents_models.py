from typing import Annotated, List, Optional, Union
from datetime import date, datetime
import uuid
from pydantic import BaseModel, Field

# -----------------------------
# Letter of Credit (LC)
# -----------------------------
class LetterOfCredit(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    lc_number: Annotated[str, Field(description="Unique LC number")]
    issue_date: Annotated[datetime, Field(description="LC issue date")]
    expiry_date: Annotated[datetime, Field(description="LC expiry date, exemple: 2023-12-31")]
    place_of_expiry: Annotated[str, Field(description="Place of expiry")]
    applicant_name: Annotated[str, Field(description="Importer name")]
    applicant_address: Annotated[str, Field(description="Importer address")]
    beneficiary_name: Annotated[str, Field(description="Exporter name")]
    beneficiary_address: Annotated[str, Field(description="Exporter address")]
    issuing_bank: Annotated[str, Field(description="Issuing bank")]
    advising_bank: Optional[Annotated[str, Field(description="Advising bank")]]
    amount: Annotated[float, Field(description="LC amount")]
    currency: Annotated[str, Field(description="Currency code")]
    lc_type: Annotated[str, Field(description="e.g., Irrevocable, At Sight")]
    goods_description: Annotated[str, Field(description="Description of goods")]
    port_of_loading: Annotated[str, Field(description="Port of loading")]
    port_of_discharge: Annotated[str, Field(description="Port of discharge")]
    latest_shipment_date: Optional[Annotated[datetime, Field(description="Latest shipment date")]]
    incoterms: Optional[Annotated[str, Field(description="Incoterms")]]
    documents_required: Annotated[List[str], Field(description="List of required documents")]
    payment_terms: Annotated[str, Field(description="Payment terms")]
  

# -----------------------------
# Commercial Invoice
# -----------------------------
class InvoiceItem(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    description: Annotated[str, Field(description="Item description")]
    quantity: Annotated[float, Field(description="Quantity shipped")]
    unit_price: Annotated[float, Field(description="Unit price")]
    total: Annotated[float, Field(description="Total price")]
   

class CommercialInvoice(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    invoice_number: Annotated[str, Field(description="Invoice number")]
    invoice_date: Annotated[datetime, Field(description="Invoice date")]
    exporter_name: Annotated[str, Field(description="Exporter name")]
    exporter_address: Annotated[str, Field(description="Exporter address")]
    importer_name: Annotated[str, Field(description="Importer name")]
    importer_address: Annotated[str, Field(description="Importer address")]
    items: Annotated[List[InvoiceItem], Field(description="List of invoice items")]
    total_amount: Annotated[float, Field(description="Total invoice amount")]
    currency: Annotated[str, Field(description="Currency code")]
    terms_of_payment: Annotated[str, Field(description="Payment terms")]
    shipment_details: Optional[Annotated[str, Field(description="Shipment details")]]
    incoterms: Optional[Annotated[str, Field(description="Incoterms")]]
   

# -----------------------------
# Bill of Lading
# -----------------------------
class BillOfLading(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    bl_number: Annotated[str, Field(description="Bill of Lading number")]
    issue_date: Annotated[datetime, Field(description="Issue date")]
    shipper_name: Annotated[str, Field(description="Shipper name")]
    shipper_address: Annotated[str, Field(description="Shipper address")]
    consignee_name: Annotated[str, Field(description="Consignee name")]
    consignee_address: Annotated[str, Field(description="Consignee address")]
    notify_party: Optional[Annotated[str, Field(description="Notify party")]]
    port_of_loading: Annotated[str, Field(description="Port of loading")]
    port_of_discharge: Annotated[str, Field(description="Port of discharge")]
    vessel_name: Annotated[str, Field(description="Vessel name")]
    voyage_number: Annotated[str, Field(description="Voyage number")]
    goods_description: Annotated[str, Field(description="Description of goods")]
    number_of_packages: Optional[Annotated[int, Field(description="Number of packages")]]
    gross_weight: Optional[Annotated[float, Field(description="Gross weight in kg")]]
    freight_terms: Annotated[str, Field(description="Freight terms, e.g., prepaid or collect", default="Prepaid")]
    originals_issued: Optional[Annotated[int, Field(description="Number of original B/L issued")]]
    

# -----------------------------
# Certificate of Origin
# -----------------------------
class CertificateOfOrigin(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    certificate_number: Annotated[str, Field(description="Certificate number")]
    issue_date: Annotated[datetime, Field(description="Date of issue")]
    exporter_name: Annotated[str, Field(description="Exporter name")]
    exporter_address: Annotated[str, Field(description="Exporter address")]
    consignee_name: Annotated[str, Field(description="Consignee name")]
    consignee_address: Annotated[str, Field(description="Consignee address")]
    goods_description: Annotated[str, Field(description="Description of goods")]
    origin_country: Annotated[str, Field(description="Country of origin")]
    authorized_signature: Optional[Annotated[str, Field(description="Authorized signature")]]
    issuing_chamber: Optional[Annotated[str, Field(description="Issuing Chamber of Commerce")]]
    
 

class DocumentsModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    letter_of_credit: LetterOfCredit
    commercial_invoice: CommercialInvoice
    bill_of_lading: BillOfLading
    certificate_of_origin: CertificateOfOrigin
    images: Optional[List[str]] = Field(default_factory=lambda: [])