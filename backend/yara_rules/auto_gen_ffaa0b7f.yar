rule Malicious_Ransom_Note
{
    meta:
        author = "SentinelX AI"
        date = "2023-10-27"
        description = "Detects a specific ransom note based on explicit strings."
        
    strings:
        $s1 = "YOUR FILES ARE ENCRYPTED" ascii wide
        $s2 = "To decrypt, pay" ascii wide
        $s3 = "USD in Bitcoin to address" ascii wide
        $s4 = "Do not turn off your computer" ascii wide

    condition:
        all of them
}