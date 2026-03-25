-- ============================================================
-- Legal Assistant - Seed Data Script
-- ============================================================
-- Populates initial data for roles and sample users
-- Run this after 02_create_tables.sql
-- ============================================================

\c legal_assist;

-- ============================================================
-- Seed Roles
-- ============================================================

INSERT INTO roles (id, name) VALUES
    ('11111111-1111-1111-1111-111111111111', 'admin'),
    ('22222222-2222-2222-2222-222222222222', 'user')
ON CONFLICT (name) DO NOTHING;

\echo '✓ Roles seeded'

-- ============================================================
-- Seed Sample Users
-- ============================================================

-- Admin user
INSERT INTO users (id, name, role_id) VALUES
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Admin User', '11111111-1111-1111-1111-111111111111')
ON CONFLICT (id) DO NOTHING;

-- Regular user (for testing)
INSERT INTO users (id, name, role_id) VALUES
    ('123e4567-e89b-12d3-a456-426614174000', 'Test User', '22222222-2222-2222-2222-222222222222')
ON CONFLICT (id) DO NOTHING;

\echo '✓ Sample users seeded'

-- ============================================================
-- Seed Sample Categories
-- ============================================================

INSERT INTO categories (id, title, description, is_active) VALUES
    ('cat11111-1111-1111-1111-111111111111', 'Indian Penal Code', 'Sections and provisions from the Indian Penal Code', true),
    ('cat22222-2222-2222-2222-222222222222', 'Insurance Law', 'Insurance policies, claims, and regulations', true),
    ('cat33333-3333-3333-3333-333333333333', 'Contract Law', 'Contract provisions, clauses, and legal agreements', true),
    ('cat44444-4444-4444-4444-444444444444', 'Property Law', 'Real estate, property rights, and transactions', true)
ON CONFLICT (title) DO NOTHING;

\echo '✓ Sample categories seeded'

-- ============================================================
-- Seed Sample Documents
-- ============================================================

\c legal_assist;

INSERT INTO documents (category_id, title, content, tags, status, created_by) VALUES
    ((SELECT id FROM categories WHERE title = 'Constitutional Rights' LIMIT 1), 'Article 14 - Right to Equality', 'The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India. This represents the basic principle of equality before law and equal access to justice.', ARRAY['equality', 'article 14', 'fundamental rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Constitutional Rights' LIMIT 1), 'Article 21 - Protection of Life and Personal Liberty', 'No person shall be deprived of his life or personal liberty except according to procedure established by law. The Supreme Court has expanded this to include the right to privacy, right to clean environment, and right to speedy trial.', ARRAY['life and liberty', 'article 21', 'fundamental rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Constitutional Rights' LIMIT 1), 'Article 32 - Right to Constitutional Remedies', 'Article 32 provides the right to approach the Supreme Court directly for the enforcement of Fundamental Rights through the issuance of writs like Habeas Corpus, Mandamus, Prohibition, Quo Warranto, and Certiorari.', ARRAY['writs', 'supreme court', 'remedies'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Criminal Law' LIMIT 1), 'IPC Section 378 - Theft', 'Whoever, intending to take dishonestly any movable property out of the possession of any person without that person''s consent, moves that property in order to such taking, is said to commit theft.', ARRAY['theft', 'ipc 378', 'property offense'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Criminal Law' LIMIT 1), 'CrPC Section 41 - When police may arrest without warrant', 'A police officer can arrest a person without a warrant or order from a Magistrate if the person is involved in a cognizable offense, or against whom a reasonable complaint has been made, or credible information received.', ARRAY['arrest', 'police power', 'crpc 41'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Criminal Law' LIMIT 1), 'Bail Procedures under CrPC Chapter 33', 'Bail is a matter of right in bailable offenses. For non-bailable offenses, bail is granted at the discretion of the court considering the gravity of the offense, likelihood of absconding, and the nature of evidence.', ARRAY['bail', 'crpc', 'release'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Consumer Protection' LIMIT 1), 'Deficiency in Service', 'Any fault, imperfection, shortcoming, or inadequacy in the quality, nature, and manner of performance which is required to be maintained under any law, resulting in harm or loss to the consumer.', ARRAY['service deficiency', 'consumer rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Consumer Protection' LIMIT 1), 'Unfair Trade Practices', 'Refers to deceptive practices like false advertising, selling second-hand goods as new, or offering gifts with the intention of recovering the cost from the item''s price. Consumers can seek compensation for these.', ARRAY['unfair trade', 'fraud', 'compensation'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Consumer Protection' LIMIT 1), 'Filing a Consumer Complaint', 'A consumer can file a complaint at the District, State, or National Consumer Disputes Redressal Commission based on the value of goods or services. The new 2019 Act also allows e-filing of complaints.', ARRAY['complaint filing', 'consumer court'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Labour & Employment' LIMIT 1), 'Minimum Wages Act Provisions', 'Employers must pay workers the minimum wages fixed by the state or central government. Deductions are strictly regulated, and failure to pay minimum wages can result in penalties and prosecution.', ARRAY['minimum wage', 'worker rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Labour & Employment' LIMIT 1), 'Maternity Benefit Act', 'Female employees are entitled to 26 weeks of paid maternity leave for their first two children. Establishments with 50 or more employees must also provide creche facilities.', ARRAY['maternity leave', 'women employees'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Labour & Employment' LIMIT 1), 'Workplace Safety regulations (Factories Act)', 'Employers must ensure clean, well-ventilated, and safe working environments. Hazardous processes require special safety committees and strict adherence to exposure limits.', ARRAY['workplace safety', 'health'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Right to Information' LIMIT 1), 'Filing an RTI Application', 'Any citizen can file an RTI request to a Public Information Officer (PIO) seeking government records. A nominal fee is required, and the information must normally be provided within 30 days.', ARRAY['rti application', 'public records'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Right to Information' LIMIT 1), 'Exemptions under Section 8 of RTI Act', 'Information that threatens national security, involves trade secrets, breeches parliamentary privilege, or invades personal privacy without public interest is exempt from disclosure.', ARRAY['rti exemptions', 'confidentiality'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Right to Information' LIMIT 1), 'First and Second Appeals in RTI', 'If a PIO denies information or fails to respond within 30 days, the citizen can file a First Appeal. If unsatisfied, a Second Appeal lies with the Central or State Information Commission.', ARRAY['rti appeals', 'information commission'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Cyber Laws' LIMIT 1), 'IT Act Section 66C - Identity Theft', 'Whoever fraudulently or dishonestly makes use of the electronic signature, password, or any other unique identification feature of any other person shall be punished with imprisonment up to 3 years.', ARRAY['identity theft', 'digital fraud', 'it act 66c'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Cyber Laws' LIMIT 1), 'Cyber Terrorism under Section 66F', 'Acts intended to threaten the unity, integrity, security, or sovereignty of India or strike terror in the people by denying access to computer resources or introducing malware carry stringent life imprisonment penalties.', ARRAY['cyber terrorism', 'national security'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Cyber Laws' LIMIT 1), 'Data Protection and Privacy', 'Under Section 43A of the IT Act, body corporates handling sensitive personal data must follow reasonable security practices. Failure resulting in wrongful loss makes them liable to pay compensation.', ARRAY['data privacy', 'corporate liability'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Environmental Rights' LIMIT 1), 'Environment Protection Act - Key Powers', 'The central government has wide powers to coordinate state actions, set environmental quality standards, restrict industrial locations, and mandate environmental impact assessments for new projects.', ARRAY['epa powers', 'environmental standards'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Environmental Rights' LIMIT 1), 'Polluter Pays Principle', 'A legal principle recognized by Indian courts stating that those who produce pollution should bear the costs of managing it and compensating victims of environmental damage.', ARRAY['polluter pays', 'compensation'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Environmental Rights' LIMIT 1), 'Public Interest Litigation for the Environment', 'Citizens can file a PIL in the High Court or Supreme Court to address severe environmental degradation, relying on Article 21 (right to a wholesome environment).', ARRAY['environmental pil', 'article 21'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Food Safety' LIMIT 1), 'FSSAI Food Adulteration Standards', 'The Food Safety and Standards Authority of India (FSSAI) prescribes regulations preventing the addition of harmful substances, misbranding, and ensuring hygienic manufacturing practices.', ARRAY['food adulteration', 'fssai'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Food Safety' LIMIT 1), 'Penalties for Sub-standard Food', 'Selling sub-standard or misbranded food articles can attract severe fines and cancelation of manufacturing licenses, protecting consumer health.', ARRAY['food penalties', 'consumer health'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Food Safety' LIMIT 1), 'Consumer Recourse for Food Poisoning', 'Victims of food poisoning can report the establishment to the local Food Safety Officer for inspection and simultaneously claim compensation in consumer courts.', ARRAY['food poisoning', 'legal recourse'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Land & Property' LIMIT 1), 'Tamil Nadu Land Reforms Act - Ceilings', 'The Act imposes a ceiling on the area of agricultural land a family can hold, aiming to acquire surplus land and distribute it among landless agriculturists.', ARRAY['land ceiling', 'tamil nadu land reform'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Land & Property' LIMIT 1), 'Patta Registration and Transfers', 'A Patta is a crucial revenue record indicating land ownership in Tamil Nadu. It must be legally transferred and updated in the taluk office upon sale or inheritance of the property.', ARRAY['patta', 'land ownership', 'revenue records'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Land & Property' LIMIT 1), 'Adverse Possession Constraints', 'Under property law, open, continuous, and hostile possession of private property for 12 years can lead to ownership rights, though it requires strict legal proof and is highly contested.', ARRAY['adverse possession', 'property dispute'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Family & Matrimonial' LIMIT 1), 'Hindu Marriage Act - Conditions for Marriage', 'Valid marriages require mutual consent, the groom to be 21 and the bride 18, neither having a living spouse, and not being within prohibited degrees of relationship.', ARRAY['marriage conditions', 'hindu law'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Family & Matrimonial' LIMIT 1), 'Mutual Consent Divorce', 'Couples living separately for at least one year can file for mutual consent divorce under Section 13B. A mandatory 6-month cooling-off period is usually required but can be waived by courts.', ARRAY['mutual divorce', 'family court'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Family & Matrimonial' LIMIT 1), 'Alimony and Maintenance', 'Courts can grant permanent alimony or monthly maintenance to a dependent spouse based on their earning capacity, lifestyle, and the other spouse''s income and liabilities.', ARRAY['alimony', 'maintenance', 'divorce'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Public Health' LIMIT 1), 'TN Public Health Act - Outbreak Containment', 'The Act grants sweeping powers to local authorities to inspect premises, abate nuisances, and isolate patients during epidemic outbreaks to prevent the spread of infectious diseases.', ARRAY['epidemics', 'public health act', 'tamil nadu'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Public Health' LIMIT 1), 'Sanitation and Waste Management Duties', 'Municipal bodies are legally obligated to maintain public drains, ensure clean drinking water, and manage solid waste to prevent public health hazards.', ARRAY['sanitation', 'civic duties'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Public Health' LIMIT 1), 'Food Hygiene in Public Eateries', 'Health inspectors have the authority to suspend operations of hotels and restaurants if they find severe unhygienic conditions violating the State Public Health Act.', ARRAY['food hygiene', 'inspections'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Agriculture Rights' LIMIT 1), 'Crop Insurance Regulations', 'State and central schemes legally protect farmers against crop failures due to natural calamities. Fast-track claim settlements mandate banks to credit compensation directly to farmer accounts.', ARRAY['crop insurance', 'farmer rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Agriculture Rights' LIMIT 1), 'Agricultural Loan Waivers and Relief', 'State governments occasionally issue legislative or executive orders waiving agricultural loans for small and marginal farmers during severe droughts or distress.', ARRAY['loan waiver', 'debt relief'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Agriculture Rights' LIMIT 1), 'APMC Acts and Farmer Markets', 'State APMC laws regulate agricultural markets to prevent the exploitation of farmers by middlemen, ensuring a transparent auction and pricing system.', ARRAY['apmc', 'agricultural market'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Police Procedures' LIMIT 1), 'Filing an FIR Guidelines', 'The police are duty-bound to register a First Information Report (FIR) under Section 154 of the CrPC for any cognizable offense, regardless of jurisdiction (Zero FIR).', ARRAY['fir', 'police duty', 'cognizable offense'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Police Procedures' LIMIT 1), 'Rights of the Accused upon Arrest', 'An arrested person must be informed of the grounds of arrest, has the right to inform a relative, the right to consult a lawyer, and must be produced before a magistrate within 24 hours.', ARRAY['arrest rights', 'police procedures'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Police Procedures' LIMIT 1), 'Remedies Against Police Inaction', 'If police refuse to register an FIR, a citizen can write to the Superintendent of Police or directly approach a Magistrate under Section 156(3) CrPC for an order to investigate.', ARRAY['police inaction', 'magistrate order'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Housing & Tenancy' LIMIT 1), 'Eviction Rules under Rent Control Acts', 'Landlords can only evict tenants on specific grounds such as willful default in rent, unauthorized subletting, causing nuisance, or bona fide requirement of the premises for personal use.', ARRAY['eviction limits', 'rent control', 'tenant rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Housing & Tenancy' LIMIT 1), 'Fair Rent Fixation', 'State tenancy laws allow Rent Control Courts to fix ''fair rent'' based on the age, cost of construction, and location of the property, preventing arbitrary rent hikes.', ARRAY['fair rent', 'tenant protection'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Housing & Tenancy' LIMIT 1), 'New Tenancy Agreements (TN Regulation of Rights and Responsibilities Act)', 'Under new rules, all rental agreements must be in writing and registered with the Rent Authority to be legally enforceable, aiming to balance tenant and landlord interests.', ARRAY['tenancy agreement', 'registration', 'tamil nadu'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Local Governance' LIMIT 1), 'Gram Sabha Powers in TN Panchayats', 'The Gram Sabha consisting of all registered voters in a village is legally empowered to approve village budgets, select beneficiaries for welfare schemes, and audit panchayat accounts.', ARRAY['gram sabha', 'panchayat rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Local Governance' LIMIT 1), 'Reservation in Local Bodies', 'The Constitution and State Acts mandate reservation of seats for Scheduled Castes, Scheduled Tribes, and a mandatory 33% (up to 50% in many states) reservation for women in local panchayats.', ARRAY['panchayat reservation', 'women leadership'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Local Governance' LIMIT 1), 'Property Tax Levies by Local Bodies', 'Municipalities and Panchayats are authorized under state law to levy and collect property taxes, water charges, and professional taxes to fund local infrastructure.', ARRAY['local tax', 'municipality'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Transport Laws' LIMIT 1), 'Motor Vehicles Act - Drunk Driving Penalties', 'Driving with blood alcohol levels exceeding 30mg per 100ml is a severe offense resulting in heavy fines, potential imprisonment, and mandatory suspension of the driving license.', ARRAY['drunk driving', 'traffic penalty'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Transport Laws' LIMIT 1), 'Hit and Run Compensation', 'The law provides a specific compensation scheme for victims of hit-and-run motor accidents where the offending vehicle cannot be traced, funded by a dedicated state mechanism.', ARRAY['hit and run', 'accident compensation'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Transport Laws' LIMIT 1), 'Third-Party Insurance Mandate', 'It is a statutory requirement for all vehicles operating in public spaces to possess valid third-party liability insurance to cover injuries or property damage caused to others.', ARRAY['mandatory insurance', 'motor vehicles act'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Education Rights' LIMIT 1), 'RTE Act - Free and Compulsory Education', 'The Right to Education Act guarantees free and compulsory education to all children aged 6 to 14 years. It prohibits screening procedures for admission and capitation fees.', ARRAY['rte', 'child education', 'fundamental right'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Education Rights' LIMIT 1), '25% Reservation in Private Schools', 'Section 12(1)(c) of the RTE Act mandates that non-minority private unaided schools reserve at least 25% of their entry-level seats for children from disadvantaged groups and weaker sections.', ARRAY['private school quota', 'social inclusion'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Education Rights' LIMIT 1), 'Anti-Corporal Punishment Rules', 'State education rules strictly forbid physical punishment or mental harassment in schools. Teachers found violating this are subject to disciplinary action under service rules.', ARRAY['corporal punishment', 'student protection'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Women & Child Protection' LIMIT 1), 'Protection of Women from Domestic Violence Act', 'The Act protects women against physical, emotional, verbal, sexual, and economic abuse. It allows magistrates to pass protection orders, residence orders, and monetary relief.', ARRAY['domestic violence', 'women rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Women & Child Protection' LIMIT 1), 'POCSO Act - Reporting Obligations', 'Under the Protection of Children from Sexual Offences (POCSO) Act, any person apprehending that an offense has been committed against a child MUST report it. Failure to report is a punishable offense.', ARRAY['pocso', 'child protection', 'mandatory reporting'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Women & Child Protection' LIMIT 1), 'Sexual Harassment at Workplace (POSH Act)', 'Every workplace with 10 or more employees must constitute an Internal Complaints Committee (ICC) to investigate complaints of sexual harassment securely and confidentially.', ARRAY['posh act', 'workplace harassment'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Senior Citizens Rights' LIMIT 1), 'Maintenance Orders for Senior Citizens', 'The Maintenance and Welfare of Parents and Senior Citizens Act guarantees parents the right to claim a monthly maintenance allowance from their adult children or heirs who inherit their property.', ARRAY['parent maintenance', 'senior citizens'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Senior Citizens Rights' LIMIT 1), 'Revocation of Property Transfer by Seniors', 'If a senior citizen transfers property to an heir under the condition that they provide basic amenities and the heir fails to do so, a special tribunal can declare the transfer void.', ARRAY['property transfer', 'elder abuse prevention'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Senior Citizens Rights' LIMIT 1), 'Old Age Pension Schemes (State)', 'Destitute senior citizens with no income source can apply for state-funded monthly old-age pensions directly distributed by the local revenue department (Taluk office).', ARRAY['old age pension', 'state welfare'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'SC/ST Atrocities' LIMIT 1), 'SC/ST Prevention of Atrocities Act - Key Offenses', 'The Act prevents atrocities including forcing the consumption of obnoxious substances, derogatory abuses based on caste, and denying access to public spaces. It ensures stringent punishments.', ARRAY['caste discrimination', 'sc st act'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'SC/ST Atrocities' LIMIT 1), 'Anticipatory Bail Prohibition', 'To prevent misuse of power and witness intimidation, Section 18 of the Act explicitly prohibits the granting of anticipatory bail to persons accused of committing an offense under this Act.', ARRAY['anticipatory bail', 'legal provisions'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'SC/ST Atrocities' LIMIT 1), 'Special Courts and Speedy Trials', 'The Act mandates the State to set up Exclusive Special Courts for speedy trials. Trials must be concluded within two months from the date of filing the charge sheet.', ARRAY['special courts', 'speedy trial'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Contract Law' LIMIT 1), 'Essentials of a Valid Contract', 'For a contract to be legally binding, it must have an offer, acceptance, lawful consideration, competent parties, free consent, and a lawful object. Agreements lacking any of these elements may be declared void.', ARRAY['valid contract', 'consideration', 'agreement'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Contract Law' LIMIT 1), 'Breach of Contract and Remedies', 'When a party fails to fulfill their contractual obligations, it constitutes a breach. The injured party can sue for damages, specific performance, injunction, or quantum meruit under the Indian Contract Act.', ARRAY['breach of contract', 'damages', 'remedies'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Contract Law' LIMIT 1), 'E-Contracts and Digital Signatures', 'Under the Information Technology Act, electronic contracts are legally recognized. Valid execution requires secure electronic signatures and compliance with digital identity verification standards.', ARRAY['e-contracts', 'digital signature', 'it act'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Tort Law' LIMIT 1), 'Negligence and Duty of Care', 'Negligence occurs when a person breaches their legal duty of care towards another, resulting in damage. To claim compensation, the plaintiff must prove that the harm was a direct foreseeable consequence of the breach.', ARRAY['negligence', 'duty of care', 'compensation'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Tort Law' LIMIT 1), 'Defamation - Libel and Slander', 'Defamation involves publishing false statements that harm a person''s reputation. It can be written (libel) or spoken (slander). Truth and fair comment are valid legal defenses against a defamation suit.', ARRAY['defamation', 'libel', 'slander', 'reputation'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Tort Law' LIMIT 1), 'Strict Liability in Tort', 'Under the rule of strict liability, any person who brings a dangerous substance onto their property is strictly liable for the damage it causes if it escapes, regardless of their level of care or negligence.', ARRAY['strict liability', 'hazardous', 'tort liability'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Probate & Estate Law' LIMIT 1), 'Validity and Execution of a Will', 'A Will must be executed by a person of sound mind, written clearly, signed by the testator, and attested by at least two witnesses. It takes effect only after the testator''s death.', ARRAY['will execution', 'testator', 'estate planning'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Probate & Estate Law' LIMIT 1), 'Intestate Succession (Dying without a Will)', 'If a person dies without leaving a valid will, their property is distributed among their legal heirs according to the personal succession laws applicable to their religion (e.g., Hindu Succession Act).', ARRAY['intestate', 'succession', 'legal heirs'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Probate & Estate Law' LIMIT 1), 'Obtaining a Probate', 'Probate is a certified copy of a Will granted by a court of competent jurisdiction. It establishes the legal validity of the Will and grants the executor the authority to distribute the estate''s assets.', ARRAY['probate', 'executor', 'court order'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Business & Corporate Law' LIMIT 1), 'Incorporating a Private Limited Company', 'Under the Companies Act, forming a private limited company requires a minimum of two directors, digital signature certificates, drafting of the MoA and AoA, and registration with the Registrar of Companies (RoC).', ARRAY['incorporation', 'companies act', 'directors'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Business & Corporate Law' LIMIT 1), 'Fiduciary Duties of Directors', 'Corporate directors have a fiduciary duty to act in good faith, avoid conflicts of interest, and exercise due care and skill in managing the company''s affairs to protect shareholders'' interests.', ARRAY['fiduciary duty', 'corporate governance'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Business & Corporate Law' LIMIT 1), 'Mergers and Amalgamations', 'Corporate mergers require the approval of the Board of Directors, a majority of shareholders, and sanction from the National Company Law Tribunal (NCLT) to ensure the protection of creditors and public interest.', ARRAY['merger', 'nclt', 'corporate restructuring'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Healthcare & Medical Law' LIMIT 1), 'Medical Malpractice and Negligence', 'Medical negligence occurs when a healthcare professional deviates from the accepted standard of care, causing injury or death to a patient. Patients can seek redressal through consumer courts or civil lawsuits.', ARRAY['medical negligence', 'malpractice', 'patient rights'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Healthcare & Medical Law' LIMIT 1), 'Patient Consent and Autonomy', 'Doctors are legally obligated to obtain informed consent from patients before conducting surgeries or invasive procedures. The patient must be fully aware of the risks, benefits, and alternatives.', ARRAY['informed consent', 'patient autonomy'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Healthcare & Medical Law' LIMIT 1), 'Clinical Establishment Act Compliance', 'Hospitals and clinics must register under the Clinical Establishments Act, maintaining minimum standards for facilities, transparent pricing of procedures, and adhering to strict biomedical waste disposal rules.', ARRAY['hospital compliance', 'clinical establishment'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Civil Procedure Law' LIMIT 1), 'Filing a Civil Suit (Plaint)', 'A civil lawsuit begins with filing a ''Plaint'' in a court of appropriate jurisdiction. It must clearly state the facts of the dispute, the cause of action, and the specific relief or compensation claimed.', ARRAY['plaint', 'lawsuit', 'civil court'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Civil Procedure Law' LIMIT 1), 'Summons and Written Statement', 'After a plaint is filed, the court issues a summons to the defendant. The defendant legally has 30 days (extendable up to 90 days) to file a ''Written Statement'' responding to the plaintiff''s allegations.', ARRAY['summons', 'written statement', 'defendant'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Civil Procedure Law' LIMIT 1), 'Execution of Decrees', 'Once a civil court passes a final judgment (decree), the winning party must file an execution petition to enforce it, which may involve attaching the judgment debtor''s property or civil arrest.', ARRAY['decree execution', 'judgment enforcement'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Insurance Law' LIMIT 1), 'Principles of Insurance: Utmost Good Faith', 'Insurance contracts are based on the principle of ''Uberrimae Fidei'' (utmost good faith). The insured must fully disclose all material facts affecting the risk; non-disclosure allows the insurer to cancel the policy.', ARRAY['utmost good faith', 'insurance principle', 'disclosure'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Insurance Law' LIMIT 1), 'IRDAI Claim Settlement Regulations', 'The Insurance Regulatory and Development Authority of India (IRDAI) mandates that insurers must settle or reject claims within 30 days of receiving all necessary documents to prevent undue harassment of policyholders.', ARRAY['irdai', 'claim settlement', 'insurance regulation'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1)),
    
    ((SELECT id FROM categories WHERE title = 'Insurance Law' LIMIT 1), 'Principle of Indemnity and Subrogation', 'Property and liability insurance strictly aim to indemnify (compensate) the exact financial loss. Through subrogation, the insurer acquires the injured party''s legal right to sue the third party who caused the loss.', ARRAY['indemnity', 'subrogation', 'compensation'], 'published', (SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'admin' LIMIT 1) LIMIT 1));

\echo '✓ Database automatically seeded with all 81 documents'


-- ============================================================
-- Verify Seeded Data
-- ============================================================

\echo ''
\echo '=== Database Summary ==='
SELECT 'Roles' as table_name, COUNT(*) as count FROM roles
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL
SELECT 'Categories', COUNT(*) FROM categories
UNION ALL
SELECT 'Documents', COUNT(*) FROM documents;

\echo ''
\echo '✓ Database seeded successfully!'
\echo ''
\echo 'Default Test User ID: 123e4567-e89b-12d3-a456-426614174000'
\echo 'Use this user_id for testing the RAG API'
\echo ''
\echo 'Next steps:'
\echo '1. Update Backend/.env with your database credentials'
\echo '2. Run: cd Backend && python -m uvicorn app.main:app --reload'
\echo '3. Visit: http://localhost:8000/docs'
