from datetime import date

from transparence.models import Party, Politician, LegalCase, politician, Source


def run():
    Source.objects.all().delete()
    Politician.objects.all().delete()
    LegalCase.objects.all().delete()
    Party.objects.all().delete()

    party_1 = Party.objects.create(abbreviation="LA", name="Liberty Alliance")

    john = Politician.objects.create(first_name="John", last_name="Doe", civility="M.", external_id="1")


    case_1 = LegalCase.objects.create(
        external_id = "CASE-001",
        category = "ABUS_BIENS_SOCIAUX",
        title = "Enquete pour abus de biens sociaux",
        description = "Une société de conseil en informatique, dirigée par Jean Dupont, a été placée en liquidation judiciaire le 15 mars 2024 par le tribunal de commerce de Nantes. Le parquet de Nantes a ouvert une enquête pour banqueroute.",
        date = date(2024,1,1),
        status = "EN_COURS",
        verdict_date = date(2025,1,1),
        party = party_1,
        politician = john,
    )

    Source.objects.create(
        external_id = "SOURCE-001-002",
        url = "https://www.legorafi.fr/2026/03/23/battu-a-pau-francois-bayrou-annonce-a-emmanuel-macron-quil-redevient-premier-ministre/",
        publisher = "GORAFI",
        type = "PRESSE",
        title = "Battu à Pau, il annonce qu’il redevient Premier ministre",
        description = "Très affecté par sa défaite de 344 voix aux élections municipales, le maire sortant de Pau a décidé de se rabattre sur un nouveau poste de Premier ministre. ",
        published_at = date(2025,1,1),
        legal_case = case_1,
    )

    source_1_2 = Source.objects.create(
        external_id = "SOURCE-001-002",
        url = "https://www.legorafi.fr/2026/03/17/bruno-salomone-legue-a-sa-famille-800-jeeps-renegade/",
        publisher = "GORAFI",
        type = "PRESSE",
        title = "Bruno Salomone lègue à sa famille 800 Jeeps Renegade",
        description = "Suite au triste décès du comédien Bruno Salomone, sa famille a été surprise de recevoir en héritage les 800 dernières Jeeps Renegade du jeu TV “Burger Quiz.",
        published_at = date(2025,1,1),
        legal_case = case_1,
    )
    case_2 = LegalCase.objects.create(
        external_id = "CASE-002",
        category = "AUTRE",
        title = "Instruction pour pressions sur la justice",
        description = "Entre 2025 et 2026, la présidence et le chef de l’État sont soupçonnés d’avoir exercé des pressions sur la justice dans le cadre d’une enquête sur des malversations dans un projet public. En juin 2013, les juges ont perquisitionné chez un ancien responsable administratif de la présidence. La veuve d’un fonctionnaire concerné a porté plainte, dénonçant une ingérence politique contraire à la séparation des pouvoirs.",
        date = date(2025,2,1),
        status = "CLASSEMENT_SANS_SUITE",
        verdict_date = date(2025,9,1),
        party = party_1,
        politician = john,
    )
    Source.objects.create(
        external_id = "SOURCE-002-001",
        url = "https://www.legorafi.fr/2026/03/25/apres-banksy-reuters-revele-qui-se-cachait-derriere-le-pseudonyme-michel-barnier/",
        publisher = "GORAFI",
        type = "PRESSE",
        title = "Après Banksy, Reuters révèle qui se cachait derrière le pseudonyme “Michel Barnier”",
        description = "Des mois d’enquête ont été nécessaire pour débusquer la personne qui se cachait derrière le soi-disant Premier ministre",
        published_at = date(2025,1,1),
        legal_case = case_2,
    )



    party_2 = Party.objects.create(abbreviation="PF", name="Progressive Front")
    jane = Politician.objects.create(first_name="John", last_name="Doe", civility="M.", external_id="1")
    case_3 = LegalCase.objects.create(
        external_id = "CASE-003",
        category = "FINANCEMENT_ILLEGAL_CAMPAGNE",
        title = "Mise en examen de Jane Doe pour escroquerie aggravée dans l'affaire des comptes de campagne",
        description = "L’agence nationale de sécurité sanitaire conseille aux Français d’arrêter de consommer des fruits et légumes pour limiter leur exposition au cadmium.",
        date = date(2025,2,1),
        status = "MISE_EN_EXAMEN",
        verdict_date = date(2025,9,1),
        party = party_2,
        politician = jane,
    )

    source_3 = Source.objects.create(
        external_id = "SOURCE-002-001",
        url = "https://www.legorafi.fr/2026/03/25/apres-banksy-reuters-revele-qui-se-cachait-derriere-le-pseudonyme-michel-barnier/",
        publisher = "GORAFI",
        type = "PRESSE",
        title = "Face au taux de cadmium dans les fruits et légumes, l’Anses recommande de manger des cigarettes",
        description = "Des mois d’enquête ont été nécessaire pour débusquer la personne qui se cachait derrière le soi-disant Premier ministre",
        published_at = date(2025,1,1),
        legal_case = case_3,
    )




    print("Seeds créés avec succès !")