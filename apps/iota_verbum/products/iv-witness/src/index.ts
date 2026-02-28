import { z } from "zod";

export const WitnessConfigSchema = z.object({
  endpoint: z.string().url(),
  apiKey: z.string().min(1),
});

export type WitnessConfig = z.infer<typeof WitnessConfigSchema>;

export function createWitnessClient(config: WitnessConfig): string {
  const parsed = WitnessConfigSchema.parse(config);
  return `iv-witness:${parsed.endpoint}`;
}
