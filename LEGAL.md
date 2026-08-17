# Legal Framework

**Last Updated:** 2026-08-17

## Disclaimer

**NOT AFFILIATED WITH DJI.**  
This project is an independent, third-party implementation. DJI, Osmo, and Osmo Mobile are registered trademarks of SZ DJI Technology Co., Ltd. This software is provided "as is" without warranty of any kind, express or implied.

> **⚠️ DISCLAIMER:** This project is maintained from Canada. Users in other jurisdictions are responsible for ensuring compliance with their local laws. The author makes no representation that this software is legal in any specific jurisdiction outside Canada.

## 1. Canadian Copyright Act (R.S.C., 1985, c. C-42) – Interoperability Exemption

Section **30.61 (1)** provides an explicit statutory exception permitting the reproduction of computer programs to achieve interoperability:

> **30.61 (1)** *"It is not an infringement of copyright in a computer program for a person who owns a copy of the computer program that is authorized by the owner of the copyright, or has a licence to use a copy of the computer program, to reproduce the copy if*  
> *(a) they reproduce the copy for the sole purpose of obtaining information that would allow the person to make the program and another computer program interoperable; and*  
> *(b) they do not use or disclose that information, except as necessary to make the program and another computer program interoperable or to assess that interoperability."*

Section **30.61 (2)** explicitly affirms the distribution of programs incorporating interoperability information:

> **30.61 (2)** *"In the case where that information is used or disclosed as necessary to make another computer program interoperable with the program, subsection (1) applies even if the other computer program incorporates the information and is then sold, rented or otherwise distributed."*

## 2. Technological Protection Measures (TPM) – s. 41.1

Section **41.1 (1)** of the Canadian *Copyright Act* prohibits the circumvention of technological protection measures:

> **41.1 (1)** *"No person shall circumvent a technological protection measure within the meaning of subsection (2)."*  
> **41.1 (2)** defines a TPM as: *"any technology, device or component that, in the ordinary course of its operation, is designed to prevent, restrict or control the reproduction, distribution, communication or other use of a work."*

**Application to this project:**

Based on the author's independent analysis of publicly available technical documentation, community research, and preliminary passive observation of Osmo Mobile 2 BLE traffic, the communication protocol does not employ encryption, cryptographic authentication, or access control mechanisms that would constitute a TPM under s. 41.1(2).

**Methodological Transparency:** The author has not and will not attempt to defeat, bypass, or circumvent any access control mechanism. All analysis is conducted through passive observation of unencrypted radio transmissions. Should the author discover, during the course of research, that encryption or authentication is present, the author will:

- Immediately cease all further analysis
- Pivot to documenting only publicly available information
- Seek independent legal advice before proceeding

## 3. International Legal Protections

While the project is maintained from Canada, the following international frameworks support interoperability research:

| Instrument                                                          | Provision                                                                                | Relevance                                         |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **WIPO Copyright Treaty (WCT)** Art. 10                             | Permits limitations on copyright that do not unreasonably prejudice legitimate interests | Supports reverse-engineering for interoperability |
| **EU Software Directive (2009/24/EC)** Art. 6                       | Explicitly permits decompilation for interoperability                                    | Provides precedent in EU jurisdictions            |
| **Berne Convention** Art. 9(2)                                      | Allows reproduction in special cases not conflicting with normal exploitation            | Fair dealing / fair use compatibility             |
| **US DMCA** § 1201(f)                                               | Reverse-engineering exemption for interoperability (with conditions)                     | Applies to US-based users                         |
| **Agreement on Trade-Related Aspects of IP Rights (TRIPS)** Art. 13 | Permits limitations on exclusive rights in certain cases                                 | International trade law precedent                 |

## 4. People's Republic of China Legal Context

Given that DJI is a Chinese company (headquartered in Shenzhen), the following Chinese legal frameworks are relevant:

| Instrument                                                     | Provision                                                                                                                    | Relevance                                                                                    |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Copyright Law of the PRC** Art. 22(6)                        | Permits reproduction of published works for scientific research without permission, provided no commercial use               | Supports research purposes                                                                   |
| **PRC Anti-Unfair Competition Law** Art. 9                     | Protects trade secrets; reverse-engineering from publicly available information is generally not considered misappropriation | Passive observation of non-confidential transmissions does not constitute trade secret theft |
| **Regulations on the Protection of Computer Software** Art. 17 | Permits reproduction for interoperability purposes under certain conditions                                                  | Similar to EU/Canadian interoperability provisions                                           |

> **Note:** Chinese intellectual property law has historically been less permissive toward reverse-engineering than Western jurisdictions. However, the following factors strengthen the legal position:
>
> - The hardware is **discontinued** and no longer commercially available
> - The analysis relies on **passive observation** of public RF transmissions
> - The implementation is an **independent black-box driver** and does not copy proprietary code
> - The purpose is **interoperability**, not commercial competition

## 5. Discontinued Hardware Considerations

The Osmo Mobile 2 is a **discontinued product** (end of sale: July 2019; end of service: August 2024). This status has legal and practical implications:

**Legal considerations:**

- **Product Discontinuation & Market Impact:** While copyright does not expire upon product discontinuation, the absence of ongoing technical support and software updates for legacy models weighs favorably in a fair dealing analysis. This driver operates as an interoperability utility for legacy hardware rather than a commercial substitute for current software offerings.
- **EU Competition Law:** Art. 102 TFEU prohibits abuse of dominant position; refusing interoperability information for discontinued products may be considered abusive
- **US Copyright Office:** The DMCA anti-circumvention provisions have undergone rulemaking that recognizes exemptions for reverse-engineering of obsolete or discontinued hardware
- **Consumer rights:** Many jurisdictions recognize a "right to repair" that extends to software interoperability for owned devices

**Practical considerations:**

- Manufacturer no longer provides security updates or support
- No commercial alternative exists for headless/automated control
- The software does not compete with any currently offered DJI product
- Users have a legitimate interest in maintaining utility of legally owned hardware

## 6. Fair Dealing for Research & Private Study (s. 29)

> **29** *"Fair dealing for the purpose of research, private study, education, parody or satire does not infringe copyright."*

**Application to this project:**

The analysis conducted to implement this software qualifies as research in the following respects:

- **Experimental Research:** The author is conducting original research into the operational characteristics of consumer-grade BLE devices, contributing to the body of knowledge on embedded systems interoperability
- **Private Study:** The work is conducted independently, without institutional sponsorship or commercial purpose
- **Educational Purpose:** The project's documentation serves as an educational resource for others interested in BLE reverse-engineering and hardware interoperability

**Limitation:** This is a **secondary** defense, not the primary legal basis. The primary basis remains the interoperability exemption under s. 30.61.

- This project is distributed on a non-commercial, open-source basis for educational and research purposes.
- All trademarks, trade names, product designations, and logos referenced herein (including "DJI" and "Osmo Mobile 2") belong to their respective owners and are used strictly to identify hardware compatibility.

## 7. Functional Black-Box Methodology & Originality of Code

This project is developed through **independent, functional black-box analysis** of the Osmo Mobile 2's BLE communication behavior.

**Methodological Approach:**

- **Passive Observation Only:** All protocol information is derived exclusively through passive observation of over-the-air RF transmissions between hardware devices owned by the author. No active probing, tampering, or circumvention of any access control mechanism is performed.
- **No Source Code Access:** The author has not accessed, received, or obtained any proprietary source code, firmware images, or internal documentation from DJI or any third party.
- **No Decompilation or Disassembly:** The author has not decompiled, disassembled, or reverse-engineered any software binary, firmware, or embedded system code.
- **No Firmware Extraction:** The author has not extracted, read, dumped, or modified any firmware from the Osmo Mobile 2 hardware.
- **Black-Box Functional Logic:** The driver replicates only the minimal functional logic required to achieve device interoperability—such as BLE packet structures, command formats, and checksum calculations. Under Canadian copyright law (*CCH Canadian Ltd. v. Law Society of Upper Canada*), functional methods of operation dictated by interoperability requirements are not subject to copyright protection.

**Independent Expression:**

While the observable behavior of the driver replicates the functional control mechanisms of the device, the source code is an independently created, original expression. The author has not copied, adapted, or translated any proprietary source code, as confirmed by the methodology described above.

**Burden of Proof:**

This project is distributed as an original work. Any allegation of copying would require a demonstration of substantial similarity to, or derivation from, a copyrighted work. The author's methodology—passive observation of public RF transmissions—does not provide any basis for such a claim.

**Persuasive International Precedent:**

The methodology used here aligns with persuasive international jurisprudence, notably the Court of Justice of the European Union in *SAS Institute Inc. v. World Programming Ltd* (C-406/10), which affirmed that observing, studying, and testing the functionality of a system to replicate its operational behavior does not constitute copyright infringement. While not binding in Canada, this reasoning is consistent with Canadian principles that copyright protects expression, not functional methods of operation.

## 8. Terms of Service, Trade Secrets & Contractual Scope

- **EULA Independence:** Analysis and control functions are executed directly via standard Bluetooth Low Energy (BLE) hardware interfaces on hardware legally owned by the author. Because this driver operates directly on physical hardware interfaces using standard BLE protocols, it functions independently of any proprietary software application or associated End User License Agreement (EULA).
- **Trade Secret Exemption:** Protocol information captured via passive observation of unencrypted radio frequency (RF) transmissions broadcast openly over public airwaves does not involve improper acquisition, breach of confidence, or trade secret misappropriation under applicable common law or provincial civil law principles.
- **Contractual Scope:** To the extent any manufacturer Terms of Service (ToS) or End User License Agreement (EULA) purport to prohibit reverse engineering for interoperability:
  - Such terms govern only the use of proprietary **software**, not the physical hardware
  - Hardware interoperability research conducted via standard hardware interfaces operates outside the scope of software EULAs
  - Statutory user rights under Section 30.61 of the Canadian *Copyright Act* limit the enforceability of contractual terms that purport to restrict statutory interoperability rights
- **Descriptive Trademark Usage:** References to "DJI", "Osmo", and "Osmo Mobile 2" are strictly descriptive, used solely to identify functional hardware compatibility.

## 9. Limitations & Liability

**Limitations of This Legal Framework:**

- This document is provided for **informational purposes only** and does not constitute legal advice
- The author is not a licensed attorney; users should consult qualified legal counsel in their jurisdiction
- Legal protections vary significantly by jurisdiction; what is lawful in Canada may not be in other countries

**Liability Disclaimer:**

- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED
- IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY
- Users assume all risks associated with hardware damage, data loss, personal injury, or legal consequences

## 10. User Obligations & Legal Compliance Notice

Users of this software are advised of the following requirements and conditions:

1. **Lawful Hardware Possession:** Users must own or have lawful possession of the Osmo Mobile 2 hardware. This software is not intended for use with hardware obtained through unauthorized means.
2. **Operational Risk Assumption:** Users assume all operational risks associated with direct hardware and motor control, including but not limited to equipment damage, personal injury, and property damage.
3. **Lawful Purpose Only:** This software is intended strictly for personal, educational, research, and non-commercial interoperability purposes. Users must not use this software for any unlawful purpose, including but not limited to unauthorized surveillance, harassment, or violation of aviation regulations.
4. **Jurisdictional Compliance:** Users outside Canada are solely responsible for verifying compliance with their local legal frameworks. The author makes no representation that this software is lawful in any jurisdiction outside Canada.

**Notice:** These obligations are conditions of use. By using this software, users accept these conditions. If you cannot or will not comply with these obligations, you are not permitted to use this software.

## 11. Independence from DJI Development Tools

This project is developed entirely independently of any DJI-provided software development tools, SDKs, APIs, or proprietary documentation:

- **No DJI SDK:** This project does not use, incorporate, or reference the DJI Mobile SDK, DJI Windows SDK, or any other DJI-provided developer tools
- **No DJI APIs:** This project does not call any DJI-hosted APIs or web services
- **No DJI Documentation:** This project does not rely on any non-public documentation provided by DJI

All development is based solely on publicly available information and independent observation of hardware behavior.

## 12. Pairing & Authentication

To the best of the author's knowledge based on preliminary observation and community research, the Osmo Mobile 2's BLE interface does not require the user to enter a PIN, passkey, or other authentication credential beyond standard BLE pairing, which is a hardware-level protocol operation. The author is not aware of any access control mechanism that would constitute a TPM.

If the author discovers during the course of research that:

1. The device requires authentication credentials not disclosed by the manufacturer, or
2. The device employs cryptographic authentication that would constitute a TPM under s. 41.1(2)

The author will:

- Immediately cease all further analysis
- Document the finding without implementing any circumvention
- Seek independent legal advice before proceeding

## 13. Export Control & Cryptographic Software

This project does not implement, include, or rely upon any cryptographic functions for the purpose of authentication, encryption, or obfuscation. All communication uses standard BLE protocol operations.

**Applicable Exemptions:**

- **U.S. Export Administration Regulations (EAR):** Publicly available cryptographic software (including Python libraries) that does not implement encryption for confidentiality generally falls under EAR exemption
- **Wassenaar Arrangement:** General-purpose cryptographic libraries used for authentication (not encryption) are typically not controlled items
- **Canadian Export Controls:** The *Export and Import Permits Act* (EIPA) controls the export of certain cryptographic goods and technologies; however, purely academic or research-oriented interoperability software is generally exempt

**Conclusion:** Based on the author's assessment, this project does not contain cryptographic functionality subject to export control regulations. All communication uses standard, unencrypted BLE protocol operations.

## 14. Firmware & Embedded Software

This project does not:

- Extract, read, or dump firmware from the Osmo Mobile 2 hardware
- Modify or patch firmware in any way
- Upload or flash custom firmware to the device
- Disassemble or decompile any embedded software

The author has no interest in firmware internals and conducts all analysis exclusively at the BLE protocol level. This constraint significantly reduces legal risk, as firmware copyright is not implicated.

## 15. GitHub Platform Compliance

This repository complies with GitHub's Terms of Service:

- **No Proprietary Code:** No copyrighted, proprietary, or confidential code from third parties is hosted herein
- **No Illegal Content:** No content that violates applicable laws is hosted
- **No DMCA Violations:** To the author's knowledge, this repository does not contain material that infringes any third-party copyright
- **No Software Piracy:** This repository does not contain or facilitate the distribution of pirated software or illegal copies

The author commits to promptly removing any content that is shown to violate GitHub's ToS or applicable law.

## 16. Historical & Preservation Context

The Osmo Mobile 2 represents a significant piece of consumer hardware history. Released in 2018, it was one of the first consumer gimbals to bring professional-grade stabilization to mobile videography. With its discontinuation, this project serves as a **digital preservation** effort to ensure that:

- A working piece of hardware does not become e-waste
- The knowledge of how to interface with it is not lost
- Future researchers can understand early consumer BLE devices

This project is not about circumvention — it is about **preservation** and **continued utility** of legally owned hardware.

## 17. Non-Commercial Intent

While this project is licensed under the MIT License, the author's **primary intent** is non-commercial:

- The author has no financial interest in this project
- The project is developed for personal, educational, and research purposes
- Any commercial use by third parties is at their own risk and is not endorsed by the author

## 18. Privacy & Data Collection

This project does not:

- Collect, store, or transmit any user data
- Connect to any remote servers
- Call any third-party APIs
- Log user activity or hardware usage

All operation is local to the user's device.
