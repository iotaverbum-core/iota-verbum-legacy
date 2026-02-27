'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { cn } from '@/lib/utils';
import { Search, BookOpen, Loader2 } from 'lucide-react';

const BOOKS = [
  'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
  'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
  '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
  'Nehemiah', 'Esther', 'Job', 'Psalm', 'Proverbs',
  'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations',
  'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
  'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk',
  'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
  'Matthew', 'Mark', 'Luke', 'John', 'Acts',
  'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
  'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy',
  '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James',
  '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
  'Jude', 'Revelation'
];

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

interface ScriptureBrowserProps {
  onSelectPassage: (passage: Passage) => void;
  selectedPassageId?: string;
  className?: string;
}

export function ScriptureBrowser({ onSelectPassage, selectedPassageId, className }: ScriptureBrowserProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedBook, setSelectedBook] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [passages, setPassages] = useState<Passage[]>([]);

  // Fetch passages from API
  useEffect(() => {
    const fetchPassages = async () => {
      setIsLoading(true);
      try {
        const params = new URLSearchParams();
        if (selectedBook) params.set('book', selectedBook);
        params.set('limit', '100');
        
        const response = await fetch(`/api/bible?${params.toString()}`);
        const data = await response.json();
        setPassages(data.passages || []);
      } catch (error) {
        console.error('Failed to fetch passages:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPassages();
  }, [selectedBook]);

  // Filter passages based on search
  const filteredPassages = passages.filter(p => {
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      return (
        p.book.toLowerCase().includes(query) ||
        p.textEn.toLowerCase().includes(query)
      );
    }
    return true;
  });

  const getLanguageBadge = (lang: string | null | undefined) => {
    if (!lang) return null;
    const colors: Record<string, string> = {
      Greek: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
      Hebrew: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400',
      Aramaic: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
    };
    return (
      <Badge className={cn('text-xs', colors[lang] || '')}>
        {lang}
      </Badge>
    );
  };

  return (
    <Card className={cn('h-full', className)}>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <BookOpen className="h-5 w-5 text-primary" />
          Scripture Browser
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Search Controls */}
        <div className="space-y-3">
          <div className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search by book or text..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9"
              />
            </div>
          </div>

          <div>
            <Label className="text-xs text-muted-foreground">Filter by Book</Label>
            <Select value={selectedBook} onValueChange={setSelectedBook}>
              <SelectTrigger className="h-9">
                <SelectValue placeholder="All books" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All books</SelectItem>
                {BOOKS.map(book => (
                  <SelectItem key={book} value={book}>{book}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Passage List */}
        <ScrollArea className="h-[400px] pr-2">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : (
            <div className="space-y-2">
              {filteredPassages.map((passage) => (
                <div
                  key={passage.id}
                  className={cn(
                    'p-3 rounded-lg border cursor-pointer transition-all',
                    selectedPassageId === passage.id
                      ? 'border-primary bg-primary/5'
                      : 'hover:border-primary/50 bg-muted/30'
                  )}
                  onClick={() => onSelectPassage(passage)}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-sm">
                        {passage.book} {passage.chapter}:{passage.verseStart}{passage.verseEnd ? `-${passage.verseEnd}` : ''}
                      </h4>
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                        {passage.textEn}
                      </p>
                    </div>
                    {getLanguageBadge(passage.originalLanguage)}
                  </div>
                </div>
              ))}

              {filteredPassages.length === 0 && !isLoading && (
                <div className="text-center py-8 text-muted-foreground">
                  <BookOpen className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No passages found</p>
                </div>
              )}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
