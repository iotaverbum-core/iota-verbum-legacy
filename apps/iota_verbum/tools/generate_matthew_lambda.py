"""
Utility script to generate Modal Bible λ-files for the Gospel of Matthew.

This script is intentionally simple: it does not depend on the engine,
only on pathlib + json. It mirrors the JSON pattern used in
modal_bible/mark/mark_04_26_29.lambda.json.

Usage (from project root):

    (.venv) python tools/generate_matthew_lambda.py

It will create / overwrite files under modal_bible/matthew/.
"""

from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "modal_bible" / "matthew"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_verses(verses_str: str) -> list[int]:
    """
    Very small helper: "1-17" -> [1,2,...,17]
    """
    start_str, end_str = verses_str.split("-")
    start, end = int(start_str), int(end_str)
    return list(range(start, end + 1))


META_BASE = {
    "author": "Iota Verbum – Modal Bible Prototype",
    "encoding": "Lambda_IV_v0.1",
    "notes": "Auto-generated Matthew λ-files; safe to hand-edit after generation.",
}

PERICOPES = [

    {
        "passage_id": "Mat01_01_17",
        "chapter": 1,
        "verses": "1-17",
        "title": "Matthew 1:1–17 – Genealogy of Jesus the Messiah",
        "frames": [
        "Genealogy",
        "DavidicMessiah",
        "Fulfilment"
    ],
        "identity": [
        "[]JesusIsTheChristSonOfDavidSonOfAbraham(Jesus, David, Abraham)"
    ],
        "unit_label": "Genealogy and Messianic Identity",
        "illocution": "Narration",
        "agents": [
        "Matthew",
        "Jesus",
        "David",
        "Abraham",
        "Israel"
    ],
        "description": "Matthew traces Jesus' lineage to show Jesus as Son of David, Son of Abraham, rooted in Israel's story.",
        "lambda_iv": [
        "[]JesusIsTheChristSonOfDavidSonOfAbraham(Jesus, David, Abraham)",
        "EFF(AnchoredInCovenantStory(Jesus, IsraelHistory))"
    ],
    },

    {
        "passage_id": "Mat01_18_25",
        "chapter": 1,
        "verses": "18-25",
        "title": "Matthew 1:18–25 – Birth of Jesus and the Name 'Immanuel'",
        "frames": [
        "BirthNarrative",
        "Incarnation",
        "Emmanuel"
    ],
        "identity": [
        "[]JesusIsEmmanuelGodWithUs(Jesus, Presence)"
    ],
        "unit_label": "Spirit-Conceived Son and Saving Name",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "Mary",
        "Joseph",
        "HolySpirit",
        "AngelOfTheLord"
    ],
        "description": "Jesus is conceived by the Holy Spirit, named as the one who will save his people from their sins, and identified as Immanuel.",
        "lambda_iv": [
        "[]JesusIsEmmanuelGodWithUs(Jesus, Presence)",
        "EFF(HeWillSaveHisPeopleFromTheirSins(Jesus, HisPeople))"
    ],
    },

    {
        "passage_id": "Mat02_01_12",
        "chapter": 2,
        "verses": "1-12",
        "title": "Matthew 2:1–12 – Magi and the King of the Jews",
        "frames": [
        "Epiphany",
        "Nations",
        "Worship"
    ],
        "identity": [
        "[]JesusIsTheTrueKingOfTheJewsForIsraelAndNations(Jesus, Israel, Nations)"
    ],
        "unit_label": "Gentile Worship of the King",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "Herod",
        "Magi",
        "ChiefPriests",
        "Scribes"
    ],
        "description": "Gentile magi seek and worship the child as King of the Jews, while Herod and Jerusalem are troubled.",
        "lambda_iv": [
        "[]JesusIsTheTrueKingOfTheJewsForIsraelAndNations(Jesus, Israel, Nations)",
        "<>NationsComeToWorship(Jesus, Nations)"
    ],
    },

    {
        "passage_id": "Mat02_13_23",
        "chapter": 2,
        "verses": "13-23",
        "title": "Matthew 2:13–23 – Flight to Egypt, Massacre, and Return",
        "frames": [
        "Exile",
        "Protection",
        "Fulfilment"
    ],
        "identity": [
        "[]GodProtectsHisMessiahThroughExileAndReturn(YHWH, Jesus)"
    ],
        "unit_label": "Suffering Around the Messiah's Birth",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "Joseph",
        "Mary",
        "Herod",
        "ChildrenOfBethlehem"
    ],
        "description": "God preserves Jesus through exile and return while Rachel weeps for her children under Herod's violence.",
        "lambda_iv": [
        "[]GodProtectsHisMessiahThroughExileAndReturn(YHWH, Jesus)",
        "EFF(SufferingSurroundsTheComingOfTheKing(Suffering, Jesus))"
    ],
    },

    {
        "passage_id": "Mat03_01_12",
        "chapter": 3,
        "verses": "1-12",
        "title": "Matthew 3:1–12 – John the Baptist and the Call to Repent",
        "frames": [
        "Preparation",
        "Repentance",
        "Judgment"
    ],
        "identity": [
        "[]JohnPreparesTheWayForTheLordByCallingToRepentance(John, Israel)"
    ],
        "unit_label": "Forerunner and Fire",
        "illocution": "PropheticWarning",
        "agents": [
        "John",
        "Crowds",
        "Pharisees",
        "Sadducees",
        "ComingOne"
    ],
        "description": "John calls Israel to repent in light of the coming one who will baptise with the Holy Spirit and fire.",
        "lambda_iv": [
        "[]JohnPreparesTheWayForTheLordByCallingToRepentance(John, Israel)",
        "<>ComingOneBaptisesWithSpiritAndFire(ComingOne, Spirit, Fire)"
    ],
    },

    {
        "passage_id": "Mat03_13_17",
        "chapter": 3,
        "verses": "13-17",
        "title": "Matthew 3:13–17 – Baptism of Jesus",
        "frames": [
        "Baptism",
        "Sonship",
        "Trinity"
    ],
        "identity": [
        "[]JesusIsTheBelovedSonInWhomTheFatherIsWellPleased(Jesus, Father, Spirit)"
    ],
        "unit_label": "Beloved Son Anointed for Mission",
        "illocution": "Theophany",
        "agents": [
        "Jesus",
        "John",
        "Father",
        "Spirit"
    ],
        "description": "Jesus is baptised to fulfil all righteousness, and the Father and Spirit publicly affirm him as the beloved Son.",
        "lambda_iv": [
        "[]JesusIsTheBelovedSonInWhomTheFatherIsWellPleased(Jesus, Father, Spirit)",
        "EFF(MissionInauguratedAtBaptism(Jesus))"
    ],
    },

    {
        "passage_id": "Mat04_01_11",
        "chapter": 4,
        "verses": "1-11",
        "title": "Matthew 4:1–11 – Temptation in the Wilderness",
        "frames": [
        "Testing",
        "Obedience",
        "Scripture"
    ],
        "identity": [
        "[]JesusObeysWhereAdamAndIsraelFailed(Jesus, Adam, Israel)"
    ],
        "unit_label": "Son Tested and Proven Faithful",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "Devil",
        "Spirit"
    ],
        "description": "Led by the Spirit, Jesus resists Satan's temptations by clinging to Scripture, succeeding where Adam and Israel failed.",
        "lambda_iv": [
        "[]JesusObeysWhereAdamAndIsraelFailed(Jesus, Adam, Israel)",
        "<>UsesScriptureAsWeaponOfObedience(Jesus, Scripture)"
    ],
    },

    {
        "passage_id": "Mat04_12_25",
        "chapter": 4,
        "verses": "12-25",
        "title": "Matthew 4:12–25 – Light in Galilee and the First Disciples",
        "frames": [
        "KingdomProclamation",
        "LightInDarkness",
        "Calling"
    ],
        "identity": [
        "[]JesusBringsLightToGalileeOfTheNations(Jesus, Galilee, Nations)"
    ],
        "unit_label": "Repent, for the Kingdom is at Hand",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "Crowds",
        "SimonPeter",
        "Andrew",
        "James",
        "John"
    ],
        "description": "Jesus fulfils Isaiah by bringing light to Galilee, proclaiming the kingdom, and calling disciples to follow him.",
        "lambda_iv": [
        "[]JesusBringsLightToGalileeOfTheNations(Jesus, Galilee, Nations)",
        "<>CallsDisciplesToFollow(Jesus, Disciples)"
    ],
    },

    {
        "passage_id": "Mat05_01_12",
        "chapter": 5,
        "verses": "1-12",
        "title": "Matthew 5:1–12 – The Beatitudes",
        "frames": [
        "Beatitudes",
        "UpsideDownBlessing",
        "Persecution"
    ],
        "identity": [
        "[]KingdomBlessednessBelongsToTheLowlyAndPersecutedInChrist(Kingdom, Lowly, Persecuted)"
    ],
        "unit_label": "Blessed Are...",
        "illocution": "Blessing",
        "agents": [
        "Jesus",
        "Disciples",
        "Crowds"
    ],
        "description": "Jesus pronounces blessing on the poor in spirit, the meek, the merciful, the pure, and the persecuted.",
        "lambda_iv": [
        "[]KingdomBlessednessBelongsToTheLowlyAndPersecutedInChrist(Kingdom, Lowly, Persecuted)",
        "EFF(PresentSufferingContrastedWithFutureReward(Disciples))"
    ],
    },

    {
        "passage_id": "Mat05_13_16",
        "chapter": 5,
        "verses": "13-16",
        "title": "Matthew 5:13–16 – Salt and Light",
        "frames": [
        "Witness",
        "Identity",
        "GloryOfGod"
    ],
        "identity": [
        "[]DisciplesAreConstitutivelySaltAndLightInTheWorld(Disciples, World)"
    ],
        "unit_label": "Public Holiness",
        "illocution": "Exhortation",
        "agents": [
        "Jesus",
        "Disciples",
        "World",
        "Father"
    ],
        "description": "Disciples are called salt and light whose good works are to lead others to glorify the Father.",
        "lambda_iv": [
        "[]DisciplesAreConstitutivelySaltAndLightInTheWorld(Disciples, World)",
        "<>DoGoodWorksToGlorifyFather(Disciples, Father)"
    ],
    },

    {
        "passage_id": "Mat05_17_20",
        "chapter": 5,
        "verses": "17-20",
        "title": "Matthew 5:17–20 – Fulfilment of the Law and Prophets",
        "frames": [
        "Law",
        "Fulfilment",
        "Righteousness"
    ],
        "identity": [
        "[]JesusFulfilsLawAndProphetsWithoutAbolishingThem(Jesus, Law, Prophets)"
    ],
        "unit_label": "Not an Iota, Not a Dot",
        "illocution": "ProgrammaticClaim",
        "agents": [
        "Jesus",
        "Disciples",
        "Law",
        "Prophets",
        "Scribes",
        "Pharisees"
    ],
        "description": "Jesus declares that he has come not to abolish the Law or the Prophets but to fulfil them, calling for exceeding righteousness.",
        "lambda_iv": [
        "[]JesusFulfilsLawAndProphetsWithoutAbolishingThem(Jesus, Law, Prophets)",
        "EFF(KingdomRighteousnessExceedsScribesAndPharisees(Righteousness, Disciples))"
    ],
    },

    {
        "passage_id": "Mat05_21_48",
        "chapter": 5,
        "verses": "21-48",
        "title": "Matthew 5:21–48 – Antitheses and Heart Righteousness",
        "frames": [
        "Ethic",
        "Heart",
        "LoveOfEnemies"
    ],
        "identity": [
        "[]KingdomEthicInternalisesAndIntensifiesTheLawAtHeartLevel(Jesus, Law, Heart)"
    ],
        "unit_label": "You Have Heard... But I Say to You",
        "illocution": "EthicalReframing",
        "agents": [
        "Jesus",
        "Disciples",
        "Enemies",
        "Father"
    ],
        "description": "Jesus deepens the Law's demands to anger, lust, oaths, retaliation, and enemy-love, revealing the Father's perfection.",
        "lambda_iv": [
        "[]KingdomEthicInternalisesAndIntensifiesTheLawAtHeartLevel(Jesus, Law, Heart)",
        "<>LoveEnemiesAsChildrenOfFather(Disciples, Enemies, Father)"
    ],
    },

    {
        "passage_id": "Mat06_01_18",
        "chapter": 6,
        "verses": "1-18",
        "title": "Matthew 6:1–18 – Giving, Prayer, and Fasting in Secret",
        "frames": [
        "Piety",
        "Hypocrisy",
        "Father"
    ],
        "identity": [
        "[]FatherWhoSeesInSecretRewardsHiddenFaithfulness(Father, Disciples)"
    ],
        "unit_label": "When You Give, Pray, Fast",
        "illocution": "Exhortation",
        "agents": [
        "Jesus",
        "Disciples",
        "Father",
        "Hypocrites"
    ],
        "description": "Jesus warns against hypocritical religion and calls disciples to secret devotion before their Father in heaven.",
        "lambda_iv": [
        "[]FatherWhoSeesInSecretRewardsHiddenFaithfulness(Father, Disciples)",
        "!<>PracticeRighteousnessToBeSeenByOthers(Disciples)"
    ],
    },

    {
        "passage_id": "Mat06_19_34",
        "chapter": 6,
        "verses": "19-34",
        "title": "Matthew 6:19–34 – Treasure, Masters, and Anxiety",
        "frames": [
        "Trust",
        "Wealth",
        "Anxiety"
    ],
        "identity": [
        "[]HeartFollowsTreasureThereforeTreasureMustBeInHeaven(Heart, Treasure)"
    ],
        "unit_label": "Seek First the Kingdom",
        "illocution": "Exhortation",
        "agents": [
        "Jesus",
        "Disciples",
        "Father"
    ],
        "description": "Jesus contrasts earthly and heavenly treasure and calls disciples away from anxiety toward trust in the Father's care.",
        "lambda_iv": [
        "[]HeartFollowsTreasureThereforeTreasureMustBeInHeaven(Heart, Treasure)",
        "<>SeekFirstKingdomAndRighteousness(Disciples, Kingdom)"
    ],
    },

    {
        "passage_id": "Mat07_01_12",
        "chapter": 7,
        "verses": "1-12",
        "title": "Matthew 7:1–12 – Judging, Asking, and the Golden Rule",
        "frames": [
        "Judgment",
        "Prayer",
        "Ethic"
    ],
        "identity": [
        "[]FatherGivesGoodGiftsToThoseWhoAskHim(Father, Disciples)"
    ],
        "unit_label": "Measure, Ask, Do",
        "illocution": "Exhortation",
        "agents": [
        "Jesus",
        "Disciples",
        "Father"
    ],
        "description": "Jesus warns about hypocritical judgment, encourages confident prayer, and summarises the Law and Prophets in the Golden Rule.",
        "lambda_iv": [
        "[]FatherGivesGoodGiftsToThoseWhoAskHim(Father, Disciples)",
        "EFF(GoldenRuleSummarisesLawAndProphets(Ethic))"
    ],
    },

    {
        "passage_id": "Mat07_13_29",
        "chapter": 7,
        "verses": "13-29",
        "title": "Matthew 7:13–29 – Two Ways, True and False, Rock and Sand",
        "frames": [
        "Warning",
        "Discipleship",
        "Judgment"
    ],
        "identity": [
        "[]EntranceToLifeIsThroughNarrowGateAndDifficultWay(Gate, Way)"
    ],
        "unit_label": "Narrow Gate and Wise Builder",
        "illocution": "Warning",
        "agents": [
        "Jesus",
        "Disciples",
        "FalseProphets",
        "Crowds"
    ],
        "description": "Jesus contrasts the narrow and broad ways, true and false prophets, genuine and counterfeit disciples, and wise and foolish builders.",
        "lambda_iv": [
        "[]EntranceToLifeIsThroughNarrowGateAndDifficultWay(Gate, Way)",
        "!<>MereHearingWithoutDoingLeadsToRuin(Disciples)"
    ],
    },

    {
        "passage_id": "Mat08_01_17",
        "chapter": 8,
        "verses": "1-17",
        "title": "Matthew 8:1–17 – Healings and the Servant's Burden",
        "frames": [
        "Healing",
        "Compassion",
        "ServantSong"
    ],
        "identity": [
        "[]JesusBearsOurInfirmitiesAndCarriesOurDiseases(Jesus, Sufferers)"
    ],
        "unit_label": "He Took Our Illnesses",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "Leper",
        "Centurion",
        "Peter",
        "Crowds"
    ],
        "description": "Jesus heals the unclean, the outsider's servant, and many sick, fulfilling that he took our illnesses and bore our diseases.",
        "lambda_iv": [
        "[]JesusBearsOurInfirmitiesAndCarriesOurDiseases(Jesus, Sufferers)",
        "EFF(HealingsAuthenticateHisMessianicIdentity(Jesus))"
    ],
    },

    {
        "passage_id": "Mat08_18_22",
        "chapter": 8,
        "verses": "18-22",
        "title": "Matthew 8:18–22 – The Cost of Following Jesus",
        "frames": [
        "Discipleship",
        "Cost",
        "Priority"
    ],
        "identity": [
        "[]FollowingJesusRequiresSupremeLoyaltyOverComfortAndFamily(Following, Cost)"
    ],
        "unit_label": "Let the Dead Bury Their Own Dead",
        "illocution": "RadicalCall",
        "agents": [
        "Jesus",
        "Scribe",
        "Disciple"
    ],
        "description": "Jesus confronts would-be disciples with the cost and urgency of following him.",
        "lambda_iv": [
        "[]FollowingJesusRequiresSupremeLoyaltyOverComfortAndFamily(Following, Cost)",
        "<>FollowJesusNowRatherThanDelay(Disciple, Jesus)"
    ],
    },

    {
        "passage_id": "Mat08_23_27",
        "chapter": 8,
        "verses": "23-27",
        "title": "Matthew 8:23–27 – Calming the Storm",
        "frames": [
        "Authority",
        "Creation",
        "Faith"
    ],
        "identity": [
        "[]JesusExercisesDivineAuthorityOverWindAndSea(Jesus, Creation)"
    ],
        "unit_label": "What Sort of Man Is This?",
        "illocution": "SignNarrative",
        "agents": [
        "Jesus",
        "Disciples"
    ],
        "description": "Jesus stills a great storm, exposing the disciples' little faith and revealing his divine authority.",
        "lambda_iv": [
        "[]JesusExercisesDivineAuthorityOverWindAndSea(Jesus, Creation)",
        "EFF(FearConfrontedByRevealedAuthority(Disciples, Jesus))"
    ],
    },

    {
        "passage_id": "Mat08_28_34",
        "chapter": 8,
        "verses": "28-34",
        "title": "Matthew 8:28–34 – Gadarene Demoniacs Delivered",
        "frames": [
        "Exorcism",
        "SpiritualWarfare",
        "Liberation"
    ],
        "identity": [
        "[]JesusSubduesDemonicPowersAndLiberatesTheOppressed(Jesus, Demons, Oppressed)"
    ],
        "unit_label": "My Name Is Legion",
        "illocution": "SignNarrative",
        "agents": [
        "Jesus",
        "Demoniacs",
        "Demons",
        "Herdsmen",
        "Townspeople"
    ],
        "description": "Jesus drives out a legion of demons, freeing the possessed men while the town begs him to leave.",
        "lambda_iv": [
        "[]JesusSubduesDemonicPowersAndLiberatesTheOppressed(Jesus, Demons, Oppressed)",
        "EFF(CityConfrontedWithHolyDisruption(Townspeople, Jesus))"
    ],
    },

    {
        "passage_id": "Mat09_01_08",
        "chapter": 9,
        "verses": "1-8",
        "title": "Matthew 9:1–8 – Paralytic Forgiven and Healed",
        "frames": [
        "AuthorityToForgive",
        "Healing",
        "Faith"
    ],
        "identity": [
        "[]SonOfManHasAuthorityOnEarthToForgiveSins(SonOfMan, Authority)"
    ],
        "unit_label": "Rise, Take Up Your Bed",
        "illocution": "SignAndClaim",
        "agents": [
        "Jesus",
        "Paralytic",
        "Scribes",
        "Crowds"
    ],
        "description": "Jesus forgives and heals a paralytic to demonstrate that the Son of Man has authority on earth to forgive sins.",
        "lambda_iv": [
        "[]SonOfManHasAuthorityOnEarthToForgiveSins(SonOfMan, Authority)",
        "EFF(VisibleHealingAuthenticatesInvisibleForgiveness(Jesus, Paralytic))"
    ],
    },

    {
        "passage_id": "Mat09_09_17",
        "chapter": 9,
        "verses": "9-17",
        "title": "Matthew 9:9–17 – Call of Matthew and New Wine",
        "frames": [
        "Calling",
        "TableFellowship",
        "NewCovenant"
    ],
        "identity": [
        "[]JesusCallsSinnersNotTheSelfRighteous(Jesus, Sinners)"
    ],
        "unit_label": "Follow Me; New Wine",
        "illocution": "CallAndParable",
        "agents": [
        "Jesus",
        "Matthew",
        "TaxCollectors",
        "Pharisees",
        "Disciples"
    ],
        "description": "Jesus calls Matthew, eats with sinners, and speaks of new wine that cannot be contained in old wineskins.",
        "lambda_iv": [
        "[]JesusCallsSinnersNotTheSelfRighteous(Jesus, Sinners)",
        "EFF(NewCovenantRealityCannotBeContainedInOldStructures(NewWine, OldWineskins))"
    ],
    },

    {
        "passage_id": "Mat09_18_38",
        "chapter": 9,
        "verses": "18-38",
        "title": "Matthew 9:18–38 – Healings, Compassion, and the Harvest",
        "frames": [
        "Healing",
        "Compassion",
        "Mission"
    ],
        "identity": [
        "[]JesussCompassionForHarassedAndHelplessCrowdsDrivesMission(Jesus, Crowds)"
    ],
        "unit_label": "Harassed and Helpless",
        "illocution": "NarrationAndExhortation",
        "agents": [
        "Jesus",
        "Crowds",
        "SynagogueLeader",
        "Woman",
        "BlindMen",
        "MuteMan",
        "Disciples"
    ],
        "description": "Jesus heals many and is moved with compassion for the harassed and helpless, urging prayer for workers.",
        "lambda_iv": [
        "[]JesussCompassionForHarassedAndHelplessCrowdsDrivesMission(Jesus, Crowds)",
        "<>PrayEarnestlyForLabourers(Disciples, Harvest)"
    ],
    },

    {
        "passage_id": "Mat10_01_42",
        "chapter": 10,
        "verses": "1-42",
        "title": "Matthew 10:1–42 – Mission Discourse",
        "frames": [
        "Mission",
        "Persecution",
        "Witness"
    ],
        "identity": [
        "[]JesusAuthorisesAndSendsDisciplesToExtendHisKingdomMinistry(Jesus, Disciples)"
    ],
        "unit_label": "Sheep Among Wolves",
        "illocution": "Commission",
        "agents": [
        "Jesus",
        "Twelve",
        "Fathers",
        "Authorities"
    ],
        "description": "Jesus commissions the Twelve, warning of persecution yet assuring the Father's care and reward.",
        "lambda_iv": [
        "[]JesusAuthorisesAndSendsDisciplesToExtendHisKingdomMinistry(Jesus, Disciples)",
        "EFF(MissionIncludesPersecutionUnderFathersCare(Disciples, Father))"
    ],
    },

    {
        "passage_id": "Mat11_01_30",
        "chapter": 11,
        "verses": "1-30",
        "title": "Matthew 11:1–30 – John’s Question, Woes, and Rest",
        "frames": [
        "Doubt",
        "Revelation",
        "Rest"
    ],
        "identity": [
        "[]JesusFulfilsIsaianicSignsAndRevealsTheFather(Jesus, Father)"
    ],
        "unit_label": "Offence and Rest",
        "illocution": "ResponseAndInvitation",
        "agents": [
        "Jesus",
        "John",
        "Disciples",
        "Cities"
    ],
        "description": "Jesus answers John's doubts with Isaianic signs, pronounces woes on unrepentant cities, and invites the weary to rest.",
        "lambda_iv": [
        "[]JesusFulfilsIsaianicSignsAndRevealsTheFather(Jesus, Father)",
        "<>ComeToJesusForRest(Weary, Jesus)"
    ],
    },

    {
        "passage_id": "Mat12_01_50",
        "chapter": 12,
        "verses": "1-50",
        "title": "Matthew 12:1–50 – Sabbath, Servant, Conflict, and True Family",
        "frames": [
        "Sabbath",
        "ServantSong",
        "Blasphemy",
        "Family"
    ],
        "identity": [
        "[]JesusIsMercifulLordOfSabbathAndSpiritAnointedServantForTheNations(Jesus, Nations)"
    ],
        "unit_label": "Something Greater Is Here",
        "illocution": "ConflictAndRevelation",
        "agents": [
        "Jesus",
        "Pharisees",
        "Crowds",
        "Family",
        "Spirit"
    ],
        "description": "Jesus reveals himself as Lord of the Sabbath and the Servant of Isaiah while confronting hardness and redefining family.",
        "lambda_iv": [
        "[]JesusIsMercifulLordOfSabbathAndSpiritAnointedServantForTheNations(Jesus, Nations)",
        "!<>AttributeSpiritsWorkToSatan(Observers, Spirit)"
    ],
    },

    {
        "passage_id": "Mat13_01_23",
        "chapter": 13,
        "verses": "1-23",
        "title": "Matthew 13:1–23 – Parable of the Sower and Its Explanation",
        "frames": [
        "Parable",
        "Reception",
        "Word"
    ],
        "identity": [
        "[]KingdomWordProducesFruitInGoodSoilButIsResistedElsewhere(Word, Soils)"
    ],
        "unit_label": "He Who Has Ears, Let Him Hear",
        "illocution": "ParableAndExplanation",
        "agents": [
        "Jesus",
        "Crowds",
        "Disciples"
    ],
        "description": "Jesus explains varied responses to the word of the kingdom through the parable of the sower.",
        "lambda_iv": [
        "[]KingdomWordProducesFruitInGoodSoilButIsResistedElsewhere(Word, Soils)",
        "EFF(HearingWithUnderstandingYieldsFruit(Disciple))"
    ],
    },

    {
        "passage_id": "Mat13_24_30",
        "chapter": 13,
        "verses": "24-30",
        "title": "Matthew 13:24–30 – Parable of the Weeds",
        "frames": [
        "Parable",
        "Patience",
        "Judgment"
    ],
        "identity": [
        "[]KingdomPresentlyMixedWithEvilUntilFinalJudgment(Kingdom, Field)"
    ],
        "unit_label": "Let Both Grow Together",
        "illocution": "Parable",
        "agents": [
        "Jesus",
        "Disciples"
    ],
        "description": "Jesus portrays the kingdom as wheat among weeds that will only be separated at the harvest.",
        "lambda_iv": [
        "[]KingdomPresentlyMixedWithEvilUntilFinalJudgment(Kingdom, Field)",
        "<>FinalSeparationAtEschatologicalHarvest(Harvest, SonOfMan)"
    ],
    },

    {
        "passage_id": "Mat13_31_33",
        "chapter": 13,
        "verses": "31-33",
        "title": "Matthew 13:31–33 – Mustard Seed and Leaven",
        "frames": [
        "Parable",
        "Growth",
        "Hiddenness"
    ],
        "identity": [
        "[]KingdomBeginsSmallYetGrowsLargeAndPermeatesAll(Kingdom)"
    ],
        "unit_label": "From Small to Great",
        "illocution": "Parable",
        "agents": [
        "Jesus",
        "Disciples"
    ],
        "description": "Through mustard seed and leaven Jesus shows the kingdom's disproportionate, permeating growth.",
        "lambda_iv": [
        "[]KingdomBeginsSmallYetGrowsLargeAndPermeatesAll(Kingdom)",
        "EFF(HiddenGrowthLeadsToVisibleShelterAndTransformation(Kingdom))"
    ],
    },

    {
        "passage_id": "Mat13_44_50",
        "chapter": 13,
        "verses": "44-50",
        "title": "Matthew 13:44–50 – Treasure, Pearl, and Net",
        "frames": [
        "Parable",
        "Value",
        "Judgment"
    ],
        "identity": [
        "[]KingdomIsOfSurpassingValueAndEndsWithSeparation(Kingdom)"
    ],
        "unit_label": "Joyful Loss and Final Sorting",
        "illocution": "Parable",
        "agents": [
        "Jesus",
        "Disciples",
        "Angels"
    ],
        "description": "Jesus depicts the kingdom as treasure worth joyful loss and a net that brings final separation.",
        "lambda_iv": [
        "[]KingdomIsOfSurpassingValueAndEndsWithSeparation(Kingdom)",
        "<>JoyfullySellAllForKingdom(Disciple, Kingdom)"
    ],
    },

    {
        "passage_id": "Mat13_53_58",
        "chapter": 13,
        "verses": "53-58",
        "title": "Matthew 13:53–58 – Rejection at Nazareth",
        "frames": [
        "Rejection",
        "Unbelief",
        "Prophet"
    ],
        "identity": [
        "[]ProphetWithoutHonourInHisHometown(Jesus, Nazareth)"
    ],
        "unit_label": "Astonishment and Offence",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "Nazarenes"
    ],
        "description": "Jesus is rejected in his hometown, and their unbelief limits mighty works.",
        "lambda_iv": [
        "[]ProphetWithoutHonourInHisHometown(Jesus, Nazareth)",
        "EFF(UnbeliefReducesParticipationInDisplayedPower(Nazarenes, Jesus))"
    ],
    },

    {
        "passage_id": "Mat14_13_21",
        "chapter": 14,
        "verses": "13-21",
        "title": "Matthew 14:13–21 – Feeding the Five Thousand",
        "frames": [
        "Provision",
        "Compassion",
        "Banquet"
    ],
        "identity": [
        "[]JesusFeedsCrowdsInWildernessAsNewShepherdAndHost(Jesus, Crowds)"
    ],
        "unit_label": "You Give Them Something to Eat",
        "illocution": "SignNarrative",
        "agents": [
        "Jesus",
        "Disciples",
        "Crowds"
    ],
        "description": "Jesus has compassion on the crowds and feeds them abundantly in the wilderness.",
        "lambda_iv": [
        "[]JesusFeedsCrowdsInWildernessAsNewShepherdAndHost(Jesus, Crowds)",
        "EFF(ScarcityBecomesAbundanceInHisHands(Loaves, Fish))"
    ],
    },

    {
        "passage_id": "Mat14_22_33",
        "chapter": 14,
        "verses": "22-33",
        "title": "Matthew 14:22–33 – Jesus Walks on the Sea",
        "frames": [
        "Presence",
        "Faith",
        "Worship"
    ],
        "identity": [
        "[]JesusComesAsIDoNotBeAfraidLordOfSea(Jesus, Disciples)"
    ],
        "unit_label": "Truly You Are the Son of God",
        "illocution": "SignNarrative",
        "agents": [
        "Jesus",
        "Peter",
        "Disciples"
    ],
        "description": "Jesus walks on the water, saves sinking Peter, and receives worship as the Son of God.",
        "lambda_iv": [
        "[]JesusComesAsIDoNotBeAfraidLordOfSea(Jesus, Disciples)",
        "EFF(WorshipArisesFromRescuedFear(Disciples, Jesus))"
    ],
    },

    {
        "passage_id": "Mat15_01_20",
        "chapter": 15,
        "verses": "1-20",
        "title": "Matthew 15:1–20 – Tradition, Defilement, and the Heart",
        "frames": [
        "Purity",
        "Tradition",
        "Heart"
    ],
        "identity": [
        "[]TrueDefilementFlowsFromHeartNotFromRitualFood(Law, Heart)"
    ],
        "unit_label": "This People Honours Me with Their Lips",
        "illocution": "Controversy",
        "agents": [
        "Jesus",
        "Pharisees",
        "Scribes",
        "Crowds",
        "Disciples"
    ],
        "description": "Jesus exposes the emptiness of human tradition and redefines defilement as flowing from the heart.",
        "lambda_iv": [
        "[]TrueDefilementFlowsFromHeartNotFromRitualFood(Law, Heart)",
        "!<>ElevateHumanTraditionsOverGodsCommand(Teachers)"
    ],
    },

    {
        "passage_id": "Mat15_21_28",
        "chapter": 15,
        "verses": "21-28",
        "title": "Matthew 15:21–28 – Canaanite Woman’s Faith",
        "frames": [
        "Faith",
        "Inclusion",
        "Persistence"
    ],
        "identity": [
        "[]GentileFaithInMessiahIsWelcomedIntoCovenantMercy(Gentiles, Jesus)"
    ],
        "unit_label": "Even the Dogs Eat the Crumbs",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "CanaaniteWoman",
        "Disciples"
    ],
        "description": "A Gentile woman perseveres in faith and receives deliverance for her daughter.",
        "lambda_iv": [
        "[]GentileFaithInMessiahIsWelcomedIntoCovenantMercy(Gentiles, Jesus)",
        "EFF(PersistentFaithReceivesMercyFromJesus(CanaaniteWoman, Jesus))"
    ],
    },

    {
        "passage_id": "Mat16_13_20",
        "chapter": 16,
        "verses": "13-20",
        "title": "Matthew 16:13–20 – Peter’s Confession and the Keys",
        "frames": [
        "Christology",
        "Church",
        "Authority"
    ],
        "identity": [
        "[]JesusIsTheChristTheSonOfTheLivingGod(Jesus, Father)"
    ],
        "unit_label": "On This Rock I Will Build My Church",
        "illocution": "Revelation",
        "agents": [
        "Jesus",
        "Peter",
        "Disciples"
    ],
        "description": "Peter confesses Jesus as the Christ, and Jesus promises to build his church and gives the keys of the kingdom.",
        "lambda_iv": [
        "[]JesusIsTheChristTheSonOfTheLivingGod(Jesus, Father)",
        "EFF(ChurchBuiltOnConfessedChristAndGivenKeys(Church, Jesus))"
    ],
    },

    {
        "passage_id": "Mat16_21_28",
        "chapter": 16,
        "verses": "21-28",
        "title": "Matthew 16:21–28 – First Passion Prediction and the Cross",
        "frames": [
        "Cross",
        "Discipleship",
        "Glory"
    ],
        "identity": [
        "[]SonOfManMustSufferBeKilledAndBeRaisedOnThirdDay(SonOfMan)"
    ],
        "unit_label": "Take Up Your Cross",
        "illocution": "PredictionAndCall",
        "agents": [
        "Jesus",
        "Disciples",
        "Peter"
    ],
        "description": "Jesus foretells his suffering and calls disciples to take up their cross and follow him.",
        "lambda_iv": [
        "[]SonOfManMustSufferBeKilledAndBeRaisedOnThirdDay(SonOfMan)",
        "<>FollowByLosingLifeToFindIt(Disciple, Jesus)"
    ],
    },

    {
        "passage_id": "Mat17_01_13",
        "chapter": 17,
        "verses": "1-13",
        "title": "Matthew 17:1–13 – Transfiguration",
        "frames": [
        "Glory",
        "Sonship",
        "Prophets"
    ],
        "identity": [
        "[]JesusIsBelovedSonToWhomLawAndProphetsBearWitness(Jesus, Moses, Elijah)"
    ],
        "unit_label": "Listen to Him",
        "illocution": "Theophany",
        "agents": [
        "Jesus",
        "Peter",
        "James",
        "John",
        "Moses",
        "Elijah",
        "Father"
    ],
        "description": "Jesus is transfigured before three disciples as the beloved Son with Moses and Elijah.",
        "lambda_iv": [
        "[]JesusIsBelovedSonToWhomLawAndProphetsBearWitness(Jesus, Moses, Elijah)",
        "<>ListenToHimAsClimacticRevelation(Disciples, Jesus)"
    ],
    },

    {
        "passage_id": "Mat17_14_27",
        "chapter": 17,
        "verses": "14-27",
        "title": "Matthew 17:14–27 – Healing the Boy and Temple Tax",
        "frames": [
        "Faith",
        "Authority",
        "Sonship"
    ],
        "identity": [
        "[]JesusAsTrueSonIsFreeYetChoosesNotToGiveOffence(Jesus, Temple)"
    ],
        "unit_label": "Little Faith and the Sons Are Free",
        "illocution": "NarrationAndTeaching",
        "agents": [
        "Jesus",
        "Disciples",
        "Father",
        "Crowds",
        "Boy",
        "Demon"
    ],
        "description": "Jesus heals a demon-possessed boy amid little faith and teaches about freedom and humility regarding temple tax.",
        "lambda_iv": [
        "[]JesusAsTrueSonIsFreeYetChoosesNotToGiveOffence(Jesus, Temple)",
        "EFF(FaithNeededForParticipationInHisPower(Disciples, Jesus))"
    ],
    },

    {
        "passage_id": "Mat18_01_35",
        "chapter": 18,
        "verses": "1-35",
        "title": "Matthew 18:1–35 – Community Discourse",
        "frames": [
        "Community",
        "Humility",
        "Forgiveness"
    ],
        "identity": [
        "[]KingdomCommunityIsMarkedByHumilityCareAndLimitlessForgiveness(Community)"
    ],
        "unit_label": "Greatest in the Kingdom",
        "illocution": "Discourse",
        "agents": [
        "Jesus",
        "Disciples"
    ],
        "description": "Jesus teaches about greatness, stumbling blocks, restoration, and limitless forgiveness.",
        "lambda_iv": [
        "[]KingdomCommunityIsMarkedByHumilityCareAndLimitlessForgiveness(Community)",
        "<>ForgiveFromHeartAsForgivenServants(Disciples, Offenders)"
    ],
    },

    {
        "passage_id": "Mat19_01_12",
        "chapter": 19,
        "verses": "1-12",
        "title": "Matthew 19:1–12 – Marriage, Divorce, and Creation",
        "frames": [
        "Marriage",
        "Creation",
        "HardnessOfHeart"
    ],
        "identity": [
        "[]FromBeginningCreatorMadeMarriageAsCovenantUnionOfMaleAndFemale(Creator, Marriage)"
    ],
        "unit_label": "What God Has Joined Together",
        "illocution": "Teaching",
        "agents": [
        "Jesus",
        "Pharisees",
        "Disciples"
    ],
        "description": "Jesus returns to Genesis to teach about marriage, divorce, and celibacy for the kingdom.",
        "lambda_iv": [
        "[]FromBeginningCreatorMadeMarriageAsCovenantUnionOfMaleAndFemale(Creator, Marriage)",
        "!<>DivorceWithoutRegardForGodsDesign(Spouses)"
    ],
    },

    {
        "passage_id": "Mat19_13_30",
        "chapter": 19,
        "verses": "13-30",
        "title": "Matthew 19:13–30 – Children and the Rich Young Man",
        "frames": [
        "ChildlikeFaith",
        "Wealth",
        "Reward"
    ],
        "identity": [
        "[]KingdomBelongsToChildlikeAndWealthIsDangerousRivalMaster(Kingdom, Wealth)"
    ],
        "unit_label": "Hard for the Rich",
        "illocution": "NarrationAndTeaching",
        "agents": [
        "Jesus",
        "Children",
        "Disciples",
        "RichYoungMan"
    ],
        "description": "Jesus welcomes children, confronts a rich seeker, and promises reward for those who leave all to follow him.",
        "lambda_iv": [
        "[]KingdomBelongsToChildlikeAndWealthIsDangerousRivalMaster(Kingdom, Wealth)",
        "<>LeaveAllForJesusAndReceiveEternalLife(Disciple, Jesus)"
    ],
    },

    {
        "passage_id": "Mat20_01_16",
        "chapter": 20,
        "verses": "1-16",
        "title": "Matthew 20:1–16 – Parable of the Workers in the Vineyard",
        "frames": [
        "Parable",
        "Grace",
        "Reversal"
    ],
        "identity": [
        "[]KingdomRewardOperatesByGenerousGraceNotStrictProportionalMerit(Kingdom)"
    ],
        "unit_label": "The Last Will Be First",
        "illocution": "Parable",
        "agents": [
        "Jesus",
        "Disciples"
    ],
        "description": "Jesus tells a parable where equal wages expose envy and highlight generous grace.",
        "lambda_iv": [
        "[]KingdomRewardOperatesByGenerousGraceNotStrictProportionalMerit(Kingdom)",
        "!<>GrumbleAgainstGenerousMasterForHisGrace(Workers)"
    ],
    },

    {
        "passage_id": "Mat20_17_28",
        "chapter": 20,
        "verses": "17-28",
        "title": "Matthew 20:17–28 – Third Passion Prediction and Servant Greatness",
        "frames": [
        "Cross",
        "Servanthood",
        "Ambition"
    ],
        "identity": [
        "[]SonOfManGivesHisLifeAsRansomForMany(SonOfMan, Many)"
    ],
        "unit_label": "Not So Among You",
        "illocution": "PredictionAndEthic",
        "agents": [
        "Jesus",
        "Disciples",
        "James",
        "John",
        "MotherOfSons"
    ],
        "description": "Jesus again foretells his suffering and redefines greatness as servanthood patterned after his own self-giving.",
        "lambda_iv": [
        "[]SonOfManGivesHisLifeAsRansomForMany(SonOfMan, Many)",
        "<>BecomeServantAndSlaveForSakeOfOthers(Disciples, Others)"
    ],
    },

    {
        "passage_id": "Mat20_29_34",
        "chapter": 20,
        "verses": "29-34",
        "title": "Matthew 20:29–34 – Two Blind Men Receive Sight",
        "frames": [
        "Healing",
        "Sight",
        "Discipleship"
    ],
        "identity": [
        "[]JesusOpensEyesOfMercySeekersWhoCryForSonOfDavid(Jesus, BlindMen)"
    ],
        "unit_label": "Lord, Let Our Eyes Be Opened",
        "illocution": "Narration",
        "agents": [
        "Jesus",
        "BlindMen",
        "Crowds"
    ],
        "description": "Two blind men cry out to the Son of David for mercy and receive sight, following him.",
        "lambda_iv": [
        "[]JesusOpensEyesOfMercySeekersWhoCryForSonOfDavid(Jesus, BlindMen)",
        "EFF(MercyReceivedLeadsToFollowing(BlindMen, Jesus))"
    ],
    },

    {
        "passage_id": "Mat21_01_22",
        "chapter": 21,
        "verses": "1-22",
        "title": "Matthew 21:1–22 – Entry, Temple, and Fig Tree",
        "frames": [
        "Kingship",
        "Judgment",
        "HouseOfPrayer"
    ],
        "identity": [
        "[]JesusEntersAsMessianicKingAndJudgesFruitlessReligion(Jesus, Temple)"
    ],
        "unit_label": "Hosanna and Withered Fig Tree",
        "illocution": "SymbolicAction",
        "agents": [
        "Jesus",
        "Crowds",
        "Children",
        "ChiefPriests",
        "Scribes",
        "FigTree"
    ],
        "description": "Jesus enters Jerusalem as king, cleanses the temple, and curses a fruitless fig tree as enacted parable.",
        "lambda_iv": [
        "[]JesusEntersAsMessianicKingAndJudgesFruitlessReligion(Jesus, Temple)",
        "EFF(FaithAndPrayerAreMarkedAsTrueTempleFruit(Disciples, Prayer))"
    ],
    },

    {
        "passage_id": "Mat22_34_40",
        "chapter": 22,
        "verses": "34-40",
        "title": "Matthew 22:34–40 – The Great Commandment",
        "frames": [
        "Law",
        "Love",
        "Summary"
    ],
        "identity": [
        "[]WholeLawAndProphetsHangOnLoveForGodAndNeighbour(Law, Love)"
    ],
        "unit_label": "On These Two Commandments",
        "illocution": "Teaching",
        "agents": [
        "Jesus",
        "Pharisees",
        "Lawyer"
    ],
        "description": "In response to a test, Jesus summarises the Law and the Prophets as love for God and neighbour.",
        "lambda_iv": [
        "[]WholeLawAndProphetsHangOnLoveForGodAndNeighbour(Law, Love)",
        "EFF(LoveOfGodAndNeighbourIsCanonicalSummation(Commands))"
    ],
    },

    {
        "passage_id": "Mat23_01_39",
        "chapter": 23,
        "verses": "1-39",
        "title": "Matthew 23:1–39 – Woes on the Scribes and Pharisees and Lament",
        "frames": [
        "Woe",
        "Hypocrisy",
        "Lament"
    ],
        "identity": [
        "[]JesusAsPropheticLordPronouncesWoeOnHypocrisyYetLamentsJerusalem(Jesus, Jerusalem)"
    ],
        "unit_label": "Woe and How Often Would I",
        "illocution": "WoeOracleAndLament",
        "agents": [
        "Jesus",
        "Scribes",
        "Pharisees",
        "Crowds",
        "Jerusalem"
    ],
        "description": "Jesus exposes religious hypocrisy in woes and laments over Jerusalem's hardness.",
        "lambda_iv": [
        "[]JesusAsPropheticLordPronouncesWoeOnHypocrisyYetLamentsJerusalem(Jesus, Jerusalem)",
        "EFF(DivineLamentPrecedesJudgmentOnUnrepentantCity(Jerusalem))"
    ],
    },

    {
        "passage_id": "Mat24_01_51",
        "chapter": 24,
        "verses": "1-51",
        "title": "Matthew 24:1–51 – Eschatological Discourse Part 1",
        "frames": [
        "Eschatology",
        "Watchfulness",
        "BirthPains"
    ],
        "identity": [
        "[]JesusIsPropheticSonOfManWhoForetellsJudgmentAndCallsToWatchfulness(Jesus, Disciples)"
    ],
        "unit_label": "See That No One Leads You Astray",
        "illocution": "ApocalypticDiscourse",
        "agents": [
        "Jesus",
        "Disciples"
    ],
        "description": "Jesus foretells temple destruction, tribulation, and coming of the Son of Man, urging watchfulness.",
        "lambda_iv": [
        "[]JesusIsPropheticSonOfManWhoForetellsJudgmentAndCallsToWatchfulness(Jesus, Disciples)",
        "<>StayAwakeAndEndureToTheEnd(Disciples)"
    ],
    },

    {
        "passage_id": "Mat25_01_13",
        "chapter": 25,
        "verses": "1-13",
        "title": "Matthew 25:1–13 – Parable of the Ten Virgins",
        "frames": [
        "Parable",
        "Readiness",
        "Delay"
    ],
        "identity": [
        "[]KingdomRequiresWatchfulReadinessAmidDelayForBridegroom(Kingdom, Bridegroom)"
    ],
        "unit_label": "Be Ready",
        "illocution": "Parable",
        "agents": [
        "Jesus",
        "Disciples"
    ],
        "description": "Jesus portrays wise and foolish virgins to stress readiness for the delayed bridegroom.",
        "lambda_iv": [
        "[]KingdomRequiresWatchfulReadinessAmidDelayForBridegroom(Kingdom, Bridegroom)",
        "!<>BorrowReadinessAtLastMoment(FoolishVirgins)"
    ],
    },

    {
        "passage_id": "Mat25_14_30",
        "chapter": 25,
        "verses": "14-30",
        "title": "Matthew 25:14–30 – Parable of the Talents",
        "frames": [
        "Parable",
        "Stewardship",
        "Accountability"
    ],
        "identity": [
        "[]ServantsAreEntrustedWithMastersResourcesAndMustGiveAccount(Servants, Master)"
    ],
        "unit_label": "Well Done, Good and Faithful Servant",
        "illocution": "Parable",
        "agents": [
        "Jesus",
        "Disciples"
    ],
        "description": "Jesus likens the kingdom to a master entrusting resources and returning for reckoning.",
        "lambda_iv": [
        "[]ServantsAreEntrustedWithMastersResourcesAndMustGiveAccount(Servants, Master)",
        "<>InvestFaithfullyRatherThanHideThroughFear(Servants, Master)"
    ],
    },

    {
        "passage_id": "Mat25_31_46",
        "chapter": 25,
        "verses": "31-46",
        "title": "Matthew 25:31–46 – Sheep and Goats",
        "frames": [
        "Judgment",
        "Mercy",
        "Presence"
    ],
        "identity": [
        "[]SonOfManJudgesNationsByMercyShownToHisBrothers(SonOfMan, Nations, Brothers)"
    ],
        "unit_label": "As You Did It to One of the Least",
        "illocution": "JudgmentOracle",
        "agents": [
        "SonOfMan",
        "Nations",
        "Brothers"
    ],
        "description": "The Son of Man separates nations on the basis of their treatment of 'the least of these' his brothers.",
        "lambda_iv": [
        "[]SonOfManJudgesNationsByMercyShownToHisBrothers(SonOfMan, Nations, Brothers)",
        "EFF(MercyToLeastIsReceivedAsDoneToChrist(Actors, Christ))"
    ],
    },

    {
        "passage_id": "Mat26_17_46",
        "chapter": 26,
        "verses": "17-46",
        "title": "Matthew 26:17–46 – Last Supper and Gethsemane",
        "frames": [
        "Passover",
        "Covenant",
        "Agony"
    ],
        "identity": [
        "[]JesusInstitutesNewCovenantInHisBloodAndSubmitsToFathersWill(Jesus, Father)"
    ],
        "unit_label": "This Is My Blood of the Covenant",
        "illocution": "InstitutionAndPrayer",
        "agents": [
        "Jesus",
        "Disciples",
        "Father"
    ],
        "description": "Jesus shares Passover, institutes the covenant meal, and prays in anguish yet submits to the Father's will.",
        "lambda_iv": [
        "[]JesusInstitutesNewCovenantInHisBloodAndSubmitsToFathersWill(Jesus, Father)",
        "<>NotMyWillButYoursBeDone(Jesus, Father)"
    ],
    },

    {
        "passage_id": "Mat27_27_54",
        "chapter": 27,
        "verses": "27-54",
        "title": "Matthew 27:27–54 – Crucifixion and Signs",
        "frames": [
        "Crucifixion",
        "Mockery",
        "Recognition"
    ],
        "identity": [
        "[]CrucifiedJesusIsTrulySonOfGodWhoseDeathOpensAccessToGod(Jesus, Father)"
    ],
        "unit_label": "Truly This Was the Son of God",
        "illocution": "PassionNarrative",
        "agents": [
        "Jesus",
        "Soldiers",
        "Crowds",
        "Centurion",
        "Bystanders"
    ],
        "description": "Jesus is mocked, crucified, and dies with cosmic signs, leading the centurion to confess him as Son of God.",
        "lambda_iv": [
        "[]CrucifiedJesusIsTrulySonOfGodWhoseDeathOpensAccessToGod(Jesus, Father)",
        "EFF(VeilTornAndEarthShakenAtHisDeath(Signs, Temple))"
    ],
    },

    {
        "passage_id": "Mat28_01_10",
        "chapter": 28,
        "verses": "1-10",
        "title": "Matthew 28:1–10 – Resurrection and First Witnesses",
        "frames": [
        "Resurrection",
        "FearAndJoy",
        "Worship"
    ],
        "identity": [
        "[]JesusIsRisenAsHeSaidAndMeetsHisFollowers(Jesus, Followers)"
    ],
        "unit_label": "Fear and Great Joy",
        "illocution": "ResurrectionNarrative",
        "agents": [
        "Jesus",
        "Women",
        "Angel"
    ],
        "description": "Women find the tomb empty, hear of Jesus' resurrection, and meet the risen Lord.",
        "lambda_iv": [
        "[]JesusIsRisenAsHeSaidAndMeetsHisFollowers(Jesus, Followers)",
        "EFF(FearTurnsToJoyAndWorshipAtRisenPresence(Followers, Jesus))"
    ],
    },

    {
        "passage_id": "Mat28_16_20",
        "chapter": 28,
        "verses": "16-20",
        "title": "Matthew 28:16–20 – The Great Commission",
        "frames": [
        "Mission",
        "Authority",
        "Presence"
    ],
        "identity": [
        "[]RisenJesusHasAllAuthorityAndRemainsWithDisciplesInMission(Jesus, Disciples)"
    ],
        "unit_label": "Make Disciples of All Nations",
        "illocution": "Commission",
        "agents": [
        "Jesus",
        "Eleven"
    ],
        "description": "The risen Christ commissions his disciples to make disciples of all nations in the presence of his abiding authority.",
        "lambda_iv": [
        "[]RisenJesusHasAllAuthorityAndRemainsWithDisciplesInMission(Jesus, Disciples)",
        "<>GoBaptiseTeachToObeyAllHeCommanded(Disciples, Nations)"
    ],
    },

]


def main() -> None:
    for p in PERICOPES:
        pid = p["passage_id"]
        chapter = p["chapter"]
        verses_str = p["verses"]

        data = {
            "meta": {
                **META_BASE,
                "book": "Matthew",
                "passage_id": pid,
                "version": f"{pid}_Lambda_IV_v0.1",
            },
            "passage_id": pid,
            "book": "Matthew",
            "chapter": chapter,
            "verses": verses_str,
            "title": p["title"],
            "interpretive_frames": p["frames"],
            "identity_invariants": p["identity"],
            "units": [
                {
                    "id": f"{pid}_u1",
                    "label": p["unit_label"],
                    "verses": parse_verses(verses_str),
                    "illocution": p["illocution"],
                    "agents": p["agents"],
                    "statements": [
                        {
                            "id": f"{pid}_s1",
                            "type": "summary",
                            "description": p["description"],
                            "lambda_iv": p["lambda_iv"],
                        }
                    ],
                }
            ],
        }

        out_path = OUTPUT_DIR / f"{pid}.lambda.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Wrote {out_path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
