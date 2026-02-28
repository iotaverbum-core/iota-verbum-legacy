"""
Utility script to generate Modal Bible λ-files for the Gospel of Mark.

Pattern matches modal_bible/mark/mark_04_26_29.lambda.json and the
Matthew / Luke generators: one JSON per pericope.

Usage (from project root):

    (.venv) python tools/generate_mark_lambda.py

It will create / overwrite files under modal_bible/mark/.
"""

from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "modal_bible" / "mark"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_verses(verses_str: str) -> list[int]:
    """
    Very small helper: "1-13" -> [1, 2, ..., 13]
    """
    start_str, end_str = verses_str.split("-")
    start, end = int(start_str), int(end_str)
    return list(range(start, end + 1))


META_BASE = {
    "author": "Iota Verbum – Modal Bible Prototype",
    "encoding": "Lambda_IV_v0.1",
    "notes": "Auto-generated Mark λ-files; safe to hand-edit after generation.",
}

PERICOPES = [

    {
        "passage_id": "Mar01_01_13",
        "chapter": 1,
        "verses": "1-13",
        "title": "Mark 1:1–13 – Prologue, John, and Baptism/Testing of Jesus",
        "frames": [
            "GospelBeginning",
            "PropheticForerunner",
            "Baptism",
            "Testing",
        ],
        "identity": [
            "[]JesusIsSpiritAnointedSonWhoPassesWildernessTesting(Jesus, Spirit, Father)",
        ],
        "unit_label": "Beginning of the Gospel",
        "illocution": "ProgrammaticPrologue",
        "agents": [
            "Jesus",
            "JohnTheBaptist",
            "Spirit",
            "Father",
            "Satan",
        ],
        "description": (
            "Mark announces the beginning of the gospel, presents John as forerunner, "
            "and shows Jesus baptised, declared beloved Son, and driven into the wilderness to be tested."
        ),
        "lambda_iv": [
            "[]JesusIsSpiritAnointedSonWhoPassesWildernessTesting(Jesus, Spirit, Father)",
            "EFF(PropheticForerunnerAndWildernessTestingFrameEntireGospel(Jesus, JohnTheBaptist))",
        ],
    },

    {
        "passage_id": "Mar01_14_20",
        "chapter": 1,
        "verses": "14-20",
        "title": "Mark 1:14–20 – First Preaching and Call of the Four",
        "frames": [
            "KingdomAnnouncement",
            "Repentance",
            "Call",
        ],
        "identity": [
            "[]JesusProclaimsArrivalOfKingdomCallingForRepentanceAndFaith(Jesus, Hearers)",
        ],
        "unit_label": "Follow Me",
        "illocution": "SummaryProclamationAndCall",
        "agents": [
            "Jesus",
            "Simon",
            "Andrew",
            "James",
            "John",
        ],
        "description": (
            "After Johns arrest, Jesus preaches the gospel of God and calls fishermen "
            "to leave nets and follow him as fishers of people."
        ),
        "lambda_iv": [
            "[]JesusProclaimsArrivalOfKingdomCallingForRepentanceAndFaith(Jesus, Hearers)",
            "EFF(CallOfDisciplesModelsImmediateResponsiveObedience(Disciples))",
        ],
    },

    {
        "passage_id": "Mar01_21_45",
        "chapter": 1,
        "verses": "21-45",
        "title": "Mark 1:21–45 – Authority in Capernaum and Cleansing a Leper",
        "frames": [
            "Authority",
            "Exorcism",
            "Healing",
            "Purity",
        ],
        "identity": [
            "[]JesusWordHasAuthorityOverDemonsAndDiseaseAndCanCleanseImpurity(Jesus, UncleanSpirits, Sick)",
        ],
        "unit_label": "Teaching with Authority",
        "illocution": "MiracleCluster",
        "agents": [
            "Jesus",
            "UncleanSpirit",
            "SynagogueCrowd",
            "SimonsHousehold",
            "Leper",
        ],
        "description": (
            "Jesus teaches with authority, casts out an unclean spirit, heals many including "
            "Simons mother-in-law, and cleanses a leper with a touch and a word."
        ),
        "lambda_iv": [
            "[]JesusWordHasAuthorityOverDemonsAndDiseaseAndCanCleanseImpurity(Jesus, UncleanSpirits, Sick)",
            "EFF(AuthorityOverImpuritySignalsInbreakingOfGodsReign(Jesus))",
        ],
    },

    {
        "passage_id": "Mar02_01_12",
        "chapter": 2,
        "verses": "1-12",
        "title": "Mark 2:1–12 – Healing the Paralytic and Forgiving Sins",
        "frames": [
            "Forgiveness",
            "Faith",
            "Authority",
        ],
        "identity": [
            "[]SonOfManHasAuthorityOnEarthToForgiveSins(Jesus, SonOfMan)",
        ],
        "unit_label": "Rise, Pick Up Your Bed",
        "illocution": "MiracleAndControversy",
        "agents": [
            "Jesus",
            "Paralytic",
            "Friends",
            "Scribes",
            "Crowd",
        ],
        "description": (
            "Friends lower a paralytic through the roof; Jesus forgives his sins, provoking "
            "scribal accusations of blasphemy, and proves his authority by healing him."
        ),
        "lambda_iv": [
            "[]SonOfManHasAuthorityOnEarthToForgiveSins(Jesus, SonOfMan)",
            "EFF(FaithExpressedInCostlyActionReceivesForgivenessAndRestoration(Friends, Paralytic))",
        ],
    },

    {
        "passage_id": "Mar02_13_17",
        "chapter": 2,
        "verses": "13-17",
        "title": "Mark 2:13–17 – Call of Levi and Table with Sinners",
        "frames": [
            "Call",
            "TableFellowship",
            "Mercy",
        ],
        "identity": [
            "[]JesusCameToCallSinnersNotTheRighteousToRepentance(Jesus, Sinners)",
        ],
        "unit_label": "Those Who Are Sick",
        "illocution": "CallNarrative",
        "agents": [
            "Jesus",
            "Levi",
            "TaxCollectors",
            "Sinners",
            "ScribesOfPharisees",
        ],
        "description": (
            "Jesus calls Levi the tax collector, eats with tax collectors and sinners, and "
            "declares that he came for the sick, not the healthy."
        ),
        "lambda_iv": [
            "[]JesusCameToCallSinnersNotTheRighteousToRepentance(Jesus, Sinners)",
            "EFF(TableFellowshipWithSinnersEmbodiesGodsMercy(Jesus, Sinners))",
        ],
    },

    {
        "passage_id": "Mar04_01_20",
        "chapter": 4,
        "verses": "1-20",
        "title": "Mark 4:1–20 – Parable of the Sower and Its Explanation",
        "frames": [
            "Hearing",
            "MysteryOfKingdom",
            "Fruitfulness",
        ],
        "identity": [
            "[]WordOfKingdomBearsFruitInThoseWhoHearAcceptAndPersevere(Word, Hearers)",
        ],
        "unit_label": "He Who Has Ears to Hear",
        "illocution": "ParableAndInterpretation",
        "agents": [
            "Jesus",
            "Crowd",
            "Disciples",
        ],
        "description": (
            "Jesus teaches from the boat the parable of the sower, then explains privately to "
            "disciples the varying soils and the mystery of the kingdom."
        ),
        "lambda_iv": [
            "[]WordOfKingdomBearsFruitInThoseWhoHearAcceptAndPersevere(Word, Hearers)",
            "EFF(ParablesBothRevealAndConcealAccordingToResponse(Hearers))",
        ],
    },

    # Growing Seed already exists as mark_04_26_29.lambda.json;
    # we leave it as-is in addition to this curated sweep.

    {
        "passage_id": "Mar04_35_41",
        "chapter": 4,
        "verses": "35-41",
        "title": "Mark 4:35–41 – Calming the Storm",
        "frames": [
            "AuthorityOverCreation",
            "Fear",
            "Faith",
        ],
        "identity": [
            "[]JesusCommandsWindAndSeaAndQuestionsDisciplesFear(Jesus, Creation, Disciples)",
        ],
        "unit_label": "Who Then Is This?",
        "illocution": "MiracleNarrative",
        "agents": [
            "Jesus",
            "Disciples",
        ],
        "description": (
            "On the lake Jesus rebukes wind and sea, bringing great calm, and exposes the disciples "
            "fear and lack of faith."
        ),
        "lambda_iv": [
            "[]JesusCommandsWindAndSeaAndQuestionsDisciplesFear(Jesus, Creation, Disciples)",
            "EFF(ThreateningChaosRevealsDepthOfTrustInJesus(Disciples))",
        ],
    },

    {
        "passage_id": "Mar05_01_20",
        "chapter": 5,
        "verses": "1-20",
        "title": "Mark 5:1–20 – Gerasene Demoniac Delivered",
        "frames": [
            "Exorcism",
            "Restoration",
            "Witness",
        ],
        "identity": [
            "[]JesusLiberatesFromLegionBondageAndSendsFreedAsWitness(Jesus, DeliveredMan)",
        ],
        "unit_label": "Go Home and Tell",
        "illocution": "MiracleNarrative",
        "agents": [
            "Jesus",
            "Legion",
            "Demoniac",
            "Townspeople",
        ],
        "description": (
            "Jesus confronts a man possessed by a legion of demons, casts them into pigs, restores "
            "the man, and sends him to proclaim in the Decapolis."
        ),
        "lambda_iv": [
            "[]JesusLiberatesFromLegionBondageAndSendsFreedAsWitness(Jesus, DeliveredMan)",
            "EFF(FearfulRejectionOfJesusContrastsWithObedientWitness(Townspeople, DeliveredMan))",
        ],
    },

    {
        "passage_id": "Mar05_21_43",
        "chapter": 5,
        "verses": "21-43",
        "title": "Mark 5:21–43 – Jairus Daughter and Bleeding Woman",
        "frames": [
            "Faith",
            "Delay",
            "Death",
        ],
        "identity": [
            "[]JesusHonoursRiskyFaithAndHasAuthorityOverDeathAndDefilement(Jesus, Sufferers)",
        ],
        "unit_label": "Do Not Fear, Only Believe",
        "illocution": "MiracleNarrative",
        "agents": [
            "Jesus",
            "Jairus",
            "Daughter",
            "BleedingWoman",
            "Crowd",
        ],
        "description": (
            "On the way to Jairus dying daughter, a bleeding woman is healed by touching Jesus garment, "
            "and Jesus raises the girl, calling for faith not fear."
        ),
        "lambda_iv": [
            "[]JesusHonoursRiskyFaithAndHasAuthorityOverDeathAndDefilement(Jesus, Sufferers)",
            "EFF(ApparentDelaysBecomeStagesForDeeperRevelationOfJesusPower(Disciples))",
        ],
    },

    {
        "passage_id": "Mar06_30_44",
        "chapter": 6,
        "verses": "30-44",
        "title": "Mark 6:30–44 – Feeding the Five Thousand",
        "frames": [
            "Compassion",
            "Provision",
            "Shepherd",
        ],
        "identity": [
            "[]JesusShepherdsSheeplessCrowdsAndMiraculouslyProvidesFood(Jesus, Crowds)",
        ],
        "unit_label": "You Give Them Something to Eat",
        "illocution": "MiracleNarrative",
        "agents": [
            "Jesus",
            "Apostles",
            "Crowds",
        ],
        "description": (
            "Jesus has compassion on crowds like sheep without a shepherd and feeds them with five "
            "loaves and two fish through the apostles hands."
        ),
        "lambda_iv": [
            "[]JesusShepherdsSheeplessCrowdsAndMiraculouslyProvidesFood(Jesus, Crowds)",
            "EFF(ScarcityBecomesOccasionForTrustingJesusProvision(Disciples))",
        ],
    },

    {
        "passage_id": "Mar08_27_38",
        "chapter": 8,
        "verses": "27-38",
        "title": "Mark 8:27–38 – Peter’s Confession and Call to Take Up the Cross",
        "frames": [
            "Christology",
            "Suffering",
            "Discipleship",
        ],
        "identity": [
            "[]ChristMustSufferAndFollowersMustTakeUpCrossToGainTrueLife(Jesus, Disciples)",
        ],
        "unit_label": "Who Do You Say That I Am?",
        "illocution": "ConfessionAndTeaching",
        "agents": [
            "Jesus",
            "Disciples",
            "Peter",
            "Crowd",
        ],
        "description": (
            "Peter confesses Jesus as the Christ; Jesus predicts his suffering and death and calls "
            "disciples to deny themselves and take up their cross."
        ),
        "lambda_iv": [
            "[]ChristMustSufferAndFollowersMustTakeUpCrossToGainTrueLife(Jesus, Disciples)",
            "EFF(PursuitOfWorldlyGainJeopardisesEternalLife(Disciples))",
        ],
    },

    {
        "passage_id": "Mar09_02_13",
        "chapter": 9,
        "verses": "2-13",
        "title": "Mark 9:2–13 – Transfiguration and Elijah Question",
        "frames": [
            "Glory",
            "Sonship",
            "ScriptureFulfilment",
        ],
        "identity": [
            "[]JesusIsBelovedSonWhoMustBeHeardAlongPathOfSuffering(Jesus, Father, Disciples)",
        ],
        "unit_label": "This Is My Beloved Son",
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
            "Jesus is transfigured in glory before three disciples; the Father commands them to "
            "listen to him as they puzzle over Elijah and suffering."
        ),
        "lambda_iv": [
            "[]JesusIsBelovedSonWhoMustBeHeardAlongPathOfSuffering(Jesus, Father, Disciples)",
            "EFF(GloryVisionInterpretsComingPassionForDisciples(Disciples))",
        ],
    },

    {
        "passage_id": "Mar10_17_31",
        "chapter": 10,
        "verses": "17-31",
        "title": "Mark 10:17–31 – Rich Man and Reward of Discipleship",
        "frames": [
            "Wealth",
            "Discipleship",
            "Reward",
        ],
        "identity": [
            "[]AttachmentToWealthHindersKingdomEntryYetGodCanDoImpossible(Wealthy, God)",
        ],
        "unit_label": "Follow Me",
        "illocution": "EncounterAndTeaching",
        "agents": [
            "Jesus",
            "RichMan",
            "Disciples",
        ],
        "description": (
            "A rich man cannot part with possessions to follow Jesus; Jesus teaches the difficulty "
            "for the rich and promises reward to those who leave all."
        ),
        "lambda_iv": [
            "[]AttachmentToWealthHindersKingdomEntryYetGodCanDoImpossible(Wealthy, God)",
            "EFF(RadicalSurrenderForJesusSakeReceivesGreaterKingdomReward(Disciples))",
        ],
    },

    {
        "passage_id": "Mar10_32_45",
        "chapter": 10,
        "verses": "32-45",
        "title": "Mark 10:32–45 – Third Passion Prediction and Ransom Saying",
        "frames": [
            "PassionPrediction",
            "ServantLeadership",
            "Ransom",
        ],
        "identity": [
            "[]SonOfManGivesHisLifeAsRansomAndRedefinesGreatnessAsService(Jesus, Disciples)",
        ],
        "unit_label": "Not to Be Served but to Serve",
        "illocution": "TeachingOnGreatness",
        "agents": [
            "Jesus",
            "Disciples",
            "James",
            "John",
            "TheTen",
        ],
        "description": (
            "On the road to Jerusalem, Jesus predicts his death again while disciples seek status; "
            "he teaches that true greatness is service and his life given as a ransom."
        ),
        "lambda_iv": [
            "[]SonOfManGivesHisLifeAsRansomAndRedefinesGreatnessAsService(Jesus, Disciples)",
            "EFF(CrossShapedServiceIsNormForKingdomLeadership(Disciples))",
        ],
    },

    {
        "passage_id": "Mar11_01_11",
        "chapter": 11,
        "verses": "1-11",
        "title": "Mark 11:1–11 – Triumphal Entry",
        "frames": [
            "Kingship",
            "TempleExpectation",
        ],
        "identity": [
            "[]JesusEntersAsDavidicKingYetWithAmbiguousReception(Jesus, Jerusalem)",
        ],
        "unit_label": "Hosanna in the Highest",
        "illocution": "EntryNarrative",
        "agents": [
            "Jesus",
            "Disciples",
            "Crowds",
        ],
        "description": (
            "Jesus enters Jerusalem on a colt amid Hosannas, presenting himself as king while "
            "quietly surveying the temple."
        ),
        "lambda_iv": [
            "[]JesusEntersAsDavidicKingYetWithAmbiguousReception(Jesus, Jerusalem)",
            "EFF(EntrySetsStageForTempleConfrontationAndJudgment(Jesus, Temple))",
        ],
    },

    {
        "passage_id": "Mar14_22_31",
        "chapter": 14,
        "verses": "22-31",
        "title": "Mark 14:22–31 – Institution of the Supper and Prediction of Scattering",
        "frames": [
            "CovenantMeal",
            "Betrayal",
            "Scattering",
        ],
        "identity": [
            "[]JesusGivesHisBodyAndBloodAsCovenantMealWhileForetellingDisciplesFailure(Jesus, Disciples)",
        ],
        "unit_label": "This Is My Blood of the Covenant",
        "illocution": "CovenantAndWarning",
        "agents": [
            "Jesus",
            "Disciples",
            "Peter",
        ],
        "description": (
            "At the meal Jesus identifies bread and cup with his body and blood and warns that all "
            "will fall away, including Peter."
        ),
        "lambda_iv": [
            "[]JesusGivesHisBodyAndBloodAsCovenantMealWhileForetellingDisciplesFailure(Jesus, Disciples)",
            "EFF(GracePrecedesAndOutlastsDisciplesFailure(Jesus, Disciples))",
        ],
    },

    {
        "passage_id": "Mar14_32_42",
        "chapter": 14,
        "verses": "32-42",
        "title": "Mark 14:32–42 – Gethsemane and Watching in Prayer",
        "frames": [
            "Agony",
            "Submission",
            "Prayer",
        ],
        "identity": [
            "[]JesusSubmitsToFathersWillUnderCrushingSorrowWhileDisciplesFailToWatch(Jesus, Father, Disciples)",
        ],
        "unit_label": "Not What I Will",
        "illocution": "AgonyNarrative",
        "agents": [
            "Jesus",
            "Peter",
            "James",
            "John",
            "Father",
        ],
        "description": (
            "Deeply distressed, Jesus prays for the cup to pass yet submits to the Father; "
            "disciples repeatedly sleep instead of watching and praying."
        ),
        "lambda_iv": [
            "[]JesusSubmitsToFathersWillUnderCrushingSorrowWhileDisciplesFailToWatch(Jesus, Father, Disciples)",
            "EFF(PrayerfulVigilanceIsNeededToWithstandTemptation(Disciples))",
        ],
    },

    {
        "passage_id": "Mar15_21_39",
        "chapter": 15,
        "verses": "21-39",
        "title": "Mark 15:21–39 – Crucifixion and Centurion’s Confession",
        "frames": [
            "Crucifixion",
            "Mockery",
            "DivineAbandonment",
        ],
        "identity": [
            "[]CrucifiedJesusIsTrueSonOfGodRecognisedInHisDeath(Jesus, Centurion)",
        ],
        "unit_label": "Truly This Man Was the Son of God",
        "illocution": "PassionClimax",
        "agents": [
            "Jesus",
            "Soldiers",
            "PassersBy",
            "ChiefPriests",
            "CrucifiedWithHim",
            "Centurion",
        ],
        "description": (
            "Jesus is crucified amid mockery, cries out in abandonment, breathes his last, and the "
            "centurion confesses him as Son of God."
        ),
        "lambda_iv": [
            "[]CrucifiedJesusIsTrueSonOfGodRecognisedInHisDeath(Jesus, Centurion)",
            "EFF(CrossRevealsIdentityOfSonOfGodThroughParadoxicalGlory(Jesus))",
        ],
    },

    {
        "passage_id": "Mar16_01_08",
        "chapter": 16,
        "verses": "1-8",
        "title": "Mark 16:1–8 – Empty Tomb and Trembling Witnesses",
        "frames": [
            "Resurrection",
            "Fear",
            "Commission",
        ],
        "identity": [
            "[]CrucifiedJesusIsRaisedAndAnnouncedYetFearInitiallySilencesWitnesses(Jesus, Women)",
        ],
        "unit_label": "He Has Risen, He Is Not Here",
        "illocution": "ResurrectionAnnouncement",
        "agents": [
            "Women",
            "YoungManInTomb",
            "Disciples",
            "Peter",
        ],
        "description": (
            "Women find the stone rolled away, hear the announcement of Jesus resurrection, and are "
            "charged to tell disciples and Peter, yet flee in trembling and fear."
        ),
        "lambda_iv": [
            "[]CrucifiedJesusIsRaisedAndAnnouncedYetFearInitiallySilencesWitnesses(Jesus, Women)",
            "EFF(ResurrectionMessageOvercomesInitialFearToLaunchWitness(Church))",
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
                "book": "Mark",
                "passage_id": pid,
                "version": f"{pid}_Lambda_IV_v0.1",
            },
            "passage_id": pid,
            "book": "Mark",
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
