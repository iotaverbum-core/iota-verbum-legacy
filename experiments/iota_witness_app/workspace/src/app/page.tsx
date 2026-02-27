'use client';

import { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { WitnessCard, WitnessCardCompact } from '@/components/iv/witness-card';
import { ScriptureBrowser } from '@/components/iv/scripture-browser';
import { OperatorLegend } from '@/components/iv/operator-badge';
import { Loader2, BookOpen, Shield, Brain, ArrowRight, CheckCircle2, Sparkles, FileText, Code } from 'lucide-react';
import { toast } from 'sonner';

// Types
interface Passage {
  id: string;
  book: string;
  chapter: number;
  verseStart: number;
  verseEnd: number | null;
  textEn: string;
  textOriginal?: string | null;
  originalLanguage?: string | null;
}

interface WitnessCardData {
  id: string;
  title: string;
  summary: string;
  modalAnalysis: string;
  themes: string;
  ethicsCheck: string;
  proofHash: string;
  verified: boolean;
  createdAt: string;
  passage?: Passage;
}

export default function Home() {
  const [selectedPassage, setSelectedPassage] = useState<Passage | null>(null);
  const [currentCard, setCurrentCard] = useState<WitnessCardData | null>(null);
  const [aiAnalysis, setAiAnalysis] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [recentCards, setRecentCards] = useState<WitnessCardData[]>([]);

  // Generate witness card
  const generateWitnessCard = useCallback(async (passage: Passage) => {
    setIsGenerating(true);
    setCurrentCard(null);
    setAiAnalysis(null);

    try {
      const response = await fetch('/api/witness-card', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          passageId: passage.id,
          includeAIAnalysis: true,
        }),
      });

      if (!response.ok) throw new Error('Failed to generate witness card');

      const data = await response.json();
      setCurrentCard(data.card);
      setAiAnalysis(data.aiAnalysis);

      // Add to recent cards
      setRecentCards(prev => {
        const newCard = data.card;
        const exists = prev.find(c => c.id === newCard.id);
        if (!exists) {
          return [newCard, ...prev].slice(0, 5);
        }
        return prev;
      });

      toast.success('Witness card generated successfully!');
    } catch (error) {
      console.error('Error generating witness card:', error);
      toast.error('Failed to generate witness card. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  }, []);

  // Handle passage selection
  const handleSelectPassage = useCallback((passage: Passage) => {
    setSelectedPassage(passage);
    generateWitnessCard(passage);
  }, [generateWitnessCard]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900">
      {/* Header */}
      <header className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {/* IV Logo */}
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#1a1f3c] to-[#2a3050] flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-xl">□◇</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">Iota Verbum</h1>
                <p className="text-xs text-muted-foreground">Computational Theology Framework</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="text-xs">
                <Shield className="h-3 w-3 mr-1 text-green-500" />
                Ethics Verified
              </Badge>
              <Badge variant="outline" className="text-xs">
                <Brain className="h-3 w-3 mr-1 text-blue-500" />
                Deterministic AI
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="border-b bg-gradient-to-r from-[#1a1f3c] via-[#2a3050] to-[#1a1f3c] text-white">
        <div className="container mx-auto px-4 py-12">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4">
              Modal Logic + AI Ethics + Biblical Theology
            </h2>
            <p className="text-lg text-white/80 mb-6">
              A computational framework for verifiable, deterministic reasoning in theological analysis.
              Generate witness cards with modal logic encodings, ethics reviews, and cryptographic proof.
            </p>
            <div className="flex items-center justify-center gap-4">
              <OperatorLegend className="justify-center" />
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="analyze" className="space-y-6">
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-3">
            <TabsTrigger value="analyze">Analyze</TabsTrigger>
            <TabsTrigger value="browse">Browse</TabsTrigger>
            <TabsTrigger value="about">About</TabsTrigger>
          </TabsList>

          {/* Analyze Tab */}
          <TabsContent value="analyze" className="space-y-6">
            <div className="grid lg:grid-cols-3 gap-6">
              {/* Scripture Browser */}
              <div className="lg:col-span-1">
                <ScriptureBrowser
                  onSelectPassage={handleSelectPassage}
                  selectedPassageId={selectedPassage?.id}
                />
              </div>

              {/* Witness Card Display */}
              <div className="lg:col-span-2 space-y-6">
                {isGenerating && (
                  <Card className="border-dashed">
                    <CardContent className="py-16">
                      <div className="flex flex-col items-center justify-center text-center">
                        <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
                        <h3 className="text-lg font-medium mb-2">Generating Witness Card</h3>
                        <p className="text-sm text-muted-foreground">
                          Analyzing modal operators, ethics compliance, and generating proof hash...
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {!isGenerating && currentCard && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold">Generated Witness Card</h3>
                      <div className="flex gap-2">
                        <Button 
                          variant="outline" 
                          size="sm" 
                          onClick={() => selectedPassage && generateWitnessCard(selectedPassage)}
                          disabled={isGenerating}
                        >
                          <Sparkles className="h-4 w-4 mr-1" />
                          Regenerate
                        </Button>
                      </div>
                    </div>
                    <WitnessCard card={currentCard} aiAnalysis={aiAnalysis} />
                  </div>
                )}

                {!isGenerating && !currentCard && (
                  <Card className="border-dashed">
                    <CardContent className="py-16">
                      <div className="flex flex-col items-center justify-center text-center">
                        <BookOpen className="h-12 w-12 text-muted-foreground/50 mb-4" />
                        <h3 className="text-lg font-medium mb-2">Select a Scripture Passage</h3>
                        <p className="text-sm text-muted-foreground max-w-md">
                          Choose a passage from the browser to generate a witness card with modal analysis, 
                          ethics review, and cryptographic proof.
                        </p>
                        <div className="flex gap-4 mt-6">
                          <div className="flex items-center gap-2 text-xs text-muted-foreground">
                            <FileText className="h-4 w-4" />
                            Export as HTML/PDF
                          </div>
                          <div className="flex items-center gap-2 text-xs text-muted-foreground">
                            <Code className="h-4 w-4" />
                            Export as JSON
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Recent Cards */}
                {recentCards.length > 0 && !isGenerating && (
                  <div className="space-y-3">
                    <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
                      Recent Witness Cards
                    </h4>
                    <div className="grid md:grid-cols-2 gap-3">
                      {recentCards.map((card) => (
                        <WitnessCardCompact 
                          key={card.id} 
                          card={card} 
                          onClick={() => {
                            setCurrentCard(card);
                            setSelectedPassage(card.passage || null);
                          }}
                        />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </TabsContent>

          {/* Browse Tab */}
          <TabsContent value="browse" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-amber-500" />
                    Modal Operators
                  </CardTitle>
                  <CardDescription>
                    The five core modal operators used in Iota Verbum analysis
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { op: 'NECESSITY', symbol: '□', divine: "God's Decree", human: 'Divine Sovereignty', desc: 'Represents God\'s eternal purpose that cannot be thwarted.' },
                      { op: 'POSSIBILITY', symbol: '◇', divine: 'Divine Permission', human: 'Human Agency', desc: 'Represents the space for human freedom within divine providence.' },
                      { op: 'WITNESS', symbol: 'W', divine: 'Divine Testimony', human: 'Human Testimony', desc: 'The bridge between divine truth and human understanding.' },
                      { op: 'SEPARATION', symbol: 'σ', divine: 'Holy Distinction', human: 'Discernment', desc: 'Distinguishing essence from accident, sacred from profane.' },
                      { op: 'STAYING', symbol: 'π', divine: 'Divine Faithfulness', human: 'Perseverance', desc: 'Covenantal endurance that maintains relationship across time.' },
                    ].map((item) => (
                      <div key={item.op} className="flex items-start gap-3 p-3 rounded-lg bg-muted/30">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#1a1f3c] to-[#2a3050] flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                          {item.symbol}
                        </div>
                        <div>
                          <h4 className="font-medium">{item.divine} / {item.human}</h4>
                          <p className="text-sm text-muted-foreground mt-1">{item.desc}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="h-5 w-5 text-green-500" />
                    Ethics Principles
                  </CardTitle>
                  <CardDescription>
                    Core ethical principles for AI output evaluation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {[
                      { name: 'Sanctity of Life', desc: 'Human life is sacred, created in God\'s image.', basis: 'Genesis 1:27' },
                      { name: 'Truthfulness', desc: 'Honesty and accuracy reflecting God\'s nature as truth.', basis: 'John 14:6' },
                      { name: 'Stewardship', desc: 'Responsible care for God\'s creation and resources.', basis: 'Genesis 2:15' },
                      { name: 'Love', desc: 'Selfless concern for others\' well-being.', basis: 'Matthew 22:37-39' },
                      { name: 'Justice', desc: 'Fairness, equity, standing against oppression.', basis: 'Micah 6:8' },
                      { name: 'Honor', desc: 'Respect for God, authority, and human dignity.', basis: '1 Peter 2:17' },
                      { name: 'Purity', desc: 'Moral and sexual purity, guarding heart and mind.', basis: 'Philippians 4:8' },
                    ].map((principle) => (
                      <div key={principle.name} className="flex items-start gap-3 p-2 rounded-lg hover:bg-muted/30 transition-colors">
                        <CheckCircle2 className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                        <div>
                          <h4 className="font-medium text-sm">{principle.name}</h4>
                          <p className="text-xs text-muted-foreground">{principle.desc}</p>
                          <p className="text-xs text-muted-foreground/70 mt-0.5">{principle.basis}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Inference Rules */}
            <Card>
              <CardHeader>
                <CardTitle>Modal Logic Inference Rules</CardTitle>
                <CardDescription>
                  Formal rules for deriving new modal statements
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {[
                    { name: 'Necessitation', premise: '⊢ P', conclusion: '⊢ □P', desc: 'If P is a theorem, then necessarily P' },
                    { name: 'Dual', premise: '□P', conclusion: '¬◇¬P', desc: 'Necessity equals impossibility of contrary' },
                    { name: 'T-Axiom', premise: '□P', conclusion: 'P', desc: 'What is necessary is actual' },
                    { name: 'Witness-Formation', premise: '□P ∧ ◇Q', conclusion: 'W(P,Q)', desc: 'Divine necessity + human possibility = witness' },
                    { name: 'Separation-Principle', premise: 'W(P,Q)', conclusion: 'σ(P,essence)', desc: 'Witness enables separation' },
                    { name: 'Staying-Condition', premise: '□F ∧ ◇H', conclusion: 'π(F,H)', desc: 'Faithfulness meets hope' },
                  ].map((rule) => (
                    <div key={rule.name} className="p-3 rounded-lg border bg-muted/20">
                      <h4 className="font-medium text-sm mb-1">{rule.name}</h4>
                      <div className="flex items-center gap-2 text-xs font-mono mb-2">
                        <span className="text-muted-foreground">{rule.premise}</span>
                        <ArrowRight className="h-3 w-3 text-primary" />
                        <span className="text-primary">{rule.conclusion}</span>
                      </div>
                      <p className="text-xs text-muted-foreground">{rule.desc}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* About Tab */}
          <TabsContent value="about" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>About Iota Verbum (IV)</CardTitle>
                <CardDescription>
                  &ldquo;The smallest word&rdquo; — A framework for computational theology
                </CardDescription>
              </CardHeader>
              <CardContent className="prose prose-sm dark:prose-invert max-w-none">
                <p className="text-foreground/80 leading-relaxed">
                  <strong>Iota Verbum</strong> (Latin for &ldquo;the smallest word&rdquo;) is a computational framework 
                  that bridges <strong>modal logic</strong>, <strong>AI ethics</strong>, and <strong>biblical theology</strong>. 
                  It provides tools for generating verifiable, deterministic analysis of scripture passages with 
                  formal logical encoding and ethical review.
                </p>

                <h3 className="text-lg font-semibold mt-6 mb-3">Core Features</h3>
                <ul className="space-y-2 text-foreground/80">
                  <li className="flex items-start gap-2">
                    <ArrowRight className="h-4 w-4 text-primary mt-1 flex-shrink-0" />
                    <span><strong>Modal Logic Engine</strong> — Encodes theological concepts using formal modal operators (□, ◇, W, σ, π)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ArrowRight className="h-4 w-4 text-primary mt-1 flex-shrink-0" />
                    <span><strong>Witness Card Generator</strong> — Creates comprehensive analysis cards with proof hashes for verification</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ArrowRight className="h-4 w-4 text-primary mt-1 flex-shrink-0" />
                    <span><strong>Ethics Review System</strong> — Evaluates AI outputs against Christian ethical principles</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ArrowRight className="h-4 w-4 text-primary mt-1 flex-shrink-0" />
                    <span><strong>Deterministic AI</strong> — Provides reproducible, verifiable analysis (temperature = 0)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ArrowRight className="h-4 w-4 text-primary mt-1 flex-shrink-0" />
                    <span><strong>Multi-language Support</strong> — Handles Greek, Hebrew, and Aramaic original texts</span>
                  </li>
                </ul>

                <h3 className="text-lg font-semibold mt-6 mb-3">Theological Foundation</h3>
                <p className="text-foreground/80 leading-relaxed">
                  The system maps theological concepts to modal logic operators, providing a formal language 
                  for discussing divine sovereignty (□ necessity), human agency (◇ possibility), testimony 
                  (W witness), holiness (σ separation), and covenantal faithfulness (π staying). This allows 
                  for precise, reproducible theological reasoning that can be verified and audited.
                </p>

                <h3 className="text-lg font-semibold mt-6 mb-3">Verification & Trust</h3>
                <p className="text-foreground/80 leading-relaxed">
                  Every witness card includes a cryptographic proof hash, ensuring that the analysis can be 
                  independently verified. The deterministic nature of the AI reasoning (using temperature = 0) 
                  means the same input will always produce the same output, enabling reproducibility and audit.
                </p>

                <h3 className="text-lg font-semibold mt-6 mb-3">Export Options</h3>
                <div className="grid md:grid-cols-2 gap-4 mt-4">
                  <div className="p-4 rounded-lg border bg-muted/20">
                    <h4 className="font-medium flex items-center gap-2">
                      <FileText className="h-4 w-4" />
                      HTML/PDF Export
                    </h4>
                    <p className="text-sm text-muted-foreground mt-2">
                      Export witness cards as styled HTML documents that can be printed to PDF or shared directly.
                    </p>
                  </div>
                  <div className="p-4 rounded-lg border bg-muted/20">
                    <h4 className="font-medium flex items-center gap-2">
                      <Code className="h-4 w-4" />
                      JSON Export
                    </h4>
                    <p className="text-sm text-muted-foreground mt-2">
                      Export machine-readable JSON for integration with other systems or archival purposes.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t bg-muted/30 mt-12">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#1a1f3c] to-[#2a3050] flex items-center justify-center">
                <span className="text-white font-bold text-sm">□◇</span>
              </div>
              <span className="text-sm text-muted-foreground">
                Iota Verbum — Computational Theology Framework
              </span>
            </div>
            <div className="flex items-center gap-4 text-xs text-muted-foreground">
              <span>Built with Next.js & Modal Logic</span>
              <span>•</span>
              <span>© 2024</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
