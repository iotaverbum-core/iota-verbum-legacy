/**
 * apps/mobile/src/ui/ShareReceipt.tsx
 * 
 * Drop this component into response.tsx just above the Back Home button.
 * Requires: expo-file-system, expo-sharing  (both included in Expo SDK 54)
 * 
 * Usage in response.tsx:
 *   import { ShareReceipt } from "../src/ui/ShareReceipt";
 *   ...
 *   <ShareReceipt
 *     entryKind={lastKind}
 *     edenText={lastResponse}
 *     modal={lastModal}
 *     attestation={lastAttestation}
 *     localMode={lastLocalMode}
 *     crisisFlag={lastCrisisFlag}
 *     createdAt={lastCreatedAt}
 *     entryId={lastEntryId}
 *     originalText={lastOriginalText}
 *   />
 */

import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import { useState } from "react";
import { Alert, Modal, Pressable, StyleSheet, Switch, Text, View } from "react-native";

import { fetchReceiptBase64 } from "../lib/api";

type Props = {
  entryKind: "season" | "moment";
  edenText: string | null;
  modal: Record<string, unknown> | null;
  attestation: Record<string, unknown> | null;
  localMode: boolean;
  crisisFlag: boolean;
  createdAt: string | null;
  entryId: string | null;
  originalText?: string | null;
};

export function ShareReceipt({
  entryKind,
  edenText,
  modal,
  attestation,
  localMode,
  crisisFlag,
  createdAt,
  entryId,
  originalText,
}: Props) {
  const [modalVisible, setModalVisible] = useState(false);
  const [includeText, setIncludeText] = useState(false);
  const [loading, setLoading] = useState(false);

  // Don't render if we don't have enough data
  if (!edenText || !modal || !attestation || !createdAt || !entryId) return null;

  async function handleShare() {
    setLoading(true);
    try {
      const base64 = await fetchReceiptBase64({
        entry_kind: entryKind,
        eden_text: edenText!,
        modal: modal!,
        attestation: attestation!,
        local_mode: localMode,
        crisis_flag: crisisFlag,
        created_at: createdAt!,
        entry_id: entryId!,
        include_original_text: includeText,
        original_text: includeText ? (originalText ?? undefined) : undefined,
      });

      if (!base64) {
        Alert.alert("Receipt unavailable", "Could not generate receipt. Please try again.");
        return;
      }

      const filename = `eden_receipt_${entryId!.slice(0, 8)}.pdf`;
      const fileUri = `${FileSystem.cacheDirectory}${filename}`;

      await FileSystem.writeAsStringAsync(fileUri, base64, {
        encoding: FileSystem.EncodingType.Base64,
      });

      const canShare = await Sharing.isAvailableAsync();
      if (!canShare) {
        Alert.alert("Sharing unavailable", "Your device does not support file sharing.");
        return;
      }

      setModalVisible(false);
      await Sharing.shareAsync(fileUri, {
        mimeType: "application/pdf",
        dialogTitle: "Share EDEN Receipt",
        UTI: "com.adobe.pdf",
      });
    } catch (err) {
      Alert.alert("Error", "Something went wrong generating the receipt.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Pressable style={styles.button} onPress={() => setModalVisible(true)}>
        <Text style={styles.buttonText}>Share receipt</Text>
      </Pressable>

      <Modal
        visible={modalVisible}
        transparent
        animationType="fade"
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.backdrop}>
          <View style={styles.card}>
            <Text style={styles.title}>Attestation receipt</Text>
            <Text style={styles.body}>
              The receipt includes the EDEN response, guardrail checks, and verification hashes. A
              spiritual director or counsellor can use it to see exactly what was generated and that
              it has not been altered.
            </Text>

            <View style={styles.toggleRow}>
              <Text style={styles.toggleLabel}>Include my original entry text</Text>
              <Switch
                value={includeText}
                onValueChange={setIncludeText}
                trackColor={{ true: "#111", false: "#ccc" }}
                thumbColor="#fff"
              />
            </View>
            {includeText ? (
              <Text style={styles.hint}>
                Your entry text will appear in the PDF. Only share with someone you trust.
              </Text>
            ) : null}

            <View style={styles.row}>
              <Pressable
                style={[styles.actionButton, loading && styles.disabled]}
                disabled={loading}
                onPress={handleShare}
              >
                <Text style={styles.buttonText}>{loading ? "Generating..." : "Generate & share"}</Text>
              </Pressable>
              <Pressable style={styles.actionButton} onPress={() => setModalVisible(false)}>
                <Text style={styles.buttonText}>Cancel</Text>
              </Pressable>
            </View>
          </View>
        </View>
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  button: {
    borderWidth: 1,
    borderColor: "#111",
    paddingVertical: 12,
    alignItems: "center",
    marginTop: 8,
  },
  buttonText: {
    color: "#111",
    fontSize: 15,
  },
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.25)",
    justifyContent: "center",
    padding: 24,
  },
  card: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#111",
    padding: 18,
  },
  title: {
    color: "#111",
    fontSize: 17,
    marginBottom: 10,
  },
  body: {
    color: "#111",
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 14,
  },
  toggleRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 8,
  },
  toggleLabel: {
    color: "#111",
    fontSize: 14,
    flex: 1,
    paddingRight: 12,
  },
  hint: {
    color: "#555",
    fontSize: 12,
    lineHeight: 17,
    marginBottom: 12,
  },
  row: {
    flexDirection: "row",
    gap: 10,
    marginTop: 6,
  },
  actionButton: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#111",
    paddingVertical: 10,
    alignItems: "center",
  },
  disabled: {
    opacity: 0.5,
  },
});
