rule Ransom_Note_Malicious_4
{
    meta:
        author = "SentinelX AI"
        date = "2023-10-27"
        description = "Detects a ransomware note based on explicit ransom demand strings."

    strings:
        $s1 = "YOUR FILES ARE ENCRYPTED." ascii wide
        $s2 = "To decrypt, pay" ascii wide
        $s3 = "Bitcoin to address" ascii wide
        $s4 = "Do not turn off your computer." ascii wide

    condition:
        all of them
}