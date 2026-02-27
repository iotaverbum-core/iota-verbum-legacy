import { Link } from "expo-router";
import { Linking, Pressable, ScrollView, StyleSheet, Text, View } from "react-native";

import { CONTACT_EMAIL, LOCAL_CRISIS_HELP_URL } from "../src/lib/api";
import { useResponseStore } from "../src/store/responseStore";
import { ShareReceipt } from "../src/ui/ShareReceipt";
import { Screen, SymbolsHeader } from "../src/ui/primitives";

export default function ResponseScreen() {
  const lastResponse = useResponseStore((s) => s.lastResponse);
  const lastLocalMode = useResponseStore((s) => s.lastLocalMode);
  const lastCrisisFlag = useResponseStore((s) => s.lastCrisisFlag);
  const lastModal = useResponseStore((s) => s.lastModal);
  const lastAttestation = useResponseStore((s) => s.lastAttestation);
  const lastCreatedAt = useResponseStore((s) => s.lastCreatedAt);
  const lastEntryId = useResponseStore((s) => s.lastEntryId);
  const lastOriginalText = useResponseStore((s) => s.lastOriginalText);
  const lastKind = useResponseStore((s) => s.lastKind);
  const history = useResponseStore((s) => s.history);

  return (
    <Screen>
      <SymbolsHeader />
      <Text style={styles.title}>EDEN</Text>
      <ScrollView>
        {lastLocalMode ? <Text style={styles.modePill}>Local mode</Text> : null}
        {lastCrisisFlag ? <Text style={styles.modePill}>Safety response</Text> : null}
        <Text style={styles.response}>{lastResponse ?? "No response yet."}</Text>
        {lastCrisisFlag ? (
          <Pressable style={styles.inlineLink} onPress={() => Linking.openURL(LOCAL_CRISIS_HELP_URL)}>
            <Text style={styles.inlineLinkText}>Find local help</Text>
          </Pressable>
        ) : null}
        <ShareReceipt
          entryKind={lastKind ?? "season"}
          edenText={lastResponse}
          modal={lastModal}
          attestation={lastAttestation}
          localMode={lastLocalMode}
          crisisFlag={lastCrisisFlag}
          createdAt={lastCreatedAt}
          entryId={lastEntryId}
          originalText={lastOriginalText}
        />
        <Text style={styles.subTitle}>Last 20</Text>
        {history.map((item) => (
          <View key={item.id} style={styles.item}>
            <Text style={styles.itemMeta}>
              {item.kind.toUpperCase()} {new Date(item.createdAt).toLocaleDateString()}
            </Text>
            {item.localMode ? <Text style={styles.itemMeta}>Local mode</Text> : null}
            <Text style={styles.itemText}>{item.text}</Text>
          </View>
        ))}
      </ScrollView>
      <Pressable style={styles.button} onPress={() => Linking.openURL(`mailto:${CONTACT_EMAIL}`)}>
        <Text style={styles.buttonText}>Report an issue</Text>
      </Pressable>
      <Link href="/" asChild>
        <Pressable style={styles.button}>
          <Text style={styles.buttonText}>Back Home</Text>
        </Pressable>
      </Link>
    </Screen>
  );
}

const styles = StyleSheet.create({
  title: {
    fontSize: 22,
    color: "#111",
    marginBottom: 12
  },
  response: {
    color: "#111",
    fontSize: 17,
    lineHeight: 24,
    marginBottom: 20
  },
  modePill: {
    alignSelf: "flex-start",
    borderWidth: 1,
    borderColor: "#111",
    paddingHorizontal: 8,
    paddingVertical: 4,
    color: "#111",
    marginBottom: 10
  },
  inlineLink: {
    alignSelf: "flex-start",
    marginBottom: 10
  },
  inlineLinkText: {
    color: "#111",
    textDecorationLine: "underline"
  },
  subTitle: {
    fontSize: 16,
    color: "#111",
    marginBottom: 8
  },
  item: {
    borderTopWidth: 1,
    borderColor: "#ddd",
    paddingVertical: 8
  },
  itemMeta: {
    color: "#444",
    fontSize: 12
  },
  itemText: {
    color: "#111",
    fontSize: 14,
    marginTop: 4
  },
  button: {
    borderWidth: 1,
    borderColor: "#111",
    paddingVertical: 12,
    alignItems: "center",
    marginTop: 8
  },
  buttonText: {
    color: "#111"
  }
});
