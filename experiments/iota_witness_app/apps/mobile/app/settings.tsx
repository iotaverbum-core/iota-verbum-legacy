import { Linking, Pressable, ScrollView, StyleSheet, Text, View } from "react-native";

import {
  CONTACT_EMAIL,
  PRIVACY_POLICY_URL,
  TERMS_URL,
  deleteMyData,
  getApiBaseUrl
} from "../src/lib/api";
import { useSettingsStore } from "../src/store/settingsStore";
import { Screen, SymbolsHeader } from "../src/ui/primitives";

export default function SettingsScreen() {
  const aiConsent = useSettingsStore((s) => s.aiConsent);
  const setConsent = useSettingsStore((s) => s.setConsent);

  return (
    <Screen>
      <SymbolsHeader />
      <ScrollView>
        <Text style={styles.title}>Settings</Text>

        <View style={styles.card}>
          <Text style={styles.label}>AI sharing</Text>
          <Text style={styles.note}>
            Allow sending your text to a third-party AI provider for EDEN drafts.
          </Text>
          <View style={styles.row}>
            <Pressable style={styles.button} onPress={() => setConsent(true)}>
              <Text style={styles.buttonText}>{aiConsent ? "Enabled" : "Enable"}</Text>
            </Pressable>
            <Pressable style={styles.button} onPress={() => setConsent(false)}>
              <Text style={styles.buttonText}>{aiConsent ? "Revoke" : "Disabled"}</Text>
            </Pressable>
          </View>
        </View>

        <Pressable style={styles.linkRow} onPress={() => Linking.openURL(PRIVACY_POLICY_URL)}>
          <Text style={styles.linkText}>Privacy Policy</Text>
        </Pressable>

        <Pressable style={styles.linkRow} onPress={() => Linking.openURL(TERMS_URL)}>
          <Text style={styles.linkText}>Terms</Text>
        </Pressable>

        <Pressable style={styles.linkRow} onPress={() => Linking.openURL(`mailto:${CONTACT_EMAIL}`)}>
          <Text style={styles.linkText}>Contact</Text>
        </Pressable>

        <Pressable
          style={styles.linkRow}
          onPress={async () => {
            await deleteMyData();
          }}
        >
          <Text style={styles.linkText}>Delete my data</Text>
        </Pressable>

        <View style={styles.card}>
          <Text style={styles.label}>About</Text>
          <Text style={styles.note}>
            EDEN is a companion app for reflection and abiding in Christ. It is not therapy,
            medical care, or crisis care.
          </Text>
          {__DEV__ ? <Text style={styles.note}>API base: {getApiBaseUrl()}</Text> : null}
        </View>
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  title: {
    fontSize: 22,
    color: "#111",
    marginBottom: 12
  },
  card: {
    borderWidth: 1,
    borderColor: "#111",
    padding: 12,
    marginBottom: 12
  },
  label: {
    color: "#111",
    fontSize: 16,
    marginBottom: 6
  },
  note: {
    color: "#222",
    fontSize: 14,
    lineHeight: 20
  },
  row: {
    flexDirection: "row",
    gap: 10,
    marginTop: 10
  },
  button: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#111",
    paddingVertical: 10,
    alignItems: "center"
  },
  buttonText: {
    color: "#111"
  },
  linkRow: {
    borderWidth: 1,
    borderColor: "#111",
    paddingVertical: 12,
    paddingHorizontal: 12,
    marginBottom: 10
  },
  linkText: {
    color: "#111",
    fontSize: 15
  }
});
