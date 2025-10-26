from typing import List
from models.chat_models import AnalyseLCRequest
from tools.tools import pdf_base64_to_images_base64

def prepare_messages(request: AnalyseLCRequest, system_instruction: str) ->tuple[List[dict], List[str]]:
    """
    Convert AnalyseLCRequest messages into a list of dicts ready for the client.
    """
    prepared_messages = []
    images = []
    for img in request.images:
        url = img.image_url_base64
        image_data = url.split(",")[1] if "," in url else url
        images.append(image_data)
        prepared_messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source_type": "base64",
                        "data": image_data,
                        "mime_type": "image/jpeg",
                    },
                ],
            }
        )

    for doc in request.documents:
        pdf_base64 = doc.file_data_base64
        temp_images = pdf_base64_to_images_base64(pdf_base64)
        images.extend(temp_images) 
        prepared_messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source_type": "base64",
                        "data": image,
                        "mime_type": "image/jpeg",
                    }
                    for image in temp_images
                ],
            }
        )
       
    prepared_messages.append(
        {
            "role": "system",
            "content": system_instruction,
        }
    )
    return (prepared_messages, images)


prompt_instruction_validate_documents = """
    You are a helpful AI assistant that extracts the types of documents from the provided pictures.
    Return a SINGLE JSON object matching EXACTLY the following schema:
    {
    "types": ["LetterOfCredit", "CommercialInvoice", ....]
    }
    Do not include any extra keys, nesting, or metadata (such as 'documents' or 'page').
    Only return recognized document types among:
    LetterOfCredit, CommercialInvoice, BillOfLading, CertificateOfOrigin.
    """


prompt_instruction_extract_documents_info = """
  You are a precise AI assistant that extracts structured data from document images.
  Extract data following this structure exactly:
{
 Exemple of output:
  "letter_of_credit": {
    "lc_number": "LC-2025-001",
    "issue_date": "2025-10-26T00:00:00",
    "expiry_date": "2025-10-26T00:00:00",
    "place_of_expiry": "Banque du Caire, Alexandria Branch",
    "applicant_name": "GreenLeaf Apparel",
    "applicant_address": "45 Rue de Marseille, France",
    "beneficiary_name": "Al-Safeer Textiles",
    "beneficiary_address": "123 Nile Street, Alexandria, Egypt",
    "issuing_bank": "Banque du Caire",
    "advising_bank": "BNP Paribas, Paris Branch",
    "amount": 100000.00,
    "currency": "USD",
    "lc_type": "Irrevocable, At Sight",
    "goods_description": "1,000 cartons of cotton T-shirts",
    "port_of_loading": "Alexandria, Egypt",
    "port_of_discharge": "Marseille, France",
    "latest_shipment_date": "2025-11-10",
    "incoterms": "CIF Marseille",
    "documents_required": [
      "Signed Commercial Invoice (3 copies)",
      "Full set of Clean on Board Bills of Lading",
      "Certificate of Origin issued by Chamber of Commerce"
    ],
    "payment_terms": "Payment at sight upon presentation of compliant documents"
  },
  "commercial_invoice": {
    "invoice_number": "INV-2025-045",
    "invoice_date": "2025-10-26T00:00:00",
    "exporter_name": "Al-Safeer Textiles",
    "exporter_address": "123 Nile Street, Alexandria, Egypt",
    "importer_name": "GreenLeaf Apparel",
    "importer_address": "45 Rue de Marseille, France",
    "items": [
      {
        "description": "Cotton T-shirts, white, size M",
        "quantity": 10000,
        "unit_price": 10.0,
        "total": 100000.0
      }
    ],
    "total_amount": 100000.0,
    "currency": "USD",
    "terms_of_payment": "As per LC No. LC-2025-001",
    "shipment_details": "Shipment via MV Ocean Star, BL No. BL-2025-019",
    "incoterms": "CIF Marseille"
  },
  "bill_of_lading": {
    "bl_number": "BL-2025-019",
    "issue_date": "2025-10-26T00:00:00",
    "shipper_name": "Al-Safeer Textiles",
    "shipper_address": "123 Nile Street, Alexandria, Egypt",
    "consignee_name": "GreenLeaf Apparel",
    "consignee_address": "45 Rue de Marseille, France",
    "notify_party": "BNP Paribas, Paris Branch",
    "port_of_loading": "Alexandria, Egypt",
    "port_of_discharge": "Marseille, France",
    "vessel_name": "MV Ocean Star",
    "voyage_number": "VOY-105",
    "goods_description": "1,000 cartons of cotton T-shirts",
    "number_of_packages": 1000,
    "gross_weight": 8500.0,
    "freight_terms": "Prepaid",
    "originals_issued": 3
  },
  "certificate_of_origin": {
    "certificate_number": "CO-2025-077",
    "issue_date": "2025-10-26T00:00:00",
    "exporter_name": "Al-Safeer Textiles",
    "exporter_address": "123 Nile Street, Alexandria, Egypt",
    "consignee_name": "GreenLeaf Apparel",
    "consignee_address": "45 Rue de Marseille, France",
    "goods_description": "1,000 cartons of cotton T-shirts made in Egypt",
    "origin_country": "Egypt",
    "authorized_signature": "M. El-Sharif",
    "issuing_chamber": "Alexandria Chamber of Commerce"
  }
}
        Your task:
        - Extract one document class per picture.
        - Return a single JSON object containing all extracted document classes.
        - Follow the exact schema and field names as defined in the provided JSON schema.

        Important formatting rules:
        1. Use exactly the same field names as in the schema. 
        Example: use "lc_number" — NOT "lc_no".
        2. Do not group fields into sub-objects.
        Example: use "applicant_name" and "applicant_address", NOT "applicant": {"name": ..., "address": ...}.
        3. Do not add new fields or rename existing ones.
        4. Do not infer nested objects — every field must be a direct property of the class.
        5. Return only one JSON object, and no extra explanations or comments.
        6. If only a date is provided, use 00:00:00 as the time.

        If information is missing or unclear in the image, set the field as None — do not create a new structure.
"""
