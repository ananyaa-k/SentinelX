rule PDF_EmptyMetadata_DockerLure {
    meta:
        author = "SentinelX AI"
        date = "2023-10-27"
        description = "Detects PDF files with an empty metadata stream (Length 0), often used in social engineering lures like 'Docker.pdf'. The absence of metadata is a significant red flag indicating an attempt to obfuscate or evade detection."
        malware_family = "Social Engineering Lure"
        filetype = "PDF"

    strings:
        $pdf_header = "%PDF-1.5" ascii wide
        
        // This regex specifically targets the metadata object definition with an empty stream.
        // It matches any PDF object definition (e.g., "4 0 obj") followed by the critical attributes:
        // "/Length 0", "/Type /Metadata", "/Subtype /XML", and an empty 'stream' ... 'endstream' block.
        // The '\s*' allows for variable whitespace (spaces, tabs, newlines) between elements,
        // making the rule robust to different formatting styles.
        // The 's' modifier allows '.' (if used) to match newlines, but '\s*' handles this for us.
        $empty_metadata_obj_def = /\d+\s+0\s+obj\s*\/Length\s+0\s*\/Type\s+\/Metadata\s*\/Subtype\s+\/XML\s*stream\s*endstream\s*endobj/s ascii wide

    condition:
        $pdf_header and $empty_metadata_obj_def
}