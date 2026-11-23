# Domain B Adsorption ML: Licensing Guide and Author Recommendations

## 1. Context and Legal Framework
This document provides guidance for Dr. V. Karthik regarding the open-source software license selection for `domain_b_adsorption_ml`.

Academic software publication requires balancing two fundamental objectives:
1. **Reproducibility and Public Good:** Granting other academic and environmental researchers the freedom to inspect, run, modify, and build upon the methodology.
2. **Attribution and Institutional Protection:** Ensuring the author and institution receive proper scholarly credit and are protected against misrepresentation or liability.

---

## 2. Recommended Options for the Author

### Option A: The MIT License (Simple, Highly Permissive)
- **Best if:** You want maximum adoption and frictionless reuse across academia and industry.
- **Key Terms:** Grants anyone the right to use, copy, modify, merge, publish, distribute, and sell copies of the software, provided the copyright notice and permission notice are included in all copies.
- **Disclaimer:** The software is provided "as is", without warranty of any kind.

### Option B: The BSD 3-Clause License (Recommended for Academic Institutions)
- **Best if:** You want the simplicity of MIT but with an explicit legal clause protecting your name and the university name from being used in promotional or commercial endorsements without consent.
- **Key Terms:** Includes all MIT permissions plus Clause 3:
  > *"Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission."*

---

## 3. How to Apply the Chosen License Prior to Release

1. Once you confirm Option A or Option B, create a file named `LICENSE` in the package root.
2. If Option B (BSD 3-Clause) is chosen:
```text
Copyright (c) 2026 Dr. V. Karthik, Department of Civil Engineering, Karpagam Academy of Higher Education.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
```
3. Remove `LICENSE_PENDING.md`.
4. Update the `license` field in `pyproject.toml` and `CITATION.cff`.


---

## 4. Activated License Record

- **Selected License:** BSD 3-Clause License
- **Copyright Statement:** Copyright (c) 2026, Dr. V. Karthik.
- **Activation Date:** 2026-11-23
- **Status:** Formally approved by author for public release via GitHub (`karthice1/domain_b_adsorption_ml`) and Zenodo.
