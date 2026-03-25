import uuid
from app.core.database import SessionLocal
from app.models.admin import Category, Document, User

def seed_documents():
    db = SessionLocal()
    try:
        # Check mock user
        mock_user_id = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
        user = db.query(User).filter(User.id == mock_user_id).first()
        if not user:
            print("Please run seed_db.py first to create the mock user.")
            return

        categories_data = [
            "Labour & Employment Law",
            "Consumer Protection Law",
            "Criminal Law (Basic Rights)",
            "Family Law",
            "Property & Housing Law",
            "Women's Rights",
            "Senior Citizen Rights",
            "Persons with Disabilities Rights",
            "Child Rights & Education Law",
            "Cyber Law & Digital Rights"
        ]

        doc_templates = {
            "Labour & Employment Law": [
                ("Understanding Salary and Wage Deductions", "Your employer cannot legally make arbitrary deductions from your wages. Any deduction must be authorized by law, such as taxes, or agreed upon in writing by the employee."),
                ("Job Termination and Notice Periods", "In most jurisdictions, employment is at-will, but contracts or state laws may require specific notice periods for termination. Ensure you understand your contract terms."),
                ("Overtime Rules and Working Hours", "Non-exempt employees are legally entitled to receive overtime pay, typically at a rate of one and a half times their regular pay, for any hours worked over a standard workweek limit."),
                ("Workplace Harassment Rights", "Every employee has the right to a safe workplace free from harassment. Employers must have clear policies and procedures for handling harassment complaints."),
                ("Maternity and Maternity Benefits", "Expectant mothers are entitled to maternity leave and benefits under the law. Employers cannot terminate employment due to pregnancy."),
                ("Provident Fund and Gratuity", "Employees who have served continuously for a specified number of years are entitled to gratuity and provident fund contributions from their employer."),
                ("Right to Form Trade Unions", "Workers have a fundamental right to associate and form trade unions to collectively negotiate their welfare, wages, and working conditions."),
                ("Occupational Safety and Health", "Organizations must rigorously maintain a hazard-free work environment, providing safety gear and training to minimize occupational accidents."),
                ("Contract Labour Rights", "Even contract workers carry rights regarding minimum wage, safety regulations, and basic amenities equivalent to what direct employees receive."),
                ("Handling Constructive Dismissal", "If your employer alters your working conditions drastically, forcing you to resign, it is considered constructive dismissal, and you can challenge it legally.")
            ],
            "Consumer Protection Law": [
                ("Online Shopping Complaint Procedures", "Consumers have the right to file grievances against e-commerce platforms if the delivered product differs from its description or if there are unwarranted delays."),
                ("Refund and Replacement Rights", "If a product is defective or a service is deficient, consumers hold the right to demand a replacement or a full refund within a reasonable timeframe."),
                ("Deficiency in Services Guide", "A deficiency basically means any fault, imperfection, or shortcoming in the quality, nature, or manner of performance required to be maintained by a service provider."),
                ("Fighting False Advertisement", "Consumers are protected against misleading advertisements that falsely represent a product's quality, leading to deceptive practices and unfair trade."),
                ("Right to Information about Goods", "Consumers have the right to be informed about the quality, quantity, potency, purity, standard, and price of goods to protect against unfair trade practices."),
                ("Medical Negligence as Service Deficiency", "Medical services also fall under consumer protection. Negligence resulting in harm to the patient allows the consumer to seek compensation in consumer courts."),
                ("Banking and Insurance Disputes", "Denial of valid insurance claims or unauthorized banking charges can be challenged under consumer protection frameworks for fair resolutions."),
                ("Real Estate Consumer Rights", "Homebuyers have structured legal avenues under consumer law to file complaints against builders for failing to deliver projects on time or as promised."),
                ("Food Safety and Adulteration", "Selling adulterated or unsafe food products violates consumer protection standards, making the seller liable for stringent penalties."),
                ("Filing a Case in Consumer Court", "Consumers can directly file a formal complaint online to the district, state, or national consumer disputes redressal commission based on the value of the goods or services.")
            ],
            "Criminal Law (Basic Rights)": [
                ("Rights Available During Arrest", "Every arrested person has the right to know the grounds of their arrest and to consult a legal practitioner of their choice immediately."),
                ("How to File an FIR", "A First Information Report (FIR) is the initial step in a criminal investigation. The police are legally mandated to register an FIR for any cognizable offense."),
                ("Protection Against Illegal Detention", "Detainees must be presented before a magistrate within 24 hours of their arrest. Failing to do so amounts to illegal detention."),
                ("Understanding Bail Basics", "Bail is the conditional release of a defendant with the promise to appear in court. For bailable offenses, it is a right. For non-bailable, it is at the court's discretion."),
                ("Right to Free Legal Aid", "Individuals who cannot afford legal representation are constitutionally entitled to free legal aid to ensure a fair trial and the upholding of justice."),
                ("Search and Seizure Protocols", "Police officers generally require a warrant issued by a magistrate to search private premises, although there are exceptions under specific circumstances."),
                ("Right to Remain Silent", "The accused has the right against self-incrimination. Silence during an investigation cannot be automatically construed as an admission of guilt."),
                ("Protection from Double Jeopardy", "A person cannot be tried and punished twice for the same criminal offense under the prevailing legal framework."),
                ("Anticipatory Bail Guidelines", "If a person anticipates arrest for a non-bailable offense, they can apply for anticipatory bail to prevent immediate detention."),
                ("Rights of Crime Victims", "Victims have the right to be treated with dignity, to be informed about the case progression, and in many systems, to claim victim compensation.")
            ],
            "Family Law": [
                ("Marriage Registration Laws", "Registering a marriage provides legal recognition and serves as vital evidence for claims related to succession, maintenance, and child custody."),
                ("Grounds for Divorce", "Divorce can be sought by either spouse on specific grounds such as cruelty, adultery, desertion, or mutual consent depending on the governing personal law."),
                ("Protection from Domestic Violence", "Special laws exist to shield individuals from physical, mental, emotional, verbal, or economic abuse within a domestic relationship, including immediate restraining orders."),
                ("Maintenance and Alimony Rights", "A dependent spouse has the right to claim financial support (maintenance) from the other spouse both during the ongoing divorce proceedings and after the final decree."),
                ("Child Custody Principles", "In deciding custody battles, the paramount consideration of the court is always the overall welfare, safety, and best interests of the child."),
                ("Adoption Regulations", "Adoption laws lay out strict guidelines and background checks to legally grant parenting rights, ensuring the child is placed in a stable and nurturing environment."),
                ("Property Division in Divorce", "Depending on the jurisdiction, marital property acquired during the subsistence of the marriage is subject to equitable division upon dissolution of the marital bond."),
                ("Rights of the Unborn Child", "Certain property and succession laws recognize the rights of an unborn child, provided the child is subsequently born alive."),
                ("Guardianship Rules", "Laws govern who is appointed as a natural or legal guardian for a minor child, managing their person and their property effectively."),
                ("Restitution of Conjugal Rights", "If one spouse leaves the other without a reasonable excuse, the aggrieved party can legally approach the court seeking the restitution of conjugal rights.")
            ],
            "Property & Housing Law": [
                ("Resolving Land Ownership Disputes", "Land disputes require meticulous checking of title deeds, encumbrance certificates, and mutation records to establish true and legally binding ownership."),
                ("Drafting Rental Agreements", "A legally sound rental agreement must clearly state the rent amount, security deposit, lock-in period, maintenance duties, and specific conditions for eviction."),
                ("Tenant Rights Against Eviction", "Tenants cannot be arbitrarily evicted without following the due legal process, which usually entails a formal eviction notice stating reasonable grounds."),
                ("Handling Property Encroachment", "If a neighbor unlawfully encroaches on your property boundary, you can file an injunction suit to immediately halt construction and claim damages."),
                ("Succession and Inheritance", "Property inheritance is guided by prevailing succession laws or an executed Will. Legal heirs must obtain a succession certificate to transfer the property."),
                ("RERA and Builder Violations", "The Real Estate Regulatory Authority (RERA) acts to protect homebuyers, ensuring builders meet project deadlines and deliver the promised construction quality."),
                ("Rights of Co-Owners", "When multiple individuals co-own a property, each possesses joint rights to use the property, and specific consent is usually required to sell or heavily alter the asset."),
                ("Adverse Possession Laws", "If someone occupies a property continuously, openly, and without the owner's permission for a statutory limit (e.g., 12 years), they may legally claim ownership."),
                ("Transfer of Property Act", "The Act governs how property can be legally transferred from one person to another through mechanisms like sale, mortgage, lease, or gift."),
                ("Easement Rights Overview", "An easement gives a person the legal right to use another person's land for a specific purpose, such as a right of way to access their own property.")
            ],
            "Women's Rights": [
                ("Legal Remedies for Domestic Violence", "Survivors of domestic violence can seek protection orders, residence orders to remain in a shared household, and monetary relief against the abuser."),
                ("Workplace Safety and POSH", "The Protection of Women from Sexual Harassment (POSH) Act mandates internal committees in workplaces to address grievances and ensure a safe, hostile-free environment."),
                ("Equal Pay for Equal Work", "Constitutional provisions and specific wage legislation assert that women cannot be paid less than their male counterparts for executing similar work functions."),
                ("Maternity Benefit Act", "Women are entitled to paid maternity leave, a nursing break, and job security explicitly to accommodate pregnancy and early motherhood."),
                ("Laws Against Dowry", "Demanding, receiving, or giving dowry is a heavily penalized criminal offense. Harassment related to dowry demands can lead to immediate arrest."),
                ("Women's Property Rights", "Irrespective of marital status, women have equal legal rights to inherit, own, manage, and dispose of ancestral and acquired personal property."),
                ("Protection Against Stalking and Cyber Crimes", "Specific penal code provisions actively criminalize stalking, voyeurism, and the distribution of private images without a woman’s explicit consent."),
                ("Right to Safe Abortion", "Laws provide women the absolute legal right to medically terminate a pregnancy under specified conditions safely up to a legal gestational limit."),
                ("Police Assistance and FIR", "A woman can lodge an FIR or a Zero FIR from any police station regardless of jurisdiction for offenses committed against her."),
                ("Free Legal Aid for Women", "Irrespective of their income capability, women are constitutionally entitled to free legal aid to navigate any civil or criminal proceedings.")
            ],
            "Senior Citizen Rights": [
                ("Maintenance by Children", "Under specific welfare laws, senior citizens possess the legal right to demand maintenance from their children or legal heirs to maintain a dignified life."),
                ("Protection of Property", "Senior citizens can legally reclaim property gifted or transferred to heirs if the heirs subsequently fail or refuse to provide necessary physical and financial care."),
                ("Welfare Schemes for Elderly", "Governments provide various welfare schemes, pension structures, and significant travel concessions strictly designated for the elderly populace."),
                ("Speedy Disposal of Cases", "Courts are generally instructed to prioritize and expedite the hearing and resolution of legal cases where a senior citizen is a party."),
                ("Old Age Homes Regulations", "The state is mandated to establish accessible old age homes for indigent senior citizens, maintaining adequate medical facilities and nutritional care."),
                ("Healthcare Subsidies", "Seniors are frequently entitled to specialized health insurance schemes, subsidized treatments, and dedicated beds in government hospitals."),
                ("Protection from Abuse", "Physical, verbal, and emotional abuse of an elderly person is an actionable offense. Law enforcement has rapid-response structures for such complaints."),
                ("Tax Benefits for Seniors", "The income tax framework offers higher exemption limits, deduction benefits on medical expenses, and specialized tax rebates for senior citizens."),
                ("Reverse Mortgage Options", "A reverse mortgage allows senior property owners to systematically convert their home equity into a consistent stream of income while retaining residence."),
                ("Will Execution and Estate Planning", "Seniors are encouraged to secure their legacy effectively through registered Wills, ensuring their assets are distributed precisely per their intent, circumventing family disputes.")
            ],
            "Persons with Disabilities Rights": [
                ("Employment Anti-Discrimination", "Employers are strictly forbidden from discriminating against persons with disabilities during hiring, promotions, or in the day-to-day work environment."),
                ("Physical Accessibility Rights", "Public infrastructure, transport systems, and digital portals must legally be accessible and barrier-free to accommodate persons with varying disabilities."),
                ("Government Benefits and Reservations", "Individuals with certified disabilities are entitled to reserved quotas in government employment sectors and state-affiliated educational institutions."),
                ("Inclusive Education Directives", "Educational institutions must provide an inclusive learning environment and reasonable accommodations to meet the learning needs of students with disabilities."),
                ("Financial Assistance Schemes", "States provide dedicated disability pensions, unemployment allowances, and accessible loans specifically formulated for the economic independence of the disabled."),
                ("Right to Legal Capacity", "Persons with disabilities enjoy full legal capacity. Any guardianship intervention must be strictly need-based, time-bound, and completely subject to regular review."),
                ("Protection from Cruelty", "Subjecting a person with a disability to intentional indignity, public humiliation, or violence is recognized as a specific, aggravated criminal offense."),
                ("Access to Justice and Information", "The justice system is required to make court premises physically accessible and ensure all provided documentation is accessible in braille or audio formats."),
                ("Healthcare and Rehabilitation", "The government guarantees barrier-free access to specialized medical care, early intervention centers, and diverse rehabilitative therapy services."),
                ("Aviation and Travel Accessibility", "Airlines and transportation services cannot deny boarding entirely on the basis of disability and must present necessary assistive devices upon requirement.")
            ],
            "Child Rights & Education Law": [
                ("Right to Free and Compulsory Education", "The state mandates free and compulsory education for all children between specified age brackets, strictly prohibiting school fees, capitation charges, or screening tests."),
                ("Prohibition of Child Labour", "Employing minors in hazardous industries is a criminal offense. Stringent laws govern and heavily restrict adolescent labor in non-hazardous environments."),
                ("Protection of Children from Sexual Offences", "Specialized acts operate to deliver aggressive protection, mandating reporting, rapid legal trials, and victim-friendly courts to shield children from sexual violence."),
                ("Juvenile Justice and Rehabilitation", "Minors engaging in conflicts with the law are managed under a distinct rehabilitative juvenile justice act, focused on reform rather than penal punishment."),
                ("Anti-Corporal Punishment Statutes", "Schools and educational environments are rigidly prohibited from utilizing corporal physical punishment or deliberate mental harassment against any student."),
                ("Mid-Day Meal Entitlements", "Under national nutrition security, school children in public institutions hold a legal right to receive a hot, nutritious, cooked meal during the active school day."),
                ("Anti-Bullying Laws in Schools", "Educational institutions bear the legal responsibility to draft and vigorously enforce explicit anti-bullying and anti-ragging procedures with clear grievance channels."),
                ("Rights of Orphans and Vulnerable Children", "The state acts as a supportive guardian, legally obliged to oversee the housing, immediate nutrition, and continuing education of orphaned or abandoned children."),
                ("Child Marriage Prohibition", "Legislations assertively outlaw the marriage of any individual below the statutory age, rendering such engagements nullifiable and actively penalizing the facilitators."),
                ("Right to Play and Leisure", "Alongside education, children possess recognized rights to rest, leisure, and participation in recreational, cultural, and artistic activities suited directly to their age.")
            ],
            "Cyber Law & Digital Rights": [
                ("Combatting Online Financial Fraud", "Victims of unauthorized banking transactions or phishing scams must urgently report the irregularity to their bank and the designated national cybercrime portal."),
                ("Data Privacy and Protection", "Entities comprehensively collecting your personal digital data must explicitly secure your prior consent and handle the information transparently with strict data protection measures."),
                ("Cyber Harassment and Defamation", "Online stalking, persistent cyberbullying, and publishing unverified defamatory statements carry heavy civil liability and direct criminal prosecution."),
                ("Identity Theft Guidelines", "Fraudulently assuming another person's digital identity to commit fraud or illicit activities is a severely punished offense under prevailing information technology laws."),
                ("Revenge Porn and Privacy Breach", "The non-consensual capture, sharing, or active distribution of sexually explicit or private images constitutes a deeply serious criminal breach driving immediate legal action."),
                ("Right against Digital Surveillance", "Any interception or intensive monitoring of an individual's digital communications by state agencies must solidly adhere to strictly defined constitutional boundaries and protocols."),
                ("Intellectual Property in Digital Media", "Digital content, including software code, original literature, and media, remains protected globally under copyright law. Unauthorized digital distribution is heavily penalized."),
                ("E-Contracts and Digital Signatures", "Electronically signed contracts are fully legally valid, highly enforceable, and comprehensively regulated by robust cryptographic and digital signature legislations."),
                ("Hacking and Unauthorized Access", "Penetrating or destroying data within a computer network or server without explicit and verified permission is categorized as a high-level, punishable cybercrime."),
                ("Safe Harbor for Intermediaries", "Social media networks and varied technical intermediaries hold conditional immunity from active liability for third-party user-generated content, provided they swiftly execute designated takedown procedures.")
            ]
        }

        # create missing categories
        category_objects = {}
        for cat_name in categories_data:
            cat = db.query(Category).filter(Category.title == cat_name).first()
            if not cat:
                cat = Category(title=cat_name, description=f"Matters related to {cat_name}")
                db.add(cat)
                db.commit()
            category_objects[cat_name] = cat
        
        # Insert documents
        count = 0
        for cat_name, docs in doc_templates.items():
            cat_obj = category_objects[cat_name]
            for title, content in docs:
                # check if exists
                existing = db.query(Document).filter(Document.title == title, Document.category_id == cat_obj.id).first()
                if not existing:
                    tag_name = "".join([c.lower() for c in cat_name if c.isalpha() or c.isspace()]).replace(" ", "_")
                    doc = Document(
                        category_id=cat_obj.id,
                        title=title,
                        content=content,
                        tags=[tag_name],
                        status="published",
                        created_by=mock_user_id
                    )
                    db.add(doc)
                    count += 1
        
        db.commit()
        print(f"Successfully inserted {count} documents across {len(categories_data)} categories.")

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    seed_documents()
