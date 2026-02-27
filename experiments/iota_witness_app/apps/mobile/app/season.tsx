import { useMutation } from "@tanstack/react-query";
import { router } from "expo-router";
import { useRef, useState } from "react";
import { Pressable, StyleSheet, Text, TextInput } from "react-native";

import { postSeason } from "../src/lib/api";
import { useResponseStore } from "../src/store/responseStore";
import { useSettingsStore } from "../src/store/settingsStore";
import { Screen, SymbolsHeader } from "../src/ui/primitives";

export default function SeasonScreen() {
  const [text, setText] = useState("");
  const submittedTextRef = useRef("");
  const setLastResponse = useResponseStore((s) => s.setLastResponse);
  const aiConsent = useSettingsStore((s) => s.aiConsent);

  const mutation = useMutation({
    mutationFn: (body: { text: string; aiConsent: boolean; localOnly: boolean }) =>
      postSeason(body.text, body.aiConsent, body.localOnly),
    onSuccess: (data) => {
      setLastResponse(
        "season",
        data.eden_text,
        data.local_mode,
        data.crisis_flag,
        data.modal,
        data.attestation,
        new Date().toISOString(),
        data.entry_id ?? null,
        submittedTextRef.current
      );
      router.push("/response");
    }
  });
  const devErrorMessage = __DEV__ && mutation.error instanceof Error ? mutation.error.message : null;

  return (
    <Screen>
      <SymbolsHeader />
      <Text style={styles.prompt}>Tell me where you are with the Lord right now. One or two paragraphs.</Text>
      <TextInput
        style={styles.input}
        value={text}
        onChangeText={setText}
        multiline
        placeholder="Write here"
        placeholderTextColor="#888"
      />
      <Pressable
        style={[styles.button, mutation.isPending && styles.disabled]}
        disabled={mutation.isPending || text.trim().length === 0}
        onPress={() => {
          submittedTextRef.current = text;
          mutation.mutate({
            text,
            aiConsent,
            localOnly: !aiConsent
          });
        }}
      >
        <Text style={styles.buttonText}>{mutation.isPending ? "Sending..." : "Submit"}</Text>
      </Pressable>
      {mutation.error ? (
        <Text style={styles.error}>
          {devErrorMessage ? `Unable to send entry: ${devErrorMessage}` : "Unable to send entry."}
        </Text>
      ) : null}
    </Screen>
  );
}

const styles = StyleSheet.create({
  prompt: {
    fontSize: 16,
    color: "#111",
    marginBottom: 12
  },
  input: {
    borderWidth: 1,
    borderColor: "#111",
    minHeight: 180,
    textAlignVertical: "top",
    padding: 12,
    color: "#111"
  },
  button: {
    marginTop: 12,
    borderWidth: 1,
    borderColor: "#111",
    paddingVertical: 12,
    alignItems: "center"
  },
  disabled: {
    opacity: 0.6
  },
  buttonText: {
    color: "#111",
    fontSize: 16
  },
  error: {
    marginTop: 10,
    color: "#111"
  }
});
