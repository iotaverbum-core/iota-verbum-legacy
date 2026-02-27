import AsyncStorage from "@react-native-async-storage/async-storage";
import Constants from "expo-constants";

const extra = (Constants.expoConfig?.extra ?? {}) as {
  apiBaseUrl?: string;
  privacyPolicyUrl?: string;
  termsUrl?: string;
  localCrisisHelpUrl?: string;
  contactEmail?: string;
};
const PROD_DEFAULT_API_BASE = "https://api.edenwitness.app";
const API_BASE = resolveApiBaseUrl();
export const PRIVACY_POLICY_URL = extra.privacyPolicyUrl ?? `${API_BASE}/v1/privacy`;
export const TERMS_URL = extra.termsUrl ?? `${API_BASE}/v1/terms`;
export const LOCAL_CRISIS_HELP_URL = extra.localCrisisHelpUrl ?? `${API_BASE}/v1/help/local-crisis`;
export const CONTACT_EMAIL = extra.contactEmail ?? "support@example.com";
const DEVICE_KEY = "iota_device_id";

type RequestPayloadPreview = {
  keys: string[];
  text_preview?: string;
};

export class ApiRequestError extends Error {
  constructor(
    message: string,
    public readonly url: string,
    public readonly status?: number,
    public readonly bodyText?: string
  ) {
    super(message);
    this.name = "ApiRequestError";
  }
}

function resolveApiBaseUrl(): string {
  const configured = normalizeBaseUrl(extra.apiBaseUrl);
  if (configured) {
    return configured;
  }
  if (__DEV__) {
    const hostBase = detectExpoHostApiBase();
    if (hostBase) {
      return hostBase;
    }
  }
  return PROD_DEFAULT_API_BASE;
}

function detectExpoHostApiBase(): string | null {
  const constantsAny = Constants as unknown as Record<string, unknown>;
  const expoConfig = (constantsAny.expoConfig ?? {}) as Record<string, unknown>;
  const expoGoConfig = (constantsAny.expoGoConfig ?? {}) as Record<string, unknown>;
  const manifest2 = (constantsAny.manifest2 ?? {}) as Record<string, unknown>;
  const manifest2Extra = (manifest2["extra"] ?? {}) as Record<string, unknown>;
  const manifest2ExpoGo = (manifest2Extra["expoGo"] ?? {}) as Record<string, unknown>;

  const hostCandidates = [
    expoConfig["hostUri"],
    expoGoConfig["debuggerHost"],
    manifest2ExpoGo["debuggerHost"]
  ];

  for (const candidate of hostCandidates) {
    if (typeof candidate !== "string" || candidate.trim().length === 0) {
      continue;
    }
    const host = candidate.split(":")[0];
    if (host) {
      return `http://${host}:8000`;
    }
  }
  return null;
}

function normalizeBaseUrl(value?: string): string | null {
  if (!value) return null;
  const trimmed = value.trim();
  if (!trimmed) return null;
  return trimmed.replace(/\/+$/, "");
}

export function getApiBaseUrl(): string {
  return API_BASE;
}

export function getApiBaseWarning(): string | null {
  if (!__DEV__) return null;
  if (normalizeBaseUrl(extra.apiBaseUrl)) return null;
  if (detectExpoHostApiBase()) return null;
  return "Set EXPO_PUBLIC_API_BASE_URL to your LAN backend URL, e.g. http://192.168.x.x:8000";
}

function simpleUuid(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export async function getDeviceId(): Promise<string> {
  const existing = await AsyncStorage.getItem(DEVICE_KEY);
  if (existing) return existing;
  const next = simpleUuid();
  await AsyncStorage.setItem(DEVICE_KEY, next);
  return next;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const payloadPreview = getPayloadPreview(init?.body);
  let res: Response;
  try {
    res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...init
    });
  } catch (error) {
    if (__DEV__) {
      console.warn("[api] request_failed_network", {
        url,
        error: error instanceof Error ? error.message : String(error),
        payload: payloadPreview
      });
    }
    throw new ApiRequestError(
      `Network request failed for ${url}`,
      url,
      undefined,
      error instanceof Error ? error.message : String(error)
    );
  }

  if (!res.ok) {
    const text = await res.text();
    if (__DEV__) {
      console.warn("[api] request_failed_http", {
        url,
        status: res.status,
        body: text,
        payload: payloadPreview
      });
    }
    throw new ApiRequestError(
      `Request failed: ${res.status}`,
      url,
      res.status,
      text || undefined
    );
  }

  if (__DEV__ && path === "/health") {
    console.info("[api] API_BASE OK", { url, status: res.status });
  }
  return (await res.json()) as T;
}

function getPayloadPreview(body: RequestInit["body"]): RequestPayloadPreview {
  if (typeof body !== "string") {
    return { keys: [] };
  }
  try {
    const parsed = JSON.parse(body) as Record<string, unknown>;
    const text = typeof parsed.text === "string" ? parsed.text : "";
    const text_preview = text ? `${text.slice(0, 12)}...` : undefined;
    return { keys: Object.keys(parsed), text_preview };
  } catch {
    return { keys: [] };
  }
}

export type EntryResponse = {
  eden_text: string;
  modal: Record<string, unknown>;
  attestation: Record<string, unknown>;
  local_mode: boolean;
  crisis_flag: boolean;
  entry_id?: string;
  moment_id?: string;
};

export type TraceResponse = {
  device_id: string;
  dominant_distortion: string;
  velocity_trend: number;
  hinge_consistency: number;
  entrustment_stability: number;
  sample_count: number;
  updated_at: string;
};

export type ShapeResponse = {
  shape: "square" | "diamond" | "triangle";
  symbol: "□" | "◇" | "Δ";
  segment: "necessary" | "enacted" | "effect";
  confidence: number;
  scores?: Record<string, number>;
};

export async function postSeason(
  text: string,
  aiConsent: boolean,
  localOnly: boolean
): Promise<EntryResponse> {
  const device_id = await getDeviceId();
  return request<EntryResponse>("/v1/season_entries", {
    method: "POST",
    body: JSON.stringify({ device_id, text, ai_consent: aiConsent, local_only: localOnly })
  });
}

export async function postMoment(
  text: string,
  aiConsent: boolean,
  localOnly: boolean
): Promise<EntryResponse> {
  const device_id = await getDeviceId();
  return request<EntryResponse>("/v1/moments", {
    method: "POST",
    body: JSON.stringify({ device_id, text, ai_consent: aiConsent, local_only: localOnly })
  });
}

export async function getTrace(): Promise<TraceResponse> {
  const device_id = await getDeviceId();
  return request<TraceResponse>(`/v1/trace?device_id=${encodeURIComponent(device_id)}`);
}

export async function getShapeForCurrentDevice(): Promise<ShapeResponse> {
  const device_id = await getDeviceId();
  return request<ShapeResponse>(`/v1/shape/${encodeURIComponent(device_id)}`);
}

export async function deleteMyData(): Promise<{ device_id: string; deleted: number }> {
  const device_id = await getDeviceId();
  return request<{ device_id: string; deleted: number }>(
    `/v1/user_data/${encodeURIComponent(device_id)}`,
    {
      method: "DELETE"
    }
  );
}

export async function getHealth(): Promise<{ status: string }> {
  return request<{ status: string }>("/health");
}

export async function checkApiHealth(): Promise<{ ok: boolean; message?: string }> {
  try {
    await getHealth();
    return { ok: true };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return { ok: false, message: `${message} (base: ${API_BASE})` };
  }
}

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

