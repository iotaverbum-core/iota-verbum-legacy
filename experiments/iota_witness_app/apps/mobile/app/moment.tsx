import { useMutation } from "@tanstack/react-query";
import { router } from "expo-router";
import { useRef, useState } from "react";
import { Pressable, StyleSheet, Text, TextInput } from "react-native";

import { postMoment } from "../src/lib/api";
import { useResponseStore } from "../src/store/responseStore";
import { useSettingsStore } from "../src/store/settingsStore";
import { Screen, SymbolsHeader } from "../src/ui/primitives";

export default function MomentScreen() {
  const [text, setText] = useState("");
  const submittedTextRef = useRef("");
  const setLastResponse = useResponseStore((s) => s.setLastResponse);
  const aiConsent = useSettingsStore((s) => s.aiConsent);

  const mutation = useMutation({
    mutationFn: (body: { text: string; aiConsent: boolean; localOnly: boolean }) =>
      postMoment(body.text, body.aiConsent, body.localOnly),
    onSuccess: (data) => {
      setLastResponse(
        "moment",
        data.eden_text,
        data.local_mode,
        data.crisis_flag,
        data.modal,
        data.attestation,
        new Date().toISOString(),
        data.moment_id ?? null,
        submittedTextRef.current
      );
      router.push("/response");
    }
  });
  const devErrorMessage = __DEV__ && mutation.error instanceof Error ? mutation.error.message : null;

  return (
    <Screen>
      <SymbolsHeader />
      <Text style={styles.prompt}>What just happened?</Text>
      <TextInput
        style={styles.input}
        value={text}
        onChangeText={setText}
        multiline
        placeholder="One sentence"
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
          {devErrorMessage ? `Unable to send moment: ${devErrorMessage}` : "Unable to send moment."}
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
    minHeight: 88,
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
