import "magic"

rule Malware_SHA256_PDF_ZIP_Delivery {
    meta:
        author = "SentinelX AI"
        date = "2023-10-27"
        description = "Detects ZIP files containing a PDF named with a SHA256 hash, characteristic of malware delivery attempts."
        reference = "Analysis of 3afef6872b721b25349bd9083f46b61461c022eab3f46354ac92dff4a2a6b881.zip"

    strings:
        // This regular expression detects a 64-character hexadecimal string followed by ".pdf".
        // This pattern is used to identify the internal PDF filename within the ZIP archive,
        // which matches the SHA256 hash, as described in the analysis.
        $re_pdf_hash_name = /[0-9a-fA-F]{64}\.pdf/ wide ascii nocase

    condition:
        // Ensure the file is a ZIP archive and contains the specific PDF filename pattern.
        magic.type contains "Zip archive data" and $re_pdf_hash_name
}