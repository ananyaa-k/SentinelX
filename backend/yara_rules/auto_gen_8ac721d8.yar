rule Ransomware_Note_Malicious4
{
    meta:
        author = "SentinelX AI"
        date = "2023-10-27"
        description = "Detects a specific ransomware note demanding Bitcoin payment based on file content."
        filename = "malicious_4_ransom.txt"

    strings:
        $s1 = "YOUR FILES ARE ENCRYPTED" ascii nocase
        $s2 = "To decrypt, pay 500 USD in Bitcoin" ascii nocase
        $s3 = "address 1Bc" ascii nocase
        $s4 = "Do not turn off your computer" ascii nocase

    condition:
        all of them
}