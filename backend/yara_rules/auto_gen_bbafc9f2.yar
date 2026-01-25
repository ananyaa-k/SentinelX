rule tata_global_intern_pdf_exploit {
    meta:
        author = "SentinelX AI"
        date = "2023-11-20"
        description = "Detects a malicious PDF with /OpenAction 19 0 R in the catalog, matching social engineering filename."

    strings:
        $s1 = "%PDF-1.5" ascii wide nocase
        $s2 = "/Catalog" ascii wide nocase
        $s3 = "/OpenAction 19 0 R" ascii wide nocase

    condition:
        all of them
        and filename matches "tata global intern\\.pdf"
}