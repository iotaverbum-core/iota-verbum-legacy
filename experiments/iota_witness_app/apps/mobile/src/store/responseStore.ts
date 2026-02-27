import AsyncStorage from "@react-native-async-storage/async-storage";
import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

type HistoryItem = {
  id: string;
  kind: "season" | "moment";
  text: string;
  localMode: boolean;
  crisisFlag: boolean;
  createdAt: string;
};

type ResponseState = {
  lastResponse: string | null;
  lastLocalMode: boolean;
  lastCrisisFlag: boolean;
  lastModal: Record<string, unknown> | null;
  lastAttestation: Record<string, unknown> | null;
  lastCreatedAt: string | null;
  lastEntryId: string | null;
  lastOriginalText: string | null;
  lastKind: "season" | "moment" | null;
  history: HistoryItem[];
  setLastResponse: (
    kind: HistoryItem["kind"],
    text: string,
    localMode: boolean,
    crisisFlag: boolean,
    modal: Record<string, unknown> | null,
    attestation: Record<string, unknown> | null,
    createdAt: string | null,
    entryId: string | null,
    originalText: string | null
  ) => void;
};

export const useResponseStore = create<ResponseState>()(
  persist(
    (set) => ({
      lastResponse: null,
      lastLocalMode: false,
      lastCrisisFlag: false,
      lastModal: null,
      lastAttestation: null,
      lastCreatedAt: null,
      lastEntryId: null,
      lastOriginalText: null,
      lastKind: null,
      history: [],
      setLastResponse: (kind, text, localMode, crisisFlag, modal, attestation, createdAt, entryId, originalText) =>
        set((state) => {
          const item: HistoryItem = {
            id: `${Date.now()}`,
            kind,
            text,
            localMode,
            crisisFlag,
            createdAt: new Date().toISOString()
          };
          return {
            lastResponse: text,
            lastLocalMode: localMode,
            lastCrisisFlag: crisisFlag,
            lastModal: modal,
            lastAttestation: attestation,
            lastCreatedAt: createdAt,
            lastEntryId: entryId,
            lastOriginalText: originalText,
            lastKind: kind,
            history: [item, ...state.history].slice(0, 20)
          };
        })
    }),
    {
      name: "iota-response-history",
      storage: createJSONStorage(() => AsyncStorage)
    }
  )
);
