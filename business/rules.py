from datetime import  datetime, timezone
from typing import List
from pydantic import BaseModel
from models.documents_models import DocumentsModel


class LCValidationResult(BaseModel):
    is_compliant: bool
    reasons: List[str]


def validate_letter_of_credit(documents: DocumentsModel) -> LCValidationResult:
    lc = documents.letter_of_credit
    invoice = documents.commercial_invoice
    bl = documents.bill_of_lading
    coo = documents.certificate_of_origin

    reasons = []
    print('Validating Letter of Credit against documents...')
    # --- Rule 1: Invoice amount must match LC amount ---
    if abs(invoice.total_amount - lc.amount) > 0.01:  # allow small rounding diff
        reasons.append(
            f"Invoice amount ({invoice.total_amount} {invoice.currency}) "
            f"differs from LC amount ({lc.amount} {lc.currency})."
        )
        print('Amount mismatch reason added:')
        print(reasons)

    # --- Rule 2: LC must not be expired ---
    today = datetime.now(timezone.utc)
    if lc.expiry_date < today:
        reasons.append(f"LC expired on {lc.expiry_date}, today is {today}.")

    # --- Rule 3: Currency must match ---
    if invoice.currency != lc.currency:
        reasons.append(f"Currency mismatch: LC uses {lc.currency}, invoice uses {invoice.currency}.")

    # # --- Rule 4: Goods description must match (simple containment check) ---
    # if lc.goods_description.lower() not in invoice.items[0].description.lower():
    #     reasons.append("Goods description in invoice does not match LC description.")

    # --- Rule 5: Port of loading/discharge must match with Bill of Lading ---
    if lc.port_of_loading.lower() != bl.port_of_loading.lower():
        reasons.append("Port of loading in Bill of Lading does not match LC.")
    if lc.port_of_discharge.lower() != bl.port_of_discharge.lower():
        reasons.append("Port of discharge in Bill of Lading does not match LC.")

    # --- Rule 6: Beneficiary/exporter name consistency ---
    if lc.beneficiary_name.lower() != invoice.exporter_name.lower():
        reasons.append("Exporter name in invoice does not match LC beneficiary.")

    # --- Rule 7: Applicant/importer name consistency ---
    if lc.applicant_name.lower() != invoice.importer_name.lower():
        reasons.append("Importer name in invoice does not match LC applicant.")

    # --- Rule 8: Country of origin must be consistent with LC goods origin expectation ---
    # (if LC required COO)
    if "Certificate of Origin" in lc.documents_required:
        if coo.goods_description.lower() not in lc.goods_description.lower():
            reasons.append("Certificate of Origin goods description differs from LC.")
    
    return LCValidationResult(
        is_compliant=len(reasons) == 0,
        reasons=reasons
    )
