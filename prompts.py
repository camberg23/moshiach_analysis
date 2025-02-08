dataset_context = """
Below is the zero‑indexed list of columns from the cleaned CSV dataset. For each column we list:
- **Column Name** (exactly as in the CSV header, in quotations)
- **Sample Responses** (drawn from the subset; sensitive data replaced with dummy values)
- **Unique Values Count:** (the number of unique values observed in the subset)
- **Type** (Open‑ended text if free‑form; Selected text if responses come from a fixed set; numeric where appropriate)
- **DType** (the data type as inferred from the cleaned data; note that almost all non‑numeric columns are stored as object, i.e. str)

---

**0**
- **Column Name:** "First name"
- **Sample Responses:** "Aaron", "Aaron", "Abrumi", "Adam", "Aharon"
- **Unique Values Count:** 357
- **Type:** Open‑ended text
- **DType:** object (str)

---

**1**
- **Column Name:** "Last name"
- **Sample Responses:** "Lipsey", "Rajchman", "Shain", "Mizrahi", "Stein"
- **Unique Values Count:** 730
- **Type:** Open‑ended text
- **DType:** object (str)

---

**2**
- **Column Name:** "Phone number"
- **Sample Responses:** "+44 7000 000001", "+541100000001", "+1 700000000001", "+541100000002", "+1 700000000003"
- **Unique Values Count:** 1148
- **Type:** Open‑ended text (phone numbers are stored as strings to preserve formatting)
- **DType:** object (str)

---

**3**
- **Column Name:** "Email"
- **Sample Responses:** "dummy1@example.com", "dummy2@example.com", "dummy3@example.com", "dummy4@example.com", "dummy5@example.com"
- **Unique Values Count:** 1150
- **Type:** Open‑ended text
- **DType:** object (str)

---

**4**
- **Column Name:** "Full Mosed Name"
- **Sample Responses:** "Chabad Dummy City", "Chabad Dummy Town", "Chabad Dummy Bay", "Chabad Dummy Region", "Chabad Dummy University"
- **Unique Values Count:** 1010
- **Type:** Open‑ended text
- **DType:** object (str)

---

**5**
- **Column Name:** "How many years have you been in Shlichus?"
- **Sample Responses:** "20", "1", "18", "22", "25"
- **Unique Values Count:** 49
- **Type:** Open‑ended text (numeric responses)
- **DType:** int64

---

**6**
- **Column Name:** "What is your main responsibility in the Mosed?"
- **Sample Responses:** "Head of Mosed", "Area Head", "Head of Mosed"
- **Unique Values Count:** 3
- **Type:** Selected text (predefined roles)
- **DType:** object (str)

---

**7**
- **Column Name:** "What is the estimated population size of your community or Chabad House/Center?"
- **Sample Responses:** "450-750", "Less than 100", "100-250"
- **Unique Values Count:** 6
- **Type:** Selected text (population ranges)
- **DType:** object (str)

---

**8**
- **Column Name:** "Which of these programs do you use (fully or occasionally)?"
- **Sample Responses:** "Jnet, JLI", "CTeens", "Compass Magazine", "CKids", "MyShilach, JLI, Chabad on Campus"
- **Unique Values Count:** 506
- **Type:** Open‑ended text
- **DType:** object (str)

---

**9**
- **Column Name:** "Describe which other program(s) you may use."
- **Sample Responses:** (Often empty)
- **Unique Values Count:** 0
- **Type:** Open‑ended text
- **DType:** object (str)

---

**10**
- **Column Name:** "How would you describe the composition of your community?"
- **Sample Responses:** "Traditional with previous affiliation", "No previous religious affiliation", "Traditional with previous affiliation", "Ashkenaz & Sephardic mix, Ba'al Teshuva, Chasidish, No previous religious affiliation, Traditional with previous affiliation"
- **Unique Values Count:** 338
- **Type:** Open‑ended text
- **DType:** object (str)

---

**11**
- **Column Name:** "What best describes your community and their desire to learn?"
- **Sample Responses:** "non observant & not curious", "Non Observant & Curious", "Non Observant & Curious", "Mitzvah Observant & Learned & Curious; Mitzvah Observant & Not Learned & Curious; Non Observant & Curious"
- **Unique Values Count:** 107
- **Type:** Open‑ended text
- **DType:** object (str)

---

**12**
- **Column Name:** "How would you describe your community?"
- **Sample Responses:** (Often empty)
- **Unique Values Count:** 0
- **Type:** Open‑ended text
- **DType:** object (str)

---

**13**
- **Column Name:** "English"
- **Sample Responses:** "Majority", "Minority", "Majority", "Fair amount", "Majority"
- **Unique Values Count:** 22
- **Type:** Selected text (language dominance)
- **DType:** object (str)

---

**14**
- **Column Name:** "Hebrew"
- **Sample Responses:** "Minority", "Minority", "Minority", "Minority", "Minority"
- **Unique Values Count:** 28
- **Type:** Selected text
- **DType:** object (str)

---

**15**
- **Column Name:** "Spanish"
- **Sample Responses:** "Minority", "Majority", "Minority", "Majority", "Minority"
- **Unique Values Count:** 22
- **Type:** Selected text
- **DType:** object (str)

---

**16**
- **Column Name:** "Russian"
- **Sample Responses:** "Minority", "Minority", "Minority", "Minority", "Minority"
- **Unique Values Count:** 13
- **Type:** Selected text
- **DType:** object (str)

---

**17**
- **Column Name:** "French"
- **Sample Responses:** "Minority", "Minority", "Minority", "Minority", "Minority"
- **Unique Values Count:** 22
- **Type:** Selected text
- **DType:** object (str)

---

**18**
- **Column Name:** "Portuguese"
- **Sample Responses:** "Minority", "Minority", "Minority", "Minority", "Minority"
- **Unique Values Count:** 26
- **Type:** Selected text
- **DType:** object (str)

---

**19**
- **Column Name:** "Given the economic and geopolitical state of the world, how do your congregants view the future?"
- **Sample Responses:** "Nothing has changed; Something is different (no spiritual connection); Don't know", "Something is different; maybe I should get closer to G-d"
- **Unique Values Count:** 135
- **Type:** Open‑ended text
- **DType:** object (str)

---

**20**
- **Column Name:** "Explain the general or specific sentiment here."
- **Sample Responses:** (Often empty)
- **Unique Values Count:** 0
- **Type:** Open‑ended text
- **DType:** object (str)

---

**21**
- **Column Name:** "What topic/content do your congregants appreciate the most?"
- **Sample Responses:** "Politics", "Parsha themes", "Chassidus" (among others)
- **Unique Values Count:** 514
- **Type:** Open‑ended text
- **DType:** object (str)

---

**22**
- **Column Name:** "Rate the curiosity within your community about the topic of Moshiach or Geulah?"
- **Sample Responses:** "2.0", "4.0", "3.0", "3.0", "4.0"
- **Unique Values Count:** 5
- **Type:** Selected text (numeric rating)
- **DType:** float64

---

**23**
- **Column Name:** "How often are you approached about Moshiach and Geulah by community members?"
- **Sample Responses:** "2.0", "3.0", "3.0", "4.0", "2.0"
- **Unique Values Count:** 5
- **Type:** Selected text (numeric rating)
- **DType:** float64

---

**24**
- **Column Name:** "What creative ideas can we provide you to advance education and programming on the Moshiach in your community?"
- **Sample Responses:** "Focus on the acts of the individual to perfect the world…", "To receive classes ready for visitors", "A nice leaflet with a story", "Short messages about Moshiach", "Moshiach Speakers Bureau / Presentations"
- **Unique Values Count:** 1068
- **Type:** Open‑ended text
- **DType:** object (str)

---

**25**
- **Column Name:** "What creative ideas can you recommend to advance the Rebbe's vision for Moshiach education and awareness for the world at large?"
- **Sample Responses:** "Make shiurim, like the JLI programs, more accessible…", "To prepare small lessons every week for the Chabad house", "Social Media", "Relate current events to the coming of the Messiah", "Create a way to live Moshiach…"
- **Unique Values Count:** 1043
- **Type:** Open‑ended text
- **DType:** object (str)

---

**26**
- **Column Name:** "Moshiach and Geulah topics can be a sensitive topic. What are the common barriers and hesitations that _shluchim _have around the subject? What can we can do to alleviate them?"
- **Sample Responses:** "Lack of Knowledge/Education", "No Barrier", "Not used", "No Barrier", "Something is different (no spiritual connection)"
- **Unique Values Count:** 185
- **Type:** Open‑ended text (or Selected text if responses are standardized)
- **DType:** object (str)

---

**27**
- **Column Name:** "How does The Moshiach Office (Tut Altz) impact your _shilchus_?"
- **Sample Responses:** "Awareness only", "Unknown", "Not used", "Monthly/Weekly Program", "No Response"
- **Unique Values Count:** 13
- **Type:** Open‑ended text (or Selected text)
- **DType:** object (str)

---

**28**
- **Column Name:** "I think to make a greater impact The Moshiach Office (Tut Altz) needs to do this"
- **Sample Responses:** "Think about terminology and adjust it for those who are comfortable…", "I need more simple resources than Aleph for my Beis Chabad.", "Request sample", "No Response", "Marketing inquiry"
- **Unique Values Count:** 651
- **Type:** Open‑ended text
- **DType:** object (str)

---

**29**
- **Column Name:** "Have you used The Alef lessons?"
- **Sample Responses:** "No", "No", "No", "No", "No"
- **Unique Values Count:** 3
- **Type:** Selected text (predefined options)
- **DType:** object (str)

---

**30**
- **Column Name:** "How can we support you in getting started?"
- **Sample Responses:** (Varies; e.g., "Request sample", "No Response")
- **Unique Values Count:** 249
- **Type:** Open‑ended text
- **DType:** object (str)

---

**31**
- **Column Name:** "Which method works best for you when teaching The Alef?"
- **Sample Responses:** (E.g., "Regular class format", "Small group format")
- **Unique Values Count:** 29
- **Type:** Open‑ended text
- **DType:** object (str)

---

**32**
- **Column Name:** "Describe your teaching method or format."
- **Sample Responses:** (Often empty)
- **Unique Values Count:** 0
- **Type:** Open‑ended text
- **DType:** object (str)

---

**33**
- **Column Name:** "Please share how we can make The Alef better?"
- **Sample Responses:** "This is positive.", "Request sample", (others vary)
- **Unique Values Count:** 83
- **Type:** Open‑ended text
- **DType:** object (str)

---

**34**
- **Column Name:** "Emails: The Moshiach Office or Merkos"
- **Sample Responses:** "Always", "Never", "Sometimes"
- **Unique Values Count:** 11
- **Type:** Open‑ended text
- **DType:** object (str)

---

**35**
- **Column Name:** "WhatsApp: Shluchim groups"
- **Sample Responses:** "Never", "Never", "Sometimes"
- **Unique Values Count:** 13
- **Type:** Open‑ended text
- **DType:** object (str)

---

**36**
- **Column Name:** "Recommendation: Personal shliach testimonial"
- **Sample Responses:** "Sometimes", "Never", (others similar)
- **Unique Values Count:** 12
- **Type:** Open‑ended text
- **DType:** object (str)

---

**37**
- **Column Name:** "Online Chabad Blogs: (Collive, Anash, etc.)"
- **Sample Responses:** "Sometimes", "Never", "Always"
- **Unique Values Count:** 11
- **Type:** Open‑ended text
- **DType:** object (str)

---

**38**
- **Column Name:** "Other Social Media: (IG or FB)"
- **Sample Responses:** "Sometimes", "Never", "Always"
- **Unique Values Count:** 5
- **Type:** Open‑ended text
- **DType:** object (str)

---

**39**
- **Column Name:** "At the Kinus Hashluchim"
- **Sample Responses:** "Sometimes", "Never", "Always"
- **Unique Values Count:** 3
- **Type:** Open‑ended text
- **DType:** object (str)

---

**40**
- **Column Name:** "At Regional Kinusim"
- **Sample Responses:** "Sometimes", "Never", "Always"
- **Unique Values Count:** 10
- **Type:** Open‑ended text
- **DType:** object (str)

---

**41**
- **Column Name:** "There is an active WhatsApp community sharing tips, tools and content on various aspects of Moshiach & Geulah that can be beneficial to your community. Would you be interested in joining?"
- **Sample Responses:** "False", "True"
- **Unique Values Count:** 4
- **Type:** Selected text (boolean options)
- **DType:** object (str)

---

**42**
- **Column Name:** "What number is best to add to the group?"
- **Sample Responses:** "1234567890.0"
- **Unique Values Count:** 710
- **Type:** Open‑ended text (numeric input stored as float due to formatting)
- **DType:** float64

---

**43**
- **Column Name:** "Email.1"
- **Sample Responses:** "Sometimes"
- **Unique Values Count:** 3
- **Type:** Selected text (usage frequency)
- **DType:** object (str)

---

**44**
- **Column Name:** "Instagram (IG)"
- **Sample Responses:** "frequently", "frequently", "Sometimes"
- **Unique Values Count:** 6
- **Type:** Selected text (usage frequency)
- **DType:** object (str)

---

**45**
- **Column Name:** "Facebook (FB)"
- **Sample Responses:** "SOMETIMES", "SOMETIMES", "SOMETIMES"
- **Unique Values Count:** 5
- **Type:** Selected text (usage frequency)
- **DType:** object (str)

---

**46**
- **Column Name:** "WhatsApp"
- **Sample Responses:** "Sometimes", "Sometimes", "Sometimes"
- **Unique Values Count:** 3
- **Type:** Selected text (usage frequency)
- **DType:** object (str)

---

**47**
- **Column Name:** "Print for shul"
- **Sample Responses:** "Sometimes", "Sometimes", "Sometimes"
- **Unique Values Count:** 4
- **Type:** Selected text (usage frequency)
- **DType:** object (str)

---

**48**
- **Column Name:** "Personal phone calls"
- **Sample Responses:** "Don't really use", "Don't really use", "Don't really use"
- **Unique Values Count:** 4
- **Type:** Selected text (usage frequency)
- **DType:** object (str)

---

**49**
- **Column Name:** "SMS text messages"
- **Sample Responses:** "Don't really use", "does not use", "Don't really use"
- **Unique Values Count:** 3
- **Type:** Selected text (usage frequency)
- **DType:** object (str)

---

**50**
- **Column Name:** "Which social media promotional tools would be helpful to you if they were provided?"
- **Sample Responses:** "Customizable personalized posts (for you via Canva)", "Customizable personalized posts (for you via Canva), Promotional videos, Designed sharable topical quotes, Marketing blurbs"
- **Unique Values Count:** 70
- **Type:** Open‑ended text
- **DType:** object (str)

---

**51**
- **Column Name:** "What direction would you like to see The Moshiach Office take? Any specific programs you would like to see developed?"
- **Sample Responses:** "$100 Cash Gift", "Develop and market the Avoda of Macht Da Eretz Yisroel…", (others vary)
- **Unique Values Count:** 402
- **Type:** Open‑ended text
- **DType:** object (str)

---

**52**
- **Column Name:** "Thank you for completing the survey. How would you like your gift?"
- **Sample Responses:** "$100 Cash Gift"
- **Unique Values Count:** 5
- **Type:** Selected text (predefined gift options)
- **DType:** object (str)

---

**53**
- **Column Name:** "What is you ideal mailing location."
- **Sample Responses:** "Europe", "USA or Canada", "South America"
- **Unique Values Count:** 5
- **Type:** Selected text (geographic region)
- **DType:** object (str)

---

**54**
- **Column Name:** "Address"
- **Sample Responses:** "123 Dummy St", "456 Example Ave", "789 Sample Blvd"
- **Unique Values Count:** 583
- **Type:** Open‑ended text
- **DType:** object (str)

---

**55**
- **Column Name:** "Address line 2"
- **Sample Responses:** "Apt D", "Floor 1", (often empty)
- **Unique Values Count:** 57
- **Type:** Open‑ended text
- **DType:** object (str)

---

**56**
- **Column Name:** "City/Town"
- **Sample Responses:** "Dummy City", "Example Town", "Sample Borough", "Testville"
- **Unique Values Count:** 371
- **Type:** Open‑ended text
- **DType:** object (str)

---

**57**
- **Column Name:** "State/Region/Province"
- **Sample Responses:** "DC", "DC", "DC", "EX"
- **Unique Values Count:** 76
- **Type:** Open‑ended text
- **DType:** object (str)

---

**58**
- **Column Name:** "Zip/Post code"
- **Sample Responses:** "00001", "00002", "00003"
- **Unique Values Count:** 468
- **Type:** Open‑ended text
- **DType:** object (str)

---

**59**
- **Column Name:** "Country"
- **Sample Responses:** "CountryA", "CountryA", "CountryB"
- **Unique Values Count:** 4
- **Type:** Open‑ended text
- **DType:** object (str)

---

**60**
- **Column Name:** "Can you accept a PayPal? What is the email connected to your account?"
- **Sample Responses:** "dummy1@example.com"
- **Unique Values Count:** 452
- **Type:** Open‑ended text
- **DType:** object (str)

---

**61**
- **Column Name:** "If grants are made available for _shluchim _to initiate or expand a weekly Moshiach class for a year. Would you consider this?"
- **Sample Responses:** "Initiate", (others similar)
- **Unique Values Count:** 4
- **Type:** Selected text (predefined options)
- **DType:** object (str)

---

**62**
- **Column Name:** "What are the estimated costs associated with arranging this class?"
- **Sample Responses:** "GBP 750 (dummy)", "USD 80 (dummy)", "USD 1000 (dummy)"
- **Unique Values Count:** 262
- **Type:** Open‑ended text
- **DType:** object (str)

---

**63**
- **Column Name:** "What would be the best way to reach you to discuss your specific needs, ideas or suggestions?"
- **Sample Responses:** "Email", "WhatsApp", "WhatsApp; Phone call; Email"
- **Unique Values Count:** 44
- **Type:** Open‑ended text
- **DType:** object (str)

---

**64**
- **Column Name:** "How would you prefer to be contacted?"
- **Sample Responses:** (Often empty; may show as 0.0/1.0 placeholders)
- **Unique Values Count:** 0
- **Type:** Selected text (predefined options)
- **DType:** float64  *(originally empty so numeric placeholders may be present)*

---

**65**
- **Column Name:** "Submitted At"
- **Sample Responses:** "2024-11-29 00:32:02", "2024-11-29 01:33:49", "2024-11-29 01:16:28", "2024-11-28 22:55:25", "2024-11-29 15:17:59"
- **Unique Values Count:** 1162
- **Type:** Open‑ended text (date/time)
- **DType:** object (str)

---

**66**
- **Column Name:** "Token"
- **Sample Responses:** "dummytoken1", "dummytoken2", "dummytoken3", "dummytoken4", "dummytoken5"
- **Unique Values Count:** 1182
- **Type:** Open‑ended text
- **DType:** object (str)

---

**Note:**
- For columns with `dtype=object`, responses are treated as strings.
- Numeric responses (e.g. years and rating scales) are stored as int64/float64.
- Some columns that were originally empty now show placeholder numeric values due to cleaning.

This comprehensive context—with exact quoted column names, dummy-sensitive sample responses, and unique values counts—should give any analysis agent full insight into the dataset structure and help ensure correct column indexing.
"""
