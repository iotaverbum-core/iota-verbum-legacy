import { z } from "zod";

export const ShepherdRunSchema = z.object({
  jobId: z.string().min(1),
  priority: z.number().int().min(0).max(10),
});

export type ShepherdRun = z.infer<typeof ShepherdRunSchema>;

export function runShepherd(run: ShepherdRun): string {
  const parsed = ShepherdRunSchema.parse(run);
  return `shepherd-node:${parsed.jobId}`;
}
