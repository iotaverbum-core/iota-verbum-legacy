import { z } from "zod";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

export const ScriptureDatasetManifest = z.object({
  id: z.string(),
  title: z.string(),
  license: z.string().optional(),
  source: z.string().optional(),
  language: z.string().default("en"),
  format: z.enum(["txt", "json", "jsonl", "csv"]).default("txt"),
  files: z.array(z.string()).min(1),
  sha256: z.string().optional(), // optional for now; can enforce later
  created_at: z.string().optional()
});

export type ScriptureDatasetManifest = z.infer<typeof ScriptureDatasetManifest>;

export async function loadManifest(manifestPath: string): Promise<ScriptureDatasetManifest> {
  const abs = resolve(manifestPath);
  const raw = await readFile(abs, "utf8");
  const json = JSON.parse(raw);
  return ScriptureDatasetManifest.parse(json);
}

/**
 * Convenience: load a text file listed in the manifest.
 * Assumes the file paths are relative to the manifest file.
 */
export async function loadTextFromManifest(manifestPath: string, relativeFile: string): Promise<string> {
  const baseDir = resolve(manifestPath, "..");
  const abs = resolve(baseDir, relativeFile);
  return await readFile(abs, "utf8");
}
