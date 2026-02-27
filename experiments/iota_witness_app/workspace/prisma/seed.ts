/**
 * Iota Verbum (IV) - Database Seed Script
 * Populates the database with sample scripture passages
 */

import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

const samplePassages = [
  {
    book: 'John',
    chapter: 1,
    verseStart: 1,
    verseEnd: null,
    textEn: 'In the beginning was the Word, and the Word was with God, and the Word was God.',
    textOriginal: 'Ἐν ἀρχῇ ἦν ὁ Λόγος, καὶ ὁ Λόγος ἦν πρὸς τὸν Θεόν, καὶ Θεὸς ἦν ὁ Λόγος.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'John',
    chapter: 1,
    verseStart: 14,
    verseEnd: null,
    textEn: 'And the Word became flesh and dwelt among us, and we have seen his glory, glory as of the only Son from the Father, full of grace and truth.',
    textOriginal: 'Καὶ ὁ Λόγος σὰρξ ἐγένετο καὶ ἐσκήνωσεν ἐν ἡμῖν, καὶ ἐθεασάμεθα τὴν δόξαν αὐτοῦ, δόξαν ὡς μονογενοῦς παρὰ Πατρός, πλήρης χάριτος καὶ ἀληθείας.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'John',
    chapter: 3,
    verseStart: 16,
    verseEnd: null,
    textEn: 'For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.',
    textOriginal: 'Οὕτως γὰρ ἠγάπησεν ὁ Θεὸς τὸν κόσμον, ὥστε τὸν Υἱὸν τὸν μονογενῆ ἔδωκεν, ἵνα πᾶς ὁ πιστεύων εἰς αὐτὸν μὴ ἀπόληται ἀλλ᾽ ἔχῃ ζωὴν αἰώνιον.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Genesis',
    chapter: 1,
    verseStart: 1,
    verseEnd: null,
    textEn: 'In the beginning, God created the heavens and the earth.',
    textOriginal: 'בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ',
    originalLanguage: 'Hebrew',
    translation: 'ESV',
  },
  {
    book: 'Genesis',
    chapter: 1,
    verseStart: 27,
    verseEnd: null,
    textEn: 'So God created man in his own image, in the image of God he created him; male and female he created them.',
    textOriginal: 'וַיִּבְרָא אֱלֹהִים אֶת-הָאָדָם בְּצַלְמוֹ בְּצֶלֶם אֱלֹהִים בָּרָא אֹתוֹ זָכָר וּנְקֵבָה בָּרָא אֹתָם',
    originalLanguage: 'Hebrew',
    translation: 'ESV',
  },
  {
    book: 'Psalm',
    chapter: 23,
    verseStart: 1,
    verseEnd: null,
    textEn: 'The LORD is my shepherd; I shall not want.',
    textOriginal: 'יְהוָה רֹעִי לֹא אֶחְסָר',
    originalLanguage: 'Hebrew',
    translation: 'ESV',
  },
  {
    book: 'Psalm',
    chapter: 23,
    verseStart: 4,
    verseEnd: null,
    textEn: 'Even though I walk through the valley of the shadow of death, I will fear no evil, for you are with me; your rod and your staff, they comfort me.',
    textOriginal: 'גַּם כִּי-אֵלֵךְ בְּגֵיא צַלְמָוֶת לֹא-אִירָא רָע כִּי-אַתָּה עִמָּדִי שִׁבְטְךָ וּמִשְׁעַנְתֶּךָ הֵמָּה יְנַחֲמֻנִי',
    originalLanguage: 'Hebrew',
    translation: 'ESV',
  },
  {
    book: 'Matthew',
    chapter: 5,
    verseStart: 3,
    verseEnd: null,
    textEn: 'Blessed are the poor in spirit, for theirs is the kingdom of heaven.',
    textOriginal: 'Μακάριοι οἱ πτωχοὶ τῷ πνεύματι, ὅτι αὐτῶν ἐστιν ἡ βασιλεία τῶν οὐρανῶν.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Matthew',
    chapter: 5,
    verseStart: 7,
    verseEnd: null,
    textEn: 'Blessed are the merciful, for they shall receive mercy.',
    textOriginal: 'Μακάριοι οἱ ἐλεήμονες, ὅτι αὐτοὶ ἐλεηθήσονται.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Matthew',
    chapter: 28,
    verseStart: 19,
    verseEnd: 20,
    textEn: 'Go therefore and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit, teaching them to observe all that I have commanded you.',
    textOriginal: 'πορευθέντες οὖν μαθητεύσατε πάντα τὰ ἔθνη, βαπτίζοντες αὐτοὺς εἰς τὸ ὄνομα τοῦ Πατρὸς καὶ τοῦ Υἱοῦ καὶ τοῦ Ἁγίου Πνεύματος, διδάσκοντες αὐτοὺς τηρεῖν πάντα ὅσα ἐνετειλάμην ὑμῖν',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Romans',
    chapter: 8,
    verseStart: 28,
    verseEnd: null,
    textEn: 'And we know that for those who love God all things work together for good, for those who are called according to his purpose.',
    textOriginal: 'οἴδαμεν δὲ ὅτι τοῖς ἀγαπῶσιν τὸν Θεὸν πάντα συνεργεῖ εἰς ἀγαθόν, τοῖς κατὰ πρόθεσιν κλητοῖς οὖσιν.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Romans',
    chapter: 8,
    verseStart: 38,
    verseEnd: 39,
    textEn: 'For I am sure that neither death nor life, nor angels nor rulers, nor things present nor things to come, nor powers, nor height nor depth, nor anything else in all creation, will be able to separate us from the love of God in Christ Jesus our Lord.',
    textOriginal: 'πέπεισμαι γὰρ ὅτι οὔτε θάνατος οὔτε ζωὴ οὔτε ἄγγελοι οὔτε ἀρχαὶ οὔτε ἐνεστῶτα οὔτε μέλλοντα οὔτε δυνάμεις οὔτε ὕψωμα οὔτε βάθος οὔτε κτίσις ἑτέρα δυνήσεται ἡμᾶς χωρίσαι ἀπὸ τῆς ἀγάπης τοῦ Θεοῦ τῆς ἐν Χριστῷ Ἰησοῦ τῷ Κυρίῳ ἡμῶν.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Philippians',
    chapter: 4,
    verseStart: 13,
    verseEnd: null,
    textEn: 'I can do all things through him who strengthens me.',
    textOriginal: 'πάντα ἰσχύω ἐν τῷ ἐνδυναμοῦντί με.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Isaiah',
    chapter: 40,
    verseStart: 31,
    verseEnd: null,
    textEn: 'But they who wait for the LORD shall renew their strength; they shall mount up with wings like eagles; they shall run and not be weary; they shall walk and not faint.',
    textOriginal: 'וְקוֹיֵ יְהוָה יַחֲלִיפוּ כֹחַ יַעֲלוּ אֵבֶר כַּנְּשָׁרִים יָרוּצוּ וְלֹא יִיגָעוּ יֵלֵכוּ וְלֹא יִיעָפוּ׃',
    originalLanguage: 'Hebrew',
    translation: 'ESV',
  },
  {
    book: 'Isaiah',
    chapter: 53,
    verseStart: 5,
    verseEnd: null,
    textEn: 'But he was pierced for our transgressions; he was crushed for our iniquities; upon him was the chastisement that brought us peace, and with his wounds we are healed.',
    textOriginal: 'וְהוּא מְחֹלָל מִפְּשָׁעֵינוּ מְדֻכָּא מֵעֲוֹנֹתֵינוּ מוּסַר שְׁלוֹמֵנוּ עָלָיו וּבַחֲבֻרָתוֹ נִרְפָּא-לָנוּ',
    originalLanguage: 'Hebrew',
    translation: 'ESV',
  },
  {
    book: 'Hebrews',
    chapter: 11,
    verseStart: 1,
    verseEnd: null,
    textEn: 'Now faith is the assurance of things hoped for, the conviction of things not seen.',
    textOriginal: 'Ἔστιν δὲ πίστις ἐλπιζομένων ὑπόστασις, πραγμάτων ἔλεγχος οὐ βλεπομένων.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Hebrews',
    chapter: 13,
    verseStart: 8,
    verseEnd: null,
    textEn: 'Jesus Christ is the same yesterday and today and forever.',
    textOriginal: 'Ἰησοῦς Χριστὸς ἐχθὲς καὶ σήμερον ὁ αὐτός, καὶ εἰς τοὺς αἰῶνας.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Ephesians',
    chapter: 2,
    verseStart: 8,
    verseEnd: 9,
    textEn: 'For by grace you have been saved through faith. And this is not your own doing; it is the gift of God, not a result of works, so that no one may boast.',
    textOriginal: 'τῇ γὰρ χάριτί ἐστε σεσῳσμένοι διὰ πίστεως· καὶ τοῦτο οὐκ ἐξ ὑμῶν, Θεοῦ τὸ δῶρον· οὐκ ἐξ ἔργων, ἵνα μή τις καυχήσηται.',
    originalLanguage: 'Greek',
    translation: 'ESV',
  },
  {
    book: 'Proverbs',
    chapter: 3,
    verseStart: 5,
    verseEnd: 6,
    textEn: 'Trust in the LORD with all your heart, and do not lean on your own understanding. In all your ways acknowledge him, and he will make straight your paths.',
    textOriginal: 'בְּטַח אֶל-יְהוָה בְּכָל-לִבֶּךָ וְאַל-בִּינָתְךָ אַל-תִּשָּׁעֵן בְּכָל-דְּרָכֶיךָ דָעֵהוּ וְהוּא יְיַשֵּׁר אֹרְחֹתֶיךָ',
    originalLanguage: 'Hebrew',
    translation: 'ESV',
  },
  {
    book: 'Jeremiah',
    chapter: 29,
    verseStart: 11,
    verseEnd: null,
    textEn: 'For I know the plans I have for you, declares the LORD, plans for welfare and not for evil, to give you a future and a hope.',
    textOriginal: 'כִּי אָנֹכִי יָדַעְתִּי אֶת-הַמַּחֲשָׁבֹת אֲשֶׁר חָשַׁבְתִּי עֲלֵיכֶם נְאֻם-יְהוָה מַחֲשְׁבוֹת שָׁלוֹם וְלֹא לְרָעָה לָתֵת לָכֶם אַחֲרִית וְתִקְוָה',
    originalLanguage: 'Hebrew',
    translation: 'ESV',
  },
];

async function main() {
  console.log('🌱 Starting database seed...');

  // Clear existing data
  await prisma.ethicsReview.deleteMany();
  await prisma.witnessCard.deleteMany();
  await prisma.modalEncoding.deleteMany();
  await prisma.scripturePassage.deleteMany();
  console.log('✅ Cleared existing data');

  // Insert sample passages
  let inserted = 0;
  for (const passage of samplePassages) {
    try {
      await prisma.scripturePassage.create({
        data: passage
      });
      inserted++;
      console.log(`✅ Inserted: ${passage.book} ${passage.chapter}:${passage.verseStart}`);
    } catch (error) {
      console.log(`⚠️ Skipped: ${passage.book} ${passage.chapter}:${passage.verseStart} (may already exist)`);
    }
  }

  console.log(`\n🎉 Seed complete! Inserted ${inserted} passages.`);
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
