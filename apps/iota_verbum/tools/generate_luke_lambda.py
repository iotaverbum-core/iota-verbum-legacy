"""
Utility script to generate Modal Bible λ-files for the Gospel of Luke.

Pattern matches modal_bible/mark/mark_04_26_29.lambda.json and the
Matthew generator: one JSON per pericope.

Usage (from project root):

    (.venv) python tools/generate_luke_lambda.py

It will create / overwrite files under modal_bible/luke/.
"""

from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "modal_bible" / "luke"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_verses(verses_str: str) -> list[int]:
    """
    Very small helper: "1-17" -> [1, 2, ..., 17]
    """
    start_str, end_str = verses_str.split("-")
    start, end = int(start_str), int(end_str)
    return list(range(start, end + 1))


META_BASE = {
    "author": "Iota Verbum – Modal Bible Prototype",
    "encoding": "Lambda_IV_v0.1",
    "notes": "Auto-generated Luke λ-files; safe to hand-edit after generation.",
}

PERICOPES = [    {
        "passage_id": "Luk05_01_11",
        "chapter": 5,
        "verses": "1-11",
        "title": "Luke 5:1–11 – Miraculous Catch and Call of Peter",
        "frames": [
            "Call",
            "Obedience",
            "Mission",
        ],
        "identity": [
            "[]JesusCallsSinnersIntoMissionThroughHolyFearAndTrust(Jesus, Peter, Disciples)",
        ],
        "unit_label": "From Nets to Catching People",
        "illocution": "CallNarrative",
        "agents": [
            "Jesus",
            "SimonPeter",
            "James",
            "John",
            "Crowds",
        ],
        "description": (
            "After a miraculous catch of fish at Jesus command, Peter falls in fear and is "
            "called with his partners to leave everything and catch people."
        ),
        "lambda_iv": [
            "[]JesusCallsSinnersIntoMissionThroughHolyFearAndTrust(Jesus, Peter, Disciples)",
            "EFF(AbandoningOldSecurityToFollowJesusIntoMission(Disciples))",
        ],
    },

    {
        "passage_id": "Luk05_12_26",
        "chapter": 5,
        "verses": "12-26",
        "title": "Luke 5:12–26 – Cleansing the Leper and Forgiving the Paralytic",
        "frames": [
            "Purity",
            "AuthorityToForgive",
            "Faith",
        ],
        "identity": [
            "[]JesusHasAuthorityToCleanseImpurityAndForgiveSins(Jesus, Impure, Sinners)",
        ],
        "unit_label": "Who Can Forgive Sins but God Alone?",
        "illocution": "MiracleAndControversy",
        "agents": [
            "Jesus",
            "Leper",
            "Paralytic",
            "Friends",
            "ScribesAndPharisees",
        ],
        "description": (
            "Jesus touches and cleanses a leper and then heals a paralytic to demonstrate his "
            "authority on earth to forgive sins."
        ),
        "lambda_iv": [
            "[]JesusHasAuthorityToCleanseImpurityAndForgiveSins(Jesus, Impure, Sinners)",
            "EFF(FaithBreaksThroughObstaclesToReachJesus(Friends, Paralytic))",
        ],
    },

    {
        "passage_id": "Luk05_27_39",
        "chapter": 5,
        "verses": "27-39",
        "title": "Luke 5:27–39 – Levi Called, New Wine in New Wineskins",
        "frames": [
            "Call",
            "TableFellowship",
            "Newness",
        ],
        "identity": [
            "[]JesusCallsSinnersAndBringsNewCovenantReality(Jesus, Levi, Sinners)",
        ],
        "unit_label": "I Have Not Come to Call the Righteous",
        "illocution": "CallAndParable",
        "agents": [
            "Jesus",
            "Levi",
            "TaxCollectors",
            "Pharisees",
            "Disciples",
        ],
        "description": (
            "Jesus calls Levi, eats with tax collectors and sinners, defends his mission, and "
            "teaches that new wine requires new wineskins."
        ),
        "lambda_iv": [
            "[]JesusCallsSinnersAndBringsNewCovenantReality(Jesus, Levi, Sinners)",
            "EFF(ReligiousResistanceToMercyRevealsAttachmentToOldForms(Pharisees))",
        ],
    },

    {
        "passage_id": "Luk06_12_26",
        "chapter": 6,
        "verses": "12-26",
        "title": "Luke 6:12–26 – Twelve Apostles and Blessings and Woes",
        "frames": [
            "Apostles",
            "Blessing",
            "Reversal",
        ],
        "identity": [
            "[]JesusConstitutesNewPeopleAroundHimselfWithReversedFortunes(Jesus, Apostles, Poor, Rich)",
        ],
        "unit_label": "Blessed Are You Who Are Poor",
        "illocution": "ConstitutionSpeech",
        "agents": [
            "Jesus",
            "TwelveApostles",
            "Disciples",
            "Crowds",
        ],
        "description": (
            "Jesus chooses twelve apostles and pronounces blessings on the poor and woes on the "
            "rich, redefining who is truly blessed."
        ),
        "lambda_iv": [
            "[]JesusConstitutesNewPeopleAroundHimselfWithReversedFortunes(Jesus, Apostles, Poor, Rich)",
            "EFF(ValuesOfKingdomInvertWorldlyMeasuresOfSuccess(Disciples))",
        ],
    },

    {
        "passage_id": "Luk06_27_49",
        "chapter": 6,
        "verses": "27-49",
        "title": "Luke 6:27–49 – Love for Enemies and House on the Rock",
        "frames": [
            "Ethics",
            "LoveOfEnemies",
            "HearingAndDoing",
        ],
        "identity": [
            "[]KingdomEthicDemandsEnemyLoveAndObedientHearingOfJesusWords(Disciples, Enemies)",
        ],
        "unit_label": "Why Do You Call Me Lord and Not Do?",
        "illocution": "EthicalInstruction",
        "agents": [
            "Jesus",
            "Disciples",
            "Enemies",
            "Hearers",
        ],
        "description": (
            "Jesus commands love of enemies, non-retaliation, generous mercy, and calls hearers "
            "to build their lives on obedient practice of his words."
        ),
        "lambda_iv": [
            "[]KingdomEthicDemandsEnemyLoveAndObedientHearingOfJesusWords(Disciples, Enemies)",
            "EFF(ObedientPracticeCreatesEnduringHouseAmidStorms(Disciples))",
        ],
    },

    {
        "passage_id": "Luk07_11_17",
        "chapter": 7,
        "verses": "11-17",
        "title": "Luke 7:11–17 – Raising the Widow’s Son at Nain",
        "frames": [
            "Compassion",
            "Death",
            "PropheticPower",
        ],
        "identity": [
            "[]JesusHasCompassionateAuthorityOverDeath(Jesus, Dead, Bereaved)",
        ],
        "unit_label": "Do Not Weep",
        "illocution": "MiracleNarrative",
        "agents": [
            "Jesus",
            "Widow",
            "DeadSon",
            "Crowds",
        ],
        "description": (
            "Jesus is moved with compassion for a widows loss, raises her son, and the people "
            "confess that God has visited his people."
        ),
        "lambda_iv": [
            "[]JesusHasCompassionateAuthorityOverDeath(Jesus, Dead, Bereaved)",
            "EFF(ResurrectionSignsSignalGodsVisitationToHisPeople(Jesus, Israel))",
        ],
    },

    {
        "passage_id": "Luk07_36_50",
        "chapter": 7,
        "verses": "36-50",
        "title": "Luke 7:36–50 – Forgiven Woman and the Debt Parable",
        "frames": [
            "Forgiveness",
            "Hospitality",
            "Love",
        ],
        "identity": [
            "[]GreaterAwarenessOfForgivenessProducesDeeperLoveForJesus(ForgivenSinners, Jesus)",
        ],
        "unit_label": "Her Many Sins Are Forgiven",
        "illocution": "TableSceneAndParable",
        "agents": [
            "Jesus",
            "PhariseeHost",
            "SinfulWoman",
            "Guests",
        ],
        "description": (
            "A sinful woman loves much at Jesus feet while a Pharisee withholds hospitality; "
            "Jesus explains that those forgiven much love much."
        ),
        "lambda_iv": [
            "[]GreaterAwarenessOfForgivenessProducesDeeperLoveForJesus(ForgivenSinners, Jesus)",
            "EFF(SelfRighteousnessBlindsToNeedForMercy(PhariseeHost))",
        ],
    },

    {
        "passage_id": "Luk08_04_15",
        "chapter": 8,
        "verses": "4-15",
        "title": "Luke 8:4–15 – Parable of the Sower",
        "frames": [
            "Hearing",
            "Fruitfulness",
            "Resistance",
        ],
        "identity": [
            "[]WordOfGodProducesFruitOnlyInPerseveringHearts(Word, Hearers)",
        ],
        "unit_label": "He Who Has Ears to Hear",
        "illocution": "ParableAndInterpretation",
        "agents": [
            "Jesus",
            "Crowds",
            "Disciples",
        ],
        "description": (
            "Jesus tells and explains the parable of the sower, showing different responses to the "
            "word and the need for persevering faith to bear fruit."
        ),
        "lambda_iv": [
            "[]WordOfGodProducesFruitOnlyInPerseveringHearts(Word, Hearers)",
            "EFF(TrialsAndRichesThreatenFruitfulnessOfTheWord(Hearers))",
        ],
    },

    {
        "passage_id": "Luk08_22_25",
        "chapter": 8,
        "verses": "22-25",
        "title": "Luke 8:22–25 – Calming the Storm",
        "frames": [
            "Authority",
            "Fear",
            "Faith",
        ],
        "identity": [
            "[]JesusCommandsWindAndWavesAndCallsDisciplesToFaith(Jesus, Creation, Disciples)",
        ],
        "unit_label": "Where Is Your Faith?",
        "illocution": "MiracleNarrative",
        "agents": [
            "Jesus",
            "Disciples",
        ],
        "description": (
            "Jesus rebukes wind and waves, calming the storm, and asks his fearful disciples where "
            "their faith is."
        ),
        "lambda_iv": [
            "[]JesusCommandsWindAndWavesAndCallsDisciplesToFaith(Jesus, Creation, Disciples)",
            "EFF(FearInStormsRevealsDepthOfTrustInJesus(Disciples))",
        ],
    },

    {
        "passage_id": "Luk08_26_39",
        "chapter": 8,
        "verses": "26-39",
        "title": "Luke 8:26–39 – Legion and the Delivered Man",
        "frames": [
            "Exorcism",
            "Restoration",
            "Witness",
        ],
        "identity": [
            "[]JesusLiberatesFromLegionOppressionAndSendsFreedOnesAsWitnesses(Jesus, DeliveredMan)",
        ],
        "unit_label": "Return to Your Home and Declare",
        "illocution": "MiracleNarrative",
        "agents": [
            "Jesus",
            "DemonisedMan",
            "Demons",
            "Townspeople",
        ],
        "description": (
            "Jesus drives out a legion of demons, restores the man to sanity, and sends him home "
            "to declare what God has done."
        ),
        "lambda_iv": [
            "[]JesusLiberatesFromLegionOppressionAndSendsFreedOnesAsWitnesses(Jesus, DeliveredMan)",
            "EFF(FearfulRejectionOfJesusContrastsWithGratefulWitness(Townspeople, DeliveredMan))",
        ],
    },

    {
        "passage_id": "Luk08_40_56",
        "chapter": 8,
        "verses": "40-56",
        "title": "Luke 8:40–56 – Jairus Daughter and the Bleeding Woman",
        "frames": [
            "Faith",
            "Delay",
            "Death",
        ],
        "identity": [
            "[]JesusHonoursPersistentFaithAndHasAuthorityOverDeathAndDefilement(Jesus, Sufferers)",
        ],
        "unit_label": "Do Not Fear, Only Believe",
        "illocution": "MiracleNarrative",
        "agents": [
            "Jesus",
            "Jairus",
            "Daughter",
            "BleedingWoman",
            "Crowds",
        ],
        "description": (
            "On the way to Jairus dying daughter, Jesus heals a bleeding woman and then raises the "
            "girl, calling for faith not fear."
        ),
        "lambda_iv": [
            "[]JesusHonoursPersistentFaithAndHasAuthorityOverDeathAndDefilement(Jesus, Sufferers)",
            "EFF(ApparentDelaysBecomeStagesForDeeperRevelationOfJesusPower(Disciples))",
        ],
    },

    {
        "passage_id": "Luk09_01_17",
        "chapter": 9,
        "verses": "1-17",
        "title": "Luke 9:1–17 – Mission of the Twelve and Feeding the Five Thousand",
        "frames": [
            "Mission",
            "Provision",
            "Participation",
        ],
        "identity": [
            "[]JesusSharesHisAuthorityWithDisciplesAndProvidesAsTheyServe(Jesus, Twelve)",
        ],
        "unit_label": "You Give Them Something to Eat",
        "illocution": "MissionNarrative",
        "agents": [
            "Jesus",
            "Twelve",
            "Crowds",
        ],
        "description": (
            "Jesus sends the Twelve to preach and heal, then feeds the multitude, involving the "
            "disciples in distributing his provision."
        ),
        "lambda_iv": [
            "[]JesusSharesHisAuthorityWithDisciplesAndProvidesAsTheyServe(Jesus, Twelve)",
            "EFF(ScarcityBecomesOccasionForTrustingJesusProvision(Disciples))",
        ],
    },

    {
        "passage_id": "Luk09_18_27",
        "chapter": 9,
        "verses": "18-27",
        "title": "Luke 9:18–27 – Peter’s Confession and Call to Take Up the Cross",
        "frames": [
            "Christology",
            "Discipleship",
            "Cross",
        ],
        "identity": [
            "[]ChristMustSufferAndFollowersMustDailyBearCrossToGainTrueLife(Jesus, Disciples)",
        ],
        "unit_label": "Who Do You Say That I Am?",
        "illocution": "ConfessionAndCall",
        "agents": [
            "Jesus",
            "Peter",
            "Disciples",
            "Crowds",
        ],
        "description": (
            "After Peter confesses Jesus as the Christ, Jesus teaches that the Son of Man must "
            "suffer and that disciples must deny themselves and take up their cross."
        ),
        "lambda_iv": [
            "[]ChristMustSufferAndFollowersMustDailyBearCrossToGainTrueLife(Jesus, Disciples)",
            "EFF(PursuitOfWorldlyGainJeopardisesEternalLife(Disciples))",
        ],
    },

    {
        "passage_id": "Luk09_28_36",
        "chapter": 9,
        "verses": "28-36",
        "title": "Luke 9:28–36 – Transfiguration and Divine Voice",
        "frames": [
            "Glory",
            "Exodus",
            "Sonship",
        ],
        "identity": [
            "[]JesusIsBelovedSonWhoseExodusMustBeCompletedAndWhoseWordsMustBeHeard(Jesus, Father, Disciples)",
        ],
        "unit_label": "This Is My Son, Listen to Him",
        "illocution": "Theophany",
        "agents": [
            "Jesus",
            "Peter",
            "James",
            "John",
            "Moses",
            "Elijah",
            "Father",
        ],
        "description": (
            "Jesus is transfigured in glory, speaks with Moses and Elijah about his exodus, and the "
            "Father commands the disciples to listen to him."
        ),
        "lambda_iv": [
            "[]JesusIsBelovedSonWhoseExodusMustBeCompletedAndWhoseWordsMustBeHeard(Jesus, Father, Disciples)",
            "EFF(GloryVisionInterpretsImpendingSuffering(Disciples))",
        ],
    },

    {
        "passage_id": "Luk09_51_62",
        "chapter": 9,
        "verses": "51-62",
        "title": "Luke 9:51–62 – Setting Face to Jerusalem and Hard Call to Follow",
        "frames": [
            "JourneyToJerusalem",
            "Rejection",
            "CostOfDiscipleship",
        ],
        "identity": [
            "[]JesusResolvesToGoToJerusalemAndDemandsUndividedLoyaltyFromFollowers(Jesus, Disciples)",
        ],
        "unit_label": "No One Who Looks Back",
        "illocution": "JourneyHeadingAndSayings",
        "agents": [
            "Jesus",
            "Disciples",
            "SamaritanVillage",
            "WouldBeFollowers",
        ],
        "description": (
            "As Jesus sets his face toward Jerusalem, he is rejected by Samaritans and teaches that "
            "following him allows no divided loyalties."
        ),
        "lambda_iv": [
            "[]JesusResolvesToGoToJerusalemAndDemandsUndividedLoyaltyFromFollowers(Jesus, Disciples)",
            "EFF(DiscipleshipRequiresPriorityOverComfortFamilyAndDelay(Disciples))",
        ],
    },

    {
        "passage_id": "Luk10_01_20",
        "chapter": 10,
        "verses": "1-20",
        "title": "Luke 10:1–20 – Mission of the Seventy-Two and Joy in Heaven",
        "frames": [
            "Mission",
            "AuthorityOverEvil",
            "HeavenlyJoy",
        ],
        "identity": [
            "[]JesusSendsWorkersWithAuthorityAndRootsJoyInHeavenlyBelonging(Jesus, Workers)",
        ],
        "unit_label": "Rejoice That Your Names Are Written in Heaven",
        "illocution": "MissionNarrative",
        "agents": [
            "Jesus",
            "SeventyTwo",
            "Towns",
        ],
        "description": (
            "Jesus sends seventy-two ahead of him, gives them authority over demons, and redirects "
            "their joy from power to their names written in heaven."
        ),
        "lambda_iv": [
            "[]JesusSendsWorkersWithAuthorityAndRootsJoyInHeavenlyBelonging(Jesus, Workers)",
            "EFF(MissionSuccessMustNotDisplaceJoyInSalvation(Workers))",
        ],
    },

    {
        "passage_id": "Luk10_25_37",
        "chapter": 10,
        "verses": "25-37",
        "title": "Luke 10:25–37 – Parable of the Good Samaritan",
        "frames": [
            "Law",
            "NeighbourLove",
            "Mercy",
        ],
        "identity": [
            "[]TrueNeighbourLoveActsMercifullyEvenAcrossHostileBoundaries(Disciple, Neighbour)",
        ],
        "unit_label": "Go and Do Likewise",
        "illocution": "Parable",
        "agents": [
            "Jesus",
            "Lawyer",
            "Priest",
            "Levite",
            "Samaritan",
            "WoundedMan",
        ],
        "description": (
            "In response to a question about neighbours, Jesus tells of a Samaritan who shows costly "
            "mercy where religious figures pass by."
        ),
        "lambda_iv": [
            "[]TrueNeighbourLoveActsMercifullyEvenAcrossHostileBoundaries(Disciple, Neighbour)",
            "EFF(AttemptToLimitNeighbourRevealsSelfJustifyingHeart(Lawyer))",
        ],
    },

    {
        "passage_id": "Luk11_01_13",
        "chapter": 11,
        "verses": "1-13",
        "title": "Luke 11:1–13 – Lord’s Prayer and Asking the Father",
        "frames": [
            "Prayer",
            "FatherhoodOfGod",
            "Persistence",
        ],
        "identity": [
            "[]FatherDelightsToGiveSpiritAndGoodGiftsToPersistentChildren(Father, Disciples)",
        ],
        "unit_label": "Ask, Seek, Knock",
        "illocution": "InstructionAndParable",
        "agents": [
            "Jesus",
            "Disciples",
            "FriendAtMidnight",
            "Father",
        ],
        "description": (
            "Jesus teaches a pattern of prayer, urges persistent asking, and assures disciples of the "
            "Father’s generosity, especially in giving the Spirit."
        ),
        "lambda_iv": [
            "[]FatherDelightsToGiveSpiritAndGoodGiftsToPersistentChildren(Father, Disciples)",
            "EFF(ViewOfFatherShapesCourageToPrayPersistently(Disciples))",
        ],
    },

    {
        "passage_id": "Luk12_13_34",
        "chapter": 12,
        "verses": "13-34",
        "title": "Luke 12:13–34 – Rich Fool and Treasure in Heaven",
        "frames": [
            "Greed",
            "Anxiety",
            "Treasure",
        ],
        "identity": [
            "[]LifeDoesNotConsistInPossessionsAndDisciplesMustSeekKingdomFirst(Disciples, Father)",
        ],
        "unit_label": "Foolish to Store Up Treasure for Self",
        "illocution": "ParableAndExhortation",
        "agents": [
            "Jesus",
            "CrowdMember",
            "RichFool",
            "Disciples",
        ],
        "description": (
            "Jesus warns against greed with the parable of the rich fool, then calls disciples to "
            "trust the Father and seek his kingdom instead of anxious hoarding."
        ),
        "lambda_iv": [
            "[]LifeDoesNotConsistInPossessionsAndDisciplesMustSeekKingdomFirst(Disciples, Father)",
            "EFF(TrustInFathersCareFreesFromAnxiousAccumulation(Disciples))",
        ],
    },

    {
        "passage_id": "Luk13_18_21",
        "chapter": 13,
        "verses": "18-21",
        "title": "Luke 13:18–21 – Mustard Seed and Leaven",
        "frames": [
            "KingdomGrowth",
            "Hiddenness",
            "Inevitability",
        ],
        "identity": [
            "[]KingdomOfGodStartsSmallAndQuietYetGrowsPervasivelyToMaturity(Kingdom, World)",
        ],
        "unit_label": "From Small to All",
        "illocution": "Parables",
        "agents": [
            "Jesus",
            "Crowds",
        ],
        "description": (
            "Jesus likens the kingdom to a mustard seed and to leaven, showing its surprising growth "
            "from small beginnings to pervasive influence."
        ),
        "lambda_iv": [
            "[]KingdomOfGodStartsSmallAndQuietYetGrowsPervasivelyToMaturity(Kingdom, World)",
            "EFF(ApparentInsignificanceDoesNotPredictKingdomsFinalScope(Disciples))",
        ],
    },

    {
        "passage_id": "Luk14_25_35",
        "chapter": 14,
        "verses": "25-35",
        "title": "Luke 14:25–35 – Cost of Discipleship and Counting the Cost",
        "frames": [
            "Discipleship",
            "Cost",
            "Renunciation",
        ],
        "identity": [
            "[]DiscipleshipDemandsSupremeAllegianceToJesusOverAllTiesAndPossessions(Disciples, Jesus)",
        ],
        "unit_label": "Whoever Does Not Renounce All",
        "illocution": "WarningAndIllustration",
        "agents": [
            "Jesus",
            "GreatCrowds",
        ],
        "description": (
            "Jesus warns large crowds that following him requires hating lesser loyalties, bearing the "
            "cross, and renouncing all possessions."
        ),
        "lambda_iv": [
            "[]DiscipleshipDemandsSupremeAllegianceToJesusOverAllTiesAndPossessions(Disciples, Jesus)",
            "EFF(UncountedCostProducesHalfBuiltTowersAndLostSalt(Disciples))",
        ],
    },

    {
        "passage_id": "Luk15_01_32",
        "chapter": 15,
        "verses": "1-32",
        "title": "Luke 15:1–32 – Lost Sheep, Coin, and Sons",
        "frames": [
            "LostAndFound",
            "Joy",
            "SelfRighteousness",
        ],
        "identity": [
            "[]FatherAndHeavenRejoiceOverRepentantSinnersWhileSelfRighteousHeartsResentGrace(Father, Sinners, Pharisees)",
        ],
        "unit_label": "Rejoicing Over the Found",
        "illocution": "Parables",
        "agents": [
            "Jesus",
            "TaxCollectorsAndSinners",
            "PhariseesAndScribes",
            "Father",
            "OlderBrother",
            "YoungerSon",
        ],
        "description": (
            "Jesus tells three parables of lost and found to reveal heaven’s joy over repentant sinners "
            "and expose Pharisaic resentment of grace."
        ),
        "lambda_iv": [
            "[]FatherAndHeavenRejoiceOverRepentantSinnersWhileSelfRighteousHeartsResentGrace(Father, Sinners, Pharisees)",
            "EFF(ParticipationInFathersJoyRequiresSharingHisHeartForTheLost(Disciples))",
        ],
    },

    {
        "passage_id": "Luk16_19_31",
        "chapter": 16,
        "verses": "19-31",
        "title": "Luke 16:19–31 – Rich Man and Lazarus",
        "frames": [
            "Reversal",
            "ScriptureSufficiency",
            "Judgment",
        ],
        "identity": [
            "[]NeglectOfPoorInThisLifeRevealsHeartThatWillFaceReversalAndJudgment(Rich, Poor)",
        ],
        "unit_label": "If They Do Not Hear Moses and the Prophets",
        "illocution": "Parable",
        "agents": [
            "RichMan",
            "Lazarus",
            "Abraham",
            "Brothers",
        ],
        "description": (
            "A rich man who ignored Lazarus in life is tormented in Hades, warning that Scripture is "
            "sufficient testimony and that reversal is coming."
        ),
        "lambda_iv": [
            "[]NeglectOfPoorInThisLifeRevealsHeartThatWillFaceReversalAndJudgment(Rich, Poor)",
            "EFF(UnheededScriptureRendersEvenResurrectionWitnessIneffective(Hearers))",
        ],
    },

    {
        "passage_id": "Luk18_01_14",
        "chapter": 18,
        "verses": "1-14",
        "title": "Luke 18:1–14 – Persistent Widow and Pharisee and Tax Collector",
        "frames": [
            "Prayer",
            "Justice",
            "Humility",
        ],
        "identity": [
            "[]GodHonoursPersistentFaithAndJustifiesHumbleSinnersNotSelfRighteous(Petitioners, God)",
        ],
        "unit_label": "He Who Humbles Himself Will Be Exalted",
        "illocution": "Parables",
        "agents": [
            "Widow",
            "UnjustJudge",
            "Pharisee",
            "TaxCollector",
            "Jesus",
        ],
        "description": (
            "Jesus teaches that disciples must always pray and not lose heart and that the humble "
            "sinner, not the self-righteous, goes home justified."
        ),
        "lambda_iv": [
            "[]GodHonoursPersistentFaithAndJustifiesHumbleSinnersNotSelfRighteous(Petitioners, God)",
            "EFF(PostureInPrayerRevealsTrueStandingBeforeGod(Worshippers))",
        ],
    },

    {
        "passage_id": "Luk18_18_30",
        "chapter": 18,
        "verses": "18-30",
        "title": "Luke 18:18–30 – Rich Ruler and Treasure in Heaven",
        "frames": [
            "Wealth",
            "Discipleship",
            "Reward",
        ],
        "identity": [
            "[]AttachmentToWealthHindersEnteringKingdomYetGodCanDoImpossible(Wealthy, God)",
        ],
        "unit_label": "Sell All and Follow Me",
        "illocution": "EncounterAndTeaching",
        "agents": [
            "Jesus",
            "RichRuler",
            "Disciples",
        ],
        "description": (
            "A rich ruler who keeps commandments cannot let go of wealth to follow Jesus, and Jesus "
            "teaches about the difficulty for the rich and the reward for those who leave all."
        ),
        "lambda_iv": [
            "[]AttachmentToWealthHindersEnteringKingdomYetGodCanDoImpossible(Wealthy, God)",
            "EFF(RadicalSurrenderForJesusSakeReceivesMultiFoldReward(Disciples))",
        ],
    },

    {
        "passage_id": "Luk19_01_10",
        "chapter": 19,
        "verses": "1-10",
        "title": "Luke 19:1–10 – Zacchaeus and the Son of Man’s Mission",
        "frames": [
            "Seeking",
            "Repentance",
            "Restitution",
        ],
        "identity": [
            "[]SonOfManCameToSeekAndSaveTheLostAndHisGraceProducesRepentantRestitution(Jesus, Lost)",
        ],
        "unit_label": "Today Salvation Has Come to This House",
        "illocution": "EncounterNarrative",
        "agents": [
            "Jesus",
            "Zacchaeus",
            "Crowd",
        ],
        "description": (
            "Jesus seeks out Zacchaeus, stays at his house, and Zacchaeus responds with joyful "
            "restitution as Jesus declares his saving mission."
        ),
        "lambda_iv": [
            "[]SonOfManCameToSeekAndSaveTheLostAndHisGraceProducesRepentantRestitution(Jesus, Lost)",
            "EFF(GrumblingAtGraceContrastsWithJoyfulRepentance(Crowd, Zacchaeus))",
        ],
    },

    {
        "passage_id": "Luk19_28_44",
        "chapter": 19,
        "verses": "28-44",
        "title": "Luke 19:28–44 – Triumphal Entry and Weeping Over Jerusalem",
        "frames": [
            "Kingship",
            "Visitation",
            "Judgment",
        ],
        "identity": [
            "[]JesusIsPeaceBringingKingWhoseRejectedVisitationLeadsToJudgment(Jesus, Jerusalem)",
        ],
        "unit_label": "You Did Not Know the Time of Your Visitation",
        "illocution": "PropheticEntry",
        "agents": [
            "Jesus",
            "Disciples",
            "Crowds",
            "Jerusalem",
        ],
        "description": (
            "Jesus enters Jerusalem as king amid praise, then weeps over the city that does not know "
            "the things for peace or the time of its visitation."
        ),
        "lambda_iv": [
            "[]JesusIsPeaceBringingKingWhoseRejectedVisitationLeadsToJudgment(Jesus, Jerusalem)",
            "EFF(MissingGodsVisitationBringsInevitableDesolation(City))",
        ],
    },

    {
        "passage_id": "Luk22_14_23",
        "chapter": 22,
        "verses": "14-23",
        "title": "Luke 22:14–23 – Institution of the Lord’s Supper",
        "frames": [
            "Passover",
            "Covenant",
            "Remembrance",
        ],
        "identity": [
            "[]JesusGivesHisBodyAndBloodAsNewCovenantMealForHisPeople(Jesus, Disciples)",
        ],
        "unit_label": "This Is My Body Given for You",
        "illocution": "CovenantMeal",
        "agents": [
            "Jesus",
            "Twelve",
        ],
        "description": (
            "At Passover Jesus interprets bread and cup as his body and blood of the covenant, given "
            "for his people amid the shadow of betrayal."
        ),
        "lambda_iv": [
            "[]JesusGivesHisBodyAndBloodAsNewCovenantMealForHisPeople(Jesus, Disciples)",
            "EFF(MealBecomesOngoingParticipationInSacrificialDeath(Church))",
        ],
    },

    {
        "passage_id": "Luk22_39_46",
        "chapter": 22,
        "verses": "39-46",
        "title": "Luke 22:39–46 – Gethsemane and Prayer Under Trial",
        "frames": [
            "Agony",
            "Submission",
            "Prayer",
        ],
        "identity": [
            "[]JesusSubmitsHisWillToFathersPlanAndCallsDisciplesToPrayAgainstTemptation(Jesus, Father, Disciples)",
        ],
        "unit_label": "Not My Will but Yours Be Done",
        "illocution": "AgonyNarrative",
        "agents": [
            "Jesus",
            "Disciples",
            "Father",
            "Angel",
        ],
        "description": (
            "In anguish Jesus prays for the cup to pass yet submits to the Father’s will, while "
            "disciples fail to stay awake and pray."
        ),
        "lambda_iv": [
            "[]JesusSubmitsHisWillToFathersPlanAndCallsDisciplesToPrayAgainstTemptation(Jesus, Father, Disciples)",
            "EFF(PrayerfulSubmissionIsPathThroughComingTrial(Disciples))",
        ],
    },

    {
        "passage_id": "Luk23_33_49",
        "chapter": 23,
        "verses": "33-49",
        "title": "Luke 23:33–49 – Crucifixion and the Righteous Sufferer",
        "frames": [
            "Crucifixion",
            "Innocence",
            "Mockery",
        ],
        "identity": [
            "[]InnocentJesusBearsMockeryAndDeathWhileExtendingForgivenessAndParadise(Jesus, Sinners)",
        ],
        "unit_label": "Father, Forgive Them",
        "illocution": "PassionNarrative",
        "agents": [
            "Jesus",
            "Soldiers",
            "Leaders",
            "Criminals",
            "Crowds",
            "Centurion",
        ],
        "description": (
            "Jesus is crucified between criminals, prays for his executioners, promises paradise to "
            "a repentant thief, and is confessed righteous by the centurion."
        ),
        "lambda_iv": [
            "[]InnocentJesusBearsMockeryAndDeathWhileExtendingForgivenessAndParadise(Jesus, Sinners)",
            "EFF(ResponseToCrucifiedJesusRevealsHeartsInFaceOfGodsJustice(Hearers))",
        ],
    },

    {
        "passage_id": "Luk24_01_12",
        "chapter": 24,
        "verses": "1-12",
        "title": "Luke 24:1–12 – Empty Tomb and Angelic Message",
        "frames": [
            "Resurrection",
            "RememberingWords",
            "Astonishment",
        ],
        "identity": [
            "[]CrucifiedJesusIsRaisedAsPromisedAndHisWordsInterpretEmptyTomb(Jesus, Women, Disciples)",
        ],
        "unit_label": "Why Do You Seek the Living Among the Dead?",
        "illocution": "ResurrectionNarrative",
        "agents": [
            "Women",
            "Angels",
            "Apostles",
            "Peter",
        ],
        "description": (
            "Women find the tomb empty, hear angels announce Jesus resurrection, remember his words, "
            "and report to incredulous apostles."
        ),
        "lambda_iv": [
            "[]CrucifiedJesusIsRaisedAsPromisedAndHisWordsInterpretEmptyTomb(Jesus, Women, Disciples)",
            "EFF(FailureToRememberWordsHindersRecognitionOfResurrection(Disciples))",
        ],
    },

    {
        "passage_id": "Luk24_13_35",
        "chapter": 24,
        "verses": "13-35",
        "title": "Luke 24:13–35 – Emmaus Road and Opened Scriptures",
        "frames": [
            "Scripture",
            "Recognition",
            "TableFellowship",
        ],
        "identity": [
            "[]RisenJesusInterpretsScripturesAboutHisSufferingsAndIsKnownInBreakingOfBread(Jesus, Disciples)",
        ],
        "unit_label": "Our Hearts Burned Within Us",
        "illocution": "ResurrectionAppearance",
        "agents": [
            "Jesus",
            "Cleopas",
            "Companion",
        ],
        "description": (
            "The risen Jesus walks with two disciples, opens the Scriptures concerning his suffering "
            "and glory, and is recognised in the breaking of bread."
        ),
        "lambda_iv": [
            "[]RisenJesusInterpretsScripturesAboutHisSufferingsAndIsKnownInBreakingOfBread(Jesus, Disciples)",
            "EFF(UnderstandingCrossAndResurrectionRequiresScripturalReReading(Disciples))",
        ],
    },

    {
        "passage_id": "Luk24_36_53",
        "chapter": 24,
        "verses": "36-53",
        "title": "Luke 24:36–53 – Commission, Promise, and Ascension",
        "frames": [
            "Witness",
            "SpiritPromise",
            "Blessing",
        ],
        "identity": [
            "[]RisenJesusCommissionsWitnessesOpensScripturesAndPromisesSpiritPowerBeforeAscension(Jesus, Disciples)",
        ],
        "unit_label": "You Are Witnesses of These Things",
        "illocution": "CommissionAndBlessing",
        "agents": [
            "Jesus",
            "Disciples",
        ],
        "description": (
            "The risen Jesus appears to the gathered disciples, opens their minds to the Scriptures, "
            "commissions them as witnesses, promises the Spirit, and ascends while blessing them."
        ),
        "lambda_iv": [
            "[]RisenJesusCommissionsWitnessesOpensScripturesAndPromisesSpiritPowerBeforeAscension(Jesus, Disciples)",
            "EFF(WorshippingJoyfulWitnessFlowsFromEncounterWithRisenAscendedLord(Church))",
        ],
    },


    {
        "passage_id": "Luk01_01_04",
        "chapter": 1,
        "verses": "1-4",
        "title": "Luke 1:1–4 – Orderly Account for Certainty",
        "frames": [
            "Witness",
            "OrderlyAccount",
            "Certainty",
        ],
        "identity": [
            "[]GospelIsAnOrderlyAccountBasedOnEyewitnessTestimony(Gospel, Eyewitnesses)",
        ],
        "unit_label": "Orderly Account for Certainty",
        "illocution": "Preface",
        "agents": [
            "Luke",
            "Theophilus",
            "Eyewitnesses",
            "MinistersOfTheWord",
        ],
        "description": (
            "Luke carefully investigates everything from the beginning and writes an orderly "
            "account so that Theophilus may have certainty about the things taught."
        ),
        "lambda_iv": [
            "[]GospelIsAnOrderlyAccountBasedOnEyewitnessTestimony(Gospel, Eyewitnesses)",
            "EFF(WritingSoBelieversMayHaveCertainty(Luke, Theophilus))",
        ],
    },

    {
        "passage_id": "Luk01_05_25",
        "chapter": 1,
        "verses": "5-25",
        "title": "Luke 1:5–25 – Birth of John Foretold",
        "frames": [
            "Temple",
            "BirthAnnouncement",
            "Preparation",
        ],
        "identity": [
            "[]JohnIsPropheticForerunnerPreparingWayForTheLord(John, Lord)",
        ],
        "unit_label": "Forerunner Promised in Barrenness",
        "illocution": "TheophanyAnnouncement",
        "agents": [
            "Zechariah",
            "Elizabeth",
            "Gabriel",
            "John",
            "Lord",
        ],
        "description": (
            "In the temple an angel promises a son to barren Elizabeth; John will be great "
            "before the Lord and prepared as forerunner, while Zechariah is struck mute for unbelief."
        ),
        "lambda_iv": [
            "[]JohnIsPropheticForerunnerPreparingWayForTheLord(John, Lord)",
            "EFF(TempleAnnouncementInBarrennessSignalsMercyAndNewExodus(Lord, Israel))",
        ],
    },

    {
        "passage_id": "Luk01_26_38",
        "chapter": 1,
        "verses": "26-38",
        "title": "Luke 1:26–38 – Son of the Most High Conceived",
        "frames": [
            "Incarnation",
            "DavidicKingship",
            "Favour",
        ],
        "identity": [
            "[]JesusIsSpiritConceivedSonOfMostHighAndDavidicKing(Jesus, Spirit, David)",
        ],
        "unit_label": "Let It Be to Me",
        "illocution": "TheophanyAnnouncement",
        "agents": [
            "Mary",
            "Gabriel",
            "Jesus",
            "HolySpirit",
            "MostHigh",
        ],
        "description": (
            "Gabriel announces to Mary that she will conceive by the Holy Spirit and bear the "
            "Son of the Most High, the Davidic king whose kingdom will never end; Mary responds in trusting submission."
        ),
        "lambda_iv": [
            "[]JesusIsSpiritConceivedSonOfMostHighAndDavidicKing(Jesus, Spirit, David)",
            "EFF(HumbleFaithReceivesSeeminglyImpossiblePromise(Mary, WordOfGod))",
        ],
    },

    {
        "passage_id": "Luk01_39_56",
        "chapter": 1,
        "verses": "39-56",
        "title": "Luke 1:39–56 – Spirit-Joy and the Magnificat",
        "frames": [
            "Joy",
            "Reversal",
            "Mercy",
        ],
        "identity": [
            "[]LordShowsCovenantMercyToLowlyAndOpposedToProud(Lord, Lowly, Proud)",
        ],
        "unit_label": "He Has Brought Down and Lifted Up",
        "illocution": "HymnOfPraise",
        "agents": [
            "Mary",
            "Elizabeth",
            "John",
            "Lord",
            "Israel",
        ],
        "description": (
            "Mary visits Elizabeth, John leaps in the womb, and Mary sings of God’s mercy "
            "that exalts the humble and brings down the proud, remembering his promises to Israel."
        ),
        "lambda_iv": [
            "[]LordShowsCovenantMercyToLowlyAndOpposedToProud(Lord, Lowly, Proud)",
            "EFF(ComingMessiahReordersSocialAndSpiritualFortunes(Messiah, World))",
        ],
    },

    {
        "passage_id": "Luk01_57_80",
        "chapter": 1,
        "verses": "57-80",
        "title": "Luke 1:57–80 – Benedictus and Dawn from on High",
        "frames": [
            "Fulfilment",
            "Dawn",
            "Forgiveness",
        ],
        "identity": [
            "[]GodRaisesHornOfSalvationToGuidePeopleIntoPeace(YHWH, People)",
        ],
        "unit_label": "Visited and Redeemed",
        "illocution": "PropheticHymn",
        "agents": [
            "Zechariah",
            "John",
            "Jesus",
            "Israel",
            "YHWH",
        ],
        "description": (
            "At John’s birth, Zechariah prophesies that God has visited and redeemed his people, "
            "raising a horn of salvation and giving light to those in darkness."
        ),
        "lambda_iv": [
            "[]GodRaisesHornOfSalvationToGuidePeopleIntoPeace(YHWH, People)",
            "EFF(PropheticForerunnerPreparesWayByProclaimingForgiveness(John, People))",
        ],
    },

    {
        "passage_id": "Luk02_01_20",
        "chapter": 2,
        "verses": "1-20",
        "title": "Luke 2:1–20 – Saviour, Christ, and Lord Announced",
        "frames": [
            "Incarnation",
            "DavidicCity",
            "GoodNewsForPoor",
        ],
        "identity": [
            "[]JesusIsSaviourChristAndLordBornInDavidCityForAllPeople(Jesus, DavidCity, Peoples)",
        ],
        "unit_label": "Good News of Great Joy",
        "illocution": "BirthNarrative",
        "agents": [
            "Jesus",
            "Mary",
            "Joseph",
            "Shepherds",
            "Angels",
        ],
        "description": (
            "In humble circumstances, Jesus is born in David’s city while angels announce him "
            "to shepherds as Saviour, Christ, and Lord, good news of great joy for all people."
        ),
        "lambda_iv": [
            "[]JesusIsSaviourChristAndLordBornInDavidCityForAllPeople(Jesus, DavidCity, Peoples)",
            "EFF(HeavenlyAnnouncementFirstComesToLowlyShepherds(Angels, Shepherds))",
        ],
    },

    {
        "passage_id": "Luk02_21_40",
        "chapter": 2,
        "verses": "21-40",
        "title": "Luke 2:21–40 – Consolation and Light for the Nations",
        "frames": [
            "Temple",
            "Consolation",
            "LightToGentiles",
        ],
        "identity": [
            "[]JesusIsConsolationOfIsraelAndLightForRevelationToGentiles(Jesus, Israel, Gentiles)",
        ],
        "unit_label": "My Eyes Have Seen Your Salvation",
        "illocution": "Recognition",
        "agents": [
            "Jesus",
            "Mary",
            "Joseph",
            "Simeon",
            "Anna",
        ],
        "description": (
            "Simeon and Anna, waiting in the temple, recognise the child Jesus as God’s salvation, "
            "light for Gentiles and glory for Israel, yet a sign opposed."
        ),
        "lambda_iv": [
            "[]JesusIsConsolationOfIsraelAndLightForRevelationToGentiles(Jesus, Israel, Gentiles)",
            "EFF(ExposureOfHeartsThroughResponseToJesus(Hearts, Jesus))",
        ],
    },

    {
        "passage_id": "Luk02_41_52",
        "chapter": 2,
        "verses": "41-52",
        "title": "Luke 2:41–52 – In My Father’s House",
        "frames": [
            "Sonship",
            "Wisdom",
            "Obedience",
        ],
        "identity": [
            "[]JesusSelfConsciouslyBelongsToFathersBusinessWhileObeyingEarthlyParents(Jesus, Father, Parents)",
        ],
        "unit_label": "Did You Not Know?",
        "illocution": "Narration",
        "agents": [
            "Jesus",
            "Mary",
            "Joseph",
            "Teachers",
        ],
        "description": (
            "At twelve years old Jesus stays behind in the temple, amazing teachers and declaring his "
            "priority for the Father’s house while returning to Nazareth in obedience."
        ),
        "lambda_iv": [
            "[]JesusSelfConsciouslyBelongsToFathersBusinessWhileObeyingEarthlyParents(Jesus, Father, Parents)",
            "EFF(GrowingInWisdomAndFavourAsPatternOfTrueSonship(Jesus))",
        ],
    },

    {
        "passage_id": "Luk03_01_20",
        "chapter": 3,
        "verses": "1-20",
        "title": "Luke 3:1–20 – Voice in the Wilderness and Fruit of Repentance",
        "frames": [
            "Preparation",
            "Repentance",
            "Judgment",
        ],
        "identity": [
            "[]JohnPreparesWayForLordByProclaimingRepentanceAndImpendingJudgment(John, Lord)",
        ],
        "unit_label": "Bear Fruits in Keeping with Repentance",
        "illocution": "PropheticWarning",
        "agents": [
            "John",
            "Crowds",
            "TaxCollectors",
            "Soldiers",
            "Herod",
        ],
        "description": (
            "John preaches a baptism of repentance for forgiveness, calls different groups to concrete "
            "fruit, and warns of coming wrath and judgment."
        ),
        "lambda_iv": [
            "[]JohnPreparesWayForLordByProclaimingRepentanceAndImpendingJudgment(John, Lord)",
            "EFF(TrueRepentanceMustBearObservableFruit(Repentant, Neighbour))",
        ],
    },

    {
        "passage_id": "Luk03_21_22",
        "chapter": 3,
        "verses": "21-22",
        "title": "Luke 3:21–22 – Heaven Opened and the Beloved Son",
        "frames": [
            "Baptism",
            "Spirit",
            "Sonship",
        ],
        "identity": [
            "[]JesusIsBelovedSonAnointedWithSpiritInPrayer(Jesus, Father, Spirit)",
        ],
        "unit_label": "You Are My Beloved Son",
        "illocution": "Theophany",
        "agents": [
            "Jesus",
            "Father",
            "Spirit",
            "People",
        ],
        "description": (
            "While Jesus is praying at his baptism, heaven opens, the Spirit descends, and the Father "
            "declares him the beloved Son."
        ),
        "lambda_iv": [
            "[]JesusIsBelovedSonAnointedWithSpiritInPrayer(Jesus, Father, Spirit)",
            "EFF(MessianicMissionCommencesUnderTrinitarianWitness(Jesus, Father, Spirit))",
        ],
    },

    {
        "passage_id": "Luk03_23_38",
        "chapter": 3,
        "verses": "23-38",
        "title": "Luke 3:23–38 – Genealogy Back to Adam",
        "frames": [
            "Genealogy",
            "SonOfAdam",
            "SonOfGod",
        ],
        "identity": [
            "[]JesusIsTrueSonOfAdamAndSonOfGodRepresentingHumanity(Jesus, Adam, God)",
        ],
        "unit_label": "Son of Adam, Son of God",
        "illocution": "Narration",
        "agents": [
            "Jesus",
            "Adam",
            "God",
            "IsraelAncestors",
        ],
        "description": (
            "Luke traces Jesus’ lineage back to Adam and God, situating him as representative human "
            "and Son of God."
        ),
        "lambda_iv": [
            "[]JesusIsTrueSonOfAdamAndSonOfGodRepresentingHumanity(Jesus, Adam, God)",
            "EFF(GenealogyPreparesForRepresentativeTestingAndRedemption(Jesus, Humanity))",
        ],
    },

    {
        "passage_id": "Luk04_01_13",
        "chapter": 4,
        "verses": "1-13",
        "title": "Luke 4:1–13 – Spirit-Led Testing of the Son",
        "frames": [
            "Testing",
            "Scripture",
            "Sonship",
        ],
        "identity": [
            "[]SpiritLedSonRemainsFaithfulUnderTemptationByTrustingScripture(Jesus, Spirit, Scripture)",
        ],
        "unit_label": "If You Are the Son of God",
        "illocution": "Narration",
        "agents": [
            "Jesus",
            "Devil",
            "Spirit",
        ],
        "description": (
            "Full of the Spirit, Jesus is led into the wilderness and resists the devil’s temptations, "
            "wielding Scripture as he proves faithful Sonship."
        ),
        "lambda_iv": [
            "[]SpiritLedSonRemainsFaithfulUnderTemptationByTrustingScripture(Jesus, Spirit, Scripture)",
            "EFF(ObedientSonReversesAdamsAndIsraelsFailuresInTesting(Jesus, Adam, Israel))",
        ],
    },

    {
        "passage_id": "Luk04_14_30",
        "chapter": 4,
        "verses": "14-30",
        "title": "Luke 4:14–30 – Spirit-Anointed Mission and Hometown Rejection",
        "frames": [
            "Mission",
            "Isaiah61",
            "Rejection",
        ],
        "identity": [
            "[]JesusIsSpiritAnointedMessiahProclaimingGoodNewsToPoorAndOppressed(Jesus, Spirit, Poor)",
        ],
        "unit_label": "Today This Scripture Is Fulfilled",
        "illocution": "ProgrammaticDeclaration",
        "agents": [
            "Jesus",
            "NazarethSynagogue",
            "Spirit",
            "Poor",
            "Oppressed",
        ],
        "description": (
            "Jesus reads Isaiah, declares its fulfilment in himself, and is rejected by his hometown "
            "when he exposes their unbelief and announces grace beyond Israel."
        ),
        "lambda_iv": [
            "[]JesusIsSpiritAnointedMessiahProclaimingGoodNewsToPoorAndOppressed(Jesus, Spirit, Poor)",
            "EFF(RejectionOfProphetForeshadowsWiderResistanceToMercy(Nazareth, Jesus))",
        ],
    },

    {
        "passage_id": "Luk04_31_44",
        "chapter": 4,
        "verses": "31-44",
        "title": "Luke 4:31–44 – Authority Over Demons, Disease, and the Mission Priority",
        "frames": [
            "Authority",
            "Exorcism",
            "PreachingMission",
        ],
        "identity": [
            "[]JesusWordCarriesAuthorityOverDemonsDiseaseAndDefinesMissionFocus(Jesus, Word)",
        ],
        "unit_label": "I Must Preach the Good News",
        "illocution": "NarrationAndPurposeStatement",
        "agents": [
            "Jesus",
            "Demoniac",
            "Crowds",
            "Simon",
            "SimonsMotherInLaw",
        ],
        "description": (
            "Jesus teaches with authority, casts out demons, heals the sick, and insists he must preach "
            "the kingdom in other towns too."
        ),
        "lambda_iv": [
            "[]JesusWordCarriesAuthorityOverDemonsDiseaseAndDefinesMissionFocus(Jesus, Word)",
            "EFF(MiraclesSupportButDoNotReplacePreachingMission(Jesus, Towns))",
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
                "book": "Luke",
                "passage_id": pid,
                "version": f"{pid}_Lambda_IV_v0.1",
            },
            "passage_id": pid,
            "book": "Luke",
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
