import AsyncStorage from "@react-native-async-storage/async-storage";
import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

type SettingsState = {
  aiConsent: boolean;
  consentPromptSeen: boolean;
  setConsent: (value: boolean) => void;
  setConsentPromptSeen: (value: boolean) => void;
  revokeConsent: () => void;
};

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      aiConsent: false,
      consentPromptSeen: false,
      setConsent: (value) => set({ aiConsent: value }),
      setConsentPromptSeen: (value) => set({ consentPromptSeen: value }),
      revokeConsent: () => set({ aiConsent: false })
    }),
    {
      name: "iota-settings",
      storage: createJSONStorage(() => AsyncStorage)
    }
  )
);
