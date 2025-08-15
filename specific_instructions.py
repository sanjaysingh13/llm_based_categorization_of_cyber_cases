# This file contains specific gotchas and context for Indian cybercrime classification
# These are important rules that help avoid common misclassifications in cybercrime cases

# String containing all the gotchas for cybercrime classification
# This will be imported and formatted into the main classification prompt
SPECIFIC_INSTRUCTIONS = """
I will add some gotchas because you might not be aware of the context specific to Indian cybercrime.

8. If a person has been put under fear by a perpetrator, pretending to be a government official, by mentioning that his identity has been used for a crime, or that a parcel in his name has contraband, add 'digital_arrest' to the classification, even if the words are not specifically mentioned.

9. You sometimes misclassify a case where a victim falls for a Facebook Ad from the perpretrators and you misclassiy it as 'social_media_friend_request' whereas it should be 'facebook_ad'.
Similarly, look out for other fake ad methods for reaching out to victim. 

10. The tag 'fraud_by_impersonation_of_influential_person' will only apply if the impersonation is of a prominent person whom the victim is likely to know, such as a department superior, a minister or a public figure. 

11. You sometimes misclassify a case where a known person has misused subsidy as a 'subsidy_fraud'. The tag is only applicable when an unknown perpetrator has used subsidy as a bait. No subsidy tranfer would have actually taken place in that case. Your 'subsidy_fraud' classification may actually be 'not_a_cyber_crime' as it pertains to misappropriation of subsidy already granted.

12. 'corporate_impersonation' should not generally be aplied to impersonation of bank representatives, as almost all cyber-crime cases would have this feature. The tag should only refer to impersonation of a well-known company.

13. 'qr_code_for_debiting_fraudulently_presented_as_crediting' is a tag where the victim thinks that he or she is scanning a code to receive money, whereas it is actually a code for sending money to the fraudster.

14. 'traditional_cheating_and_fraud' will generally apply where there is some prior acquaintainance between victim and perpretator in the real world. It will also be indicated if the perpetrator has some in-depth knowledge about the victim, like he is constructing a house and the scam involves cement delivery. Or it is related to the victim's trade or business. Cyber criminals generally operate in an anonymous and non-discriminating environment.

15. 'CSP_fraud' is a local type of cybercrime of which you might not be aware. Customer Sevice Point (CSP) is a grass-root level customer service provider for banks. Generally shthe fraud will be for fake CSP installation.

16. "AEPS_fraud' is a similar local type of cybercrime involving Aadhar Enabled Payment System. Money can be withdrawn from the victim's account by using the victim's Aadhar number and biometrics, by obtaining the biometric data of the victim illegally.

17. 'suo_moto_case' will refer to cases initiated by police officers themselves, after developing information, such as information about fake call centres or a special ant-cybercrime drive based on intelligence and analysis.

18. 'general_purpose_fir_suitable_for_wider_investigation' will refer to cases where the complaint goes beyond a specific crime instance and will enable investigations into the wider gamut of that category of cybercrime, including the enabler ecosystems.
"""
