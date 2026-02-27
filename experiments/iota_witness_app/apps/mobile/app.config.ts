import type { ExpoConfig } from "expo/config";

declare const process: { env: Record<string, string | undefined> };

const isProductionBuild = process.env.NODE_ENV === "production" || process.env.EAS_BUILD === "true";

const config: ExpoConfig = {
  name: "EDEN",
  slug: "eden-witness",
  scheme: "eden-witness",
  version: "1.0.0",
  orientation: "portrait",
  userInterfaceStyle: "light",
  extra: {
    apiBaseUrl: process.env.EXPO_PUBLIC_API_BASE_URL ?? (isProductionBuild ? "https://api.edenwitness.app" : ""),
    privacyPolicyUrl:
      process.env.EXPO_PUBLIC_PRIVACY_POLICY_URL ?? "https://edenwitness.app/privacy",
    termsUrl: process.env.EXPO_PUBLIC_TERMS_URL ?? "https://edenwitness.app/terms",
    localCrisisHelpUrl:
      process.env.EXPO_PUBLIC_LOCAL_CRISIS_HELP_URL ?? "https://edenwitness.app/help/local-crisis",
    contactEmail: process.env.EXPO_PUBLIC_CONTACT_EMAIL ?? "support@edenwitness.app",
    eas: {
      projectId: "6f5a9c4e-4f6e-4ea7-b5c8-8f7002ca7f66"
    }
  },
  ios: {
    supportsTablet: false,
    bundleIdentifier: "app.edenwitness.mobile",
    privacyManifests: {
      NSPrivacyTracking: false,
      NSPrivacyCollectedDataTypes: [],
      NSPrivacyAccessedAPITypes: []
    }
  },
  android: {
    package: "app.edenwitness.mobile"
  },
  plugins: [
    "expo-router",
    [
      "expo-build-properties",
      {
        ios: {
          privacyManifestAggregationEnabled: true
        }
      }
    ]
  ]
};

export default config;
