/**
 * Add to apps/mobile/src/lib/api.ts
 * 
 * Receipt request type and API call.
 * Call this after a successful season or moment submission.
 */

export type ReceiptRequest = {
  entry_kind: "season" | "moment";
  eden_text: string;
  modal: Record<string, unknown>;
  attestation: Record<string, unknown>;
  local_mode: boolean;
  crisis_flag: boolean;
  created_at: string;          // ISO string
  entry_id: string;
  include_original_text: boolean;
  original_text?: string;
};

/**
 * Fetches a receipt PDF and returns it as a base64 string.
 * Returns null if the request fails (non-fatal — receipt is optional).
 */
export async function fetchReceiptBase64(payload: ReceiptRequest): Promise<string | null> {
  const url = `${API_BASE}/v1/receipt`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) return null;
    const blob = await res.blob();
    return await blobToBase64(blob);
  } catch {
    return null;
  }
}

function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const result = reader.result as string;
      // Strip the data URL prefix
      resolve(result.split(",")[1] ?? "");
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}
